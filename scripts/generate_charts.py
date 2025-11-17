#!/usr/bin/env python3
"""
Real Estate Data Analysis - Chart Generation
Generates comprehensive, attractive visualizations of real estate data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style for attractive charts
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Configure matplotlib for better looking charts
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9

# Load data
print("Loading combined dataset...")
df = pd.read_csv('data/combined_real_estate_bina_format.csv')
print(f"Loaded {len(df):,} records\n")

# Data cleaning for analysis
df_clean = df.copy()

# Clean price data (remove outliers and zero prices)
df_clean = df_clean[df_clean['price_value'] > 0]
df_clean = df_clean[df_clean['price_value'] < df_clean['price_value'].quantile(0.99)]

# Clean area data
df_clean = df_clean[df_clean['area_value'] > 0]
df_clean = df_clean[df_clean['area_value'] < df_clean['area_value'].quantile(0.99)]

# Clean floor data
df_clean = df_clean[df_clean['floor'] > 0]
df_clean = df_clean[df_clean['floor'] < 50]

# Clean rooms data
df_clean = df_clean[df_clean['rooms'] > 0]
df_clean = df_clean[df_clean['rooms'] <= 10]

print(f"After cleaning: {len(df_clean):,} records\n")

# =============================================================================
# CHART 1: Price Distribution
# =============================================================================
print("Generating Chart 1: Price Distribution...")
fig, ax = plt.subplots(figsize=(14, 8))

prices = df_clean['price_value'].dropna()
ax.hist(prices, bins=50, color='#3498db', edgecolor='black', alpha=0.7)

ax.set_xlabel('Price (AZN)', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of Properties', fontsize=12, fontweight='bold')
ax.set_title('Real Estate Price Distribution in Azerbaijan', fontsize=16, fontweight='bold', pad=20)

# Add statistics
mean_price = prices.mean()
median_price = prices.median()
ax.axvline(mean_price, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_price:,.0f} AZN')
ax.axvline(median_price, color='green', linestyle='--', linewidth=2, label=f'Median: {median_price:,.0f} AZN')

# Add text box with statistics
stats_text = f'Total Properties: {len(prices):,}\nMean: {mean_price:,.0f} AZN\nMedian: {median_price:,.0f} AZN\nStd Dev: {prices.std():,.0f} AZN'
ax.text(0.98, 0.97, stats_text, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

ax.legend(loc='upper right', framealpha=0.9)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('charts/01_price_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: charts/01_price_distribution.png\n")

# =============================================================================
# CHART 2: Price by Number of Rooms
# =============================================================================
print("Generating Chart 2: Price by Number of Rooms...")
fig, ax = plt.subplots(figsize=(14, 8))

room_price = df_clean[['rooms', 'price_value']].dropna()
room_price = room_price[room_price['rooms'] <= 6]  # Focus on 1-6 rooms

room_stats = room_price.groupby('rooms')['price_value'].agg(['mean', 'median', 'count'])
room_stats = room_stats[room_stats['count'] >= 50]  # Only show rooms with sufficient data

x = room_stats.index
width = 0.35

bars1 = ax.bar(x - width/2, room_stats['mean'], width, label='Mean Price',
               color='#e74c3c', alpha=0.8, edgecolor='black')
bars2 = ax.bar(x + width/2, room_stats['median'], width, label='Median Price',
               color='#2ecc71', alpha=0.8, edgecolor='black')

# Add value labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:,.0f}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')

ax.set_xlabel('Number of Rooms', fontsize=12, fontweight='bold')
ax.set_ylabel('Price (AZN)', fontsize=12, fontweight='bold')
ax.set_title('Average Property Price by Number of Rooms', fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.legend(framealpha=0.9)
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('charts/02_price_by_rooms.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: charts/02_price_by_rooms.png\n")

# =============================================================================
# CHART 3: Area Distribution
# =============================================================================
print("Generating Chart 3: Area Distribution...")
fig, ax = plt.subplots(figsize=(14, 8))

areas = df_clean['area_value'].dropna()
areas = areas[areas <= 500]  # Focus on typical apartments

ax.hist(areas, bins=60, color='#9b59b6', edgecolor='black', alpha=0.7)

ax.set_xlabel('Area (m²)', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of Properties', fontsize=12, fontweight='bold')
ax.set_title('Property Area Distribution', fontsize=16, fontweight='bold', pad=20)

# Add statistics
mean_area = areas.mean()
median_area = areas.median()
ax.axvline(mean_area, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_area:.1f} m²')
ax.axvline(median_area, color='green', linestyle='--', linewidth=2, label=f'Median: {median_area:.1f} m²')

# Add text box
stats_text = f'Total Properties: {len(areas):,}\nMean: {mean_area:.1f} m²\nMedian: {median_area:.1f} m²'
ax.text(0.98, 0.97, stats_text, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

ax.legend(loc='upper right', framealpha=0.9)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('charts/03_area_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: charts/03_area_distribution.png\n")

# =============================================================================
# CHART 4: Price per Square Meter by Rooms
# =============================================================================
print("Generating Chart 4: Price per Square Meter Analysis...")
fig, ax = plt.subplots(figsize=(14, 8))

# Calculate price per m²
df_price_m2 = df_clean[['rooms', 'price_value', 'area_value']].dropna()
df_price_m2 = df_price_m2[df_price_m2['rooms'] <= 6]
df_price_m2['price_per_m2'] = df_price_m2['price_value'] / df_price_m2['area_value']

# Remove outliers
df_price_m2 = df_price_m2[df_price_m2['price_per_m2'] < df_price_m2['price_per_m2'].quantile(0.95)]
df_price_m2 = df_price_m2[df_price_m2['price_per_m2'] > df_price_m2['price_per_m2'].quantile(0.05)]

# Box plot
bp = ax.boxplot([df_price_m2[df_price_m2['rooms'] == r]['price_per_m2'].values
                  for r in sorted(df_price_m2['rooms'].unique())],
                 labels=sorted(df_price_m2['rooms'].unique()),
                 patch_artist=True,
                 medianprops=dict(color='red', linewidth=2),
                 boxprops=dict(facecolor='#3498db', alpha=0.7),
                 whiskerprops=dict(linewidth=1.5),
                 capprops=dict(linewidth=1.5))

ax.set_xlabel('Number of Rooms', fontsize=12, fontweight='bold')
ax.set_ylabel('Price per m² (AZN)', fontsize=12, fontweight='bold')
ax.set_title('Price per Square Meter by Number of Rooms', fontsize=16, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('charts/04_price_per_sqm.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: charts/04_price_per_sqm.png\n")

# =============================================================================
# CHART 5: Room Count Distribution
# =============================================================================
print("Generating Chart 5: Room Count Distribution...")
fig, ax = plt.subplots(figsize=(14, 8))

room_counts = df_clean['rooms'].dropna()
room_counts = room_counts[room_counts <= 7]

room_dist = room_counts.value_counts().sort_index()

colors = plt.cm.viridis(np.linspace(0, 1, len(room_dist)))
bars = ax.bar(room_dist.index, room_dist.values, color=colors, edgecolor='black', alpha=0.8)

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height):,}\n({height/len(room_counts)*100:.1f}%)',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_xlabel('Number of Rooms', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of Properties', fontsize=12, fontweight='bold')
ax.set_title('Distribution of Properties by Number of Rooms', fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(room_dist.index)
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('charts/05_room_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: charts/05_room_distribution.png\n")

# =============================================================================
# CHART 6: Floor Distribution
# =============================================================================
print("Generating Chart 6: Floor Distribution...")
fig, ax = plt.subplots(figsize=(14, 8))

floors = df_clean['floor'].dropna()
floors = floors[floors <= 25]

ax.hist(floors, bins=25, color='#e67e22', edgecolor='black', alpha=0.7)

ax.set_xlabel('Floor Number', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of Properties', fontsize=12, fontweight='bold')
ax.set_title('Property Distribution by Floor', fontsize=16, fontweight='bold', pad=20)

mean_floor = floors.mean()
median_floor = floors.median()
ax.axvline(mean_floor, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_floor:.1f}')
ax.axvline(median_floor, color='green', linestyle='--', linewidth=2, label=f'Median: {median_floor:.1f}')

stats_text = f'Total Properties: {len(floors):,}\nMean Floor: {mean_floor:.1f}\nMedian Floor: {median_floor:.1f}'
ax.text(0.98, 0.97, stats_text, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='orange', alpha=0.3))

ax.legend(framealpha=0.9)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('charts/06_floor_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: charts/06_floor_distribution.png\n")

# =============================================================================
# CHART 7: Top Cities by Property Count
# =============================================================================
print("Generating Chart 7: Top Cities...")
fig, ax = plt.subplots(figsize=(14, 8))

city_counts = df['city_name'].dropna().value_counts().head(15)

colors = plt.cm.Spectral(np.linspace(0, 1, len(city_counts)))
bars = ax.barh(range(len(city_counts)), city_counts.values, color=colors, edgecolor='black', alpha=0.8)

# Add value labels
for i, (bar, value) in enumerate(zip(bars, city_counts.values)):
    ax.text(value + max(city_counts.values)*0.01, i, f'{value:,}',
            va='center', fontsize=10, fontweight='bold')

ax.set_yticks(range(len(city_counts)))
ax.set_yticklabels(city_counts.index)
ax.set_xlabel('Number of Properties', fontsize=12, fontweight='bold')
ax.set_ylabel('City', fontsize=12, fontweight='bold')
ax.set_title('Top 15 Cities by Number of Properties', fontsize=16, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('charts/07_top_cities.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: charts/07_top_cities.png\n")

# =============================================================================
# CHART 8: Property Features Analysis
# =============================================================================
print("Generating Chart 8: Property Features...")
fig, ax = plt.subplots(figsize=(14, 8))

features = {
    'Has Repair': df['has_repair'].value_counts().get(True, 0),
    'Has Mortgage': df['has_mortgage'].value_counts().get(True, 0),
    'Bill of Sale': df['has_bill_of_sale'].value_counts().get(True, 0),
    'VIP Listing': df['vipped'].value_counts().get(True, 0),
    'Featured': df['featured'].value_counts().get(True, 0),
    'Business': df['is_business'].value_counts().get(True, 0)
}

features_sorted = dict(sorted(features.items(), key=lambda x: x[1], reverse=True))
colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']

bars = ax.bar(range(len(features_sorted)), features_sorted.values(),
              color=colors, edgecolor='black', alpha=0.8)

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height):,}\n({height/len(df)*100:.1f}%)',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_xticks(range(len(features_sorted)))
ax.set_xticklabels(features_sorted.keys(), rotation=45, ha='right')
ax.set_ylabel('Number of Properties', fontsize=12, fontweight='bold')
ax.set_title('Property Features Distribution', fontsize=16, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('charts/08_property_features.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: charts/08_property_features.png\n")

# =============================================================================
# CHART 9: Price Range Categories
# =============================================================================
print("Generating Chart 9: Price Range Categories...")
fig, ax = plt.subplots(figsize=(14, 8))

prices_clean = df_clean['price_value'].dropna()

# Define price ranges
bins = [0, 50000, 100000, 150000, 200000, 300000, 500000, float('inf')]
labels = ['<50K', '50K-100K', '100K-150K', '150K-200K', '200K-300K', '300K-500K', '>500K']

price_ranges = pd.cut(prices_clean, bins=bins, labels=labels)
range_counts = price_ranges.value_counts().sort_index()

colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(range_counts)))
bars = ax.bar(range(len(range_counts)), range_counts.values, color=colors,
              edgecolor='black', alpha=0.8)

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height):,}\n({height/len(prices_clean)*100:.1f}%)',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_xticks(range(len(range_counts)))
ax.set_xticklabels(range_counts.index, rotation=45, ha='right')
ax.set_ylabel('Number of Properties', fontsize=12, fontweight='bold')
ax.set_xlabel('Price Range (AZN)', fontsize=12, fontweight='bold')
ax.set_title('Distribution of Properties by Price Range', fontsize=16, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('charts/09_price_ranges.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: charts/09_price_ranges.png\n")

# =============================================================================
# CHART 10: Area vs Price Scatter
# =============================================================================
print("Generating Chart 10: Area vs Price Correlation...")
fig, ax = plt.subplots(figsize=(14, 8))

scatter_data = df_clean[['area_value', 'price_value', 'rooms']].dropna()
scatter_data = scatter_data[scatter_data['area_value'] <= 300]
scatter_data = scatter_data[scatter_data['rooms'] <= 5]

# Create scatter plot with color by rooms
for room in sorted(scatter_data['rooms'].unique()):
    data = scatter_data[scatter_data['rooms'] == room]
    ax.scatter(data['area_value'], data['price_value'], alpha=0.5,
              s=30, label=f'{int(room)} Room{"s" if room > 1 else ""}')

ax.set_xlabel('Area (m²)', fontsize=12, fontweight='bold')
ax.set_ylabel('Price (AZN)', fontsize=12, fontweight='bold')
ax.set_title('Property Price vs Area (by Number of Rooms)', fontsize=16, fontweight='bold', pad=20)
ax.legend(title='Rooms', framealpha=0.9)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('charts/10_area_vs_price.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: charts/10_area_vs_price.png\n")

# =============================================================================
# CHART 11: Building Floor Count Distribution
# =============================================================================
print("Generating Chart 11: Building Heights...")
fig, ax = plt.subplots(figsize=(14, 8))

building_floors = df_clean['floors'].dropna()
building_floors = building_floors[building_floors <= 30]

ax.hist(building_floors, bins=30, color='#34495e', edgecolor='black', alpha=0.7)

ax.set_xlabel('Total Floors in Building', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of Properties', fontsize=12, fontweight='bold')
ax.set_title('Distribution by Building Height (Total Floors)', fontsize=16, fontweight='bold', pad=20)

mean_floors = building_floors.mean()
median_floors = building_floors.median()
ax.axvline(mean_floors, color='red', linestyle='--', linewidth=2,
          label=f'Mean: {mean_floors:.1f} floors')
ax.axvline(median_floors, color='green', linestyle='--', linewidth=2,
          label=f'Median: {median_floors:.1f} floors')

stats_text = f'Total Buildings: {len(building_floors):,}\nMean: {mean_floors:.1f} floors\nMedian: {median_floors:.1f} floors'
ax.text(0.98, 0.97, stats_text, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.5))

ax.legend(framealpha=0.9)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('charts/11_building_heights.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: charts/11_building_heights.png\n")

# =============================================================================
# CHART 12: Top Locations
# =============================================================================
print("Generating Chart 12: Top Locations...")
fig, ax = plt.subplots(figsize=(14, 10))

location_counts = df['location_name'].dropna().value_counts().head(20)

colors = plt.cm.plasma(np.linspace(0, 1, len(location_counts)))
bars = ax.barh(range(len(location_counts)), location_counts.values,
               color=colors, edgecolor='black', alpha=0.8)

# Add value labels
for i, (bar, value) in enumerate(zip(bars, location_counts.values)):
    ax.text(value + max(location_counts.values)*0.01, i, f'{value:,}',
            va='center', fontsize=9, fontweight='bold')

ax.set_yticks(range(len(location_counts)))
ax.set_yticklabels(location_counts.index, fontsize=9)
ax.set_xlabel('Number of Properties', fontsize=12, fontweight='bold')
ax.set_ylabel('Location', fontsize=12, fontweight='bold')
ax.set_title('Top 20 Locations by Property Count', fontsize=16, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('charts/12_top_locations.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: charts/12_top_locations.png\n")

# =============================================================================
# Summary
# =============================================================================
print("="*80)
print("CHART GENERATION COMPLETE!")
print("="*80)
print(f"\nGenerated 12 high-quality charts in the 'charts/' directory")
print(f"\nCharts created:")
print("  1. Price Distribution")
print("  2. Price by Number of Rooms")
print("  3. Area Distribution")
print("  4. Price per Square Meter")
print("  5. Room Count Distribution")
print("  6. Floor Distribution")
print("  7. Top Cities")
print("  8. Property Features")
print("  9. Price Range Categories")
print(" 10. Area vs Price Correlation")
print(" 11. Building Heights")
print(" 12. Top Locations")
print("\n" + "="*80)
