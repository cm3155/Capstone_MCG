import os
from typing import Dict, List, Set
from collections import defaultdict
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
from Reference_Code.Keyword_Extractor import extract_sec_keywords
from Sec_Processor import clean_sec_data
import json
import time
from datetime import datetime

class Keyword_Filing_Analyzer:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        print(f"Scanning directory: {base_dir}")
        self.banks = self._get_banks()
        print(f"Found {len(self.banks)} banks: {', '.join(self.banks[:5])}...")
        
    def _get_banks(self) -> List[str]:
        banks = [d for d in os.listdir(self.base_dir) 
                if os.path.isdir(os.path.join(self.base_dir, d))]
        return sorted(banks)
    
    def process_single_bank(self, bank: str) -> Dict:
        start_time = time.time()
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Worker starting bank: {bank}")
        
        bank_dir = os.path.join(self.base_dir, bank)
        years = [d for d in os.listdir(bank_dir) 
                if os.path.isdir(os.path.join(bank_dir, d))]
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Found years for {bank}: {years}")
        
        bank_data = {
            'bank_name': bank,
            'processed_data': {},
            'keywords': defaultdict(list)
        }
        
        for year in years:
            try:
                year_start = time.time()
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {bank} - Processing year {year}")
                
                processed_data = clean_sec_data(bank, int(year))
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {bank} - {year}: Data cleaned in {time.time() - year_start:.2f}s")
                
                if processed_data:
                    kw_start = time.time()
                    year_keywords = extract_sec_keywords(processed_data, top_n=50)
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] {bank} - {year}: Keywords extracted in {time.time() - kw_start:.2f}s")
                    
                    bank_data['processed_data'][year] = processed_data
                    bank_data['keywords'][year] = year_keywords
                
            except Exception as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Error processing {bank} - {year}: {str(e)}")
                continue
        
        total_time = time.time() - start_time
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Completed {bank} in {total_time:.2f}s")
        return bank_data
    
    def process_all_banks(self, max_workers: int = 4) -> Dict:
        """Process banks in parallel with debugging."""
        results = {}
        total_banks = len(self.banks)
        start_time = time.time()
        
        print(f"\nStarting parallel processing with {max_workers} workers")
        completed_banks = 0
        
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Submit all jobs
            future_to_bank = {
                executor.submit(self.process_single_bank, bank): bank 
                for bank in self.banks
            }
            
            # Track progress and collect results
            for future in as_completed(future_to_bank):
                bank = future_to_bank[future]
                try:
                    bank_data = future.result()
                    results[bank_data['bank_name']] = bank_data
                    completed_banks += 1
                    elapsed_time = time.time() - start_time
                    avg_time_per_bank = elapsed_time / completed_banks
                    estimated_remaining = avg_time_per_bank * (total_banks - completed_banks)
                    
                    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] "
                          f"Progress: {completed_banks}/{total_banks} banks completed "
                          f"({(completed_banks/total_banks)*100:.1f}%)")
                    print(f"Average time per bank: {avg_time_per_bank:.1f}s")
                    print(f"Estimated time remaining: {estimated_remaining/60:.1f} minutes")
                    
                except Exception as e:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Failed to process {bank}: {str(e)}")
        
        total_time = time.time() - start_time
        print(f"\nAll banks processed in {total_time/60:.1f} minutes")
        return results
    
    def analyze_keywords(self, results: Dict) -> pd.DataFrame:
        print("\nAnalyzing keywords...")
        summary_data = []
        
        for bank, bank_data in results.items():
            for year, year_keywords in bank_data['keywords'].items():
                for file, categories in year_keywords.items():
                    for category, keywords in categories.items():
                        summary_data.append({
                            'bank': bank,
                            'year': year,
                            'filing': file,
                            'category': category,
                            'keywords': keywords
                        })
        
        return pd.DataFrame(summary_data)
    
    def save_results(self, results: Dict, output_dir: str):
        print(f"\nSaving results to {output_dir}")
        os.makedirs(output_dir, exist_ok=True)
        
        print("Saving raw results...")
        with open(os.path.join(output_dir, 'all_results.json'), 'w') as f:
            json.dump(results, f, indent=2)
        
        print("Creating summary...")
        df = self.analyze_keywords(results)
        df.to_csv(os.path.join(output_dir, 'keyword_summary.csv'), index=False)
        
        print("Creating frequency analysis...")
        keyword_freq = df.explode('keywords').groupby(['category', 'keywords']).size()
        keyword_freq.to_csv(os.path.join(output_dir, 'keyword_frequency.csv'))
        
        print("Creating bank summary...")
        bank_summary = df.groupby(['bank', 'year', 'category']).agg({
            'keywords': lambda x: list(set([item for sublist in x for item in sublist]))
        }).reset_index()
        bank_summary.to_csv(os.path.join(output_dir, 'bank_summary.csv'), index=False)

def analyze_bank_filings(base_dir: str, output_dir: str, max_workers: int = 4):
    """Main function to analyze bank filings."""
    print(f"Starting analysis of bank filings in {base_dir}")
    print(f"Results will be saved to {output_dir}")
    
    start_time = time.time()
    analyzer = Keyword_Filing_Analyzer(base_dir)
    
    print(f"\nProcessing banks in parallel with {max_workers} workers...")
    results = analyzer.process_all_banks(max_workers=max_workers)
    
    print("\nSaving results...")
    analyzer.save_results(results, output_dir)
    
    total_time = time.time() - start_time
    print(f"\nAnalysis complete! Total time: {total_time/60:.1f} minutes")
    return results