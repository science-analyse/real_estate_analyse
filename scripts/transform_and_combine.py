import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Define the baseline schema (from bina_sale_20251117_213934.csv)
BASELINE_COLUMNS = [
    'id', 'area_value', 'area_units', 'leased', 'floor', 'floors', 'rooms',
    'city_id', 'city_name', 'location_id', 'location_name', 'location_full_name',
    'price_value', 'price_currency', 'company_id', 'company_name', 'company_target_type',
    'has_mortgage', 'has_bill_of_sale', 'has_repair', 'paid_daily', 'is_business',
    'vipped', 'featured', 'updated_at', 'path', 'photos_count', 'photos', 'url', 'scraped_at'
]

def create_empty_baseline():
    """Create an empty DataFrame with baseline schema"""
    df = pd.DataFrame(columns=BASELINE_COLUMNS)
    return df

def standardize_phone(phone):
    """Standardize phone number format"""
    if pd.isna(phone):
        return None
    phone_str = str(phone).replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
    return phone_str

def transform_bina_sale(file_path):
    """Transform bina_sale dataset (already in baseline format)"""
    print(f"Loading {file_path}...")
    df = pd.read_csv(file_path)
    df['source_dataset'] = 'bina_sale'
    return df

def transform_ipoteka_xlsx(file_path):
    """Transform ipotekaAz.xlsx to baseline format"""
    print(f"Loading {file_path}...")
    df = pd.read_excel(file_path)

    result = create_empty_baseline()
    result['id'] = df['announcement_id']
    result['area_value'] = df['area'].apply(lambda x: pd.to_numeric(str(x).replace(' m²', '').replace(',', ''), errors='coerce') if pd.notna(x) else np.nan)
    result['area_units'] = 'm²'
    result['leased'] = False
    result['floor'] = df['flat'].apply(lambda x: pd.to_numeric(str(x).split('/')[0] if '/' in str(x) else x, errors='coerce'))
    result['floors'] = df['baxis_sayi']
    result['rooms'] = df['room_count']
    result['city_name'] = df['area']
    result['price_value'] = 0
    result['price_currency'] = 'AZN'
    result['has_mortgage'] = False
    result['has_bill_of_sale'] = df['document_type'].notna()
    result['has_repair'] = df['repair_type'].notna()
    result['updated_at'] = df['update_date']
    result['url'] = 'https://ipoteka.az/elan/' + df['announcement_id'].astype(str)
    result['scraped_at'] = datetime.now().isoformat()
    result['source_dataset'] = 'ipotekaAz'
    result['contact_phone'] = df['phone_cleaned']

    return result

def transform_ipoteka_csv(file_path):
    """Transform ipotekaAz.csv to baseline format"""
    print(f"Loading {file_path}...")
    try:
        df = pd.read_csv(file_path)
        # Similar transformation as xlsx version
        result = create_empty_baseline()

        # Map common fields if they exist
        if 'announcement_id' in df.columns:
            result['id'] = df['announcement_id']

        result['source_dataset'] = 'ipotekaAz_csv'
        result['scraped_at'] = datetime.now().isoformat()
        return result
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return create_empty_baseline()

def transform_binalar_listings(file_path):
    """Transform binalar_listings.csv to baseline format"""
    print(f"Loading {file_path}...")
    df = pd.read_csv(file_path)

    result = create_empty_baseline()
    result['id'] = df['id']
    result['area_value'] = df['area']
    result['area_units'] = 'm²'
    result['rooms'] = df['rooms']
    result['floor'] = df['floor'].apply(lambda x: pd.to_numeric(str(x).split('/')[0] if '/' in str(x) else x, errors='coerce'))
    result['price_value'] = df['price_raw'].fillna(0).astype(int)
    result['price_currency'] = 'AZN'
    result['location_name'] = df['address']
    result['url'] = df['url']
    result['scraped_at'] = datetime.now().isoformat()
    result['source_dataset'] = 'binalar_listings'
    result['contact_phone'] = df['phone']

    return result

