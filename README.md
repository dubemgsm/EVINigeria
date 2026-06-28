# Education Vulnerability Index (EVI) Dashboard: Borno, Adamawa, and Yobe (BAY) States

An interactive data science and spatial analysis platform that maps school-level vulnerability, resource distribution, and predictive disruption risks across **65 Local Government Areas (LGAs)** in Borno, Adamawa, and Yobe (BAY) States, Northeast Nigeria.

The complete dashboard and interactive Leaflet maps are hosted publicly at:  
👉 **[https://dubemgsm.github.io/EVINigeria/](https://dubemgsm.github.io/EVINigeria/)**

---

## 💡 Quick Links & Key Results

### 🔗 Quick Links
- 📊 **[Interactive Dashboard (Live)](https://dubemgsm.github.io/EVINigeria/)** — Main interface showing statistical summary cards and interactive GIS maps. (Alternative: [Local Source](docs/index.html))
- 📋 **[Priority Decision Page (Live)](https://dubemgsm.github.io/EVINigeria/priority.html)** — Differentiated recommended actions and statistics for the Top 10 priority LGAs. (Alternative: [Local Source](docs/priority.html))
- 📈 **[Prioritisation Strategy (Live)](https://dubemgsm.github.io/EVINigeria/strategy.html)** — Deep dive into EVI formulation, machine learning clustering, and key results. (Alternative: [Local Source](docs/strategy.html))
- 📂 **[Top 10 Priority LGAs Dataset (priority_lgas.csv)](priority_lgas.csv)** — The exported decision-ready CSV data file.

### 🔑 Key Result Summary
#### **Where should EBI act first?**
EBI should focus immediate intervention resources on the **Top 10 Priority LGAs** identified by the EVI, with the highest concentration in **Borno State** (8 of the top 10):
1. **Maiduguri** (Borno) — *Action: Increase classroom capacity*
2. **Gwoza** (Borno) — *Action: Temporary learning centres + emergency response*
3. **Jere** (Borno) — *Action: Increase classroom capacity*
4. **Bama** (Borno) — *Action: Temporary learning centres + emergency response*
5. **Konduga** (Borno) — *Action: Temporary learning centres + emergency response*
6. **Potiskum** (Yobe) — *Action: Increase classroom capacity*
7. **Ngala** (Borno) — *Action: Build new schools*
8. **Fune** (Yobe) — *Action: Increase classroom capacity*
9. **Damboa** (Borno) — *Action: Temporary learning centres + emergency response*
10. **Biu** (Borno) — *Action: Increase classroom capacity*

#### **Why?**
These areas suffer from the most extreme combinations of **high conflict intensity**, **large school-age populations**, and **low school density**. This targeted, differentiated approach ensures resources are deployed where they will generate the highest programmatic impact.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Data Sources](#data-sources)
3. [Methodology](#methodology)
   - [Feature Engineering](#1-feature-engineering)
   - [Education Vulnerability Index (EVI) Formulation](#2-education-vulnerability-index-evi-formulation)
   - [K-Means Profile Clustering](#3-k-means-profile-clustering)
   - [Predictive Disruption Risk Model](#4-predictive-disruption-risk-model)
4. [Key Findings & Intervention Strategy](#key-findings--intervention-strategy)
5. [Interactive Visualizations](#interactive-visualizations)
6. [Pipeline Architecture & How to Rerun](#pipeline-architecture--how-to-rerun)
7. [Deployment & CI/CD](#deployment--cicd)

---

## Project Overview

Northeast Nigeria has been significantly affected by prolonged humanitarian challenges, leading to major disruptions in school infrastructure, student displacement, and teacher shortages. 

This project implements a reproducible Python data pipeline to clean, integrate, and analyze spatial and demographic data. It calculates a standardized **Education Vulnerability Index (EVI)**, clusters LGAs based on operational profiles, and trains a predictive model to classify future disruption risks. The final interactive web dashboard provides decision-makers with actionable, localized insights to optimize funding, security resources, and school construction.

---

## Data Sources

All input data was manually downloaded from the following providers and uploaded into the `data/raw/` directory:

1. **Boundaries (GIS Shapefile)**: Downloaded from the **UN OCHA Common Operational Datasets (COD)** (`data/raw/nga_shp/nga_admin2.shp`)
   - Official spatial geometries at administrative level 2 (LGAs) for Nigeria. Standardized to `EPSG:4326` (WGS84) and clipped to the BAY states (65 LGAs). Projected to UTM Zone 32N (`EPSG:32632`) for planar metric distance calculations.
2. **Conflict Events**: Downloaded from the **Armed Conflict Location & Event Data Project (ACLED)** (`data/raw/acled_conflict.csv`)
   - Detailed spatial event logging of conflict incidents, including geographic coordinates, dates, and recorded fatalities.
3. **Schools Status**: Downloaded from **GRID3 / iMMAP Nigeria** (`data/raw/schools.csv`)
   - GPS locations of schools, classification categories, and operational layers.
4. **Demographics (SADD)**: Downloaded from the **UN OCHA / GRID3 Sex and Age Disaggregated Data** (`data/raw/population.csv`)
   - Population breakdowns at the LGA level, specifically isolating school-aged children.

---

## Methodology

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌────────────────┐
│ ACLED        │     │ Population   │     │ School Locs  │     │ Admin Boundary │
│ Conflict     │     │ Demographic  │     │ Database     │     │ Shapefile      │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘     └────────┬───────┘
       │                    │                    │                      │
       ▼                    ▼                    ▼                      ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                           Feature Engineering Pipeline                        │
├───────────────────────────────────────────────────────────────────────────────┤
│  • Recency/Fatality Weighted Conflict Intensity                               │
│  • Planar Euclidean distance to nearest schools/conflicts (UTM 32N)          │
│  • School Density per 1,000 children & Population Pressure                    │
└──────────────────────┬────────────────────────────────────────────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                           Statistical Engine & ML                             │
├───────────────────────────────────────────────────────────────────────────────┤
│  • Standardized Education Vulnerability Index (EVI) Calculation               │
│  • Unsupervised KMeans Clustering (4 Risk Profiles)                           │
│  • Predictive Disruption Risk Classifier (Random Forest)                      │
└──────────────────────┬────────────────────────────────────────────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                           Visualization & Deployment                          │
├───────────────────────────────────────────────────────────────────────────────┤
│  • Folium Interactive Leaflet Maps (EVI, Clusters, Infrastructure Mismatch)    │
│  • Compilation of Main HTML Switcher and Priority Dashboard (Jinja template)  │
│  • Automatic Push & Deploy to GitHub Pages via Actions                        │
└───────────────────────────────────────────────────────────────────────────────┘
```

### 1. Feature Engineering
The pipeline constructs several complex metrics at the LGA level:
* **Conflict Intensity**: Computed by weighting conflict events according to:
  - **Recency**: A time-decay weighting using a 5-year half-life ($\lambda \approx 0.1386$) relative to the latest record in the dataset.
  - **Fatalities**: Log-scaled using $1 + \ln(1 + \text{fatalities})$ to prevent extreme outlier events from skewing the metrics.
* **Spatial Proximities**: Planar distance measurements in meters computed from the LGA centroid to the nearest conflict event and school locations.
* **School Density**: Calculated as the number of schools per 1,000 school-aged children.
* **Population Pressure**: Total school-age population per LGA.

### 2. Education Vulnerability Index (EVI) Formulation
Each calculated feature is normalized to a $[0, 1]$ scale via MinMax scaling. The raw EVI is computed as:

$$\text{EVI}_{\text{raw}} = (0.4 \times \text{Conflict Intensity}) + (0.4 \times \text{Population Pressure}) - (0.2 \times \text{School Density})$$

The raw index is then normalized to $[0, 1]$ to yield the final **EVI Score**, where **1.0** indicates maximum vulnerability and **0.0** indicates minimum vulnerability. LGAs are ranked from 1 to 65.

### 3. K-Means Profile Clustering
Unsupervised K-Means clustering ($k = 4$) is applied to group the LGAs into distinct risk profiles:
* **Emergency**: High conflict intensity and severe educational disruption.
* **Expansion**: Extreme school-age population pressure with lagging infrastructure.
* **Relatively stable**: Low conflict and high school density.
* **Infrastructure gap**: Low conflict, but critically low school density/access.

### 4. Predictive Disruption Risk Model
A Random Forest Classifier is trained to identify LGAs at risk of future educational disruption.
* **Target Variable (Proxy)**: A binary indicator set to 1 if an LGA lies above the median for conflict intensity or EVI score.
* **Features**: Conflict Intensity, Population Pressure, School Density, and Proximity to Conflict.
* **Hyperparameters**: 150 estimators, max depth of 4 (limited to prevent overfitting on the 65 LGA samples).

---

## Key Findings & Intervention Strategy

The Education Vulnerability Index (EVI) identifies a clear concentration of high-priority LGAs in Northeast Nigeria, particularly in northern Borno State.

### Key Findings
The analysis reveals that:
- **The top 10 most vulnerable LGAs** are characterised by a combination of high conflict intensity, large school-age populations, and low school density.
- A majority of these LGAs fall into the **“Emergency Zone”** cluster, indicating simultaneous pressure from insecurity and insufficient education infrastructure.
- Several LGAs show **extreme mismatch** between population and school coverage, suggesting that even in areas with lower conflict intensity, access constraints remain severe.

### Geographic Pattern
- Vulnerability is **spatially concentrated**, not evenly distributed.
- Northern and conflict-exposed LGAs show:
  - significantly higher disruption risk probabilities
  - lower availability of functioning schools
- This clustering of vulnerability indicates that targeted interventions in a small number of LGAs could generate disproportionately high impact.

### Implications for EBI
The findings suggest the need for differentiated intervention strategies:
1. **Emergency Zones (Highest Priority)**
   - Immediate deployment of temporary learning centres and mobile education units.
   - Focus on restoring minimum access in high-risk areas.
2. **Expansion Zones**
   - Rapid scaling of classroom capacity and teacher deployment.
   - Address overburdened existing infrastructure.
3. **Infrastructure Gap Areas**
   - Long-term investment in new school construction and rehabilitation of dormant facilities.

### Decision Insight
Rather than distributing resources evenly, EBI should prioritise the top-ranked LGAs identified by the EVI, where education disruption risk is highest, infrastructure gaps are most severe, and population demand is most concentrated. This targeted approach ensures that limited resources are deployed where they will have the greatest impact.

---

## Interactive Visualizations

The generated dashboard includes several dedicated interactive GIS visualizers:
* **EVI Score Map**: Choropleth visualization showing the gradient of vulnerability scores across all LGAs.
* **Cluster Profile Map**: Color-coded clusters illustrating spatial patterns of the 4 K-Means operational categories.
* **Infrastructure Mismatch Map**: Highlights the discrepancy between high population pressure and low school density to point out exact locations where school construction is most needed.
* **Interactive Switcher & Priority Matrix**: Main interface displaying ranked prioritizations of LGAs paired with a search and switcher framework for maps.

---

## Pipeline Architecture & How to Rerun

### Prerequisites & Installation
Ensure you have Python 3.8+ installed. You can install all required dependencies (including geospatial libraries) using `pip`:

```bash
pip install pandas geopandas numpy shapely scikit-learn folium branca
```

> **Note**: For Linux environments, ensure that system-level libraries for Geospatial Data (such as `libgdal-dev` or `proj-bin`) are available.

### Rerun the Complete Pipeline
To execute all cleaning, feature engineering, modeling, and dashboard generation steps in sequence, run the parent script from the project root:

```bash
python update_pipeline.py
```

### Script Execution Sequence
If you wish to run steps manually, execute them in this order:
1. `python scripts/clean_data.py`: Loads raw CSVs/Shapefile, resolves name mismatches, handles nulls, and saves processed subsets.
2. `python scripts/build_evi.py`: Performs coordinate projections, nearest distance lookups, and EVI score calculations.
3. `python scripts/clustering.py`: Standardizes variables and performs K-Means clustering.
4. `python scripts/prediction.py`: Trains the Random Forest classifier and outputs risk probability scores.
5. `python scripts/visualize.py`: Generates the HTML Leaflet map files using `folium`.
6. `python scripts/generate_dashboard.py`: Compiles the main layout dashboard and tables.

---

## Deployment & CI/CD

This repository is equipped with a GitHub Actions workflow:
- **Config file**: `.github/workflows/static.yml`
- **Execution**: Runs automatically on pushes to the `main` branch.
- **Action**: Packages the static files compiled in the `/docs` directory, uploads them, and deploys them to GitHub Pages.
- **Permissions**: Configured with explicit `pages: write` and `id-token: write` scopes to handle deployment securely.