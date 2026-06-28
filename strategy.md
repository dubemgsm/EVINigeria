# Education Bridge Initiative (EBI): Prioritisation Strategy

## 1. Context
The Education Bridge Initiative (EBI) operates in conflict-affected regions where education access is highly uneven and rapidly changing. While field teams possess strong contextual knowledge, the organisation’s current planning approach relies on fragmented and unevenly available information. As a result, EBI lacks a systematic, data-driven mechanism to prioritise interventions across regions, particularly when conflict dynamics shift quickly.

This proposal addresses that gap by introducing a scalable, data-driven prioritisation framework that complements field knowledge with geospatial and predictive analytics.

---

## 2. Objectives
The project aims to:
- **Develop an Education Vulnerability Index (EVI)** to identify areas with the greatest unmet education needs.
- **Classify regions into risk profiles** to support differentiated intervention strategies.
- **Predict future education disruption risks** using historical and real-time data.
- **Deliver an interactive decision-support tool** usable by non-technical staff.
- **Enable rapid updates** as new data becomes available.

---

## 3. Approach
The proposed approach integrates geospatial analysis, statistical modelling, and machine learning into a unified prioritisation system.

### 3.1 Data Integration
The model combines three core datasets:
- **Conflict event data** (intensity, frequency, recency)
- **Population distribution**, with a focus on school-age children
- **School infrastructure data**

These datasets are harmonised at the Local Government Area (LGA) level to enable consistent analysis.

### 3.2 Education Vulnerability Index (EVI)
An index is constructed to quantify education vulnerability:

$$\text{EVI} = \text{Conflict Intensity} + \text{Population Pressure} - \text{School Access}$$

All components are normalised and weighted to produce a comparable score across LGAs. The EVI allows EBI to:
- Rank areas by urgency.
- Identify mismatches between population and school infrastructure.
- Allocate resources more effectively.

Analysis shows that conflict intensity and population pressure are the strongest contributors to vulnerability, while school density reduces risk where adequate infrastructure exists.

The consistency of results across multiple indicators confirms the robustness of the prioritisation approach.

### 3.3 Risk Profiling (Clustering)
Using unsupervised machine learning (K-Means clustering), LGAs are grouped into distinct risk categories:
- **Emergency zones**: high conflict, low access.
- **Expansion zones**: high population pressure, moderate access.
- **Infrastructure gaps**: low conflict but insufficient schools.
- **Stable areas**: relatively balanced conditions.

This classification enables tailored programmatic responses.

### 3.4 Predictive Modelling
A predictive model is developed to estimate the probability of education disruption in each LGA. The model uses:
- Conflict trends over time.
- Population density.
- School access indicators.

Outputs are expressed as probabilities, allowing EBI to anticipate emerging hotspots rather than reacting to crises after they occur.

Additionally, temporal modeling correlates conflict events with religious calendars and national events to isolate seasonal and holiday conflict spikes.

### 3.5 Decision-Support Tool
All outputs are integrated into an interactive dashboard, including:
- EVI maps
- Risk classification maps
- Priority ranking tables

These tools are designed for usability by non-technical staff and can directly inform planning and resource allocation decisions.

### 3.6 Automation and Scalability
The system includes an automated pipeline that updates outputs as new data becomes available. The methodology relies exclusively on open data and modular code, ensuring it can be:
- Applied to other countries.
- Adapted to varying data availability.
- Updated without rebuilding the system.

---

## 4. Top Priority Areas for Education Intervention
The Education Vulnerability Index (EVI) identifies a clear concentration of high-priority LGAs in Northeast Nigeria, particularly in northern Borno State.

### 4.1 Geographic Pattern
- Vulnerability is spatially concentrated, not evenly distributed.
- Northern and conflict-exposed LGAs show:
  - significantly higher disruption risk probabilities
  - lower availability of functioning schools
- This clustering of vulnerability indicates that targeted interventions in a small number of LGAs could generate disproportionately high impact.

### 4.2 Implications for EBI
The findings suggest the need for differentiated intervention strategies:
1. **Emergency Zones (Highest Priority)**
   - Immediate deployment of:
     - temporary learning centres
     - mobile education units
   - Focus on restoring minimum access in high-risk areas
2. **Expansion Zones**
   - Rapid scaling of:
     - classroom capacity
     - teacher deployment
   - Address overburdened existing infrastructure
3. **Infrastructure Gap Areas**
   - Long-term investment in:
     - new school construction
     - rehabilitation of dormant facilities

### 4.3 Decision Insight
Rather than distributing resources evenly, EBI should prioritise the top-ranked LGAs identified by the EVI, where:
- education disruption risk is highest
- infrastructure gaps are most severe
- population demand is most concentrated

This targeted approach ensures that limited resources are deployed where they will have the greatest impact.



## 5. Proposed Activities
1. Data acquisition and validation.
2. Data cleaning and geospatial alignment.
3. Feature engineering and indicator construction.
4. Index development and validation.
5. Clustering and predictive modelling.
6. Dashboard and visualization development.
7. Automation pipeline creation.

---

## 6. Deliverables
- **Education Vulnerability Index dataset** (LGA level)
- **Risk classification model and outputs**
- **Predictive model for disruption risk**
- **Interactive geospatial dashboard** (deployed via GitHub Pages)
- **Top-priority LGA ranking** for intervention
- **Open-source repository** with full data and methodology

---

## 7. Operational Security and Seasonality

Security analysis of conflict events in Nigeria from 2011 to date indicates clear seasonal and holiday-related surges in violence. EBI operations should adjust activity levels accordingly:

- **Holiday Activity Reduction:** Conflict incidents rise by 14.4% during holidays and religious periods (Ramadan, Easter, and fixed national holidays), with fatalities increasing by 15.9% in the 7 days before and after these periods. Field teams should plan for skeletal operations during these windows.
- **Dry Season Caution (January – April):** Improved ground mobility during the dry season triggers a surge in offensive operations, peaking in February with an average of 12.8 fatalities/day. High-exposure field activities should be minimized.
- **Rainy Season Window (June – October):** Heavy rains and flooded roads decrease overall conflict frequency, creating safer operational windows for facility rehabilitation and team development.

---

## 8. Scalability

This approach requires only three inputs:
- conflict data
- population data
- school location data

These datasets are globally available, allowing the model to be applied across other EBI operational contexts without redesign.

### How to Replicate for a New Location
EBI analysts can adapt this modeling framework to any new operational context by following these steps:
1. **Gather Data**: Obtain boundary shapefiles/GeoJSON, conflict coordinates (e.g., ACLED), population stats, and school coordinates for your new location.
2. **Replace Raw Files**: Place these datasets inside the `data/raw/` folder of the repository.
3. **Update clean_data.py**: Open `scripts/clean_data.py` and update the file paths and column mappings to match the names of your new administrative units.
4. **Rerun Pipeline**: Execute `python update_pipeline.py` in the terminal. The distance calculators, index engine, and map generators will dynamically rebuild the entire dashboard around your new region.

---

## Model Insights and Limitations

- Conflict intensity is the strongest predictor of disruption risk
- School density reduces vulnerability where sufficient infrastructure exists
- School data may be incomplete in remote areas
- Conflict data may underreport events
- Population data is based on estimates

---

This system enables EBI to move from reactive response to proactive, data-driven planning.
