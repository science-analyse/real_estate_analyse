#!/usr/bin/env python3
"""
Fix formatting issues for specific charts
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("Set2")

# Configure for better formatting
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']

# Load data
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

print(f"Clean data: {len(df_clean):,} records\n")

# Formatter functions
def thousands_formatter(x, pos):
    """Format numbers with K suffix"""
    if x >= 1000:
        return f'{int(x/1000)}K'
    return f'{int(x)}'

def price_formatter(x, pos):
    """Format prices in thousands"""
    return f'{int(x/1000)}K'

# =============================================================================
# CHART 1: Price Distribution (FIXED)
# =============================================================================
print("Fixing Chart 1: Price Distribution...")
fig, ax = plt.subplots(figsize=(16, 9))

prices = df_clean['price_value'].dropna()

# Create histogram with better bins
n, bins, patches = ax.hist(prices, bins=40, color='#3498db', edgecolor='#2c3e50',
                           alpha=0.85, linewidth=1.5)

# Color gradient for bars
cm = plt.cm.viridis
norm = plt.Normalize(vmin=bins.min(), vmax=bins.max())
for bin_edge, patch in zip(bins, patches):
    patch.set_facecolor(cm(norm(bin_edge)))

ax.set_xlabel('Price (AZN)', fontsize=14, fontweight='bold', labelpad=10)
ax.set_ylabel('Number of Properties', fontsize=14, fontweight='bold', labelpad=10)
ax.set_title('Real Estate Price Distribution in Azerbaijan',
             fontsize=18, fontweight='bold', pad=20)

# Format x-axis
ax.xaxis.set_major_formatter(FuncFormatter(thousands_formatter))
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'{int(x):,}'))

# Add statistics lines
mean_price = prices.mean()
median_price = prices.median()
ax.axvline(mean_price, color='#e74c3c', linestyle='--', linewidth=3,
          label=f'Mean: {mean_price:,.0f} AZN', alpha=0.8)
ax.axvline(median_price, color='#2ecc71', linestyle='--', linewidth=3,
          label=f'Median: {median_price:,.0f} AZN', alpha=0.8)

# Statistics box
stats_text = (f'Total Properties: {len(prices):,}\n'
              f'Mean Price: {mean_price:,.0f} AZN\n'
              f'Median Price: {median_price:,.0f} AZN\n'
              f'Std Dev: {prices.std():,.0f} AZN\n'
              f'Min: {prices.min():,.0f} AZN\n'
              f'Max: {prices.max():,.0f} AZN')

props = dict(boxstyle='round,pad=1', facecolor='#ecf0f1', alpha=0.9, edgecolor='#34495e', linewidth=2)
ax.text(0.97, 0.97, stats_text, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', horizontalalignment='right',
        bbox=props, family='monospace')

ax.legend(loc='upper right', fontsize=12, framealpha=0.95, edgecolor='black', fancybox=True)
ax.grid(True, alpha=0.4, linestyle='--', linewidth=0.8)
ax.set_axisbelow(True)

# Rotate x-axis labels if needed
plt.xticks(rotation=0, ha='center', fontsize=11)
plt.yticks(fontsize=11)

plt.tight_layout()
plt.savefig('charts/01_price_distribution.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("✓ Fixed: charts/01_price_distribution.png\n")

# =============================================================================
# CHART 3: Area Distribution (FIXED)
# =============================================================================
print("Fixing Chart 3: Area Distribution...")
fig, ax = plt.subplots(figsize=(16, 9))

areas = df_clean['area_value'].dropna()
areas = areas[areas <= 500]

# Create histogram
n, bins, patches = ax.hist(areas, bins=50, color='#9b59b6', edgecolor='#6c3483',
                           alpha=0.85, linewidth=1.5)

# Color gradient
cm = plt.cm.plasma
norm = plt.Normalize(vmin=bins.min(), vmax=bins.max())
for bin_edge, patch in zip(bins, patches):
    patch.set_facecolor(cm(norm(bin_edge)))

ax.set_xlabel('Area (m²)', fontsize=14, fontweight='bold', labelpad=10)
ax.set_ylabel('Number of Properties', fontsize=14, fontweight='bold', labelpad=10)
ax.set_title('Property Area Distribution', fontsize=18, fontweight='bold', pad=20)

# Format axes
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'{int(x):,}'))

# Statistics
mean_area = areas.mean()
median_area = areas.median()
ax.axvline(mean_area, color='#e74c3c', linestyle='--', linewidth=3,
          label=f'Mean: {mean_area:.1f} m²', alpha=0.8)
ax.axvline(median_area, color='#2ecc71', linestyle='--', linewidth=3,
          label=f'Median: {median_area:.1f} m²', alpha=0.8)

# Statistics box
stats_text = (f'Total Properties: {len(areas):,}\n'
              f'Mean Area: {mean_area:.1f} m²\n'
              f'Median Area: {median_area:.1f} m²\n'
              f'Std Dev: {areas.std():.1f} m²\n'
              f'Min: {areas.min():.1f} m²\n'
              f'Max: {areas.max():.1f} m²')

props = dict(boxstyle='round,pad=1', facecolor='#e8f8f5', alpha=0.9, edgecolor='#1abc9c', linewidth=2)
ax.text(0.97, 0.97, stats_text, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', horizontalalignment='right',
        bbox=props, family='monospace')

ax.legend(loc='upper right', fontsize=12, framealpha=0.95, edgecolor='black', fancybox=True)
ax.grid(True, alpha=0.4, linestyle='--', linewidth=0.8)
ax.set_axisbelow(True)

plt.xticks(fontsize=11)
plt.yticks(fontsize=11)

plt.tight_layout()
plt.savefig('charts/03_area_distribution.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("✓ Fixed: charts/03_area_distribution.png\n")

# =============================================================================
# CHART 6: Floor Distribution (FIXED)
# =============================================================================
print("Fixing Chart 6: Floor Distribution...")
fig, ax = plt.subplots(figsize=(16, 9))

floors = df_clean['floor'].dropna()
floors = floors[floors <= 25]

# Create histogram
n, bins, patches = ax.hist(floors, bins=25, color='#e67e22', edgecolor='#d35400',
                           alpha=0.85, linewidth=1.5)

# Color gradient
cm = plt.cm.autumn
norm = plt.Normalize(vmin=bins.min(), vmax=bins.max())
for bin_edge, patch in zip(bins, patches):
    patch.set_facecolor(cm(norm(bin_edge)))

ax.set_xlabel('Floor Number', fontsize=14, fontweight='bold', labelpad=10)
ax.set_ylabel('Number of Properties', fontsize=14, fontweight='bold', labelpad=10)
ax.set_title('Property Distribution by Floor Level', fontsize=18, fontweight='bold', pad=20)

# Format y-axis
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'{int(x):,}'))

# Statistics
mean_floor = floors.mean()
median_floor = floors.median()
ax.axvline(mean_floor, color='#e74c3c', linestyle='--', linewidth=3,
          label=f'Mean: {mean_floor:.1f}', alpha=0.8)
ax.axvline(median_floor, color='#2ecc71', linestyle='--', linewidth=3,
          label=f'Median: {median_floor:.1f}', alpha=0.8)

# Statistics box
stats_text = (f'Total Properties: {len(floors):,}\n'
              f'Mean Floor: {mean_floor:.1f}\n'
              f'Median Floor: {median_floor:.1f}\n'
              f'Std Dev: {floors.std():.1f}\n'
              f'Most Common: {floors.mode().values[0]:.0f}\n'
              f'Range: {floors.min():.0f} - {floors.max():.0f}')

props = dict(boxstyle='round,pad=1', facecolor='#fef5e7', alpha=0.9, edgecolor='#f39c12', linewidth=2)
ax.text(0.97, 0.97, stats_text, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', horizontalalignment='right',
        bbox=props, family='monospace')

ax.legend(loc='upper right', fontsize=12, framealpha=0.95, edgecolor='black', fancybox=True)
ax.grid(True, alpha=0.4, linestyle='--', linewidth=0.8)
ax.set_axisbelow(True)

plt.xticks(fontsize=11)
plt.yticks(fontsize=11)

plt.tight_layout()
plt.savefig('charts/06_floor_distribution.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("✓ Fixed: charts/06_floor_distribution.png\n")

# =============================================================================
# CHART 11: Building Heights (FIXED)
# =============================================================================
print("Fixing Chart 11: Building Heights...")
fig, ax = plt.subplots(figsize=(16, 9))

building_floors = df_clean['floors'].dropna()
building_floors = building_floors[building_floors <= 30]

# Create histogram
n, bins, patches = ax.hist(building_floors, bins=30, color='#34495e', edgecolor='#2c3e50',
                           alpha=0.85, linewidth=1.5)

# Color gradient
cm = plt.cm.cool
norm = plt.Normalize(vmin=bins.min(), vmax=bins.max())
for bin_edge, patch in zip(bins, patches):
    patch.set_facecolor(cm(norm(bin_edge)))

ax.set_xlabel('Total Floors in Building', fontsize=14, fontweight='bold', labelpad=10)
ax.set_ylabel('Number of Properties', fontsize=14, fontweight='bold', labelpad=10)
ax.set_title('Distribution by Building Height (Total Floors)', fontsize=18, fontweight='bold', pad=20)

# Format y-axis
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'{int(x):,}'))

# Statistics
mean_floors = building_floors.mean()
median_floors = building_floors.median()
ax.axvline(mean_floors, color='#e74c3c', linestyle='--', linewidth=3,
          label=f'Mean: {mean_floors:.1f} floors', alpha=0.8)
ax.axvline(median_floors, color='#2ecc71', linestyle='--', linewidth=3,
          label=f'Median: {median_floors:.1f} floors', alpha=0.8)

# Statistics box
stats_text = (f'Total Properties: {len(building_floors):,}\n'
              f'Mean Floors: {mean_floors:.1f}\n'
              f'Median Floors: {median_floors:.1f}\n'
              f'Std Dev: {building_floors.std():.1f}\n'
              f'Most Common: {building_floors.mode().values[0]:.0f}\n'
              f'Range: {building_floors.min():.0f} - {building_floors.max():.0f}')

props = dict(boxstyle='round,pad=1', facecolor='#eaecee', alpha=0.9, edgecolor='#5d6d7e', linewidth=2)
ax.text(0.97, 0.97, stats_text, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', horizontalalignment='right',
        bbox=props, family='monospace')

ax.legend(loc='upper right', fontsize=12, framealpha=0.95, edgecolor='black', fancybox=True)
ax.grid(True, alpha=0.4, linestyle='--', linewidth=0.8)
ax.set_axisbelow(True)

plt.xticks(fontsize=11)
plt.yticks(fontsize=11)

plt.tight_layout()
plt.savefig('charts/11_building_heights.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("✓ Fixed: charts/11_building_heights.png\n")

print("="*80)
print("ALL FORMATTING ISSUES FIXED!")
print("="*80)
print("\nFixed charts:")
print("  ✓ 01_price_distribution.png")
print("  ✓ 03_area_distribution.png")
print("  ✓ 06_floor_distribution.png")
print("  ✓ 11_building_heights.png")
print("\n" + "="*80)
