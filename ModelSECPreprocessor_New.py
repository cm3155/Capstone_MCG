import os
import re
import csv
import nltk
from bs4 import BeautifulSoup
import html
from typing import Dict, List

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

class ModelSECPreprocessor:
    def __init__(self):
        # Basic stopwords that are very common in SEC filings + NLTK stopwords
        self.stopwords = {
            'or', 'billion', 'clear', 'beginnings', 'able', 'rial', 'ernst', 'allows', 'boliviano', 'lats', 
            'amount', 'state', 'dinar', 'cv', 'detail', 's', 'fifteen', 'backed', 'those', 'aren', 
            'been', 'kuwait', 'himself', 'atlantic', 'ha', 'got', 'af', 'around', 'as', 'tg', 
            'lake', 'cy', 'bill', 'beside', 'fifty', 'countries', 'costa', 'mw', 'million', 
            'detroit', 'km', 'buy', 'base', 'emphasis', 'across', 'against', 'necessarily', 
            'tens', 'gulf', 'below', 'version', 'how', 'child', 'seven', 'various', 'often', 
            'mil', 'measure', 'case', 'value', 'algeria', 'case', 'edu', 'come', 'line', 'everybody', 
            'kh', 'alaska', 'terms', 'these', 'greater', 'sent', 'dollars', 'set', 'roman', 'hi', 
            'seem', 'containing', 'front', 'texas', 'sub', 'trying', 'term', 'wyoming', 'results', 
            'beyond', 'each', 'cannot', 'move', 'row', 'millions', 'earth', 'contain', 'described', 
            'cm', 'toward', 'him', 'ro', 'ru', 'returns', 'known', 'best', 'stop', 'viii', 'seven',
            'single', 'somewhat', 'decades', 'conduct', 'double', 'pride', 'ten', 'yield', 'next', 
            'unique', 'neednt', 'instead', 'taught', 'lots', 'online', 'forth', 'energy', 'cannot', 
            'distance', 'climate', 'role', 'base', 'connecticut', 'property', 'fourteen', 'done', 
            'cr', 'opposite', 'etc', 'generation', 'du', 'succeed', 'despite', 'per', 'city', 'oil', 
            'wrong', 'million', 'nine', 'al', 'quarterly', 'ocean', 'longer', 'downward', 'quietly', 
            'moreover', 'major', 'mention', 'she', 'why', 'definition', 'weight', 've', 'iii', 'south', 
            'elsewhere', 'provided', 'whichever', 'end', 'world', 'tenth', 'wyoming', 'florin', 'huge', 
            'ke', 'exactly', 'provided', 'present', 'forward', 'five', 'stages', 'believed', 'studies', 
            'moral', 'laws', 'whole', 'located', 'korean', 'arrive', 'west', 'than',
            'giving', 'equal', 'established', 'u', 'appears', 'watch', 'element', 'though', 'arose', 
            'matter', 'house', 'jobs', 'constant', 'decade', 'billions', 'dollars', 'association', 
            'nine', 'effective', 'wide', 'minutes', 'longest', 'currently', 'double', 'instead', 'lay', 
            'majority', 'path', 'law', 'costa', 'urban', 'head', 'said', 'line', 'speaks', 'applying', 
            'should', 'occurring', 'season', 'poor', 'benefit', 'especially', 'hardly', 'annum', 
            'additional', 'seconds', 'pull', 'reporting', 'france', 'hour', 'quarterly', 'society', 
            'chapter', 'articles', 'claim', 'history', 'success', 'doesnt', 'focused', 'produced', 
            'issues', 'fifth', 'instance', 'volume', 'offering', 'fund', 'himself',
            'additionally', 'nothing', 'knowledge', 'growth', 'the', 'show', 'available', 'total', 'latter', 
            'available', 'estimated', 'rapid', 'smaller', 'goods', 'personal', 'members', 'owner', 
            'municipal', 'especially', 'part', 'rare', 'leading', 'major', 'transferred', 'industrial', 
            'column', 'impossible', 'otherwise', 'equivalent', 'chapter', 'referred', 'initial', 'basis', 
            'regard', 'quality', 'claimed', 'revised', 'learning', 'quarter', 'literature', 'ahead', 
            'descriptions', 'developments', 'regional', 'locations', 'specific', 'heavily', 'active', 
            'sector', 'respond', 'comments', 'substantial', 'claims', 'priority', 'hundreds', 'used', 
            'accomplish', 'generated', 'declared', 'input', 'provided', 'average', 'adjusted', 'executed', 
            'worked', 'sufficient', 'responses', 'affected', 'connected', 'amount', 'recognized', 
            'supports', 'leads', 'ensures', 'compared', 'affected', 'functions', 'reviewed',
            'implementation', 'updated', 'desired', 'elements', 'limited', 'retained', 'leadership', 
            'designed', 'conditions', 'importance', 'accounts', 'reported', 'impacted', 'preparation', 
            'developed', 'efficiency', 'agreed', 'expected', 'experienced', 'concepts', 'recorded', 
            'involved', 'enhanced', 'distributed', 'achieved', 'impact', 'focus', 'reduced', 'initiatives', 
            'influenced', 'reflects', 'access', 'prior', 'reduction', 'activities', 'custom', 'intended', 
            'additional', 'presence', 'factors', 'arise', 'solution', 'formation', 'governed', 'emerged', 
            'measures', 'expanded', 'outputs', 'interpretation', 'solution', 'responded', 'advanced', 
            'scheduled', 'utilized', 'illustrates', 'defined', 'determine', 'modified', 'sought', 
            'maintain', 'resulted', 'illustration', 'maintained', 'regulated', 'overview', 'alternative', 
            'assume', 'duration', 'implementation', 'extend', 'illustration', 'summarized', 'decrease',
            'expansion', 'consequence', 'administration', 'monitor', 'notably', 
            'establish', 'detected', 'observe', 'creation', 'rationale', 'organization', 'reforms', 
            'standards', 'communication', 'mechanisms', 'address', 'criteria', 'assign', 'strength',  'innovation', 
            'empirical', 'derivation', 'recognition', 'characterized', 
            'specificity', 'contribute', 'establishment', 'distribution', 'transformation', 'sustainable', 
            'accomplishment', 'methodology', 'associated', 'categorization', 'attributes', 'initiated', 
            'preservation', 'developing', 'collaboration', 'equity', 'construct', 'relevance', 'strategy', 
            'continuously', 'exemplified', 'pertaining', 'implemented', 'represent', 'prioritize', 'verified', 
            'distinction', 'objective', 'commonly', 'competence', 'prioritization', 'strategic', 'resource', 
            'dynamics', 'indicative', 'dominance', 'facilitation', 'diversity', 'transparency', 'represents',
            'a', 'about', 'above', 'afghani', 'after', 'again', 'all', 'am', 'america',
            'american', 'among', 'an', 'and', 'angeles', 'annual', 'annually', 'annum',
            'any', 'apr', 'april', 'are', 'ariary', 'as', 'at', 'atlantic', 'aug',
            'august', 'b', 'baht', 'balboa', 'be', 'because', 'been', 'before', 'being',
            'below', 'between', 'billion', 'birr', 'blvd', 'bolivar', 'boliviano', 'both',
            'boulevard', 'business', 'but', 'by', 'c', 'can', 'cedi', 'chicago', 'city',
            'colon', 'commonwealth', 'coopers', 'country', 'county', 'creek', 'córdoba',
            'd', 'daily', 'dalasi', 'date', 'day', 'dec', 'december', 'deloitte', 'denar',
            'detroit', 'did', 'dinar', 'dirham', 'do', 'dobra', 'does', 'doing', 'dong',
            'down', 'dram', 'during', 'e', 'each', 'east', 'eight', 'eighteen', 'eighth',
            'eighty', 'eleven', 'end', 'ernst', 'escudo', 'euro', 'f', 'feb', 'february',
            'few', 'fifteen', 'fifth', 'fifty', 'financial', 'first', 'five', 'florin',
            'for', 'forint', 'forty', 'four', 'fourteen', 'fourth', 'from', 'further', 'g',
            'gourde', 'guarani', 'gulden', 'gulf', 'h', 'had', 'has', 'have', 'having',
            'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how',
            'hryvnia', 'hundred', 'i', 'if', 'ii', 'iii', 'in', 'include', 'indian', 'into',
            'is', 'it', 'item', 'its', 'itself', 'iv', 'ix', 'j', 'jan', 'january', 'jul',
            'july', 'jun', 'june', 'just', 'k', 'kina', 'kip', 'konvertibilna marka',
            'koruna', 'kpmg', 'krona', 'krone', 'kroon', 'kuna', 'kwacha', 'kwanza', 'kyat',
            'l', 'lake', 'lari', 'lats', 'lek', 'lempira', 'leone', 'leu', 'lev',
            'lilangeni', 'lira', 'litas', 'london', 'los', 'loti', 'm', 'manat', 'mar',
            'march', 'may', 'me', 'mediterranean', 'metical', 'miami', 'million', 'month',
            'monthly', 'more', 'most', 'mountain', 'my', 'myself', 'n', 'naira', 'nakfa',
            'new lira', 'new sheqel', 'ngultrum', 'nine', 'nineteen', 'ninety', 'ninth',
            'no', 'nor', 'north', 'northeast', 'northwest', 'not', 'nov', 'november', 'now',
            'nuevo sol', 'o', 'ocean', 'oct', 'october', 'of', 'off', 'on', 'once', 'one',
            'only', 'or', 'other', 'ouguiya', 'our', 'ours', 'ourselves', 'out', 'over',
            'own', 'p', 'pacific', 'parkway', 'pataca', 'peso', 'pound', 'pricewaterhouse',
            'pricewaterhousecoopers', 'pula', 'q', 'qtr', 'quarter', 'quarterly', 'quetzal',
            'r', 'rand', 'real', 'renminbi', 'report', 'rial', 'riel', 'ringgit', 'river',
            'riyal', 'ruble', 'rufiyaa', 'rupee', 'rupiah', 's', 'same', 'sea', 'second',
            'sep', 'sept', 'september', 'seven', 'seventeen', 'seventh', 'seventy', 'she',
            'shilling', 'should', 'six', 'sixteen', 'sixth', 'sixty', 'so', 'som', 'some',
            'somoni', 'south', 'southeast', 'southwest', 'special drawing rights', 'state',
            'statements', 'street', 'such', 't', 'taka', 'tala', 'ten', 'tenge', 'tenth',
            'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there',
            'these', 'they', 'third', 'thirteen', 'thirty', 'this', 'those', 'thousand',
            'three', 'through', 'to', 'tokyo', 'too', 'touche', 'trillion', 'tugrik',
            'twelve', 'twenty', 'two', 'u', 'under', 'united', 'until', 'up', 'usa', 'v',
            'vatu', 'very', 'vi', 'vii', 'viii', 'w', 'was', 'we', 'week', 'weekly', 'were',
            'west', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why',
            'with', 'won', 'x', 'xi', 'xii', 'xiii', 'xiv', 'xix', 'xv', 'xvi', 'xvii',
            'xviii', 'xx', 'y', 'year', 'yearly', 'yen', 'york', 'you', 'young', 'your',
            'yours', 'yourself', 'yourselves', 'z', 'zloty', 'et', 'et visa inc', 'eu', 'eu australia merchants','eu exert', 'europe',
            'following', ' following table',
            'company', 'corporation', 'inc', 'ltd', 'filing', 'report', 'fiscal',
            'year', 'quarter', 'financial', 'statement', 'form', 'securities',
            'exchange', 'commission', 'item', 'pursuant', 'section', 'act',
            'following', 'page', 'please', 'see', 'note', 'table', "i", "me",
            "my", "myself", "we", "our", "ours", "ourselves", "you", "your", 
            "yours", "yourself", "yourselves", "he", "him", "his", "himself", 
            "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", 
            "their", "theirs", "themselves", "what", "which", "who", "whom", "this",
            "that", "these", "those", "am", "is", "are", "was", "were", "be",
            "been", "being", "have", "has", "had", "having", "do", "does", "did", 
            "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", 
            "until", "while", "of", "at", "by", "for", "with", "about", "against", 
            "between", "into", "through", "during", "before", "after", "above", 
            "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", 
            "under", "again", "further", "then", "once", "here", "there", "when", 
            "where", "why", "how", "all", "any", "both", "each", "few", "more", 
            "most", "other", "some", "such", "no", "nor", "not", "only", "own", 
            "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", 
            "don", "should", "now"
        }
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        

    def clean_text(self, text: str) -> str:
        """Basic but efficient text cleaning"""
        # Convert to lowercase
        text = text.lower()

        # Remove HTML
        text = BeautifulSoup(text, 'html.parser').get_text()
        text = html.unescape(text)

        # Remove common SEC filing headers/footers
        text = re.sub(r'form\s+10-[kq].*?filing', '', text, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r'united states\s+securities and exchange commission.*?washington', '', text, flags=re.IGNORECASE)
        
        # Basic cleaning
        text = re.sub(r'&#\d+;', ' ', text) # Remove HTML numeric character references (e.g., &#123;)
        text = re.sub(r'&[a-zA-Z]+;', ' ', text) # Remove HTML named character entities (e.g., &amp;, &lt;)
        text = re.sub(r'\b\d+[a-zA-Z]\b', '', text) #Remove standalone number followed by a letter
        text = re.sub(r'\s*\n\s*', ' ', text) # Replace newline characters with a space, also removing any leading/trailing spaces around newlines
        text = re.sub(r'[•®©™]', '', text) # Remove special symbols
        text = re.sub(r'[^\w\s.]', '', text)  # Remove all punctuation except periods
        text = re.sub(r'\s+', ' ', text)      # Normalize whitespace
        text = re.sub(r'[\n\r\t]+', ' ', text)  # Replace newlines and tabs with space
        text = re.sub(r'\s{2,}', ' ', text)     # Remove multiple spaces
        
        # Remove standalone numbers and dates
        text = re.sub(r'\b\d+(?:\.\d+)?\s*(?:dollars|cents|shares)?\b', '', text)
        text = re.sub(r'\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},\s+\d{4}\b', '', text, flags=re.IGNORECASE)

        words = word_tokenize(text)
        words = [self.lemmatizer.lemmatize(self.stemmer.stem(word)) for word in words if word not in self.stopwords]
        return ' '.join(words).strip()

   
    def preprocess_for_analysis(self, text: str) -> str:
        """Final preprocessing before model analysis"""
        # Remove very short lines (likely headers/footers)
        lines = text.split('\n')
        lines = [line for line in lines if len(line.strip()) > 30]
        text = ' '.join(lines)
        
        # Remove common boilerplate phrases
        boilerplate = [
            "for the fiscal year ended",
            "for the period ended",
            "for the quarter ended",
            "table of contents",
            "index to financial statements",
        ]
        
        for phrase in boilerplate:
            text = text.replace(phrase, '')
        
        return text.strip()
    
    def extract_text_from_folders(self, root_folder: str) -> List[Dict[str, str]]:
        data = []
        for foldername, _, filenames in os.walk(root_folder):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                        text = file.read()
                    if text.strip():
                        cleaned_text = self.clean_text(text)
                        folder_levels = foldername.replace(root_folder, '').strip(os.sep).split(os.sep)
                        row = {
                            'Company_Name': folder_levels[2] if len(folder_levels) > 2 else '',
                            'Year': folder_levels[3] if len(folder_levels) > 3 else '',
                            'Filename': filename,
                            'Text': cleaned_text
                        }
                        data.append(row)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
        return data

    def save_to_csv(self, data: List[Dict[str, str]], output_file: str):
        fieldnames = ['Company_Name', 'Year', 'Filename', 'Text']
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)   
    

    def process_folders(self, root_folder: str, output_file: str):
        """Processes multiple folders and saves structured text data to CSV."""
        data = self.extract_text_from_folders(root_folder)
        self.save_to_csv(data, output_file)

if __name__ == "__main__":
    root_folder = input("Enter the root folder path: ")
    output_file = input("Enter the output CSV file path: ")
    preprocessor = ModelSECPreprocessor()
    preprocessor.process_folders(root_folder, output_file)
    print(f"CSV file saved to {output_file}")