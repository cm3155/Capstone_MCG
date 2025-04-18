import os
import shutil

# Updated mapping of bank names to their first column format
bank_name_map = {
    'JPMorgan Chase Co': 'jpmorgan_chase_&_co',
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
    'HSBC Holdings': 'hsbc_north_america_holdings,_inc',
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
    'First Horizon National Corp': 'first_horizon,_corp',
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
    'SouthState Corp': 'southstate,_corp',
    'Associated BancCorp': 'associated_banc-corp',
    'Prosperity Bancshares Inc': 'prosperity_bancshares,_inc'
}

# Directory where your files are located
source_dir = 'C:/Users/cassi/Capstone_MCG/All_Data_Processed/txt_earning_calls'

# Loop through files in the source directory
for root, dirs, files in os.walk(source_dir):
    for file in files:
        # Convert filename to lowercase for case-insensitive matching
        filename = file.lower()
        
        # Loop through the bank names and check if the name is in the filename
        for bank_name in bank_name_map:
            if bank_name.lower() in filename:  # case-insensitive matching
                formatted_name = bank_name_map[bank_name]
                
                # Define the new folder structure: ally_financial_inc/Earnings_Calls/filename.txt
                new_folder = os.path.join(source_dir, formatted_name, 'Earnings_Calls')
                
                # Create the folder if it doesn't exist
                if not os.path.exists(new_folder):
                    os.makedirs(new_folder)
                
                # Move the file to the new folder
                shutil.move(os.path.join(root, file), os.path.join(new_folder, file))
                print(f"Moved file '{file}' to '{new_folder}'")
                break  # Stop searching once the correct bank is found
        else:
            print(f"Could not extract bank name from the file '{file}'")
