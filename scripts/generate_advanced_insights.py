#!/usr/bin/env python3
"""
Advanced Real Estate Market Insights - Additional Charts
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter, MaxNLocator
import warnings
warnings.filterwarnings('ignore')

plt.style.use('default')

print("Loading data...")
df = pd.read_csv('data/combined_real_estate_bina_format.csv')

# Clean data
df_clean = df.copy()
df_clean = df_clean[df_clean['price_value'] > 0]
df_clean = df_clean[df_clean['price_value'] < df_clean['price_value'].quantile(0.99)]
df_clean = df_clean[df_clean['area_value'] > 0]
df_clean = df_clean[df_clean['area_value'] < df_clean['area_value'].quantile(0.99)]
df_clean = df_clean[df_clean['floor'] > 0]
df_clean = df_clean[df_clean['floor'] < 50]
df_clean = df_clean[df_clean['rooms'] > 0]
df_clean = df_clean[df_clean['rooms'] <= 10]

print(f"Clean data: {len(df_clean):,} records\n")

def format_price(x, p):
    if x >= 1000000:
        return f'{x/1000000:.1f}M'
    elif x >= 1000:
        return f'{int(x/1000)}K'
    return f'{int(x)}'

def format_count(x, p):
    return f'{int(x):,}'

# =============================================================================
# CHART 13: Average Price by Top 10 Cities
# =============================================================================
print("Generating Chart 13: Average Price by Top Cities...")

fig = plt.figure(figsize=(16, 10))
ax = plt.subplot(111)

# Get top cities by count and calculate mean price
city_data = df_clean.groupby('city_name').agg({
    'price_value': ['mean', 'count']
}).reset_index()
city_data.columns = ['city_name', 'mean_price', 'count']
city_data = city_data[city_data['count'] >= 100]  # At least 100 properties
city_data = city_data.nlargest(12, 'count')
city_data = city_data.sort_values('mean_price', ascending=True)

# Create horizontal bar chart
colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(city_data)))
bars = ax.barh(range(len(city_data)), city_data['mean_price'],
               color=colors, edgecolor='white', linewidth=2, alpha=0.9)

# Add value labels
for i, (bar, value, count) in enumerate(zip(bars, city_data['mean_price'], city_data['count'])):
    ax.text(value + max(city_data['mean_price'])*0.02, i,
            f'{value:,.0f} AZN\n({count:,} props)',
            va='center', fontsize=11, fontweight='bold')

ax.set_yticks(range(len(city_data)))
ax.set_yticklabels(city_data['city_name'], fontsize=12)
ax.set_xlabel('Average Price (AZN)', fontsize=16, fontweight='bold', labelpad=15)
ax.set_ylabel('City', fontsize=16, fontweight='bold', labelpad=15)
ax.set_title('Average Property Price by City (Top 12 Cities)',
             fontsize=20, fontweight='bold', pad=25)

ax.xaxis.set_major_formatter(FuncFormatter(format_price))
ax.grid(True, alpha=0.3, axis='x', linestyle='-', linewidth=1)
ax.set_axisbelow(True)
ax.tick_params(axis='both', which='major', labelsize=12, length=8, width=2)

for spine in ax.spines.values():
    spine.set_linewidth(2)
    spine.set_edgecolor('#2c3e50')

plt.tight_layout(pad=2)
plt.savefig('charts/13_avg_price_by_city.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("✓ Saved: charts/13_avg_price_by_city.png\n")

# =============================================================================
# CHART 14: Impact of Features on Price
# =============================================================================
print("Generating Chart 14: Feature Impact on Price...")

fig = plt.figure(figsize=(16, 10))
ax = plt.subplot(111)

# Calculate average prices for properties with/without features
features_impact = []

for feature, name in [
    ('has_repair', 'Has Repair'),
    ('has_mortgage', 'Has Mortgage'),
    ('has_bill_of_sale', 'Bill of Sale'),
    ('vipped', 'VIP Listing'),
    ('featured', 'Featured')
]:
    with_feature = df_clean[df_clean[feature] == True]['price_value'].mean()
    without_feature = df_clean[df_clean[feature] == False]['price_value'].mean()

    features_impact.append({
        'feature': name,
        'with': with_feature,
        'without': without_feature,
        'diff': with_feature - without_feature,
        'diff_pct': ((with_feature - without_feature) / without_feature) * 100
    })

features_df = pd.DataFrame(features_impact).sort_values('diff', ascending=True)

x = np.arange(len(features_df))
width = 0.35

bars1 = ax.barh(x - width/2, features_df['without'], width,
                label='Without Feature', color='#e74c3c', alpha=0.9,
                edgecolor='white', linewidth=2)
bars2 = ax.barh(x + width/2, features_df['with'], width,
                label='With Feature', color='#2ecc71', alpha=0.9,
                edgecolor='white', linewidth=2)

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        width_val = bar.get_width()
        ax.text(width_val + max(features_df['with'])*0.01,
                bar.get_y() + bar.get_height()/2,
                f'{width_val/1000:.0f}K',
                ha='left', va='center', fontsize=11, fontweight='bold')

ax.set_yticks(x)
ax.set_yticklabels(features_df['feature'], fontsize=12)
ax.set_xlabel('Average Price (AZN)', fontsize=16, fontweight='bold', labelpad=15)
ax.set_ylabel('Feature', fontsize=16, fontweight='bold', labelpad=15)
ax.set_title('Impact of Property Features on Average Price',
             fontsize=20, fontweight='bold', pad=25)

ax.xaxis.set_major_formatter(FuncFormatter(format_price))
ax.legend(fontsize=14, framealpha=0.98, edgecolor='#2c3e50',
         fancybox=True, shadow=True, loc='lower right')
ax.grid(True, alpha=0.3, axis='x', linestyle='-', linewidth=1)
ax.set_axisbelow(True)
ax.tick_params(axis='both', which='major', labelsize=12, length=8, width=2)

for spine in ax.spines.values():
    spine.set_linewidth(2)
    spine.set_edgecolor('#2c3e50')

plt.tight_layout(pad=2)
plt.savefig('charts/14_feature_impact_on_price.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("✓ Saved: charts/14_feature_impact_on_price.png\n")

# =============================================================================
# CHART 15: Average Area per Room Count
# =============================================================================
print("Generating Chart 15: Average Area per Room Count...")

fig = plt.figure(figsize=(16, 10))
ax = plt.subplot(111)

room_area = df_clean.groupby('rooms').agg({
    'area_value': ['mean', 'median', 'std', 'count']
}).reset_index()
room_area.columns = ['rooms', 'mean_area', 'median_area', 'std_area', 'count']
room_area = room_area[(room_area['rooms'] <= 6) & (room_area['count'] >= 50)]

x = room_area['rooms'].values
mean_vals = room_area['mean_area'].values
median_vals = room_area['median_area'].values

width = 0.35

bars1 = ax.bar(x - width/2, mean_vals, width, label='Mean Area',
               color='#3498db', alpha=0.9, edgecolor='white', linewidth=2)
bars2 = ax.bar(x + width/2, median_vals, width, label='Median Area',
               color='#f39c12', alpha=0.9, edgecolor='white', linewidth=2)

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.0f}m²',
                ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_xlabel('Number of Rooms', fontsize=16, fontweight='bold', labelpad=15)
ax.set_ylabel('Area (m²)', fontsize=16, fontweight='bold', labelpad=15)
ax.set_title('Average Property Area by Number of Rooms',
             fontsize=20, fontweight='bold', pad=25)
ax.set_xticks(x)
ax.set_xticklabels([f'{int(r)} Room{"s" if r > 1 else ""}' for r in x])
ax.legend(fontsize=14, framealpha=0.98, edgecolor='#2c3e50',
         fancybox=True, shadow=True)
ax.grid(True, alpha=0.3, axis='y', linestyle='-', linewidth=1)
ax.set_axisbelow(True)
ax.tick_params(axis='both', which='major', labelsize=12, length=8, width=2)

for spine in ax.spines.values():
    spine.set_linewidth(2)
    spine.set_edgecolor('#2c3e50')

plt.tight_layout(pad=2)
plt.savefig('charts/15_area_by_rooms.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("✓ Saved: charts/15_area_by_rooms.png\n")

# =============================================================================
# CHART 16: Market Segmentation (Budget, Mid, Luxury)
# =============================================================================
print("Generating Chart 16: Market Segmentation...")

fig = plt.figure(figsize=(16, 10))
ax = plt.subplot(111)

# Define market segments
df_clean['segment'] = pd.cut(df_clean['price_value'],
                             bins=[0, 80000, 200000, float('inf')],
                             labels=['Budget\n(<80K)', 'Mid-Range\n(80K-200K)', 'Luxury\n(>200K)'])

# Count properties in each segment
segment_counts = df_clean['segment'].value_counts().sort_index()

# Create pie chart with better aesthetics
colors = ['#3498db', '#2ecc71', '#e74c3c']
explode = (0.05, 0.05, 0.1)

wedges, texts, autotexts = ax.pie(segment_counts.values,
                                   labels=segment_counts.index,
                                   autopct='%1.1f%%',
                                   colors=colors,
                                   explode=explode,
                                   startangle=90,
                                   textprops={'fontsize': 14, 'fontweight': 'bold'},
                                   pctdistance=0.85)

# Enhance text
for text in texts:
    text.set_fontsize(16)
    text.set_fontweight('bold')

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(15)
    autotext.set_fontweight('bold')

# Add center circle for donut effect
centre_circle = plt.Circle((0, 0), 0.70, fc='white', linewidth=3, edgecolor='#2c3e50')
ax.add_artist(centre_circle)

# Add title
ax.set_title('Real Estate Market Segmentation by Price',
             fontsize=20, fontweight='bold', pad=25)

# Add legend with counts
legend_labels = [f'{label}\n{count:,} properties'
                for label, count in zip(segment_counts.index, segment_counts.values)]
ax.legend(legend_labels, loc='upper left', bbox_to_anchor=(1, 0, 0.3, 1),
         fontsize=13, framealpha=0.98, edgecolor='#2c3e50', fancybox=True)

plt.tight_layout(pad=2)
plt.savefig('charts/16_market_segmentation.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("✓ Saved: charts/16_market_segmentation.png\n")

# =============================================================================
# CHART 17: Floor Preference (Ground vs Higher Floors)
# =============================================================================
print("Generating Chart 17: Floor Preference Analysis...")

fig = plt.figure(figsize=(16, 10))
ax = plt.subplot(111)

# Categorize floors
df_clean['floor_category'] = pd.cut(df_clean['floor'],
                                    bins=[0, 1, 3, 6, 10, 50],
                                    labels=['Ground\n(1st)', 'Low\n(2-3)',
                                           'Mid\n(4-6)', 'High\n(7-10)', 'Very High\n(11+)'])

floor_stats = df_clean.groupby('floor_category').agg({
    'price_value': ['mean', 'count']
}).reset_index()
floor_stats.columns = ['floor_category', 'mean_price', 'count']
floor_stats = floor_stats.dropna()

x = range(len(floor_stats))
colors = ['#e67e22', '#3498db', '#2ecc71', '#9b59b6', '#e74c3c']

# Create bar chart
bars = ax.bar(x, floor_stats['mean_price'], color=colors,
              alpha=0.9, edgecolor='white', linewidth=2)

# Add value labels
for i, (bar, price, count) in enumerate(zip(bars, floor_stats['mean_price'], floor_stats['count'])):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{price/1000:.0f}K AZN\n({count:,} props)',
            ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_xticks(x)
ax.set_xticklabels(floor_stats['floor_category'], fontsize=13)
ax.set_xlabel('Floor Category', fontsize=16, fontweight='bold', labelpad=15)
ax.set_ylabel('Average Price (AZN)', fontsize=16, fontweight='bold', labelpad=15)
ax.set_title('Average Price by Floor Level Category',
             fontsize=20, fontweight='bold', pad=25)

ax.yaxis.set_major_formatter(FuncFormatter(format_price))
ax.grid(True, alpha=0.3, axis='y', linestyle='-', linewidth=1)
ax.set_axisbelow(True)
ax.tick_params(axis='both', which='major', labelsize=12, length=8, width=2)

for spine in ax.spines.values():
    spine.set_linewidth(2)
    spine.set_edgecolor('#2c3e50')

plt.tight_layout(pad=2)
plt.savefig('charts/17_floor_preference.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("✓ Saved: charts/17_floor_preference.png\n")

# =============================================================================
# CHART 18: Building Type Analysis (by total floors)
# =============================================================================
print("Generating Chart 18: Building Type Distribution...")

fig = plt.figure(figsize=(16, 10))
ax = plt.subplot(111)

# Categorize building types
df_clean['building_type'] = pd.cut(df_clean['floors'],
                                   bins=[0, 5, 10, 16, 100],
                                   labels=['Low-Rise\n(≤5 floors)',
                                          'Mid-Rise\n(6-10 floors)',
                                          'High-Rise\n(11-16 floors)',
                                          'Skyscraper\n(>16 floors)'])

building_stats = df_clean.groupby('building_type').agg({
    'price_value': ['mean', 'count'],
    'area_value': 'mean'
}).reset_index()
building_stats.columns = ['building_type', 'mean_price', 'count', 'mean_area']
building_stats = building_stats.dropna()

x = range(len(building_stats))
colors = ['#95a5a6', '#3498db', '#2ecc71', '#e74c3c']

bars = ax.bar(x, building_stats['count'], color=colors,
              alpha=0.9, edgecolor='white', linewidth=2)

# Add value labels
for i, (bar, count, price) in enumerate(zip(bars, building_stats['count'], building_stats['mean_price'])):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{count:,}\nAvg: {price/1000:.0f}K',
            ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_xticks(x)
ax.set_xticklabels(building_stats['building_type'], fontsize=13)
ax.set_xlabel('Building Type', fontsize=16, fontweight='bold', labelpad=15)
ax.set_ylabel('Number of Properties', fontsize=16, fontweight='bold', labelpad=15)
ax.set_title('Property Distribution by Building Type',
             fontsize=20, fontweight='bold', pad=25)

ax.yaxis.set_major_formatter(FuncFormatter(format_count))
ax.grid(True, alpha=0.3, axis='y', linestyle='-', linewidth=1)
ax.set_axisbelow(True)
ax.tick_params(axis='both', which='major', labelsize=12, length=8, width=2)

for spine in ax.spines.values():
    spine.set_linewidth(2)
    spine.set_edgecolor('#2c3e50')

plt.tight_layout(pad=2)
plt.savefig('charts/18_building_type_distribution.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("✓ Saved: charts/18_building_type_distribution.png\n")

# =============================================================================
# CHART 19: Top Locations Average Price
# =============================================================================
print("Generating Chart 19: Top Locations by Average Price...")

fig = plt.figure(figsize=(16, 11))
ax = plt.subplot(111)

# Get top locations by property count
location_stats = df_clean.groupby('location_name').agg({
    'price_value': ['mean', 'count']
}).reset_index()
location_stats.columns = ['location', 'mean_price', 'count']
location_stats = location_stats[location_stats['count'] >= 200]  # At least 200 properties
location_stats = location_stats.nlargest(15, 'count')
location_stats = location_stats.sort_values('mean_price', ascending=True)

# Create horizontal bar chart
colors = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(location_stats)))
bars = ax.barh(range(len(location_stats)), location_stats['mean_price'],
               color=colors, edgecolor='white', linewidth=2, alpha=0.9)

# Add value labels
for i, (bar, value, count) in enumerate(zip(bars, location_stats['mean_price'], location_stats['count'])):
    ax.text(value + max(location_stats['mean_price'])*0.02, i,
            f'{value/1000:.0f}K AZN\n({count:,})',
            va='center', fontsize=10, fontweight='bold')

ax.set_yticks(range(len(location_stats)))
ax.set_yticklabels(location_stats['location'], fontsize=11)
ax.set_xlabel('Average Price (AZN)', fontsize=16, fontweight='bold', labelpad=15)
ax.set_ylabel('Location', fontsize=16, fontweight='bold', labelpad=15)
ax.set_title('Average Price by Top 15 Locations (min. 200 properties)',
             fontsize=20, fontweight='bold', pad=25)

ax.xaxis.set_major_formatter(FuncFormatter(format_price))
ax.grid(True, alpha=0.3, axis='x', linestyle='-', linewidth=1)
ax.set_axisbelow(True)
ax.tick_params(axis='both', which='major', labelsize=11, length=8, width=2)

for spine in ax.spines.values():
    spine.set_linewidth(2)
    spine.set_edgecolor('#2c3e50')

plt.tight_layout(pad=2)
plt.savefig('charts/19_top_locations_price.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("✓ Saved: charts/19_top_locations_price.png\n")

# =============================================================================
# CHART 20: Room vs Area Efficiency
# =============================================================================
print("Generating Chart 20: Area per Room Efficiency...")

fig = plt.figure(figsize=(16, 10))
ax = plt.subplot(111)

# Calculate area per room
df_clean['area_per_room'] = df_clean['area_value'] / df_clean['rooms']
room_efficiency = df_clean[df_clean['rooms'] <= 6].groupby('rooms')['area_per_room'].agg(['mean', 'median', 'std'])

x = room_efficiency.index
mean_vals = room_efficiency['mean'].values
median_vals = room_efficiency['median'].values

width = 0.35

bars1 = ax.bar(x - width/2, mean_vals, width, label='Mean Area/Room',
               color='#e74c3c', alpha=0.9, edgecolor='white', linewidth=2)
bars2 = ax.bar(x + width/2, median_vals, width, label='Median Area/Room',
               color='#3498db', alpha=0.9, edgecolor='white', linewidth=2)

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}m²',
                ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_xlabel('Number of Rooms', fontsize=16, fontweight='bold', labelpad=15)
ax.set_ylabel('Area per Room (m²/room)', fontsize=16, fontweight='bold', labelpad=15)
ax.set_title('Average Area per Room by Property Size',
             fontsize=20, fontweight='bold', pad=25)
ax.set_xticks(x)
ax.set_xticklabels([f'{int(r)} Room{"s" if r > 1 else ""}' for r in x])
ax.legend(fontsize=14, framealpha=0.98, edgecolor='#2c3e50',
         fancybox=True, shadow=True)
ax.grid(True, alpha=0.3, axis='y', linestyle='-', linewidth=1)
ax.set_axisbelow(True)
ax.tick_params(axis='both', which='major', labelsize=12, length=8, width=2)

for spine in ax.spines.values():
    spine.set_linewidth(2)
    spine.set_edgecolor('#2c3e50')

plt.tight_layout(pad=2)
plt.savefig('charts/20_area_per_room_efficiency.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("✓ Saved: charts/20_area_per_room_efficiency.png\n")

print("="*80)
print("ADVANCED INSIGHTS GENERATION COMPLETE!")
print("="*80)
print("\nNew charts created:")
print("  13. Average Price by City")
print("  14. Feature Impact on Price")
print("  15. Average Area by Rooms")
print("  16. Market Segmentation")
print("  17. Floor Preference Analysis")
print("  18. Building Type Distribution")
print("  19. Top Locations by Price")
print("  20. Area per Room Efficiency")
print("\nTotal charts: 20")
print("="*80)
