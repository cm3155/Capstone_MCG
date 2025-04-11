from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import csv
from collections import defaultdict
import os
from typing import List, Dict, Tuple, Set

class KeywordExtractor:
    def __init__(self, processed_data: Dict[str, Dict[str, List[str]]], top_n: int = 20):
        """Initialize the KeywordExtractor."""
        if not isinstance(processed_data, dict):
            raise ValueError("processed_data must be a dictionary")
        if not isinstance(top_n, int) or top_n <= 0:
            raise ValueError("top_n must be a positive integer")
            
        self.processed_data = processed_data
        self.top_n = top_n
        self.bert_model = SentenceTransformer('all-MiniLM-L6-v2')

        # Modified TF-IDF parameters for small document sets
        self.tfidf = TfidfVectorizer(
            ngram_range=(1, 3),
            max_features=1000,
            min_df=1,  
            max_df=1.0,  
            stop_words='english'
        )
        
        self.embedding_cache = {}
        self._initialize_categories()

    def _initialize_categories(self):
        self.categories ={
            "Data": [
                "information management", "data governance", "data quality", "data access", "data traceability",
                "data health", "data centers", "ata services", "data integration", "data stewardship",
                "data privacy", "data security", "data compliance", "data migration", "data modeling",
                "data warehousing", "master data management", "mdm", "data cataloging", "data retention", "data monetization",
                "information management", "data health", "data governance", "data access", "data traceability",
                "insights", "data centers", "data services", "data and analytics",'access', 'acquisition', 'architecture', 'availability', 'auto-scaling', 'auto-optimization', 'audit',
                'metadata repositories', 'federated search', 'data observability', 'semantic search',
                'integrity checks', 'validation rules', 'consistency standards', 'deduplication',
                'real-time pipelines', 'etl', 'api-based integration', 'middleware',
                'anonymization', 'pseudonymization', 'access logs',
                'distributed systems', 'object storage', 'file systems', 'archival solutions',
                'knowledge graphs', 'dynamic cataloging', 'operational insights', 'data democratization',
                'stewardship roles', 'audit trails', 'role based controls', 'data ethics frameworks',
                'data as a service', 'subscription models', 'ip monetization', 'marketplace ecosystems'
            ],
            "Analytics": [
                "predictive analytics", "prescriptive analytics", "descriptive analytics", "diagnostic analytics", "real-time analytics",
                "data visualization", "statistical analysis", "machine learning", "artificial intelligence", "customer analytics",
                "fraud detection", "risk analytics", "operational analytics", "marketing analytics",
                "social media analytics", "sentiment analysis", "text analytics", "churn analysis", "market basket analysis",
                "customer segmentation", "lifetime value analysis", "anomaly detection", "behavioral analytics", "analytic framework",
                "roles and skills", "analytics services", "analytics processes", "analysis complexity", "analytics",
                "capital efficiency", "create recommendations", "accuracy", "operational efficiency", "different sources",
                "personalization", "personalized", "credit decision", "fraud detection", "market data", "forecasted data",
                "actual data", "reporting", "historical data", "competitor analytics", 'predictive modeling', 'decision intelligence', 'automation in analytics',
                'behavioral insights', 'real-time optimization', 'strategic forecasts',
                'reinforcement learning', 'causality analysis', 'ensemble modeling', 'geospatial analytics',
                'journey mapping', 'propensity models', 'omnichannel behavior', 'upsell strategies',
                'workflow optimization', 'process mining', 'productivity analytics', 'capacity planning',
                'channel attribution', 'ROI measurement', 'audience profiling', 'campaign simulations',
                'anomaly scoring', 'predictive triggers', 'identity matching', 'heuristic analysis',
                'credit scoring', 'hedging models', 'stress testing', 'fiscal forecasts',
                'embedding AI', 'cloud-based dashboards', 'serverless analytics', 'visualization ecosystems'
            ],
            "Technology": [
                "cloud computing", "edge computing", "cybersecurity", "blockchain", "internet of things", "IoT"
                "artificial intelligence", "machine learning", "big data", "devops", "api management",
                "software engineering", "it infrastructure", "data encryption", "identity and access management",
                "zero trust architecture", "digital transformation", "it governance", "disaster recovery", "cloud security",
                "it infrastructure", "it development", "it support and service delivery", "software procurement", "it strategy",
                "investment in iechnology", "ai", "artificial intelligence", "machine learning", "ml", "big Data",
                "data Analytics", "genai", "generative ai", "capabilities", "cloud", "cloud Services", "technology",
                "ai-powered", "rolled out", "api", "llm", "large language model", 'quantum computing', 'neuromorphic systems', 'bioinformatics platforms', 'holographic interfaces',
                'containerization', 'microservices', 'hybrid clouds', 'DevSecOps',
                'robotic process automation', 'intelligent automation', 'workflow bots', 'self-healing systems',
                'intrusion detection', 'threat hunting', 'biometric access', 'penetration testing',
                'transformers', 'generative adversarial networks', 'explainable AI', 'autoML',
                'serverless computing', 'cloud-native design', 'multi-cloud orchestration', 'data lakes',
                'edge-to-cloud continuum', 'digital twins', 'virtual collaboration platforms', 'no-code/low-code platforms'
            ],
            "Analog": [
                "leadership", "employee engagement", "organizational culture", "risk management", "process automation",
                "compliance management", "audit management", "stakeholder engagement", "innovation management",
                "performance management", "strategic planning", "change management", "team collaboration",
                "crisis management", "corporate governance", "customer experience", "ethics and integrity",
                "decision-making frameworks", "workforce training", "cross-functional collaboration", "leadership", "people",
                "measures", "process optimization", "process automation", "work Skills", "training Programs",
                "strategic Decisions", "managing Risks", "driving Innovation", "marketing Risk", "risk Management",
                "fraud risk", "innovation", "virtual", "e-commerce", "governance", "stewardship",
                "cybersecurity", "privacy", "compliance", "confidentiality", "data privacy", 'growth mindset', 'transformational leadership', 'servant leadership', 'emotional intelligence',
                'diversity equity inclusion', 'psychological safety', 'learning organizations', 'agile mindsets',
                'scenario analysis', 'risk-aware culture', 'resilience planning', 'business continuity',
                'co-creation', 'knowledge-sharing ecosystems', 'cross-functional pods', 'project retrospectives',
                'value stream mapping', 'lean methodologies', 'throughput analysis', 'time-in-motion studies',
                'ESG compliance', 'sustainability goals', 'stakeholder accountability',
                'upskilling', 'reskilling', 'microlearning', 'mentorship programs',
                'net promoter score', 'personalized interactions', 'journey orchestration', 'proactive service'
            ]
        }
        
        # Preprocess category keywords
        self.categories = {
            category: [kw.lower() for kw in keywords]
            for category, keywords in self.categories.items()
        }
        
        # Create category embeddings cache
        self.category_embeddings = {
            category: self.bert_model.encode(keywords)
            for category, keywords in self.categories.items()
        }

    def get_embedding(self, text: str) -> np.ndarray:
        if text not in self.embedding_cache:
            self.embedding_cache[text] = self.bert_model.encode([text])[0]
        return self.embedding_cache[text]

    def extract_tfidf_keywords(self, text_list: List[str]) -> List[Tuple[str, float]]:
        if not text_list:
            return []

        # Join sentences and ensure we have valid text
        documents = [' '.join(filter(None, sentences)) for sentences in text_list]
        documents = [doc for doc in documents if doc.strip()]
        
        if not documents:
            return []

        try:
            tfidf_matrix = self.tfidf.fit_transform(documents)
            feature_names = self.tfidf.get_feature_names_out()
            avg_scores = np.mean(tfidf_matrix.toarray(), axis=0)
            
            # Sort keywords by score
            keywords = sorted(
                zip(feature_names, avg_scores),
                key=lambda x: x[1],
                reverse=True
            )
            
            # Filter out single-character keywords and low scores
            keywords = [
                (kw, score) for kw, score in keywords
                if len(kw) > 1 and score > 0.0
            ]
            
            return keywords[:self.top_n]
        except Exception as e:
            print(f"Error in TF-IDF extraction: {str(e)}")
            return []

    def categorize_keywords(self, keywords: List[str]) -> Dict[str, List[str]]:
        if not keywords:
            return {}

        categorized = defaultdict(set)
        keyword_embeddings = np.array([self.get_embedding(kw) for kw in keywords])
        
        for category, category_embs in self.category_embeddings.items():
            similarities = cosine_similarity(keyword_embeddings, category_embs)
            threshold = 0.7 # Change as needed
            
            for i, keyword in enumerate(keywords):
                if similarities[i].max() > threshold:
                    categorized[category].add(keyword)
        
        return {
            category: sorted(list(kws))
            for category, kws in categorized.items()
        }

    def extract_keywords(self) -> Dict[str, Dict[str, List[str]]]:
        results = {}
        
        for filename, data in self.processed_data.items():
            if not isinstance(data, dict) or 'sentences' not in data or 'keywords' not in data:
                continue
            
            sentences = data['sentences']
            keywords = data['keywords']
            
            tfidf_keywords = self.extract_tfidf_keywords([sentences])
            combined_keywords = list(set(
                kw for kw, _ in tfidf_keywords
            ) | set(keywords))
            
            results[filename] = self.categorize_keywords(combined_keywords)
                
        return results
    
        