def transform_yeniemlak_xlsx(file_path):
    """Transform yeniemlak.xlsx to baseline format"""
    print(f"Loading {file_path}...")
    df = pd.read_excel(file_path)

    result = create_empty_baseline()
    # Extract ID from link if possible
    result['id'] = range(len(df))
    result['url'] = 'https://' + df['link'].astype(str)
    result['scraped_at'] = datetime.now().isoformat()
    result['source_dataset'] = 'yeniemlak'
    result['contact_phone'] = df['phone_number']

    return result

def transform_yeniemlak_csv(file_path):
    """Transform yeniemlakAz.csv to baseline format"""
    print(f"Loading {file_path}...")
    try:
        df = pd.read_csv(file_path)
        result = create_empty_baseline()
        result['id'] = range(len(df))
        result['source_dataset'] = 'yeniemlakAz_csv'
        result['scraped_at'] = datetime.now().isoformat()
        return result
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return create_empty_baseline()

def transform_myhome_listings(file_path):
    """Transform myhome_listings to baseline format"""
    print(f"Loading {file_path}...")
    df = pd.read_csv(file_path)

    result = create_empty_baseline()
    result['id'] = df['id']
    result['area_value'] = df['area']
    result['area_units'] = 'm²'
    result['rooms'] = df['room_count']
    result['floor'] = df['floor']
    result['floors'] = df['floor_count']
    result['city_id'] = df['city']
    result['city_name'] = df['city']
    result['location_name'] = df['region']
    result['location_full_name'] = df['address']
    result['price_value'] = df['price'].apply(lambda x: pd.to_numeric(str(x).replace('AZN', '').replace(',', '').strip(), errors='coerce')).fillna(0).astype(int)
    result['price_currency'] = 'AZN'
    result['has_repair'] = df['is_repaired'].fillna(0) > 0
    result['vipped'] = df['is_vip'] == 1
    result['featured'] = df['is_premium'] == 1
    result['has_mortgage'] = df['credit_possible'] == 1
    result['updated_at'] = df['formatted_date']
    result['scraped_at'] = datetime.now().isoformat()
    result['source_dataset'] = 'myhome'
    result['contact_phone'] = df['phone_number']
    result['latitude'] = df['lat']
    result['longitude'] = df['lng']

    return result

def transform_unvan_xlsx(file_path):
    """Transform unvan.xlsx to baseline format"""
    print(f"Loading {file_path}...")
    df = pd.read_excel(file_path)

    result = create_empty_baseline()
    result['id'] = df['id']
    result['area_value'] = df['area'].apply(lambda x: pd.to_numeric(str(x).replace(' m²', '').replace('m²', '').strip(), errors='coerce'))
    result['area_units'] = 'm²'
    result['rooms'] = df['room_count'].apply(lambda x: pd.to_numeric(str(x).split()[0] if pd.notna(x) else np.nan, errors='coerce'))
    result['price_value'] = df['price'].apply(lambda x: pd.to_numeric(str(x).replace('AZN', '').replace(',', '').strip(), errors='coerce')).fillna(0).astype(int)
    result['price_currency'] = 'AZN'
    result['location_name'] = df['address']
    result['location_full_name'] = df['address_2']
    result['company_name'] = df['owner']
    result['updated_at'] = df['date']
    result['url'] = df['link']
    result['scraped_at'] = datetime.now().isoformat()
    result['source_dataset'] = 'unvan'
    result['contact_phone'] = df['phone']

    return result

def transform_mulk_data(file_path):
    """Transform mulk_data to baseline format"""
    print(f"Loading {file_path}...")
    df = pd.read_csv(file_path)

    result = create_empty_baseline()
    result['id'] = df['listing_id']
    result['area_value'] = df['area_numeric']
    result['area_units'] = 'm²'
    result['rooms'] = df['rooms_numeric']
    result['floor'] = df['current_floor']
    result['floors'] = df['total_floors']
    result['price_value'] = df['price_numeric']
    result['price_currency'] = 'AZN'
    result['location_name'] = df['location_district']
    result['location_full_name'] = df['full_address']
    result['has_bill_of_sale'] = df['deed_available'] == 'Yes'
    result['updated_at'] = df['listing_date']
    result['url'] = df['url']
    result['photos_count'] = df['image_count']
    result['scraped_at'] = df['scraped_at']
    result['source_dataset'] = 'mulk'
    result['contact_phone'] = df['contact_phone']

    return result

