#!/usr/bin/env python3
"""
Complete chart regeneration with perfect formatting
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter, MaxNLocator
import warnings
warnings.filterwarnings('ignore')

# Use a clean style
plt.style.use('default')

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

# =============================================================================
# CHART 1: Price Distribution
# =============================================================================
print("Generating Chart 1: Price Distribution...")

fig = plt.figure(figsize=(16, 10))
ax = plt.subplot(111)

prices = df_clean['price_value'].dropna()

# Histogram
counts, bins, patches = ax.hist(prices, bins=35, color='#3498db',
                                edgecolor='white', linewidth=2, alpha=0.9)

# Apply gradient color
colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(patches)))
for patch, color in zip(patches, colors):
    patch.set_facecolor(color)

# Labels and title
ax.set_xlabel('Price (AZN)', fontsize=16, fontweight='bold', labelpad=15)
ax.set_ylabel('Number of Properties', fontsize=16, fontweight='bold', labelpad=15)
ax.set_title('Real Estate Price Distribution in Azerbaijan',
             fontsize=20, fontweight='bold', pad=25)

# Format axes
def format_price(x, p):
    if x >= 1000000:
        return f'{x/1000000:.1f}M'
    elif x >= 1000:
        return f'{int(x/1000)}K'
    return f'{int(x)}'

def format_count(x, p):
    return f'{int(x):,}'

ax.xaxis.set_major_formatter(FuncFormatter(format_price))
ax.yaxis.set_major_formatter(FuncFormatter(format_count))
ax.xaxis.set_major_locator(MaxNLocator(nbins=10))
ax.yaxis.set_major_locator(MaxNLocator(nbins=8))

# Statistics
mean_price = prices.mean()
median_price = prices.median()

ax.axvline(mean_price, color='#e74c3c', linestyle='--', linewidth=3.5,
          label=f'Mean: {mean_price/1000:.0f}K AZN', alpha=0.9, zorder=5)
ax.axvline(median_price, color='#27ae60', linestyle='--', linewidth=3.5,
          label=f'Median: {median_price/1000:.0f}K AZN', alpha=0.9, zorder=5)

# Stats box
stats = (f'Properties: {len(prices):,}\n\n'
         f'Mean:   {mean_price:>12,.0f} AZN\n'
         f'Median: {median_price:>12,.0f} AZN\n'
         f'Std:    {prices.std():>12,.0f} AZN\n'
         f'Min:    {prices.min():>12,.0f} AZN\n'
         f'Max:    {prices.max():>12,.0f} AZN')

props = dict(boxstyle='round,pad=1.2', facecolor='white',
            alpha=0.95, edgecolor='#34495e', linewidth=2.5)
ax.text(0.98, 0.98, stats, transform=ax.transAxes, fontsize=13,
        verticalalignment='top', horizontalalignment='right',
        bbox=props, family='monospace', fontweight='normal')

# Legend
ax.legend(loc='upper left', fontsize=14, framealpha=0.98,
         edgecolor='#2c3e50', fancybox=True, shadow=True)

# Grid
ax.grid(True, alpha=0.3, linestyle='-', linewidth=1, color='gray')
ax.set_axisbelow(True)

# Tick parameters
ax.tick_params(axis='both', which='major', labelsize=13, length=8, width=2)

# Spines
for spine in ax.spines.values():
    spine.set_linewidth(2)
    spine.set_edgecolor('#2c3e50')

plt.tight_layout(pad=2)
plt.savefig('charts/01_price_distribution.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("✓ Saved: charts/01_price_distribution.png\n")

# =============================================================================
# CHART 3: Area Distribution
# =============================================================================
print("Generating Chart 3: Area Distribution...")

fig = plt.figure(figsize=(16, 10))
ax = plt.subplot(111)

areas = df_clean['area_value'].dropna()
areas = areas[areas <= 500]

# Histogram
counts, bins, patches = ax.hist(areas, bins=40, color='#9b59b6',
                                edgecolor='white', linewidth=2, alpha=0.9)

# Gradient
colors = plt.cm.Purples(np.linspace(0.4, 0.9, len(patches)))
for patch, color in zip(patches, colors):
    patch.set_facecolor(color)

# Labels
ax.set_xlabel('Area (m²)', fontsize=16, fontweight='bold', labelpad=15)
ax.set_ylabel('Number of Properties', fontsize=16, fontweight='bold', labelpad=15)
ax.set_title('Property Area Distribution', fontsize=20, fontweight='bold', pad=25)

# Format axes
ax.yaxis.set_major_formatter(FuncFormatter(format_count))
ax.xaxis.set_major_locator(MaxNLocator(nbins=10))
ax.yaxis.set_major_locator(MaxNLocator(nbins=8))

# Statistics
mean_area = areas.mean()
median_area = areas.median()

ax.axvline(mean_area, color='#e74c3c', linestyle='--', linewidth=3.5,
          label=f'Mean: {mean_area:.0f} m²', alpha=0.9, zorder=5)
ax.axvline(median_area, color='#27ae60', linestyle='--', linewidth=3.5,
          label=f'Median: {median_area:.0f} m²', alpha=0.9, zorder=5)

# Stats box
stats = (f'Properties: {len(areas):,}\n\n'
         f'Mean:   {mean_area:>8.1f} m²\n'
         f'Median: {median_area:>8.1f} m²\n'
         f'Std:    {areas.std():>8.1f} m²\n'
         f'Min:    {areas.min():>8.1f} m²\n'
         f'Max:    {areas.max():>8.1f} m²')

props = dict(boxstyle='round,pad=1.2', facecolor='white',
            alpha=0.95, edgecolor='#8e44ad', linewidth=2.5)
ax.text(0.98, 0.98, stats, transform=ax.transAxes, fontsize=13,
        verticalalignment='top', horizontalalignment='right',
        bbox=props, family='monospace')

# Legend
ax.legend(loc='upper left', fontsize=14, framealpha=0.98,
         edgecolor='#2c3e50', fancybox=True, shadow=True)

# Grid
ax.grid(True, alpha=0.3, linestyle='-', linewidth=1, color='gray')
ax.set_axisbelow(True)

# Ticks
ax.tick_params(axis='both', which='major', labelsize=13, length=8, width=2)

# Spines
for spine in ax.spines.values():
    spine.set_linewidth(2)
    spine.set_edgecolor('#2c3e50')

plt.tight_layout(pad=2)
plt.savefig('charts/03_area_distribution.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("✓ Saved: charts/03_area_distribution.png\n")

# =============================================================================
# CHART 6: Floor Distribution
# =============================================================================
print("Generating Chart 6: Floor Distribution...")

fig = plt.figure(figsize=(16, 10))
ax = plt.subplot(111)

floors = df_clean['floor'].dropna()
floors = floors[floors <= 25]

# Histogram
counts, bins, patches = ax.hist(floors, bins=25, color='#e67e22',
                                edgecolor='white', linewidth=2, alpha=0.9)

# Gradient
colors = plt.cm.Oranges(np.linspace(0.4, 0.9, len(patches)))
for patch, color in zip(patches, colors):
    patch.set_facecolor(color)

# Labels
ax.set_xlabel('Floor Number', fontsize=16, fontweight='bold', labelpad=15)
ax.set_ylabel('Number of Properties', fontsize=16, fontweight='bold', labelpad=15)
ax.set_title('Property Distribution by Floor Level', fontsize=20, fontweight='bold', pad=25)

# Format axes
ax.yaxis.set_major_formatter(FuncFormatter(format_count))
ax.xaxis.set_major_locator(MaxNLocator(nbins=12))
ax.yaxis.set_major_locator(MaxNLocator(nbins=8))

# Statistics
mean_floor = floors.mean()
median_floor = floors.median()

ax.axvline(mean_floor, color='#e74c3c', linestyle='--', linewidth=3.5,
          label=f'Mean: {mean_floor:.1f}', alpha=0.9, zorder=5)
ax.axvline(median_floor, color='#27ae60', linestyle='--', linewidth=3.5,
          label=f'Median: {median_floor:.1f}', alpha=0.9, zorder=5)

# Stats box
mode_floor = floors.mode().values[0]
stats = (f'Properties: {len(floors):,}\n\n'
         f'Mean:   {mean_floor:>6.1f}\n'
         f'Median: {median_floor:>6.1f}\n'
         f'Mode:   {mode_floor:>6.0f}\n'
         f'Std:    {floors.std():>6.1f}\n'
         f'Range:  {floors.min():.0f} - {floors.max():.0f}')

props = dict(boxstyle='round,pad=1.2', facecolor='white',
            alpha=0.95, edgecolor='#d35400', linewidth=2.5)
ax.text(0.98, 0.98, stats, transform=ax.transAxes, fontsize=13,
        verticalalignment='top', horizontalalignment='right',
        bbox=props, family='monospace')

# Legend
ax.legend(loc='upper left', fontsize=14, framealpha=0.98,
         edgecolor='#2c3e50', fancybox=True, shadow=True)

# Grid
ax.grid(True, alpha=0.3, linestyle='-', linewidth=1, color='gray')
ax.set_axisbelow(True)

# Ticks
ax.tick_params(axis='both', which='major', labelsize=13, length=8, width=2)

# Spines
for spine in ax.spines.values():
    spine.set_linewidth(2)
    spine.set_edgecolor('#2c3e50')

plt.tight_layout(pad=2)
plt.savefig('charts/06_floor_distribution.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("✓ Saved: charts/06_floor_distribution.png\n")

# =============================================================================
# CHART 11: Building Heights
# =============================================================================
print("Generating Chart 11: Building Heights...")

fig = plt.figure(figsize=(16, 10))
ax = plt.subplot(111)

building_floors = df_clean['floors'].dropna()
building_floors = building_floors[building_floors <= 30]

# Histogram
counts, bins, patches = ax.hist(building_floors, bins=30, color='#34495e',
                                edgecolor='white', linewidth=2, alpha=0.9)

# Gradient
colors = plt.cm.Greys(np.linspace(0.4, 0.9, len(patches)))
for patch, color in zip(patches, colors):
    patch.set_facecolor(color)

# Labels
ax.set_xlabel('Total Floors in Building', fontsize=16, fontweight='bold', labelpad=15)
ax.set_ylabel('Number of Properties', fontsize=16, fontweight='bold', labelpad=15)
ax.set_title('Distribution by Building Height', fontsize=20, fontweight='bold', pad=25)

# Format axes
ax.yaxis.set_major_formatter(FuncFormatter(format_count))
ax.xaxis.set_major_locator(MaxNLocator(nbins=10))
ax.yaxis.set_major_locator(MaxNLocator(nbins=8))

# Statistics
mean_floors = building_floors.mean()
median_floors = building_floors.median()

ax.axvline(mean_floors, color='#e74c3c', linestyle='--', linewidth=3.5,
          label=f'Mean: {mean_floors:.1f} floors', alpha=0.9, zorder=5)
ax.axvline(median_floors, color='#27ae60', linestyle='--', linewidth=3.5,
          label=f'Median: {median_floors:.1f} floors', alpha=0.9, zorder=5)

# Stats box
mode_floors = building_floors.mode().values[0]
stats = (f'Properties: {len(building_floors):,}\n\n'
         f'Mean:   {mean_floors:>6.1f} floors\n'
         f'Median: {median_floors:>6.1f} floors\n'
         f'Mode:   {mode_floors:>6.0f} floors\n'
         f'Std:    {building_floors.std():>6.1f} floors\n'
         f'Range:  {building_floors.min():.0f} - {building_floors.max():.0f}')

props = dict(boxstyle='round,pad=1.2', facecolor='white',
            alpha=0.95, edgecolor='#2c3e50', linewidth=2.5)
ax.text(0.98, 0.98, stats, transform=ax.transAxes, fontsize=13,
        verticalalignment='top', horizontalalignment='right',
        bbox=props, family='monospace')

# Legend
ax.legend(loc='upper left', fontsize=14, framealpha=0.98,
         edgecolor='#2c3e50', fancybox=True, shadow=True)

# Grid
ax.grid(True, alpha=0.3, linestyle='-', linewidth=1, color='gray')
ax.set_axisbelow(True)

# Ticks
ax.tick_params(axis='both', which='major', labelsize=13, length=8, width=2)

# Spines
for spine in ax.spines.values():
    spine.set_linewidth(2)
    spine.set_edgecolor('#2c3e50')

plt.tight_layout(pad=2)
plt.savefig('charts/11_building_heights.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("✓ Saved: charts/11_building_heights.png\n")

print("="*80)
print("ALL CHARTS REGENERATED WITH PERFECT FORMATTING!")
print("="*80)
print("\nFixed charts:")
print("  ✓ 01_price_distribution.png")
print("  ✓ 03_area_distribution.png")
print("  ✓ 06_floor_distribution.png")
print("  ✓ 11_building_heights.png")
print("\n" + "="*80)
