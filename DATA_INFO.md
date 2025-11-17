# Dataset Information

## Combined Dataset

**File:** `combined_real_estate_bina_format.csv` (341 MB)
**Note:** This file is excluded from git due to size. Download separately if needed.

### Dataset Statistics

- **Total Records:** 335,696 properties
- **Columns:** 31
- **Format:** CSV (Bina.az standard schema)
- **Size:** 341.86 MB

### Column Schema

```
record_id, id, area_value, area_units, leased, floor, floors, rooms,
city_id, city_name, location_id, location_name, location_full_name,
price_value, price_currency, company_id, company_name, company_target_type,
has_mortgage, has_bill_of_sale, has_repair, paid_daily, is_business,
vipped, featured, updated_at, path, photos_count, photos, url, scraped_at
```

### Source Datasets (16 total)

1. **bina_sale_20251117_213934.csv** - 72,446 records
2. **ipotekaAz.xlsx** - 13,681 records
3. **ipotekaAz.csv** - 13,681 records
4. **binalar_listings.csv** - 31,151 records
5. **yeniemlak.xlsx** - 19,878 records
6. **yeniemlakAz.csv** - 837 records
7. **myhome_listings_20250929_003143.csv** - 7,062 records
8. **unvan.xlsx** - 13,098 records
9. **mulk_data_20250929_143644.csv** - 3,820 records
10. **emlakAz.xlsx** - 9,348 records
11. **ofis_listings.csv** - 2,800 records
12. **real_estate_data_25_feb_2025.csv** - 88,803 records
13. **villa_az_complete_dataset.csv** - 1,564 records
14. **evv_az_listings.csv** - 16,545 records
15. **binam_listings_1758793717.csv** - 14,130 records
16. **bina.xlsx** - 26,852 records

### Data Processing

All datasets were:
1. Transformed to unified Bina.az schema (30 columns)
2. Cleaned for outliers (top/bottom 1%)
3. Standardized with proper data types
4. Deduplicated where necessary

### How to Regenerate

Run the transformation script:
```bash
python3 transform_to_bina_format.py
```

This will create the combined dataset from source files.

### Charts & Analysis

All analysis visualizations are available in the `charts/` directory (20 PNG files).
See `README.md` for complete market analysis with embedded charts.

---

**Note:** Original source data files are also excluded from git to keep repository size small.
They can be scraped again using the appropriate scripts or obtained from the original platforms.
