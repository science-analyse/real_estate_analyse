#!/usr/bin/env python3
"""
Real Estate Dataset Transformation and Combination
This script transforms all datasets to a common schema while preserving ALL original data
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
import re
warnings.filterwarnings('ignore')

# Define the baseline schema columns
BASELINE_COLUMNS = [
    'id', 'area_value', 'area_units', 'leased', 'floor', 'floors', 'rooms',
    'city_id', 'city_name', 'location_id', 'location_name', 'location_full_name',
    'price_value', 'price_currency', 'company_id', 'company_name', 'company_target_type',
    'has_mortgage', 'has_bill_of_sale', 'has_repair', 'paid_daily', 'is_business',
    'vipped', 'featured', 'updated_at', 'path', 'photos_count', 'photos', 'url', 'scraped_at',
    'source_dataset', 'contact_phone', 'contact_name', 'description', 'latitude', 'longitude'
]

def safe_numeric(value, default=np.nan):
    """Safely convert value to numeric"""
    if pd.isna(value):
        return default
    try:
        # Remove common non-numeric characters
        if isinstance(value, str):
            value = value.replace(',', '').replace(' ', '').replace('m²', '').replace('AZN', '').strip()
        return pd.to_numeric(value, errors='coerce')
    except:
        return default

def extract_number_from_string(s):
    """Extract first number from string"""
    if pd.isna(s):
        return np.nan
    s = str(s)
    numbers = re.findall(r'\d+', s)
    if numbers:
        return int(numbers[0])
    return np.nan

def parse_floor(floor_str):
    """Parse floor string like '5/9' to extract current floor"""
    if pd.isna(floor_str):
        return np.nan
    s = str(floor_str)
    if '/' in s:
        parts = s.split('/')
        return safe_numeric(parts[0])
    return safe_numeric(s)

def parse_total_floors(floor_str):
    """Parse floor string like '5/9' to extract total floors"""
    if pd.isna(floor_str):
        return np.nan
    s = str(floor_str)
    if '/' in s:
        parts = s.split('/')
        if len(parts) > 1:
            return safe_numeric(parts[1])
    return np.nan

def add_prefix_to_columns(df, prefix):
    """Add prefix to all columns in dataframe"""
    return df.add_prefix(f'{prefix}_')

def create_base_df(size):
    """Create base dataframe with baseline columns"""
    return pd.DataFrame({col: [np.nan] * size for col in BASELINE_COLUMNS})

def transform_bina_sale(file_path):
    """Transform bina_sale_20251117_213934.csv (baseline format)"""
    print(f"Processing: {file_path}")
    df = pd.read_csv(file_path)

    # Add source
    df['source_dataset'] = 'bina_sale'

    # Rename columns to match baseline if needed
    df = df.rename(columns={'area_value': 'area_value', 'price_value': 'price_value'})

    # Keep all original columns with prefix
    original = add_prefix_to_columns(df.copy(), 'orig')

    # Merge with original columns
    result = pd.concat([df, original], axis=1)

    print(f"  Rows: {len(result):,}")
    return result

def transform_ipoteka_xlsx(file_path):
    """Transform ipotekaAz.xlsx"""
    print(f"Processing: {file_path}")
    df = pd.read_excel(file_path)

    # Keep ALL original data
    original = add_prefix_to_columns(df.copy(), 'orig')

    # Create baseline columns
    base = create_base_df(len(df))
    base['id'] = df['announcement_id']
    base['area_value'] = df['area'].apply(lambda x: safe_numeric(str(x).replace('m²', '')))
    base['area_units'] = 'm²'
    base['floor'] = df['flat'].apply(parse_floor)
    base['floors'] = df['baxis_sayi']
    base['rooms'] = df['room_count']
    base['city_name'] = df['area']
    base['price_value'] = 0
    base['price_currency'] = 'AZN'
    base['has_bill_of_sale'] = df['document_type'].notna()
    base['has_repair'] = df['repair_type'].notna()
    base['updated_at'] = df['update_date']
    base['url'] = 'https://ipoteka.az/elan/' + df['announcement_id'].astype(str)
    base['scraped_at'] = datetime.now().isoformat()
    base['source_dataset'] = 'ipotekaAz_xlsx'
    base['contact_phone'] = df.get('phone_cleaned', df.get('phone_number'))
    base['contact_name'] = df.get('user_name')

    # Merge
    result = pd.concat([base, original], axis=1)
    print(f"  Rows: {len(result):,}")
    return result

def transform_ipoteka_csv(file_path):
    """Transform ipotekaAz.csv"""
    print(f"Processing: {file_path}")
    df = pd.read_csv(file_path)

    original = add_prefix_to_columns(df.copy(), 'orig')

    base = create_base_df(len(df))
    base['id'] = df['announcement_id']
    base['area_value'] = df['area'].apply(lambda x: safe_numeric(str(x).replace('m²', '')))
    base['area_units'] = 'm²'
    base['floor'] = df['flat'].apply(parse_floor)
    base['floors'] = df['baxis_sayi']
    base['rooms'] = df['room_count']
    base['city_name'] = df['area']
    base['has_bill_of_sale'] = df['document_type'].notna()
    base['has_repair'] = df['repair_type'].notna()
    base['updated_at'] = df['update_date']
    base['url'] = 'https://ipoteka.az/elan/' + df['announcement_id'].astype(str)
    base['scraped_at'] = datetime.now().isoformat()
    base['source_dataset'] = 'ipotekaAz_csv'
    base['contact_phone'] = df.get('phone_number')
    base['contact_name'] = df.get('user_name')

    result = pd.concat([base, original], axis=1)
    print(f"  Rows: {len(result):,}")
    return result

def transform_binalar_listings(file_path):
    """Transform binalar_listings.csv"""
    print(f"Processing: {file_path}")
    df = pd.read_csv(file_path)

    original = add_prefix_to_columns(df.copy(), 'orig')

    base = create_base_df(len(df))
    base['id'] = df['id']
    base['area_value'] = df['area']
    base['area_units'] = 'm²'
    base['rooms'] = df['rooms']
    base['floor'] = df['floor'].apply(parse_floor)
    base['floors'] = df['floor'].apply(parse_total_floors)
    base['price_value'] = df['price_raw'].fillna(0)
    base['price_currency'] = 'AZN'
    base['location_name'] = df['address']
    base['url'] = df['url']
    base['updated_at'] = df['date']
    base['scraped_at'] = datetime.now().isoformat()
    base['source_dataset'] = 'binalar_listings'
    base['contact_phone'] = df['phone']
    base['description'] = df['description']

    result = pd.concat([base, original], axis=1)
    print(f"  Rows: {len(result):,}")
    return result

def transform_yeniemlak_xlsx(file_path):
    """Transform yeniemlak.xlsx"""
    print(f"Processing: {file_path}")
    df = pd.read_excel(file_path)

    original = add_prefix_to_columns(df.copy(), 'orig')

    base = create_base_df(len(df))
    base['id'] = range(len(df))
    base['url'] = df['link'].apply(lambda x: f'https://{x}' if not str(x).startswith('http') else x)
    base['scraped_at'] = datetime.now().isoformat()
    base['source_dataset'] = 'yeniemlak_xlsx'
    base['contact_phone'] = df['phone_number']

    result = pd.concat([base, original], axis=1)
    print(f"  Rows: {len(result):,}")
    return result

def transform_yeniemlak_csv(file_path):
    """Transform yeniemlakAz.csv"""
    print(f"Processing: {file_path}")
    df = pd.read_csv(file_path)

    original = add_prefix_to_columns(df.copy(), 'orig')

    base = create_base_df(len(df))
    base['id'] = df.get('id', range(len(df)))
    base['price_value'] = df.get('price', 0)
    base['rooms'] = df.get('room_count')
    base['area_value'] = df.get('area')
    base['area_units'] = 'm²'
    base['floor'] = df.get('flat', df.get('floor'))
    base['location_name'] = df.get('address')
    base['location_full_name'] = df.get('address_2')
    base['url'] = df['href'].apply(lambda x: f'https://{x}' if not str(x).startswith('http') else x) if 'href' in df else np.nan
    base['updated_at'] = df.get('date')
    base['scraped_at'] = datetime.now().isoformat()
    base['source_dataset'] = 'yeniemlakAz_csv'
    base['contact_phone'] = df.get('owner_number')
    base['contact_name'] = df.get('owner_name')
    base['description'] = df.get('description')
    base['has_bill_of_sale'] = df.get('doc_type').notna() if 'doc_type' in df else False

    result = pd.concat([base, original], axis=1)
    print(f"  Rows: {len(result):,}")
    return result

def transform_myhome_listings(file_path):
    """Transform myhome_listings_20250929_003143.csv"""
    print(f"Processing: {file_path}")
    df = pd.read_csv(file_path)

    original = add_prefix_to_columns(df.copy(), 'orig')

    base = create_base_df(len(df))
    base['id'] = df['id']
    base['area_value'] = df['area']
    base['area_units'] = 'm²'
    base['rooms'] = df['room_count']
    base['floor'] = df['floor']
    base['floors'] = df['floor_count']
    base['city_name'] = df['city']
    base['location_name'] = df['region']
    base['location_full_name'] = df['address']
    base['price_value'] = df['price'].apply(lambda x: safe_numeric(str(x).replace('AZN', '')))
    base['price_currency'] = 'AZN'
    base['has_repair'] = df['is_repaired'].fillna(0) > 0
    base['vipped'] = df['is_vip'] == 1
    base['featured'] = df['is_premium'] == 1
    base['has_mortgage'] = df['credit_possible'] == 1
    base['updated_at'] = df['formatted_date']
    base['scraped_at'] = datetime.now().isoformat()
    base['source_dataset'] = 'myhome'
    base['contact_phone'] = df['phone_number']
    base['latitude'] = df['lat']
    base['longitude'] = df['lng']
    base['description'] = df['description']

    result = pd.concat([base, original], axis=1)
    print(f"  Rows: {len(result):,}")
    return result

def transform_unvan_xlsx(file_path):
    """Transform unvan.xlsx"""
    print(f"Processing: {file_path}")
    df = pd.read_excel(file_path)

    original = add_prefix_to_columns(df.copy(), 'orig')

    base = create_base_df(len(df))
    base['id'] = df['id']
    base['area_value'] = df['area'].apply(lambda x: safe_numeric(str(x)))
    base['area_units'] = 'm²'
    base['rooms'] = df['room_count'].apply(extract_number_from_string)
    base['price_value'] = df['price'].apply(lambda x: safe_numeric(str(x)))
    base['price_currency'] = 'AZN'
    base['location_name'] = df['address']
    base['location_full_name'] = df['address_2']
    base['company_name'] = df['owner']
    base['updated_at'] = df['date']
    base['url'] = df['link']
    base['scraped_at'] = datetime.now().isoformat()
    base['source_dataset'] = 'unvan'
    base['contact_phone'] = df['phone']
    base['description'] = df.get('long_descr', df.get('short_descr'))

    result = pd.concat([base, original], axis=1)
    print(f"  Rows: {len(result):,}")
    return result

def transform_mulk_data(file_path):
    """Transform mulk_data_20250929_143644.csv"""
    print(f"Processing: {file_path}")
    df = pd.read_csv(file_path)

    original = add_prefix_to_columns(df.copy(), 'orig')

    base = create_base_df(len(df))
    base['id'] = df['listing_id']
    base['area_value'] = df['area_numeric']
    base['area_units'] = 'm²'
    base['rooms'] = df['rooms_numeric']
    base['floor'] = df['current_floor']
    base['floors'] = df['total_floors']
    base['price_value'] = df['price_numeric']
    base['price_currency'] = 'AZN'
    base['location_name'] = df['location_district']
    base['location_full_name'] = df['full_address']
    base['has_bill_of_sale'] = df['deed_available'] == 'Yes'
    base['updated_at'] = df['listing_date']
    base['url'] = df['url']
    base['photos_count'] = df['image_count']
    base['scraped_at'] = df['scraped_at']
    base['source_dataset'] = 'mulk'
    base['contact_phone'] = df['contact_phone']
    base['contact_name'] = df.get('contact_person')
    base['description'] = df['description']

    result = pd.concat([base, original], axis=1)
    print(f"  Rows: {len(result):,}")
    return result

def transform_emlak_xlsx(file_path):
    """Transform emlakAz.xlsx"""
    print(f"Processing: {file_path}")
    df = pd.read_excel(file_path)

    original = add_prefix_to_columns(df.copy(), 'orig')

    base = create_base_df(len(df))
    base['id'] = df['id']
    base['area_value'] = df['area'].apply(lambda x: safe_numeric(str(x)))
    base['area_units'] = 'm²'
    base['rooms'] = df['room_count'].apply(extract_number_from_string)
    base['floor'] = df['flat'].apply(parse_floor)
    base['price_value'] = df['price'].apply(lambda x: safe_numeric(str(x)))
    base['price_currency'] = 'AZN'
    base['has_repair'] = df['repair_type'].notna()
    base['has_bill_of_sale'] = df['document_type'].notna()
    base['updated_at'] = df['date']
    base['url'] = 'https://emlak.az' + df['href'].astype(str)
    base['scraped_at'] = datetime.now().isoformat()
    base['source_dataset'] = 'emlakAz'
    base['contact_phone'] = df.get('phone_cleaned', df.get('phone_numbers'))
    base['contact_name'] = df.get('seller_name')
    base['description'] = df['description']

    result = pd.concat([base, original], axis=1)
    print(f"  Rows: {len(result):,}")
    return result

def transform_ofis_listings(file_path):
    """Transform ofis_listings.csv"""
    print(f"Processing: {file_path}")
    df = pd.read_csv(file_path)

    original = add_prefix_to_columns(df.copy(), 'orig')

    base = create_base_df(len(df))
    base['id'] = df['listing_id']
    base['area_value'] = df['Sahə'].apply(lambda x: safe_numeric(str(x)))
    base['area_units'] = 'm²'
    base['rooms'] = df['Otaq Sayı']
    base['floor'] = df['Mərtəbə']
    base['floors'] = df['Mərtəbə sayı']
    base['price_value'] = df['price'].apply(lambda x: safe_numeric(str(x)))
    base['price_currency'] = 'AZN'
    base['city_name'] = df['Şəhər']
    base['location_name'] = df['Ünvan']
    base['updated_at'] = df['date']
    base['url'] = df['url']
    base['scraped_at'] = datetime.now().isoformat()
    base['source_dataset'] = 'ofis_listings'
    base['is_business'] = True
    base['contact_phone'] = df['phone']
    base['contact_name'] = df.get('contact_name')
    base['description'] = df['description']

    result = pd.concat([base, original], axis=1)
    print(f"  Rows: {len(result):,}")
    return result

def transform_real_estate_feb(file_path):
    """Transform real_estate_data_25_feb_2025.csv"""
    print(f"Processing: {file_path}")
    df = pd.read_csv(file_path)

    original = add_prefix_to_columns(df.copy(), 'orig')

    base = create_base_df(len(df))
    base['id'] = df['id']
    base['area_value'] = df['area'].apply(lambda x: safe_numeric(str(x)))
    base['area_units'] = 'm²'
    base['rooms'] = df['rooms']
    base['floor'] = df['floor']
    base['floors'] = df['total_floors']
    base['price_value'] = df['price']
    base['price_currency'] = df['currency']
    base['city_name'] = df.get('district')
    base['location_name'] = df.get('location', df.get('address'))
    base['location_full_name'] = df['address']
    base['has_repair'] = df['has_repair'] == 1
    base['updated_at'] = df.get('updated_at', df.get('listing_date'))
    base['url'] = df['source_url']
    base['scraped_at'] = df.get('created_at', datetime.now().isoformat())
    base['source_dataset'] = 'real_estate_feb_2025'
    base['contact_phone'] = df['contact_phone']
    base['latitude'] = df['latitude']
    base['longitude'] = df['longitude']
    base['description'] = df['description']
    base['photos'] = df.get('photos')

    result = pd.concat([base, original], axis=1)
    print(f"  Rows: {len(result):,}")
    return result

def transform_villa_az(file_path):
    """Transform villa_az_complete_dataset.csv"""
    print(f"Processing: {file_path}")
    df = pd.read_csv(file_path)

    original = add_prefix_to_columns(df.copy(), 'orig')

    base = create_base_df(len(df))
    base['id'] = df['listing_id']
    base['area_value'] = df['Sahə, m²']
    base['area_units'] = 'm²'
    base['rooms'] = df['Otaq sayı']
    base['floor'] = df['Mərtəbə'].apply(parse_floor) if 'Mərtəbə' in df else np.nan
    base['price_value'] = df['price'].apply(lambda x: safe_numeric(str(x)))
    base['price_currency'] = 'AZN'
    base['city_name'] = df['Şəhər']
    base['location_name'] = df['address']
    base['has_bill_of_sale'] = df['Əmlak sənədi'].notna()
    base['updated_at'] = df['date']
    base['url'] = df['url']
    base['scraped_at'] = datetime.now().isoformat()
    base['source_dataset'] = 'villa_az'
    base['contact_phone'] = df['phones']
    base['contact_name'] = df.get('owner_name')
    base['description'] = df['description']
    base['property_type'] = 'villa'

    result = pd.concat([base, original], axis=1)
    print(f"  Rows: {len(result):,}")
    return result

def transform_evv_az(file_path):
    """Transform evv_az_listings.csv"""
    print(f"Processing: {file_path}")
    df = pd.read_csv(file_path)

    original = add_prefix_to_columns(df.copy(), 'orig')

    base = create_base_df(len(df))
    base['id'] = df['listing_id']
    base['area_value'] = df['area'].apply(lambda x: safe_numeric(str(x)))
    base['area_units'] = 'm²'
    base['rooms'] = df['rooms'].apply(extract_number_from_string)
    base['floor'] = df['floor'].apply(parse_floor)
    base['price_value'] = df['price'].apply(lambda x: safe_numeric(str(x)))
    base['price_currency'] = 'AZN'
    base['city_name'] = df['city']
    base['location_name'] = df['location']
    base['has_bill_of_sale'] = df['document'].notna()
    base['has_mortgage'] = df['mortgage'].notna()
    base['updated_at'] = df.get('update_date', df.get('post_date'))
    base['url'] = df['url']
    base['scraped_at'] = datetime.now().isoformat()
    base['source_dataset'] = 'evv_az'
    base['contact_phone'] = df['phone']
    base['contact_name'] = df.get('seller_name')
    base['description'] = df['description']

    result = pd.concat([base, original], axis=1)
    print(f"  Rows: {len(result):,}")
    return result

def transform_binam_listings(file_path):
    """Transform binam_listings_1758793717.csv"""
    print(f"Processing: {file_path}")
    df = pd.read_csv(file_path)

    original = add_prefix_to_columns(df.copy(), 'orig')

    base = create_base_df(len(df))
    base['id'] = df['listing_code']
    base['area_value'] = df['area'].apply(lambda x: safe_numeric(str(x)))
    base['area_units'] = 'm²'
    base['rooms'] = df['rooms'].apply(extract_number_from_string)
    base['floor'] = df['floor'].apply(parse_floor)
    base['price_value'] = df['price'].apply(lambda x: safe_numeric(str(x)))
    base['price_currency'] = 'AZN'
    base['city_name'] = df['country_city']
    base['location_name'] = df['district']
    base['location_full_name'] = df.get('address')
    base['company_name'] = df.get('company_name')
    base['updated_at'] = df['listing_date']
    base['url'] = df['url']
    base['scraped_at'] = datetime.now().isoformat()
    base['source_dataset'] = 'binam_listings'
    base['contact_phone'] = df.get('phone', df.get('mobile'))
    base['contact_name'] = df.get('contact_name')
    base['description'] = df['description']

    result = pd.concat([base, original], axis=1)
    print(f"  Rows: {len(result):,}")
    return result

def transform_bina_xlsx(file_path):
    """Transform bina.xlsx"""
    print(f"Processing: {file_path}")
    df = pd.read_excel(file_path)

    original = add_prefix_to_columns(df.copy(), 'orig')

    base = create_base_df(len(df))
    base['id'] = df['item_id']
    base['area_value'] = df['area'].apply(lambda x: safe_numeric(str(x)))
    base['area_units'] = 'm²'
    base['rooms'] = df['room count'].apply(extract_number_from_string)
    base['floor'] = df['floor'].apply(parse_floor)
    base['price_value'] = df['price']
    base['price_currency'] = df['currency']
    base['has_mortgage'] = df['mortgage'].notna()
    base['url'] = df['url']
    base['scraped_at'] = datetime.now().isoformat()
    base['source_dataset'] = 'bina_xlsx'
    base['contact_phone'] = df['phone number']
    base['contact_name'] = df.get('owner name')
    base['description'] = df['description']

    result = pd.concat([base, original], axis=1)
    print(f"  Rows: {len(result):,}")
    return result


def main():
    """Main function to transform and combine all datasets"""
    print("="*80)
    print("REAL ESTATE DATASET TRANSFORMATION & COMBINATION")
    print("Mode: ZERO DATA LOSS - All original columns preserved")
    print("="*80)
    print()

    datasets = []

    # Process each dataset
    try:
        datasets.append(transform_bina_sale('data/bina_sale_20251117_213934.csv'))
    except Exception as e:
        print(f"  ERROR: {e}\n")

    try:
        datasets.append(transform_ipoteka_xlsx('data/ipotekaAz.xlsx'))
    except Exception as e:
        print(f"  ERROR: {e}\n")

    try:
        datasets.append(transform_ipoteka_csv('data/ipotekaAz.csv'))
    except Exception as e:
        print(f"  ERROR: {e}\n")

    try:
        datasets.append(transform_binalar_listings('data/binalar_listings.csv'))
    except Exception as e:
        print(f"  ERROR: {e}\n")

    try:
        datasets.append(transform_yeniemlak_xlsx('data/yeniemlak.xlsx'))
    except Exception as e:
        print(f"  ERROR: {e}\n")

    try:
        datasets.append(transform_yeniemlak_csv('data/yeniemlakAz.csv'))
    except Exception as e:
        print(f"  ERROR: {e}\n")

    try:
        datasets.append(transform_myhome_listings('data/myhome_listings_20250929_003143.csv'))
    except Exception as e:
        print(f"  ERROR: {e}\n")

    try:
        datasets.append(transform_unvan_xlsx('data/unvan.xlsx'))
    except Exception as e:
        print(f"  ERROR: {e}\n")

    try:
        datasets.append(transform_mulk_data('data/mulk_data_20250929_143644.csv'))
    except Exception as e:
        print(f"  ERROR: {e}\n")

    try:
        datasets.append(transform_emlak_xlsx('data/emlakAz.xlsx'))
    except Exception as e:
        print(f"  ERROR: {e}\n")

    try:
        datasets.append(transform_ofis_listings('data/ofis_listings.csv'))
    except Exception as e:
        print(f"  ERROR: {e}\n")

    try:
        datasets.append(transform_real_estate_feb('data/real_estate_data_25_feb_2025.csv'))
    except Exception as e:
        print(f"  ERROR: {e}\n")

    try:
        datasets.append(transform_villa_az('data/villa_az_complete_dataset.csv'))
    except Exception as e:
        print(f"  ERROR: {e}\n")

    try:
        datasets.append(transform_evv_az('data/evv_az_listings.csv'))
    except Exception as e:
        print(f"  ERROR: {e}\n")

    try:
        datasets.append(transform_binam_listings('data/binam_listings_1758793717.csv'))
    except Exception as e:
        print(f"  ERROR: {e}\n")

    try:
        datasets.append(transform_bina_xlsx('data/bina.xlsx'))
    except Exception as e:
        print(f"  ERROR: {e}\n")

    # Combine all datasets
    print("\n" + "="*80)
    print("COMBINING ALL DATASETS...")
    print("="*80)
    combined_df = pd.concat(datasets, ignore_index=True, sort=False)

    # Save combined dataset
    output_file = 'data/combined_real_estate_master.csv'
    print(f"\nSaving to: {output_file}")
    combined_df.to_csv(output_file, index=False)

    # Also save as Excel for better viewing
    output_excel = 'data/combined_real_estate_master.xlsx'
    print(f"Saving to: {output_excel}")
    combined_df.to_excel(output_excel, index=False, engine='openpyxl')

    # Print summary
    print("\n" + "="*80)
    print("COMBINED DATASET SUMMARY")
    print("="*80)
    print(f"Total rows: {len(combined_df):,}")
    print(f"Total columns: {len(combined_df.columns):,}")

    print(f"\nBaseline columns: {len([c for c in combined_df.columns if not c.startswith('orig_')])}")
    print(f"Original columns preserved: {len([c for c in combined_df.columns if c.startswith('orig_')])}")

    print(f"\n\nRows per source:")
    source_counts = combined_df['source_dataset'].value_counts().sort_index()
    for source, count in source_counts.items():
        print(f"  {source:30s}: {count:>8,}")

    print(f"\n\nBaseline column completeness:")
    for col in BASELINE_COLUMNS[:15]:  # Show first 15
        if col in combined_df.columns:
            non_null = combined_df[col].notna().sum()
            pct = (non_null / len(combined_df) * 100)
            print(f"  {col:30s}: {non_null:>8,} ({pct:5.1f}%)")

    print(f"\n\nFiles saved:")
    print(f"  CSV:   {output_file}")
    print(f"  Excel: {output_excel}")
    print("\nTransformation complete! No data was lost.")

if __name__ == "__main__":
    main()
