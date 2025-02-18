import os
import time
import torch
import numpy as np
from typing import Dict, List, Tuple
import torch.nn.functional as F
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from tqdm.auto import tqdm
import pandas as pd
import gc
import warnings
import json
import multiprocessing as mp
from functools import partial
import logging
from datetime import datetime
from  ModelSECPreprocessor import ModelSECPreprocessor

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - Process %(process)d - %(message)s',
    handlers=[
        logging.FileHandler('sec_analyzer.log'),
        logging.StreamHandler()
    ]
)

class SECFilingAnalyzer:
    def __init__(
        self,
        categories: Dict[str, List[str]],
        batch_size: int = 32,
        chunk_size: int = 512,
        device: str = None,
        num_workers: int = 4,
        cache_dir: str = 'model_cache'
    ):
        self.categories = categories
        self.batch_size = batch_size
        self.chunk_size = chunk_size
        self.num_workers = num_workers
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        logging.info(f"Initializing SECFilingAnalyzer with device: {self.device}")
        
        self.preprocessor = ModelSECPreprocessor()
        self.initialize_models(cache_dir)
        
        self.weights = {
            'semantic_similarity': 0.5,
            'keyword_relevance': 0.35,
            'sentiment_context': 0.15,
        }

    def initialize_models(self, cache_dir: str):
        logging.info("Initializing models...")
        start_time = time.time()
        
        os.makedirs(cache_dir, exist_ok=True)
        
        logging.info("Loading MPNet for semantic analysis...")
        self.embedding_model = SentenceTransformer(
            'sentence-transformers/all-mpnet-base-v2',
            cache_folder=cache_dir
        ).to(self.device)
        
        logging.info("Loading FinBERT for sentiment analysis...")
        self.sentiment_tokenizer = AutoTokenizer.from_pretrained(
            "ProsusAI/finbert",
            cache_dir=cache_dir,
            local_files_only=True if os.path.exists(os.path.join(cache_dir, 'finbert')) else False
        )
        self.sentiment_model = AutoModelForSequenceClassification.from_pretrained(
            "ProsusAI/finbert",
            cache_dir=cache_dir,
            local_files_only=True if os.path.exists(os.path.join(cache_dir, 'finbert')) else False
        ).to(self.device)
        
        if self.device == 'cuda':
            self.sentiment_model = self.sentiment_model.half()
            torch.backends.cudnn.benchmark = True
        
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words='english',
            ngram_range=(1, 3),
            max_features=10000
        )
        
        logging.info("Computing category embeddings...")
        self.category_embeddings = self._compute_category_embeddings()
        
        logging.info(f"Models initialized successfully! Time taken: {time.time() - start_time:.2f}s")

    def _compute_category_embeddings(self) -> Dict[str, torch.Tensor]:
        category_embeddings = {}
        for category, terms in tqdm(self.categories.items(), desc="Computing category embeddings"):
            embeddings = self.embedding_model.encode(
                terms,
                convert_to_tensor=True,
                show_progress_bar=False
            )
            category_embeddings[category] = embeddings.to(self.device)
        return category_embeddings

    def _calculate_semantic_similarity(self, text_embedding: torch.Tensor, category: str) -> float:
        similarities = F.cosine_similarity(
            text_embedding.unsqueeze(0),
            self.category_embeddings[category],
            dim=1
        )
        return similarities.max().item()

    def _calculate_keyword_relevance(self, text: str, category: str) -> float:
        try:
            keywords = [k.lower() for k in self.categories[category]]
            documents = [text] + keywords
            tfidf_matrix = self.vectorizer.fit_transform(documents)
            text_vector = tfidf_matrix[0]
            keyword_vectors = tfidf_matrix[1:]
            relevance_score = cosine_similarity(text_vector, keyword_vectors).mean()
        except Exception as e:
            logging.error(f"Error calculating keyword relevance: {str(e)}")
            relevance_score = 0.0
        return relevance_score

    def _calculate_sentiment_scores(self, text: str) -> float:
        inputs = self.sentiment_tokenizer(
            text,
            padding=True,
            truncation=True,
            max_length=self.chunk_size,
            return_tensors="pt"
        ).to(self.device)
        with torch.no_grad():
            outputs = self.sentiment_model(**inputs)
            sentiment_scores = F.softmax(outputs.logits, dim=1)
            positive_score = sentiment_scores[0][2].item()
            negative_score = sentiment_scores[0][0].item()
            return positive_score - negative_score

    def process_chunk(self, chunk: str) -> Dict:
        try:
            chunk_embedding = self.embedding_model.encode(chunk, convert_to_tensor=True).to(self.device)
            results = {}
            
            for category in ['Data', 'Analytics', 'Technology', 'Analog']:
                # Calculate all metrics
                semantic_sim = self._calculate_semantic_similarity(chunk_embedding, category)
                keyword_rel = self._calculate_keyword_relevance(chunk, category)
                sentiment = self._calculate_sentiment_scores(chunk)
                
                # Calculate weighted score (1-5 scale as required)
                weighted_score = (
                    self.weights['semantic_similarity'] * semantic_sim +
                    self.weights['keyword_relevance'] * keyword_rel +
                    self.weights['sentiment_context'] * ((sentiment + 1) / 2)
                )
                final_score = 1 + (weighted_score * 4)  # Convert to 1-5 scale
                
                # Store in format matching CSV requirements
                results[f'{category}_avg_score'] = final_score
                results[f'{category}_relevance'] = semantic_sim * 100  # Convert to percentage
                results[f'{category}_sentiment'] = sentiment
                results[f'{category}_explanation'] = self.generate_explanation(
                    category, semantic_sim, keyword_rel, sentiment
                )
                
            return results
            
        except Exception as e:
            logging.error(f"Error processing chunk: {str(e)}")
            return None

    def process_file(self, file_info: tuple) -> dict:
        filepath, company, year = file_info
        
        try:
            filename = os.path.basename(filepath)
            
            # Extract metadata
            filing_type = "10-K" if "10-K" in filename else "10-Q"
            
            # Parse filing date from filename
            filing_date = None
            for part in filename.split('_'):
                if '-' in part and len(part) >= 10:
                    try:
                        date_obj = pd.to_datetime(part[:10])
                        filing_date = date_obj.strftime('%-m/%-d/%y')
                    except:
                        pass
            
            # Determine section
            if "Item_1.txt" in filename:
                section = "Item_1.txt"
            elif "Item_1A" in filename or "Risk_Factors" in filename:
                section = "Item_1A.txt"
            elif "Item_7" in filename or "MD&A" in filename:
                section = "Item_7.txt"
            elif "Item_7A" in filename:
                section = "Item_7A.txt"
            else:
                section = filename

            # Process the chunks
            processed_data = self.preprocessor.process_file(filepath)
            chunks = processed_data['chunks']
            chunk_results = []
            
            for chunk in chunks:
                result = self.process_chunk(chunk)
                if result:
                    chunk_results.append(result)

            if not chunk_results:
                return None

            # Average the chunk results
            final_result = {
                'filename': filename,
                'filing_type': filing_type,
                'filing_date': filing_date,
                'section': section
            }
            
            # Average each metric across chunks
            for category in ['Data', 'Analytics', 'Technology', 'Analog']:
                final_result[f'{category}_avg_score'] = np.mean([r[f'{category}_avg_score'] for r in chunk_results])
                final_result[f'{category}_relevance'] = np.mean([r[f'{category}_relevance'] for r in chunk_results])
                final_result[f'{category}_sentiment'] = np.mean([r[f'{category}_sentiment'] for r in chunk_results])
                # Use the explanation from the most relevant chunk
                most_relevant_idx = np.argmax([r[f'{category}_relevance'] for r in chunk_results])
                final_result[f'{category}_explanation'] = chunk_results[most_relevant_idx][f'{category}_explanation']

            return final_result

        except Exception as e:
            logging.error(f"Error processing file {filepath}: {str(e)}")
            return None

    def generate_explanation(self, category: str, semantic_sim: float, keyword_relevance: float, sentiment: float) -> str:
        semantic_percent = semantic_sim * 100
        keyword_percent = keyword_relevance * 100
        
        sentiment_desc = "neutral"
        if sentiment > 0.6:
            sentiment_desc = "strongly positive"
        elif sentiment > 0.2:
            sentiment_desc = "positive"
        elif sentiment < -0.6:
            sentiment_desc = "strongly negative"
        elif sentiment < -0.2:
            sentiment_desc = "negative"
        
        explanation = (
            f"{category} Analysis: "
            f"Semantic similarity analysis shows {semantic_percent:.2f}% alignment with {category.lower()}-related concepts. "
            f"Keyword analysis indicates {keyword_percent:.2f}% relevance to {category.lower()} terminology. "
            f"Sentiment analysis reveals {sentiment_desc} context (score: {sentiment:.2f}) "
            f"regarding {category.lower()}-related discussions."
        )
        
        return explanation
        
       
    def analyze_filings(self, base_dir: str, output_dir: str = "/Users/owner/Desktop/MCG/GWUxMCG/NLP Analysis/results", num_processes: int = None):
        """
        Analyzes SEC filings and directly saves results to CSV files by company and year.
        """
        if num_processes is None:
            num_processes = max(1, mp.cpu_count() - 1)
                
        os.makedirs(output_dir, exist_ok=True)
        start_time = time.time()
        
        logging.info(f"Starting analysis with {num_processes} processes")
        
        # Organize files by company-year first
        company_year_files = {}
        for company in os.listdir(base_dir):
            company_dir = os.path.join(base_dir, company)
            if not os.path.isdir(company_dir):
                continue
                
            for year in os.listdir(company_dir):
                year_dir = os.path.join(company_dir, year)
                if not os.path.isdir(year_dir):
                    continue
                
                key = (company, year)
                if key not in company_year_files:
                    company_year_files[key] = []
                    
                for filename in os.listdir(year_dir):
                    if filename.endswith('.txt'):
                        filepath = os.path.join(year_dir, filename)
                        company_year_files[key].append(filepath)
        
        if not company_year_files:
            logging.error("No files found to process")
            return "No files found"
        
        total_files = sum(len(files) for files in company_year_files.values())
        logging.info(f"Found {total_files} files across {len(company_year_files)} company-year combinations")
        
        # Process each company-year combination
        with tqdm(total=len(company_year_files), desc="Processing company-years") as pbar:
            for (company, year), filepaths in company_year_files.items():
                try:
                    logging.info(f"Processing {company} - {year}")
                    results = []
                    
                    # Process files for this company-year in parallel
                    with mp.Pool(processes=num_processes) as pool:
                        file_infos = [(fp, company, year) for fp in filepaths]
                        for result in pool.imap_unordered(self.process_file, file_infos):
                            if result is not None:
                                results.append(result)
                    
                    # Save results immediately if we have any
                    if results:
                        df = pd.DataFrame(results)
                        
                        # Ensure all required columns exist and are in correct order
                        required_columns = [
                            'filename', 'filing_type', 'filing_date', 'section',
                            'Data_avg_score', 'Data_relevance', 'Data_sentiment', 'Data_explanation',
                            'Analytics_avg_score', 'Analytics_relevance', 'Analytics_sentiment', 'Analytics_explanation',
                            'Technology_avg_score', 'Technology_relevance', 'Technology_sentiment', 'Technology_explanation',
                            'Analog_avg_score', 'Analog_relevance', 'Analog_sentiment', 'Analog_explanation'
                        ]
                        
                        for col in required_columns:
                            if col not in df.columns:
                                df[col] = None
                        
                        df = df[required_columns]
                        
                        # Save to CSV
                        output_file = os.path.join(output_dir, f"{company}_{year}_results.csv")
                        df.to_csv(output_file, index=False)
                        
                        file_size = os.path.getsize(output_file)
                        logging.info(f"Saved {company}_{year} results ({file_size/1024:.1f} KB)")
                        print(f"\n✓ Saved {company}_{year}_results.csv ({file_size/1024:.1f} KB)")
                        print(f"  Files processed: {len(results)}/{len(filepaths)}")
                    
                    # Clean up memory
                    results.clear()
                    gc.collect()
                    
                except Exception as e:
                    logging.error(f"Error processing {company}_{year}: {str(e)}")
                    print(f"\n❌ Error processing {company}_{year}: {str(e)}")
                
                pbar.update(1)
        
        # Final summary
        total_time = time.time() - start_time
        hours, remainder = divmod(total_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        print("\n=== Analysis Complete ===")
        print(f"Total processing time: {int(hours)}h {int(minutes)}m {int(seconds)}s")
        
        saved_files = [f for f in os.listdir(output_dir) if f.endswith('_results.csv')]
        print(f"\nResults saved: {len(saved_files)}/{len(company_year_files)} company-years")
        total_size = sum(os.path.getsize(os.path.join(output_dir, f)) for f in saved_files)
        print(f"Total data size: {total_size/1024/1024:.1f} MB")
        
        return "Analysis complete"