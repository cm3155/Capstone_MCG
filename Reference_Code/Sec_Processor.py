from bs4 import BeautifulSoup
import html
import re
import os
import glob
from typing import Dict, List, Tuple
import spacy


class SECProcessor:
    def __init__(self, company_name: str, year: int):
        self.company_name = company_name.lower().replace(' ', '_')
        self.year = year
        self.base_dir = f"data/{self.company_name}/{self.year}"
        self.processed_data = {}
        self.nlp = spacy.load('en_core_web_sm')
        
        # Define custom stopwords
        # Used this to help  
        # https://sraf.nd.edu/textual-analysis/stopwords/
        # https://github.com/stopwords-iso/stopwords-en/blob/master/stopwords-en.txt
        self.custom_stopwords = { 
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
        'following', ' following table'}
   # Combine spaCy's default stopwords with custom stopwords
        self.all_stopwords = self.nlp.Defaults.stop_words.union(self.custom_stopwords)


    def clean_text(self, text: str) -> str:
        """Clean raw text by removing HTML, special characters, and extra spaces."""
        # Convert to lowercase early to ensure consistent processing
        text = text.lower()
        
        soup = BeautifulSoup(text, 'html.parser')
        text = soup.get_text()
        text = html.unescape(text)

        # Enhanced text cleaning
        text = re.sub(r'&#\d+;', ' ', text)
        text = re.sub(r'&[a-zA-Z]+;', ' ', text)
        text = re.sub(r'\s*\n\s*', ' ', text)
        text = re.sub(r'[•®©™]', '', text)
        text = re.sub(r'\b\d+\b', '', text)  # Remove standalone numbers
        text = re.sub(r'[^\w\s]', ' ', text)  # Remove punctuation
        text = re.sub(r'\s+', ' ', text)      # Normalize whitespace
        
        return text.strip()

    def is_valid_token(self, token) -> bool:
        """
        Check if a token should be kept in the processed text.
        Returns False for stopwords, punctuation, and other unwanted tokens.
        """
        return (
            token.text.lower() not in self.all_stopwords and
            not token.is_stop and
            not token.is_punct and
            not token.is_space and
            len(token.text.strip()) > 1  # Remove single characters
        )

    def clean_phrase(self, phrase: str) -> str:
        """Clean a phrase by removing stopwords and unwanted characters."""
        doc = self.nlp(phrase.lower())
        cleaned_tokens = [token.text for token in doc if self.is_valid_token(token)]
        return ' '.join(cleaned_tokens)

    def extract_features(self, text: str) -> Tuple[List[str], List[str]]:
        """
        Extract sentences and important phrases from text with improved stopword filtering.
        Returns cleaned sentences and unique keywords/phrases.
        """
        doc = self.nlp(text)
        sentences = []
        important_phrases = set()

        # Process sentences
        for sent in doc.sents:
            cleaned_tokens = [
                token.text for token in sent 
                if self.is_valid_token(token)
            ]
            if cleaned_tokens:  # Only add non-empty sentences
                sentences.append(' '.join(cleaned_tokens))

        # Extract and clean noun chunks
        for chunk in doc.noun_chunks:
            cleaned_chunk = self.clean_phrase(chunk.text)
            if cleaned_chunk:
                important_phrases.add(cleaned_chunk)

        # Extract and clean named entities
        for ent in doc.ents:
            cleaned_ent = self.clean_phrase(ent.text)
            if cleaned_ent:
                important_phrases.add(cleaned_ent)

        return sentences, sorted(list(important_phrases))

    def process_files(self) -> Dict[str, Dict[str, List[str]]]:
        """Process all files in the specified directory."""
        processed_data = {}
        file_pattern = os.path.join(self.base_dir, "*.txt")
        
        for filepath in glob.glob(file_pattern):
            filename = os.path.basename(filepath)
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    text = file.read()
                    if not text.strip():
                        continue  # Skip empty files
                        
                    cleaned_text = self.clean_text(text)
                    sentences, keywords = self.extract_features(cleaned_text)
                    
                    if sentences or keywords:  # Only add if we have valid content
                        processed_data[filename] = {
                            "sentences": sentences,
                            "keywords": keywords
                        }
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                
        return processed_data

def clean_sec_data(company_name: str, year: int) -> Dict[str, Dict[str, List[str]]]:
    """Process SEC data for a specific company and year."""
    processor = SECProcessor(company_name, year)
    return processor.process_files()