def transform_emlak_xlsx(file_path):
    """Transform emlakAz.xlsx to baseline format"""
    print(f"Loading {file_path}...")
    try:
        df = pd.read_excel(file_path)
        result = create_empty_baseline()
        result['id'] = range(len(df))
        result['source_dataset'] = 'emlakAz'
        result['scraped_at'] = datetime.now().isoformat()

        # Map fields if they exist
        if 'area' in df.columns:
            result['area_value'] = df['area']
        if 'price' in df.columns:
            result['price_value'] = df['price']

        return result
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return create_empty_baseline()

def transform_ofis_listings(file_path):
    """Transform ofis_listings.csv to baseline format"""
    print(f"Loading {file_path}...")
    try:
        df = pd.read_csv(file_path)
        result = create_empty_baseline()
        result['id'] = range(len(df))
        result['source_dataset'] = 'ofis_listings'
        result['scraped_at'] = datetime.now().isoformat()
        result['is_business'] = True

        # Map common fields
        if 'area' in df.columns:
            result['area_value'] = df['area']
        if 'price' in df.columns:
            result['price_value'] = df['price']
        if 'url' in df.columns:
            result['url'] = df['url']

        return result
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return create_empty_baseline()

def transform_real_estate_feb(file_path):
    """Transform real_estate_data_25_feb_2025.csv to baseline format"""
    print(f"Loading {file_path}...")
    try:
        df = pd.read_csv(file_path)
        result = create_empty_baseline()
        result['id'] = range(len(df))
        result['source_dataset'] = 'real_estate_feb_2025'
        result['scraped_at'] = '2025-02-25'

        # Map fields based on common column names
        for col in df.columns:
            if 'area' in col.lower():
                result['area_value'] = pd.to_numeric(df[col], errors='coerce')
            elif 'price' in col.lower():
                result['price_value'] = pd.to_numeric(df[col], errors='coerce')
            elif 'room' in col.lower():
                result['rooms'] = pd.to_numeric(df[col], errors='coerce')

        return result
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return create_empty_baseline()

def transform_villa_az(file_path):
    """Transform villa_az_complete_dataset.csv to baseline format"""
    print(f"Loading {file_path}...")
    try:
        df = pd.read_csv(file_path)
        result = create_empty_baseline()
        result['id'] = range(len(df))
        result['source_dataset'] = 'villa_az'
        result['scraped_at'] = datetime.now().isoformat()
        result['property_type'] = 'villa'

        # Map common fields
        for col in df.columns:
            if 'area' in col.lower():
                result['area_value'] = pd.to_numeric(df[col], errors='coerce')
            elif 'price' in col.lower():
                result['price_value'] = pd.to_numeric(df[col], errors='coerce')
            elif 'room' in col.lower():
                result['rooms'] = pd.to_numeric(df[col], errors='coerce')

        return result
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return create_empty_baseline()

def transform_evv_az(file_path):
    """Transform evv_az_listings.csv to baseline format"""
    print(f"Loading {file_path}...")
    try:
        df = pd.read_csv(file_path)
        result = create_empty_baseline()
        result['id'] = range(len(df))
        result['source_dataset'] = 'evv_az'
        result['scraped_at'] = datetime.now().isoformat()

        # Map common fields
        for col in df.columns:
            if 'area' in col.lower():
                result['area_value'] = pd.to_numeric(df[col], errors='coerce')
            elif 'price' in col.lower():
                result['price_value'] = pd.to_numeric(df[col], errors='coerce')
            elif 'room' in col.lower():
                result['rooms'] = pd.to_numeric(df[col], errors='coerce')
            elif 'url' in col.lower():
                result['url'] = df[col]

        return result
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return create_empty_baseline()

