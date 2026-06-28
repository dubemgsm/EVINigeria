import os
import json
import pandas as pd
import geopandas as gpd
import numpy as np
import folium
from branca.colormap import LinearColormap

# File paths
SHP_PATH = "data/raw/nga_shp/nga_admin2.shp"
EVI_PATH = "data/processed/evi_scores.csv"
CLUSTERS_PATH = "data/processed/clusters.csv"
RISK_PATH = "data/processed/disruption_risk.csv"
DOCS_DIR = "docs"

os.makedirs(DOCS_DIR, exist_ok=True)

print("1. Loading shapefile and standardized results...")
gdf = gpd.read_file(SHP_PATH)
if gdf.crs != "EPSG:4326":
    gdf = gdf.to_crs("EPSG:4326")

bay_shp = gdf[gdf['adm1_name'].isin(['Borno', 'Adamawa', 'Yobe'])].copy()
bay_shp['adm2_name'] = bay_shp['adm2_name'].replace({'Tarmua': 'Tarmuwa'})
bay_shp.loc[bay_shp['adm2_name'] == 'Girei', 'adm2_pcode'] = 'NG002004'
bay_shp.loc[bay_shp['adm2_name'] == 'Gombi', 'adm2_pcode'] = 'NG002005'

# Load CSV files
evi_df = pd.read_csv(EVI_PATH)
clusters_df = pd.read_csv(CLUSTERS_PATH)
risk_df = pd.read_csv(RISK_PATH)

# Merge datasets
merged_df = pd.merge(evi_df, clusters_df[['pcode', 'cluster_label']], on='pcode', how='left')
merged_df = pd.merge(merged_df, risk_df[['pcode', 'disruption_probability', 'disruption_risk_label']], on='pcode', how='left')

# Calculate mismatch ratio: population pressure / (school density + epsilon)
merged_df['mismatch_ratio'] = merged_df['population_pressure'] / (merged_df['school_density'].replace(0, np.nan).fillna(0.01))

# Merge merged data into shapefile
bay_gdf = bay_shp.merge(merged_df, left_on='adm2_pcode', right_on='pcode', how='inner')

# Convert datetime/timestamp columns to strings to prevent JSON serialization errors in folium
for col in bay_gdf.columns:
    if col != 'geometry':
        if 'datetime' in str(bay_gdf[col].dtype) or col in ['valid_on', 'valid_to']:
            bay_gdf[col] = bay_gdf[col].astype(str)

# Check shapefile length
print(f"Merged shapefile length: {len(bay_gdf)}")

# Define map helper function
def create_base_map():
    # Centered around BAY states
    return folium.Map(location=[11.5, 13.0], zoom_start=7, tiles="cartodbpositron")

print("2. Generating EVI Map...")
evi_map = create_base_map()
# Create colormap for EVI
evi_cmap = LinearColormap(['#ffeda0', '#feb24c', '#f03b20'], vmin=0, vmax=1, caption="Education Vulnerability Index (EVI)")
evi_cmap.add_to(evi_map)

# Style function
def style_evi(feature):
    val = feature['properties'].get('evi_score', 0)
    return {
        'fillColor': evi_cmap(val),
        'color': '#434343',
        'weight': 0.8,
        'fillOpacity': 0.75
    }

# Highlight function
def highlight_style(feature):
    return {
        'weight': 2.0,
        'color': '#ffffff',
        'fillOpacity': 0.9
    }

# Create GeoJson layer
folium.GeoJson(
    bay_gdf,
    style_function=style_evi,
    highlight_function=highlight_style,
    tooltip=folium.GeoJsonTooltip(
        fields=['adm1_name', 'adm2_name', 'evi_score', 'rank'],
        aliases=['State:', 'LGA:', 'EVI Score:', 'Vulnerability Rank:'],
        localize=True,
        sticky=False,
        labels=True,
        style="""
            background-color: #F0EFEF;
            border: 1px solid #BCBCBC;
            border-radius: 4px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            font-family: sans-serif;
            font-size: 13px;
            padding: 8px;
        """
    ),
    popup=folium.GeoJsonPopup(
        fields=['adm1_name', 'adm2_name', 'evi_score', 'rank', 'conflict_intensity', 'school_age_total', 'school_density', 'cluster_label'],
        aliases=['State', 'LGA', 'EVI Score', 'Vulnerability Rank', 'Conflict Intensity', 'School-Age Children', 'Schools per 1k Kids', 'Cluster Type'],
        localize=True,
        labels=True,
        style="font-family: sans-serif; font-size: 12px; width: 220px;"
    )
).add_to(evi_map)

evi_map.save(os.path.join(DOCS_DIR, "evi_map.html"))


print("3. Generating Cluster Map...")
cluster_map = create_base_map()

