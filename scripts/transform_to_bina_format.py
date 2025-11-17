#!/usr/bin/env python3
"""
Real Estate Dataset Transformation - All to Bina.az Format
Transforms all datasets to match bina_sale_20251117_213934.csv schema (30 columns)
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
import re
warnings.filterwarnings('ignore')

# Exact schema from bina_sale_20251117_213934.csv (30 columns)
BINA_SCHEMA = [
    'id', 'area_value', 'area_units', 'leased', 'floor', 'floors', 'rooms',
    'city_id', 'city_name', 'location_id', 'location_name', 'location_full_name',
    'price_value', 'price_currency', 'company_id', 'company_name', 'company_target_type',
    'has_mortgage', 'has_bill_of_sale', 'has_repair', 'paid_daily', 'is_business',
    'vipped', 'featured', 'updated_at', 'path', 'photos_count', 'photos', 'url', 'scraped_at'
]

def create_empty_row():
    """Create a dict with all schema columns initialized to None"""
    return {col: None for col in BINA_SCHEMA}

def safe_numeric(value, default=None):
    """Safely convert value to numeric"""
    if pd.isna(value):
        return default
    try:
        if isinstance(value, str):
            value = value.replace(',', '').replace(' ', '').replace('m²', '').replace('AZN', '').replace('₼', '').strip()
        return pd.to_numeric(value, errors='coerce')
    except:
        return default

def safe_int(value, default=None):
    """Safely convert to integer"""
    num = safe_numeric(value, default)
    if num is not None and not pd.isna(num):
        return int(num)
    return default

def safe_float(value, default=None):
    """Safely convert to float"""
    num = safe_numeric(value, default)
    if num is not None and not pd.isna(num):
        return float(num)
    return default

def safe_bool(value, default=False):
    """Safely convert to boolean"""
    if pd.isna(value):
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        value_lower = value.lower().strip()
        if value_lower in ['yes', 'true', '1', 'var', 'bəli']:
            return True
        if value_lower in ['no', 'false', '0', 'yox']:
            return False
    return default

def parse_floor(floor_str):
    """Parse floor string like '5/9' to get current floor"""
    if pd.isna(floor_str):
        return None
    s = str(floor_str).strip()
    if '/' in s:
        parts = s.split('/')
        return safe_float(parts[0])
    return safe_float(s)

def parse_total_floors(floor_str):
    """Parse floor string like '5/9' to get total floors"""
    if pd.isna(floor_str):
        return None
    s = str(floor_str).strip()
    if '/' in s:
        parts = s.split('/')
        if len(parts) > 1:
            return safe_float(parts[1])
    return None

def extract_number(s):
    """Extract first number from string"""
    if pd.isna(s):
        return None
    s = str(s)
    numbers = re.findall(r'\d+\.?\d*', s)
    if numbers:
        return safe_float(numbers[0])
    return None

def transform_row(row_data):
    """Transform a row to bina schema"""
    return pd.Series(row_data, index=BINA_SCHEMA)

# =============================================================================
# TRANSFORMATION FUNCTIONS FOR EACH DATASET
# =============================================================================

def transform_bina_sale(file_path):
    """Baseline: bina_sale_20251117_213934.csv"""
    print(f"Processing: {file_path}")
    df = pd.read_csv(file_path)

    # Already in correct format, just ensure column order
    result = df[BINA_SCHEMA].copy()

    print(f"  Rows: {len(result):,}")
    return result

def transform_ipoteka_xlsx(file_path):
    """Transform ipotekaAz.xlsx"""
    print(f"Processing: {file_path}")
    df = pd.read_excel(file_path)

    rows = []
    for _, row in df.iterrows():
        new_row = create_empty_row()
        new_row['id'] = safe_int(row.get('announcement_id'))
        new_row['area_value'] = safe_float(extract_number(row.get('area')))
        new_row['area_units'] = 'm²'
        new_row['leased'] = False
        new_row['floor'] = parse_floor(row.get('flat'))
        new_row['floors'] = safe_float(row.get('baxis_sayi'))
        new_row['rooms'] = safe_float(row.get('room_count'))
        new_row['city_name'] = str(row.get('area')) if pd.notna(row.get('area')) else None
        new_row['price_value'] = 0
        new_row['price_currency'] = 'AZN'
        new_row['has_mortgage'] = False
        new_row['has_bill_of_sale'] = safe_bool(pd.notna(row.get('document_type')))
        new_row['has_repair'] = safe_bool(pd.notna(row.get('repair_type')))
        new_row['updated_at'] = str(row.get('update_date')) if pd.notna(row.get('update_date')) else None
        new_row['url'] = f"https://ipoteka.az/elan/{row.get('announcement_id')}" if pd.notna(row.get('announcement_id')) else None
        new_row['scraped_at'] = datetime.now().isoformat()
        rows.append(new_row)

    result = pd.DataFrame(rows, columns=BINA_SCHEMA)
    print(f"  Rows: {len(result):,}")
    return result

def transform_ipoteka_csv(file_path):
    """Transform ipotekaAz.csv"""
    print(f"Processing: {file_path}")
    df = pd.read_csv(file_path)

    rows = []
    for _, row in df.iterrows():
        new_row = create_empty_row()
        new_row['id'] = safe_int(row.get('announcement_id'))
        new_row['area_value'] = safe_float(extract_number(row.get('area')))
        new_row['area_units'] = 'm²'
        new_row['leased'] = False
        new_row['floor'] = parse_floor(row.get('flat'))
        new_row['floors'] = safe_float(row.get('baxis_sayi'))
        new_row['rooms'] = safe_float(row.get('room_count'))
        new_row['city_name'] = str(row.get('area')) if pd.notna(row.get('area')) else None
        new_row['price_value'] = 0
        new_row['price_currency'] = 'AZN'
        new_row['has_mortgage'] = False
        new_row['has_bill_of_sale'] = safe_bool(pd.notna(row.get('document_type')))
        new_row['has_repair'] = safe_bool(pd.notna(row.get('repair_type')))
        new_row['updated_at'] = str(row.get('update_date')) if pd.notna(row.get('update_date')) else None
        new_row['url'] = f"https://ipoteka.az/elan/{row.get('announcement_id')}" if pd.notna(row.get('announcement_id')) else None
        new_row['scraped_at'] = datetime.now().isoformat()
        rows.append(new_row)

    result = pd.DataFrame(rows, columns=BINA_SCHEMA)
    print(f"  Rows: {len(result):,}")
    return result

def transform_binalar_listings(file_path):
    """Transform binalar_listings.csv"""
    print(f"Processing: {file_path}")
    df = pd.read_csv(file_path)

    rows = []
    for _, row in df.iterrows():
        new_row = create_empty_row()
        new_row['id'] = safe_int(row.get('id'))
        new_row['area_value'] = safe_float(row.get('area'))
        new_row['area_units'] = 'm²'
        new_row['leased'] = False
        new_row['floor'] = parse_floor(row.get('floor'))
        new_row['floors'] = parse_total_floors(row.get('floor'))
        new_row['rooms'] = safe_float(row.get('rooms'))
        new_row['location_name'] = str(row.get('address')) if pd.notna(row.get('address')) else None
        new_row['price_value'] = safe_int(row.get('price_raw'), 0)
        new_row['price_currency'] = 'AZN'
        new_row['updated_at'] = str(row.get('date')) if pd.notna(row.get('date')) else None
        new_row['url'] = str(row.get('url')) if pd.notna(row.get('url')) else None
        new_row['scraped_at'] = datetime.now().isoformat()
        rows.append(new_row)

    result = pd.DataFrame(rows, columns=BINA_SCHEMA)
    print(f"  Rows: {len(result):,}")
    return result

def transform_yeniemlak_xlsx(file_path):
    """Transform yeniemlak.xlsx"""
    print(f"Processing: {file_path}")
    df = pd.read_excel(file_path)

    rows = []
    for idx, row in df.iterrows():
        new_row = create_empty_row()
        new_row['id'] = idx + 1
        link = str(row.get('link', ''))
        new_row['url'] = f'https://{link}' if link and not link.startswith('http') else link
        new_row['scraped_at'] = datetime.now().isoformat()
        new_row['price_currency'] = 'AZN'
        new_row['area_units'] = 'm²'
        rows.append(new_row)

    result = pd.DataFrame(rows, columns=BINA_SCHEMA)
    print(f"  Rows: {len(result):,}")
    return result

def transform_yeniemlak_csv(file_path):
    """Transform yeniemlakAz.csv"""
    print(f"Processing: {file_path}")
    df = pd.read_csv(file_path)

    rows = []
    for _, row in df.iterrows():
        new_row = create_empty_row()
        new_row['id'] = safe_int(row.get('id'))
        new_row['area_value'] = safe_float(row.get('area'))
        new_row['area_units'] = 'm²'
        new_row['leased'] = False
        new_row['floor'] = safe_float(row.get('flat'))
        new_row['rooms'] = safe_float(row.get('room_count'))
        new_row['location_name'] = str(row.get('address')) if pd.notna(row.get('address')) else None
        new_row['location_full_name'] = str(row.get('address_2')) if pd.notna(row.get('address_2')) else None
        new_row['price_value'] = safe_int(row.get('price'), 0)
        new_row['price_currency'] = 'AZN'
        new_row['has_bill_of_sale'] = safe_bool(pd.notna(row.get('doc_type')))
        new_row['updated_at'] = str(row.get('date')) if pd.notna(row.get('date')) else None
        href = row.get('href')
        new_row['url'] = f'https://{href}' if pd.notna(href) and not str(href).startswith('http') else str(href) if pd.notna(href) else None
        new_row['scraped_at'] = datetime.now().isoformat()
        rows.append(new_row)

    result = pd.DataFrame(rows, columns=BINA_SCHEMA)
    print(f"  Rows: {len(result):,}")
    return result

def transform_myhome_listings(file_path):
    """Transform myhome_listings_20250929_003143.csv"""
    print(f"Processing: {file_path}")
    df = pd.read_csv(file_path)

    rows = []
    for _, row in df.iterrows():
        new_row = create_empty_row()
        new_row['id'] = safe_int(row.get('id'))
        new_row['area_value'] = safe_float(row.get('area'))
        new_row['area_units'] = 'm²'
        new_row['leased'] = False
        new_row['floor'] = safe_float(row.get('floor'))
        new_row['floors'] = safe_float(row.get('floor_count'))
        new_row['rooms'] = safe_float(row.get('room_count'))
        new_row['city_name'] = str(row.get('city')) if pd.notna(row.get('city')) else None
        new_row['location_name'] = str(row.get('region')) if pd.notna(row.get('region')) else None
        new_row['location_full_name'] = str(row.get('address')) if pd.notna(row.get('address')) else None
        new_row['price_value'] = safe_int(extract_number(row.get('price')), 0)
        new_row['price_currency'] = 'AZN'
        new_row['has_mortgage'] = safe_bool(row.get('credit_possible'))
        new_row['has_repair'] = safe_bool(row.get('is_repaired'))
        new_row['vipped'] = safe_bool(row.get('is_vip'))
        new_row['featured'] = safe_bool(row.get('is_premium'))
        new_row['updated_at'] = str(row.get('formatted_date')) if pd.notna(row.get('formatted_date')) else None
        new_row['photos_count'] = 0
        new_row['scraped_at'] = datetime.now().isoformat()
        rows.append(new_row)

    result = pd.DataFrame(rows, columns=BINA_SCHEMA)
    print(f"  Rows: {len(result):,}")
    return result

def transform_unvan_xlsx(file_path):
    """Transform unvan.xlsx"""
    print(f"Processing: {file_path}")
    df = pd.read_excel(file_path)

    rows = []
    for _, row in df.iterrows():
        new_row = create_empty_row()
        new_row['id'] = safe_int(row.get('id'))
        new_row['area_value'] = safe_float(extract_number(row.get('area')))
        new_row['area_units'] = 'm²'
        new_row['leased'] = False
        new_row['rooms'] = safe_float(extract_number(row.get('room_count')))
        new_row['location_name'] = str(row.get('address')) if pd.notna(row.get('address')) else None
        new_row['location_full_name'] = str(row.get('address_2')) if pd.notna(row.get('address_2')) else None
        new_row['price_value'] = safe_int(extract_number(row.get('price')), 0)
        new_row['price_currency'] = 'AZN'
        new_row['company_name'] = str(row.get('owner')) if pd.notna(row.get('owner')) else None
        new_row['updated_at'] = str(row.get('date')) if pd.notna(row.get('date')) else None
        new_row['url'] = str(row.get('link')) if pd.notna(row.get('link')) else None
        new_row['scraped_at'] = datetime.now().isoformat()
        rows.append(new_row)

    result = pd.DataFrame(rows, columns=BINA_SCHEMA)
    print(f"  Rows: {len(result):,}")
    return result

def transform_mulk_data(file_path):
    """Transform mulk_data_20250929_143644.csv"""
    print(f"Processing: {file_path}")
    df = pd.read_csv(file_path)

    rows = []
    for _, row in df.iterrows():
        new_row = create_empty_row()
        new_row['id'] = safe_int(row.get('listing_id'))
        new_row['area_value'] = safe_float(row.get('area_numeric'))
        new_row['area_units'] = 'm²'
        new_row['leased'] = False
        new_row['floor'] = safe_float(row.get('current_floor'))
        new_row['floors'] = safe_float(row.get('total_floors'))
        new_row['rooms'] = safe_float(row.get('rooms_numeric'))
        new_row['location_name'] = str(row.get('location_district')) if pd.notna(row.get('location_district')) else None
        new_row['location_full_name'] = str(row.get('full_address')) if pd.notna(row.get('full_address')) else None
        new_row['price_value'] = safe_int(row.get('price_numeric'), 0)
        new_row['price_currency'] = 'AZN'
        new_row['has_bill_of_sale'] = safe_bool(row.get('deed_available') == 'Yes')
        new_row['updated_at'] = str(row.get('listing_date')) if pd.notna(row.get('listing_date')) else None
        new_row['url'] = str(row.get('url')) if pd.notna(row.get('url')) else None
        new_row['photos_count'] = safe_int(row.get('image_count'), 0)
        new_row['scraped_at'] = str(row.get('scraped_at')) if pd.notna(row.get('scraped_at')) else datetime.now().isoformat()
        rows.append(new_row)

    result = pd.DataFrame(rows, columns=BINA_SCHEMA)
    print(f"  Rows: {len(result):,}")
    return result

def transform_emlak_xlsx(file_path):
    """Transform emlakAz.xlsx"""
    print(f"Processing: {file_path}")
    df = pd.read_excel(file_path)

    rows = []
    for _, row in df.iterrows():
        new_row = create_empty_row()
        new_row['id'] = safe_int(row.get('id'))
        new_row['area_value'] = safe_float(extract_number(row.get('area')))
        new_row['area_units'] = 'm²'
        new_row['leased'] = False
        new_row['floor'] = parse_floor(row.get('flat'))
        new_row['rooms'] = safe_float(extract_number(row.get('room_count')))
        new_row['price_value'] = safe_int(extract_number(row.get('price')), 0)
        new_row['price_currency'] = 'AZN'
        new_row['has_repair'] = safe_bool(pd.notna(row.get('repair_type')))
        new_row['has_bill_of_sale'] = safe_bool(pd.notna(row.get('document_type')))
        new_row['company_name'] = str(row.get('seller_name')) if pd.notna(row.get('seller_name')) else None
        new_row['updated_at'] = str(row.get('date')) if pd.notna(row.get('date')) else None
        href = row.get('href')
        new_row['url'] = f'https://emlak.az{href}' if pd.notna(href) else None
        new_row['scraped_at'] = datetime.now().isoformat()
        rows.append(new_row)

    result = pd.DataFrame(rows, columns=BINA_SCHEMA)
    print(f"  Rows: {len(result):,}")
    return result

def transform_ofis_listings(file_path):
    """Transform ofis_listings.csv"""
    print(f"Processing: {file_path}")
    df = pd.read_csv(file_path)

    rows = []
    for _, row in df.iterrows():
        new_row = create_empty_row()
        new_row['id'] = safe_int(row.get('listing_id'))
        new_row['area_value'] = safe_float(extract_number(row.get('Sahə')))
        new_row['area_units'] = 'm²'
        new_row['leased'] = False
        new_row['floor'] = safe_float(row.get('Mərtəbə'))
        new_row['floors'] = safe_float(row.get('Mərtəbə sayı'))
        new_row['rooms'] = safe_float(row.get('Otaq Sayı'))
        new_row['city_name'] = str(row.get('Şəhər')) if pd.notna(row.get('Şəhər')) else None
        new_row['location_name'] = str(row.get('Ünvan')) if pd.notna(row.get('Ünvan')) else None
        new_row['price_value'] = safe_int(extract_number(row.get('price')), 0)
        new_row['price_currency'] = 'AZN'
        new_row['is_business'] = True
        new_row['updated_at'] = str(row.get('date')) if pd.notna(row.get('date')) else None
        new_row['url'] = str(row.get('url')) if pd.notna(row.get('url')) else None
        new_row['scraped_at'] = datetime.now().isoformat()
        rows.append(new_row)

    result = pd.DataFrame(rows, columns=BINA_SCHEMA)
    print(f"  Rows: {len(result):,}")
    return result

def transform_real_estate_feb(file_path):
    """Transform real_estate_data_25_feb_2025.csv"""
    print(f"Processing: {file_path}")
    df = pd.read_csv(file_path)

    rows = []
    for _, row in df.iterrows():
        new_row = create_empty_row()
        new_row['id'] = safe_int(row.get('id'))
        new_row['area_value'] = safe_float(extract_number(row.get('area')))
        new_row['area_units'] = 'm²'
        new_row['leased'] = False
        new_row['floor'] = safe_float(row.get('floor'))
        new_row['floors'] = safe_float(row.get('total_floors'))
        new_row['rooms'] = safe_float(row.get('rooms'))
        new_row['city_name'] = str(row.get('district')) if pd.notna(row.get('district')) else None
        new_row['location_name'] = str(row.get('location')) if pd.notna(row.get('location')) else str(row.get('address')) if pd.notna(row.get('address')) else None
        new_row['location_full_name'] = str(row.get('address')) if pd.notna(row.get('address')) else None
        new_row['price_value'] = safe_int(row.get('price'), 0)
        new_row['price_currency'] = str(row.get('currency', 'AZN'))
        new_row['has_repair'] = safe_bool(row.get('has_repair'))
        new_row['updated_at'] = str(row.get('updated_at')) if pd.notna(row.get('updated_at')) else str(row.get('listing_date')) if pd.notna(row.get('listing_date')) else None
        new_row['url'] = str(row.get('source_url')) if pd.notna(row.get('source_url')) else None
        new_row['photos'] = str(row.get('photos')) if pd.notna(row.get('photos')) else None
        new_row['scraped_at'] = str(row.get('created_at')) if pd.notna(row.get('created_at')) else datetime.now().isoformat()
        rows.append(new_row)

    result = pd.DataFrame(rows, columns=BINA_SCHEMA)
    print(f"  Rows: {len(result):,}")
    return result

def transform_villa_az(file_path):
    """Transform villa_az_complete_dataset.csv"""
    print(f"Processing: {file_path}")
    df = pd.read_csv(file_path)

    rows = []
    for _, row in df.iterrows():
        new_row = create_empty_row()
        new_row['id'] = safe_int(row.get('listing_id'))
        new_row['area_value'] = safe_float(row.get('Sahə, m²'))
        new_row['area_units'] = 'm²'
        new_row['leased'] = False
        new_row['floor'] = parse_floor(row.get('Mərtəbə'))
        new_row['rooms'] = safe_float(row.get('Otaq sayı'))
        new_row['city_name'] = str(row.get('Şəhər')) if pd.notna(row.get('Şəhər')) else None
        new_row['location_name'] = str(row.get('address')) if pd.notna(row.get('address')) else None
        new_row['price_value'] = safe_int(extract_number(row.get('price')), 0)
        new_row['price_currency'] = 'AZN'
        new_row['has_bill_of_sale'] = safe_bool(pd.notna(row.get('Əmlak sənədi')))
        new_row['updated_at'] = str(row.get('date')) if pd.notna(row.get('date')) else None
        new_row['url'] = str(row.get('url')) if pd.notna(row.get('url')) else None
        new_row['scraped_at'] = datetime.now().isoformat()
        rows.append(new_row)

    result = pd.DataFrame(rows, columns=BINA_SCHEMA)
    print(f"  Rows: {len(result):,}")
    return result

def transform_evv_az(file_path):
    """Transform evv_az_listings.csv"""
    print(f"Processing: {file_path}")
    df = pd.read_csv(file_path)

    rows = []
    for _, row in df.iterrows():
        new_row = create_empty_row()
        new_row['id'] = safe_int(row.get('listing_id'))
        new_row['area_value'] = safe_float(extract_number(row.get('area')))
        new_row['area_units'] = 'm²'
        new_row['leased'] = False
        new_row['floor'] = parse_floor(row.get('floor'))
        new_row['rooms'] = safe_float(extract_number(row.get('rooms')))
        new_row['city_name'] = str(row.get('city')) if pd.notna(row.get('city')) else None
        new_row['location_name'] = str(row.get('location')) if pd.notna(row.get('location')) else None
        new_row['price_value'] = safe_int(extract_number(row.get('price')), 0)
        new_row['price_currency'] = 'AZN'
        new_row['has_bill_of_sale'] = safe_bool(pd.notna(row.get('document')))
        new_row['has_mortgage'] = safe_bool(pd.notna(row.get('mortgage')))
        new_row['company_name'] = str(row.get('seller_name')) if pd.notna(row.get('seller_name')) else None
        new_row['updated_at'] = str(row.get('update_date')) if pd.notna(row.get('update_date')) else str(row.get('post_date')) if pd.notna(row.get('post_date')) else None
        new_row['url'] = str(row.get('url')) if pd.notna(row.get('url')) else None
        new_row['scraped_at'] = datetime.now().isoformat()
        rows.append(new_row)

    result = pd.DataFrame(rows, columns=BINA_SCHEMA)
    print(f"  Rows: {len(result):,}")
    return result

def transform_binam_listings(file_path):
    """Transform binam_listings_1758793717.csv"""
    print(f"Processing: {file_path}")
    df = pd.read_csv(file_path)

    rows = []
    for _, row in df.iterrows():
        new_row = create_empty_row()
        new_row['id'] = safe_int(row.get('listing_code'))
        new_row['area_value'] = safe_float(extract_number(row.get('area')))
        new_row['area_units'] = 'm²'
        new_row['leased'] = False
        new_row['floor'] = parse_floor(row.get('floor'))
        new_row['rooms'] = safe_float(extract_number(row.get('rooms')))
        new_row['city_name'] = str(row.get('country_city')) if pd.notna(row.get('country_city')) else None
        new_row['location_name'] = str(row.get('district')) if pd.notna(row.get('district')) else None
        new_row['location_full_name'] = str(row.get('address')) if pd.notna(row.get('address')) else None
        new_row['price_value'] = safe_int(extract_number(row.get('price')), 0)
        new_row['price_currency'] = 'AZN'
        new_row['company_name'] = str(row.get('company_name')) if pd.notna(row.get('company_name')) else None
        new_row['updated_at'] = str(row.get('listing_date')) if pd.notna(row.get('listing_date')) else None
        new_row['url'] = str(row.get('url')) if pd.notna(row.get('url')) else None
        new_row['scraped_at'] = datetime.now().isoformat()
        rows.append(new_row)

    result = pd.DataFrame(rows, columns=BINA_SCHEMA)
    print(f"  Rows: {len(result):,}")
    return result

def transform_bina_xlsx(file_path):
    """Transform bina.xlsx"""
    print(f"Processing: {file_path}")
    df = pd.read_excel(file_path)

    rows = []
    for _, row in df.iterrows():
        new_row = create_empty_row()
        new_row['id'] = safe_int(row.get('item_id'))
        new_row['area_value'] = safe_float(extract_number(row.get('area')))
        new_row['area_units'] = 'm²'
        new_row['leased'] = False
        new_row['floor'] = parse_floor(row.get('floor'))
        new_row['rooms'] = safe_float(extract_number(row.get('room count')))
        new_row['price_value'] = safe_int(row.get('price'), 0)
        new_row['price_currency'] = str(row.get('currency', 'AZN'))
        new_row['has_mortgage'] = safe_bool(pd.notna(row.get('mortgage')))
        new_row['company_name'] = str(row.get('owner name')) if pd.notna(row.get('owner name')) else None
        new_row['url'] = str(row.get('url')) if pd.notna(row.get('url')) else None
        new_row['scraped_at'] = datetime.now().isoformat()
        rows.append(new_row)

    result = pd.DataFrame(rows, columns=BINA_SCHEMA)
    print(f"  Rows: {len(result):,}")
    return result

# =============================================================================
# MAIN FUNCTION
# =============================================================================

def main():
    """Main function to transform and combine all datasets"""
    print("="*80)
    print("REAL ESTATE DATASET TRANSFORMATION")
    print("Target Format: bina_sale_20251117_213934.csv (30 columns)")
    print("="*80)
    print()

    datasets = []
    errors = []

    # Process each dataset
    file_transforms = [
        ('data/bina_sale_20251117_213934.csv', transform_bina_sale),
        ('data/ipotekaAz.xlsx', transform_ipoteka_xlsx),
        ('data/ipotekaAz.csv', transform_ipoteka_csv),
        ('data/binalar_listings.csv', transform_binalar_listings),
        ('data/yeniemlak.xlsx', transform_yeniemlak_xlsx),
        ('data/yeniemlakAz.csv', transform_yeniemlak_csv),
        ('data/myhome_listings_20250929_003143.csv', transform_myhome_listings),
        ('data/unvan.xlsx', transform_unvan_xlsx),
        ('data/mulk_data_20250929_143644.csv', transform_mulk_data),
        ('data/emlakAz.xlsx', transform_emlak_xlsx),
        ('data/ofis_listings.csv', transform_ofis_listings),
        ('data/real_estate_data_25_feb_2025.csv', transform_real_estate_feb),
        ('data/villa_az_complete_dataset.csv', transform_villa_az),
        ('data/evv_az_listings.csv', transform_evv_az),
        ('data/binam_listings_1758793717.csv', transform_binam_listings),
        ('data/bina.xlsx', transform_bina_xlsx),
    ]

    for file_path, transform_func in file_transforms:
        try:
            df = transform_func(file_path)
            datasets.append(df)
        except Exception as e:
            errors.append(f"{file_path}: {str(e)}")
            print(f"  ERROR: {e}\n")

    # Combine all datasets
    print("\n" + "="*80)
    print("COMBINING DATASETS")
    print("="*80)
    combined_df = pd.concat(datasets, ignore_index=True)

    # Add source identifier based on scraped_at or create sequence
    # For better tracking, add a record_id
    combined_df.insert(0, 'record_id', range(1, len(combined_df) + 1))

    # Save results
    output_csv = 'data/combined_real_estate_bina_format.csv'
    output_excel = 'data/combined_real_estate_bina_format.xlsx'

    print(f"\nSaving CSV: {output_csv}")
    combined_df.to_csv(output_csv, index=False)

    print(f"Saving Excel: {output_excel}")
    combined_df.to_excel(output_excel, index=False, engine='openpyxl')

    # Print summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total records: {len(combined_df):,}")
    print(f"Total columns: {len(combined_df.columns)}")
    print(f"Datasets processed: {len(datasets)}")
    if errors:
        print(f"Errors: {len(errors)}")
        for error in errors:
            print(f"  - {error}")

    print(f"\nColumn completeness (non-null values):")
    for col in BINA_SCHEMA[:20]:  # Show first 20
        non_null = combined_df[col].notna().sum()
        pct = (non_null / len(combined_df) * 100) if len(combined_df) > 0 else 0
        print(f"  {col:30s}: {non_null:>8,} ({pct:5.1f}%)")

    print(f"\nOutput files:")
    print(f"  {output_csv}")
    print(f"  {output_excel}")
    print("\nDone!")

if __name__ == "__main__":
    main()