def transform_binam_listings(file_path):
    """Transform binam_listings to baseline format"""
    print(f"Loading {file_path}...")
    try:
        df = pd.read_csv(file_path)
        result = create_empty_baseline()
        result['id'] = range(len(df))
        result['source_dataset'] = 'binam_listings'
        result['scraped_at'] = datetime.now().isoformat()

        # Map common fields
        for col in df.columns:
            if 'area' in col.lower():
                result['area_value'] = pd.to_numeric(df[col], errors='coerce')
            elif 'price' in col.lower():
                result['price_value'] = pd.to_numeric(df[col], errors='coerce')
            elif 'room' in col.lower():
                result['rooms'] = pd.to_numeric(df[col], errors='coerce')

        return result
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return create_empty_baseline()

def transform_bina_xlsx(file_path):
    """Transform bina.xlsx to baseline format"""
    print(f"Loading {file_path}...")
    try:
        df = pd.read_excel(file_path)
        result = create_empty_baseline()
        result['id'] = range(len(df))
        result['source_dataset'] = 'bina_xlsx'
        result['scraped_at'] = datetime.now().isoformat()

        # Map common fields
        for col in df.columns:
            if 'area' in col.lower():
                result['area_value'] = pd.to_numeric(df[col], errors='coerce')
            elif 'price' in col.lower():
                result['price_value'] = pd.to_numeric(df[col], errors='coerce')
            elif 'room' in col.lower():
                result['rooms'] = pd.to_numeric(df[col], errors='coerce')

        return result
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return create_empty_baseline()

def main():
    """Main function to transform and combine all datasets"""
    print("Starting dataset transformation and combination...\n")

    datasets = []

    # Transform each dataset
    datasets.append(transform_bina_sale('data/bina_sale_20251117_213934.csv'))
    datasets.append(transform_ipoteka_xlsx('data/ipotekaAz.xlsx'))
    datasets.append(transform_ipoteka_csv('data/ipotekaAz.csv'))
    datasets.append(transform_binalar_listings('data/binalar_listings.csv'))
    datasets.append(transform_yeniemlak_xlsx('data/yeniemlak.xlsx'))
    datasets.append(transform_yeniemlak_csv('data/yeniemlakAz.csv'))
    datasets.append(transform_myhome_listings('data/myhome_listings_20250929_003143.csv'))
    datasets.append(transform_unvan_xlsx('data/unvan.xlsx'))
    datasets.append(transform_mulk_data('data/mulk_data_20250929_143644.csv'))
    datasets.append(transform_emlak_xlsx('data/emlakAz.xlsx'))
    datasets.append(transform_ofis_listings('data/ofis_listings.csv'))
    datasets.append(transform_real_estate_feb('data/real_estate_data_25_feb_2025.csv'))
    datasets.append(transform_villa_az('data/villa_az_complete_dataset.csv'))
    datasets.append(transform_evv_az('data/evv_az_listings.csv'))
    datasets.append(transform_binam_listings('data/binam_listings_1758793717.csv'))
    datasets.append(transform_bina_xlsx('data/bina.xlsx'))

    # Combine all datasets
    print("\nCombining all datasets...")
    combined_df = pd.concat(datasets, ignore_index=True)

    # Save combined dataset
    output_file = 'data/combined_real_estate_dataset.csv'
    print(f"\nSaving combined dataset to {output_file}...")
    combined_df.to_csv(output_file, index=False)

    # Print summary statistics
    print("\n" + "="*80)
    print("COMBINED DATASET SUMMARY")
    print("="*80)
    print(f"Total rows: {len(combined_df):,}")
    print(f"Total columns: {len(combined_df.columns)}")
    print(f"\nRows per source:")
    print(combined_df['source_dataset'].value_counts().to_string())
    print(f"\nMissing values by column:")
    missing = combined_df.isnull().sum()
    missing_pct = (missing / len(combined_df) * 100).round(2)
    missing_df = pd.DataFrame({'Missing': missing, 'Percentage': missing_pct})
    print(missing_df[missing_df['Missing'] > 0].to_string())

    print(f"\nDataset saved successfully to: {output_file}")

if __name__ == "__main__":
    main()
