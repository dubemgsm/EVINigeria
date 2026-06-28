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

## 4. Proposed Activities
1. Data acquisition and validation.
2. Data cleaning and geospatial alignment.
3. Feature engineering and indicator construction.
4. Index development and validation.
5. Clustering and predictive modelling.
6. Dashboard and visualization development.
7. Automation pipeline creation.

---

## 5. Deliverables
- **Education Vulnerability Index dataset** (LGA level)
- **Risk classification model and outputs**
- **Predictive model for disruption risk**
- **Interactive geospatial dashboard** (deployed via GitHub Pages)
- **Top-priority LGA ranking** for intervention
- **Open-source repository** with full data and methodology
