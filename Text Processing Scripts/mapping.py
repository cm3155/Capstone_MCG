import os

# Dictionary mapping CIK numbers to bank names
cik_to_bank = {
    "0000040729": "ally_financial_inc",
    "0000004962": "american_express_company",
    "0000820027": "ameriprise_financial,_inc",
    "0000007789": "associated_banc-corp",
    "0000070858": "bank_of_america_corporation",
    "0001390777": "bank_of_new_york_mellon_corporation,_the",
    "0000875357": "bok_financial_corporation",
    "0000927628": "capital_one_financial_corporation",
    "0000316709": "charles_schwab_corporation,_the",
    "0000831001": "citigroup_inc",
    "0000759944": "citizens_financial_group,_inc",
    "0000887343": "columbia_banking_system,_inc",
    "0000028412": "comerica_incorporated",
    "0000039263": "cullen_frost",
    "0001393612": "discover_financial_services",
    "0001069157": "east_west_bancorp,_inc",
    "0000037808": "f.n.b._corporation",
    "0000035527": "fifth_third_bancorp",
    "0000798941": "first_citizens_bancshares,_inc",
    "0000036966": "first_horizon_corporation",
    "0000910073": "flagstar_financial,_inc",
    "0000886982": "goldman_sachs_group,_inc.,_the",
    "0000083246": "hsbc_north_america_holdings_inc",
    "0000049196": "huntington_bancshares_incorporated",
    "0000027673": "john_deere_capital_corporation",
    "0000019617": "jpmorgan_chase_&_co",
    "0000091576": "keycorp",
    "0000036270": "m&t_bank_corporation",
    "0000895421": "morgan_stanley",
    "0000073124": "northern_trust_corporation",
    "0000707179": "old_national_bancorp",
    "0001115055": "pinnacle_financial_partners,_inc",
    "0000713676": "pnc_financial_services_group,_inc.,_the",
    "0000763901": "popular,_inc",
    "0001068851": "prosperity_bancshares,_inc",
    "0000720005": "raymond_james_financial,_inc",
    "0001281761": "regions_financial_corporation",
    "0000811830": "santander_holdings_usa,_inc",
    "0000764038": "southstate_corporation",
    "0000093751": "state_street_corporation",
    "0001601712": "synchrony_financial",
    "0000018349": "synovus_financial_corp",
    "0000092230": "truist_financial_corporation",
    "0000036104": "u.s._bancorp",
    "0000101382": "umb_financial_corporation",
    "0000714310": "valley_national_bancorp",
    "0000801337": "webster_financial_corporation",
    "0000072971": "wells_fargo_&_company",
    "0001212545": "western_alliance_bancorporation",
    "0001015328": "wintrust_financial_corporation"
}

def rename_files(root_directory):
    for parent, subfolders, files in os.walk(root_directory):
        for file in files:
            cik = file.split('.')[0]  # Extract filename without extension
            if cik in cik_to_bank:
                subfolder = os.path.basename(parent)
                grandparent = os.path.basename(os.path.dirname(parent))
                new_name = f"{cik_to_bank[cik]}_{grandparent}_{subfolder}{os.path.splitext(file)[1]}"
                old_path = os.path.join(parent, file)
                new_path = os.path.join(parent, new_name)
                os.rename(old_path, new_path)
                print(f"Renamed: {old_path} -> {new_path}")

# Example usage
root_directory = "C:/Users/cassi/Capstone_MCG/Last Sources"
rename_files(root_directory)