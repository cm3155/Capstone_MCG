# Analyzing AI Capabilities of Large Financial Service Organizations

## Organization

* All_Data: Contains all raw text data, grouped by source (News Article, SEC 10-K or 10-Q, Earnings Call Transcript). 
* All_Data_Processed: Contains cleaned and processed text data, grouped by bank. 
* Analysis: Contains scripts relating to the analysis portion of the project, including clustering, calibration, visualization, and quantitative ranking. 
* Scoring: Contains scripts and csvs relating to DATA framework scoring, including final DATA scores. Scores are broken up into presence, maturity, and strategy scores. 
* Text Processing Scripts: Contains scripts that were used to manipulate, engineer, and clean raw text data. The most important to our analysis include Files_Preprocessor.py (cleans raw text), FullPreprocessor.py (preprocesses and cleans text, including stemming and lemmatization), and Keyword_Extractor.py (adapted from last year's keyword extractor; was used to generate keywords). 

## Description

With the development of new Artificial Intelligence technologies and the growth of fintech competition, 
the industry has become heavily focused on adopting an Information Led Business (ILB) approach to increase 
competitive advantages and improve the speed of decision-making. Large banks vary in their current use of 
traditional ML and the adoption of advanced data analytics to provide current customers service and pursue 
new potential opportunities. MCG wants our reporting to build a research background upon which they can 
identify banks as potential customers and quantify via a developed framework how working with MCG can improve 
their AI/analytic capabilities in ways that lead to increased financial performance

## Methodology

This project uses both structured and unstructured data from a variety of sources to perform an in depth review 
of US banks’ AI and data analytics capabilities from 2020-2024. The structured data includes the banks’ financial 
performance metrics and history over the analyzed period. The data was obtained from sources including  
George Washington University Library Financial Research Databases, Bloomberg terminals, Factset databases, 
individual bank websites (Investor Relations, Financial Disclosures), and publicly available government data 
(SEC filings). In terms of the unstructured (text) data, this compromises of earnings call transcripts, 10-K/10-Q 
filings, public disclosures and bank-generated press releases, analyst reports, and news articles about AI and data 
analytics capabilities. We obtained these text based sources  from the same GW Library Financial Research Databases, 
individual bank websites, and publicly available government databases (such as SEC filings). By acquiring this 
structured and unstructured data, it allowed us to conduct a thorough analysis of how AI and data capabilities affect 
the financial performance of these top 50 banks. 