def extract_sec_keywords(
    processed_data: Dict[str, Dict[str, List[str]]],
    top_n: int = 20
) -> Dict[str, Dict[str, List[str]]]:
    extractor = KeywordExtractor(processed_data, top_n)
    return extractor.extract_keywords()

def load_all_txt_files(folder_path: str) -> Dict[str, Dict[str, List[str]]]:
    processed_data = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                full_path = os.path.join(root, file)
                with open(full_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                relative_path = os.path.relpath(full_path, folder_path)
                processed_data[relative_path] = {
                    'sentences': [text],  # No sentence splitting
                    'keywords': []
                }
    return processed_data 

def save_keywords_to_csv(results: Dict[str, Dict[str, List[str]]], output_path: str):
    category_keywords = defaultdict(set)
    
    # Aggregate keywords by category across all files
    for file_result in results.values():
        for category, keywords in file_result.items():
            category_keywords[category].update(keywords)
    
    # Write to CSV
    with open(output_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Keyword"])
        for category, keywords in sorted(category_keywords.items()):
            for keyword in sorted(keywords):
                writer.writerow([category, keyword])

# Call this at the end
if __name__ == "__main__":
    folder = "C:/Users/cassi/Capstone_MCG/All_Data_Processed"  # Replace with your actual path
    data = load_all_txt_files(folder)
    result = extract_sec_keywords(data, top_n=300)
    
    # Save result to CSV
    output_csv_path = "C:/Users/cassi/Capstone_MCG/keywords_by_category_2.csv"
    save_keywords_to_csv(result, output_csv_path)
