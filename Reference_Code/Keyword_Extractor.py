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
        self.categories = {
        "Data": [
            # Data Governance & Quality
            "data governance", "data quality", "metadata management", "data stewardship", "master data management",
            "data lineage", "data cataloging", "data ownership", "data governance frameworks", "data validation",

            # Data Infrastructure
            "data infrastructure", "data warehousing", "data architecture", "data centers",
            "file systems", "distributed systems", "object storage", "archival solutions",

            # Data Security & Compliance
            "data privacy", "data security", "access controls", "encryption", "role-based access",
            "anonymization", "pseudonymization", "audit trails", "data ethics frameworks",

            # Data Integration & Access
            "data integration", "data access", "real-time pipelines", "ETL", "api-based integration", "middleware",
            "data observability", "data democratization", "federated search", "semantic search",

            # Data Monetization
            "data monetization", "data as a service", "subscription models", "marketplace ecosystems",
            "IP monetization", "operational insights"
        ],
        "Analytics": [
            # Advanced Analytics & AI
            "machine learning", "artificial intelligence", "advanced analytics", "reinforcement learning",
            "decision intelligence", "automation in analytics", "heuristic analysis", "generative AI", "LLM",
            "causality analysis", "explainable AI",

            # Predictive & Prescriptive Analytics
            "predictive analytics", "prescriptive analytics", "predictive modeling", "forecasting", "propensity models",
            "strategic forecasts", "fiscal forecasts", "predictive triggers", "scenario analysis", "simulation models",

            # Banking-Specific Analytics
            "credit scoring", "fraud detection", "risk analytics", "churn analysis", "customer segmentation",
            "lifetime value analysis", "hedging models", "stress testing", "compliance analytics",

            # Operational Analytics
            "operational analytics", "workflow optimization", "process mining", "capacity planning",
            "performance dashboards", "anomaly detection", "productivity analytics", "real-time optimization",

            # Analytics Governance & Management
            "analytics governance", "analytics services", "analytic framework", "roles and skills", "reporting",
            "analytics processes", "data visualization", "cloud-based dashboards", "serverless analytics",
            "analytics platforms", "visualization ecosystems"
        ],
        "Technology": [
            # Cloud & Infrastructure
            "cloud", "cloud computing", "multi-cloud", "hybrid cloud", "serverless computing", "containerization",
            "microservices", "edge computing", "infrastructure as code", "digital twins", "cloud-native design",

            # AI/ML Platform & Tools
            "ai platforms", "ai tools", "autoML", "intelligent automation", "neuromorphic systems", "quantum computing",

            # API & Integration
            "api", "api management", "api-based integration", "middleware", "integration layers",
            "enterprise bus", "workflow bots", "system interoperability", "orchestration tools",

            # DevOps & Delivery
            "devops", "DevSecOps", "CI/CD", "agile development", "software delivery", "test automation",
            "self-healing systems", "incident response", "IT governance", "infrastructure management",

            # Emerging Technologies
            "blockchain", "holographic interfaces", "bioinformatics platforms", "robotic process automation",
            "virtual collaboration platforms", "no-code/low-code platforms", "threat hunting",
            "zero trust architecture", "penetration testing"
        ],
        "Analog": [
            # Leadership & Strategy
            "leadership", "strategic planning", "vision setting", "decision-making frameworks",
            "transformational leadership", "servant leadership", "business continuity", "resilience planning",

            # Talent & Capabilities
            "talent development", "upskilling", "reskilling", "workforce training", "microlearning",
            "mentorship programs", "emotional intelligence", "growth mindset", "learning organizations",

            # Operating Model & Governance
            "operating model", "corporate governance", "risk management", "audit management",
            "organizational structure", "scenario planning", "change management", "strategic decisions",

            # Digital Culture & Innovation
            "innovation", "digital culture", "agile mindsets", "co-creation", "project retrospectives",
            "journey orchestration", "virtual teams", "proactive service", "customer experience",

            # Ecosystem Partnerships
            "ecosystem partnerships", "stakeholder engagement", "knowledge-sharing ecosystems",
            "cross-functional pods", "collaborative networks", "stakeholder accountability",
            "ESG compliance", "sustainability goals", "net promoter score"
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
    folder = "C:/Users/cassi/Capstone_MCG/All_Data_Processed_Engineered"  # Replace with your actual path
    data = load_all_txt_files(folder)
    result = extract_sec_keywords(data, top_n=300)
    
    # Save result to CSV
    output_csv_path = "C:/Users/cassi/Capstone_MCG/keywords_by_category_2.csv"
    save_keywords_to_csv(result, output_csv_path)
