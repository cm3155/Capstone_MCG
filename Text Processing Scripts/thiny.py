import os
import re

# Define the folder path where the files are located
folder_path = '/path/to/your/folder'

# List of bank names and tickers to insert space between
bank_name_map = {
    'JPMorgan Chase & Co': 'jpmorgan_chase_&_co',
    'Bank of America Corp': 'bank_of_america_corp',
    'Citigroup Inc': 'citigroup_inc',
    'Wells Fargo Co': 'wells_fargo_&_co',
    'Goldman Sachs Group Inc': 'goldman_sachs_group,_inc.',
    'Morgan Stanley': 'morgan_stanley',
    'US Bancorp': 'u.s._bancorp',
    'PNC Financial Services Group Inc': 'pnc_financial_services_group,_inc.',
    'Truist Financial Corp': 'truist_financial,_corp',
    'Capital One Financial Corp': 'capital_one_financial_corp',
    'Charles Schwab Corp': 'charles_schwab,_the',
    'Bank of New York Mellon Corp': 'bank_of_new_york_mellon,_the',
    'State Street Corp': 'state_street,_corp',
    'American Express Co': 'american_express_company',
    'HSBC North America Holdings Inc': 'hsbc_north_america_holdings,_inc',
    'First Citizens BancShares Inc': 'first_citizens_bancshares,_inc',
    'Citizens Financial Group Inc': 'citizens_financial_group,_inc',
    'Fifth Third Bancorp': 'fifth_third_bancorp',
    'MT Bank Corp': 'm&t_bank,_corp',
    'Huntington Bancshares Inc': 'huntington_bancshares,_inc',
    'Ally Financial Inc': 'ally_financial_inc',
    'KeyCorp': 'keycorp',
    'Ameriprise Financial Inc': 'ameriprise_financial_inc',
    'Banco Santander': 'santander_holdings,_usa,_inc',
    'Regions Financial Corp': 'regions_financial,_corp',
    'Northern Trust Corp': 'northern_trust,_corp',
    'Discover Financial Services': 'discover_financial_services',
    'Synchrony Financial': 'synchrony_financial',
    'Flagstar Financial Inc': 'flagstar_financial,_inc',
    'Raymond James Financial Inc': 'raymond_james_financial,_inc',
    'First Horizon Corp': 'first_horizon,_corp',
    'Western Alliance Bancorp': 'western_alliance_bancorp',
    'Western Alliance Bancorporation': 'western_alliance_bancorp',
    'Comerica Inc': 'comerica_inc',
    'Webster Financial Corp': 'webster_financial,_corp',
    'East West Bancorp Inc': 'east_west_bancorp,_inc',
    'Popular Inc': 'popular,_inc',
    'John Deere Capital Corp': 'john_deere_capital,_corp',
    'Wintrust Financial Corp': 'wintrust_financial,_corp',
    'Valley National Bancorp': 'valley_national_bancorp',
    'Synovus Financial Corp': 'synovus_financial,_corp',
    'Old National Bancorp': 'old_national_bancorp',
    'Columbia Banking System Inc': 'columbia_banking_system,_inc',
    'CullenFrost Bankers Inc': 'cullen_frost',
    'Pinnacle Financial Partners Inc': 'pinnacle_financial_partners,_inc',
    'BOK Financial Corp': 'bok_financial_corp',
    'FNB Corp': 'f.n.b._corp',
    'UMB Financial Corp': 'umb_financial,_corp',
    'South State Corp': 'southstate,_corp',
    'Associated BancCorp': 'associated_banc-corp',
    'Prosperity Bancshares Inc': 'prosperity_bancshares,_inc'
}


def add_space_between_bank_and_ticker(file_name):
    """
    Function to add a space between the bank name and the ticker symbol in the file name.
    """
    # Loop through the bank names and tickers to add space between them
    for bank_name, ticker in bank_name_map.items():
        # Build a regex pattern to match the bank name followed immediately by the ticker
        pattern = re.compile(rf"({re.escape(bank_name)})(?={ticker})")
        # If a match is found, add a space between the bank name and ticker
        file_name = re.sub(pattern, r"\1 " + ticker, file_name)
    return file_name

def rename_files_in_directory(folder_path):
    """
    Renames files in the specified directory by adding a space between bank names and tickers.
    """
    # List all files in the folder
    for file_name in os.listdir(folder_path):
        # Get the full path of the file
        file_path = os.path.join(folder_path, file_name)
        
        # If it's a file, rename it
        if os.path.isfile(file_path):
            new_file_name = add_space_between_bank_and_ticker(file_name)
            
            # If the file name changed, rename it
            if new_file_name != file_name:
                new_file_path = os.path.join(folder_path, new_file_name)
                os.rename(file_path, new_file_path)
                print(f'Renamed: {file_name} -> {new_file_name}')

# Run the renaming function
rename_files_in_directory('C:/Users/cassi/Capstone_MCG/All_Data_Processed/txt_earning_calls')