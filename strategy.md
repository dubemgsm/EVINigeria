# Education Bridge Initiative (EBI): Prioritisation Strategy

## Key Findings
Our data-driven spatial analysis has identified the top 10 most vulnerable Local Government Areas (LGAs) in Northeast Nigeria for targeted intervention:
1. **Maiduguri** (Borno)
2. **Gwoza** (Borno)
3. **Jere** (Borno)
4. **Bama** (Borno)
5. **Konduga** (Borno)
6. **Potiskum** (Yobe)
7. **Ngala** (Borno)
8. **Fune** (Yobe)
9. **Damboa** (Borno)
10. **Biu** (Borno)

- **Borno & Northern Concentration:** Critical education vulnerability is heavily concentrated in northern and conflict-exposed areas, with 8 of the top 10 priority LGAs located in Borno State.
- **Infrastructure Mismatch Insights:** The analysis reveals extreme mismatches between population demand and school coverage. In major urban centers (e.g. Maiduguri and Jere), high population density severely overburdens existing infrastructure. Even in areas with lower conflict intensity, structural access constraints remain severe due to extremely low school density.

---

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

### Key Findings
The analysis reveals that:
- The top 10 most vulnerable LGAs are characterised by a combination of:
  - high conflict intensity
  - large school-age populations
  - low school density
- A majority of these LGAs fall into the “Emergency Zone” cluster, indicating simultaneous pressure from insecurity and insufficient education infrastructure.
- Several LGAs show extreme mismatch between population and school coverage, suggesting that even in areas with lower conflict intensity, access constraints remain severe.

### Geographic Pattern
- Vulnerability is spatially concentrated, not evenly distributed.
- Northern and conflict-exposed LGAs show:
  - significantly higher disruption risk probabilities
  - lower availability of functioning schools
- This clustering of vulnerability indicates that targeted interventions in a small number of LGAs could generate disproportionately high impact.

### Implications for EBI
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

### Decision Insight
Rather than distributing resources evenly, EBI should prioritise the top-ranked LGAs identified by the EVI, where:
- education disruption risk is highest
- infrastructure gaps are most severe
- population demand is most concentrated

This targeted approach ensures that limited resources are deployed where they will have the greatest impact.

---

## Model Insights and Limitations

### Which Variables Most Influence EVI?
Our statistical indexing and predictive machine learning models show that:
- **Conflict Intensity (40% index weight / 53.8% feature importance):</strong> Measured by log-scaled fatalities and conflict recency. This is the single most dominant factor driving immediate risk of education disruption.
- **School-Age Population Pressure (40% index weight / 19.5% feature importance):</strong> Measures demographic pressure. It represents the potential demand in an LGA, exposing structural mismatches when school infrastructure is absent or overstrained.
- **School Access Density (20% index weight / 18.8% feature importance):</strong> Standardized school density per 1,000 children. Lower density strongly correlates with higher vulnerability scores.

### Data Limitations
To maintain a decision-ready yet realistic stance, the index acknowledges the following limitations:
- **Temporal Resolution of Infrastructure:** The school dataset (GRID3/iMMAP) offers a static census snapshot. It may not reflect real-time physical damage or community-led temporary reopenings.
- **IDP Displacement Dynamics:** Demographics are projected from UN OCHA/GRID3 SADD surveys. Sudden security events can cause rapid, localized migrations of internally displaced persons (IDPs) that outpace census updates.
- **Reporting Gaps:** ACLED conflict data, while updated weekly, is subject to reporting constraints or telecommunication outages in remote, high-risk areas.

---

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