# Map cluster labels to distinct hexadecimal colors
cluster_colors = {
    "Emergency": "#d9534f",          # soft red
    "Expansion": "#f0ad4e",          # soft orange
    "Infrastructure gap": "#5bc0de", # soft cyan/blue
    "Relatively stable": "#5cb85c"   # soft green
}

def style_cluster(feature):
    lbl = feature['properties'].get('cluster_label', 'Infrastructure gap')
    return {
        'fillColor': cluster_colors.get(lbl, '#777777'),
        'color': '#434343',
        'weight': 0.8,
        'fillOpacity': 0.75
    }

# Create custom legend for clusters in HTML
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 180px; height: 130px; 
     border:2px solid grey; z-index:9999; font-size:12px;
     background-color:white; opacity: 0.85; padding: 10px;
     border-radius: 5px; font-family: sans-serif;">
     <b>LGA Cluster Risk Profiles</b><br>
     <i style="background:#d9534f; width:12px; height:12px; float:left; margin-right:8px; border-radius: 2px;"></i> Emergency<br>
     <i style="background:#f0ad4e; width:12px; height:12px; float:left; margin-right:8px; border-radius: 2px;"></i> Expansion<br>
     <i style="background:#5bc0de; width:12px; height:12px; float:left; margin-right:8px; border-radius: 2px;"></i> Infrastructure gap<br>
     <i style="background:#5cb85c; width:12px; height:12px; float:left; margin-right:8px; border-radius: 2px;"></i> Relatively stable<br>
     </div>
     '''
cluster_map.get_root().html.add_child(folium.Element(legend_html))

folium.GeoJson(
    bay_gdf,
    style_function=style_cluster,
    highlight_function=highlight_style,
    tooltip=folium.GeoJsonTooltip(
        fields=['adm1_name', 'adm2_name', 'cluster_label'],
        aliases=['State:', 'LGA:', 'Risk Profile:'],
        localize=True,
        sticky=False,
        labels=True,
        style="background-color: #F0EFEF; border: 1px solid #BCBCBC; border-radius: 4px; font-family: sans-serif; font-size: 13px; padding: 8px;"
    ),
    popup=folium.GeoJsonPopup(
        fields=['adm1_name', 'adm2_name', 'cluster_label', 'evi_score', 'conflict_intensity', 'school_age_total', 'school_density'],
        aliases=['State', 'LGA', 'Risk Profile', 'EVI Score', 'Conflict Intensity', 'School-Age Children', 'Schools per 1k Kids'],
        localize=True,
        labels=True,
        style="font-family: sans-serif; font-size: 12px; width: 220px;"
    )
).add_to(cluster_map)

cluster_map.save(os.path.join(DOCS_DIR, "cluster_map.html"))


print("4. Generating Mismatch Map...")
mismatch_map = create_base_map()

# Map mismatch values: we scale mismatch_ratio using quantiles or logs
m_min = bay_gdf['mismatch_ratio'].min()
m_max = bay_gdf['mismatch_ratio'].max()
print(f"Mismatch ratio range: {m_min:.2f} to {m_max:.2f}")

# Define color map for mismatch
# PuRd (Purple-Red) or RdPu
mismatch_cmap = LinearColormap(['#f7f7f7', '#d7b5d8', '#df65b0', '#980043'], 
                               vmin=m_min, vmax=m_max/4.0, # capped at 25% of max to show variations better (due to outliers)
                               caption="Infrastructure Mismatch Ratio (Population / School Density)")
mismatch_cmap.add_to(mismatch_map)

def style_mismatch(feature):
    val = feature['properties'].get('mismatch_ratio', 0)
    return {
        'fillColor': mismatch_cmap(val),
        'color': '#434343',
        'weight': 0.8,
        'fillOpacity': 0.75
    }

folium.GeoJson(
    bay_gdf,
    style_function=style_mismatch,
    highlight_function=highlight_style,
    tooltip=folium.GeoJsonTooltip(
        fields=['adm1_name', 'adm2_name', 'mismatch_ratio'],
        aliases=['State:', 'LGA:', 'Mismatch Ratio:'],
        localize=True,
        sticky=False,
        labels=True,
        style="background-color: #F0EFEF; border: 1px solid #BCBCBC; border-radius: 4px; font-family: sans-serif; font-size: 13px; padding: 8px;"
    ),
    popup=folium.GeoJsonPopup(
        fields=['adm1_name', 'adm2_name', 'mismatch_ratio', 'school_age_total', 'school_count', 'school_density'],
        aliases=['State', 'LGA', 'Mismatch Ratio', 'School-Age Children', 'School Count', 'Schools per 1k Kids'],
        localize=True,
        labels=True,
        style="font-family: sans-serif; font-size: 12px; width: 220px;"
    )
).add_to(mismatch_map)

mismatch_map.save(os.path.join(DOCS_DIR, "mismatch_map.html"))

print("Visualization maps created successfully!")
