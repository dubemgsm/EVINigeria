import os
import pandas as pd

# File paths
EVI_PATH = "data/processed/evi_scores.csv"
CLUSTERS_PATH = "data/processed/clusters.csv"
RISK_PATH = "data/processed/disruption_risk.csv"
DOCS_DIR = "docs"

print("1. Loading processed data for dashboard generation...")
evi_df = pd.read_csv(EVI_PATH)
clusters_df = pd.read_csv(CLUSTERS_PATH)
risk_df = pd.read_csv(RISK_PATH)

# Merge datasets for dashboard
merged_df = pd.merge(evi_df, clusters_df[['pcode', 'cluster_label']], on='pcode', how='left')
merged_df = pd.merge(merged_df, risk_df[['pcode', 'disruption_probability', 'disruption_risk_label']], on='pcode', how='left')

# Calculate high-level statistics
total_school_age_pop = int(merged_df['school_age_total'].sum())
total_schools = int(merged_df['school_count'].sum())
total_conflicts = int(merged_df['conflict_intensity'].sum()) # let's count raw events instead if we want, or use intensity
# Let's load conflict_by_lga.csv to get raw counts
conflict_lga = pd.read_csv("data/processed/conflict_by_lga.csv")
total_conflict_events = int(conflict_lga['conflict_count'].sum())
total_conflict_fatalities = int(conflict_lga['fatalities'].sum())

# Most vulnerable LGA (Rank 1)
most_vulnerable_row = merged_df.sort_values(by='rank').iloc[0]
most_vulnerable_lga = f"{most_vulnerable_row['lga']} ({most_vulnerable_row['state']})"

print(f"Stats - Pop: {total_school_age_pop}, Schools: {total_schools}, Conflicts: {total_conflict_events}, Fatalities: {total_conflict_fatalities}")

# Generate Top 10 Priority LGAs Table Rows HTML
top_10 = merged_df.sort_values(by='rank').head(10)
table_rows_html = ""
for idx, row in top_10.iterrows():
    # Style cluster label badge
    badge_colors = {
        "Emergency": "background-color: #fce8e6; color: #a82e2e; border: 1px solid #f5c2c2;",
        "Expansion": "background-color: #fef3e6; color: #b26a15; border: 1px solid #fcdbb5;",
        "Infrastructure gap": "background-color: #eaf6fa; color: #1e7085; border: 1px solid #c7ebf3;",
        "Relatively stable": "background-color: #edf7ed; color: #2e7d32; border: 1px solid #c3e6cb;"
    }
    badge_style = badge_colors.get(row['cluster_label'], "background-color: #e0e0e0; color: #333;")
    
    table_rows_html += f"""
    <tr>
        <td style="font-weight: bold; text-align: center; color: #1a1a1a;">#{row['rank']}</td>
        <td style="font-weight: 600; color: #111;">{row['lga']}</td>
        <td>{row['state']}</td>
        <td style="font-family: monospace; font-weight: bold; color: #3b82f6;">{row['evi_score']:.4f}</td>
        <td><span style="padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold; {badge_style}">{row['cluster_label']}</span></td>
        <td style="font-family: monospace; font-weight: 600; color: {'#ef4444' if row['disruption_probability'] >= 0.7 else '#f59e0b' if row['disruption_probability'] >= 0.4 else '#10b981'};">{row['disruption_probability']*100:.1f}%</td>
    </tr>
    """

# 2. Write docs/index.html (Dashboard)
index_html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Education Vulnerability Dashboard (BAY States)</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --primary: #3b82f6;
            --primary-grad: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            --accent: #ef4444;
            --accent-grad: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%);
            --border: #e2e8f0;
        }}
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            line-height: 1.5;
            padding: 0;
        }}
        
        .header {{
            background: var(--primary-grad);
            color: #ffffff;
            padding: 40px 5%;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }}
        
        .header h1 {{
            font-size: 28px;
            font-weight: 800;
            letter-spacing: -0.5px;
        }}
        
        .header p {{
            font-size: 14px;
            opacity: 0.85;
            margin-top: 5px;
        }}
        
        .nav-links {{
            display: flex;
            gap: 15px;
        }}
        
        .nav-button {{
            background-color: rgba(255,255,255,0.15);
            color: #ffffff;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 14px;
            transition: all 0.2s ease;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        
        .nav-button:hover {{
            background-color: #ffffff;
            color: var(--primary);
            transform: translateY(-2px);
        }}
        
        .nav-button.active {{
            background-color: #ffffff;
            color: var(--primary);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .container {{
            max-width: 1400px;
            margin: 40px auto;
            padding: 0 20px;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 25px;
        }}
        
        /* KPI Cards */
        .kpi-card {{
            background: var(--card-bg);
            border-radius: 16px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.02);
            border: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: transform 0.2s ease;
        }}
        
        .kpi-card:hover {{
            transform: translateY(-4px);
        }}
        
        .kpi-label {{
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            color: var(--text-muted);
            letter-spacing: 0.5px;
        }}
        
        .kpi-value {{
            font-size: 28px;
            font-weight: 800;
            margin-top: 10px;
            color: var(--text-main);
            letter-spacing: -0.5px;
        }}
        
        .kpi-subtext {{
            font-size: 12px;
            color: var(--text-muted);
            margin-top: 10px;
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        
        /* Layout Grid Sections */
        .full-width {{
            grid-column: span 4;
        }}
        
        .split-left {{
            grid-column: span 3;
        }}
        
        .split-right {{
            grid-column: span 1;
        }}
        
        @media (max-width: 1024px) {{
            .split-left, .split-right, .kpi-card {{
                grid-column: span 4;
            }}
        }}
        
        .card {{
            background: var(--card-bg);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.02);
            border: 1px solid var(--border);
            margin-bottom: 25px;
        }}
        
        .card h2 {{
            font-size: 20px;
            font-weight: 800;
            margin-bottom: 20px;
            color: var(--text-main);
            border-left: 4px solid var(--primary);
            padding-left: 12px;
            letter-spacing: -0.5px;
        }}
        
        /* Styled Table */
        .table-container {{
            width: 100%;
            overflow-x: auto;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 14px;
        }}
        
        th {{
            background-color: #f1f5f9;
            color: var(--text-muted);
            font-weight: 700;
            padding: 14px 18px;
            text-transform: uppercase;
            font-size: 11px;
            letter-spacing: 0.5px;
            border-bottom: 2px solid var(--border);
        }}
        
        td {{
            padding: 14px 18px;
            border-bottom: 1px solid var(--border);
            color: var(--text-muted);
        }}
        
        tr:hover td {{
            background-color: #f8fafc;
        }}
        
        /* Sidebar/Methodology Details */
        .methodology-item {{
            margin-bottom: 15px;
            padding-bottom: 15px;
            border-bottom: 1px dashed var(--border);
        }}
        
        .methodology-item:last-child {{
            border-bottom: none;
        }}
        
        .methodology-title {{
            font-weight: bold;
            font-size: 13px;
            color: var(--text-main);
            margin-bottom: 5px;
        }}
        
        .methodology-desc {{
            font-size: 12px;
            color: var(--text-muted);
        }}
        
        .formula-box {{
            background-color: #f1f5f9;
            padding: 15px;
            border-radius: 8px;
            font-family: monospace;
            font-size: 11px;
            margin-top: 10px;
            border: 1px solid var(--border);
            overflow-x: auto;
            color: #0f172a;
        }}
        
        .footer {{
            text-align: center;
            padding: 40px;
            color: var(--text-muted);
            font-size: 12px;
            border-top: 1px solid var(--border);
            background-color: #ffffff;
            margin-top: 60px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>Education Vulnerability Dashboard</h1>
            <p>Borno, Adamawa, and Yobe (BAY) States, Nigeria • LGA Unit of Analysis</p>
        </div>
        <div class="nav-links">
            <a href="index.html" class="nav-button active">Dashboard</a>
            <a href="maps.html" class="nav-button">Interactive Maps</a>
            <a href="strategy.html" class="nav-button">Strategy</a>
        </div>
    </div>
    
    <div class="container">
        <!-- Summary & Actions Row -->
        <div class="card full-width" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px; background: linear-gradient(to right, #ffffff, #f8fafc); border-left: 5px solid var(--primary); margin-bottom: 25px;">
            <div style="flex: 1; min-width: 300px;">
                <p style="font-size: 16px; font-weight: 600; color: var(--text-main); margin-bottom: 5px;">
                    This project identifies the top 10 priority LGAs for education intervention using a data-driven Education Vulnerability Index.
                </p>
                <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 0;">
                    Explore the priority rankings, read our intervention strategy, or view GIS mapping layers. 
                    <a href="https://github.com/dubemgsm/EVINigeria" target="_blank" style="color: var(--primary); text-decoration: none; font-weight: bold; margin-left: 5px;">View GitHub Repository</a>
                </p>
            </div>
            <div style="display: flex; gap: 12px; flex-wrap: wrap;">
                <a href="maps.html" class="nav-button" style="background-color: var(--primary); color: #fff; border: none; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 14px;">View Map</a>
                <a href="#top-lgas" class="nav-button" style="background-color: #f1f5f9; color: var(--text-main); border: 1px solid var(--border); padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 14px;">View Top LGAs</a>
                <a href="strategy.html" class="nav-button" style="background-color: #f1f5f9; color: var(--text-main); border: 1px solid var(--border); padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 14px;">Read Strategy</a>
            </div>
        </div>

        <!-- Stats Row -->
        <div class="kpi-card">
            <div>
                <span class="kpi-label">School-Age Children</span>
                <div class="kpi-value">{total_school_age_pop:,}</div>
            </div>
            <div class="kpi-subtext">Total target population in BAY</div>
        </div>
        
        <div class="kpi-card">
            <div>
                <span class="kpi-label">Total Schools</span>
                <div class="kpi-value">{total_schools:,}</div>
            </div>
            <div class="kpi-subtext">Registered educational facilities</div>
        </div>
        
        <div class="kpi-card">
            <div>
                <span class="kpi-label">Conflict Incidents</span>
                <div class="kpi-value">{total_conflict_events:,}</div>
            </div>
            <div class="kpi-subtext">Fatalities: <span style="font-weight:bold; color:red;">{total_conflict_fatalities:,}</span></div>
        </div>
        
        <div class="kpi-card" style="border-left: 4px solid var(--accent);">
            <div>
                <span class="kpi-label">Highest Vulnerability LGA</span>
                <div class="kpi-value" style="font-size:22px; color:var(--accent); word-break: break-all;">{most_vulnerable_lga}</div>
            </div>
            <div class="kpi-subtext">Rank #1 on EVI Score</div>
        </div>
        
        <!-- Table & Sidebar Split Row -->
        <div class="card split-left" id="top-lgas">
            <h2>Top 10 Priority LGAs requiring Intervention</h2>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th style="width: 80px; text-align: center;">Rank</th>
                            <th>LGA</th>
                            <th>State</th>
                            <th>EVI Score</th>
                            <th>Risk Profile Cluster</th>
                            <th>Disruption Risk Prob.</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows_html}
                    </tbody>
                </table>
            </div>
        </div>
        
        <div class="card split-right">
            <h2>Index Construction</h2>
            <div style="font-size: 13px; color: var(--text-muted); margin-bottom: 20px;">
                The index identifies LGAs where conflict intensity and population pressure outstrip local school infrastructure.
            </div>
            
            <div class="methodology-item">
                <div class="methodology-title">Conflict Intensity (40%)</div>
                <div class="methodology-desc">Decay-weighted over time (5-year half-life) and log-scaled fatalities to manage incident anomalies.</div>
            </div>
            
            <div class="methodology-item">
                <div class="methodology-title">Population Pressure (40%)</div>
                <div class="methodology-desc">Total volume of school-age children (girls and boys) situated within the LGA.</div>
            </div>
            
            <div class="methodology-item">
                <div class="methodology-title">School Access Density (-20%)</div>
                <div class="methodology-desc">Standardized school density representing facilities available per 1,000 children.</div>
            </div>
            
            <div class="formula-box">
                EVI = 0.4*Conflict_norm + 0.4*PopPressure_norm - 0.2*SchoolDensity_norm
            </div>
        </div>
    </div>
    
    <div class="footer">
        © 2026 Education Vulnerability Index (EVI) Nigeria Project • Powered by standard WGS84 GIS mappings and Leaflet interactive visualizations.
    </div>
</body>
</html>
"""

with open(os.path.join(DOCS_DIR, "index.html"), "w") as f:
    f.write(index_html_content)
print("Saved docs/index.html")

# 3. Write docs/maps.html (Maps switchboard)
maps_html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive GIS Maps - EVI Project</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --primary: #3b82f6;
            --primary-grad: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            --border: #e2e8f0;
        }
        
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            line-height: 1.5;
            display: flex;
            flex-direction: column;
            height: 100vh;
            overflow: hidden;
        }
        
        .header {
            background: var(--primary-grad);
            color: #ffffff;
            padding: 20px 5%;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
            flex-shrink: 0;
        }
        
        .header h1 {
            font-size: 22px;
            font-weight: 800;
            letter-spacing: -0.5px;
        }
        
        .nav-links {
            display: flex;
            gap: 15px;
        }
        
        .nav-button {
            background-color: rgba(255,255,255,0.15);
            color: #ffffff;
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 13px;
            transition: all 0.2s ease;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        .nav-button:hover {
            background-color: #ffffff;
            color: var(--primary);
        }
        
        .nav-button.active {
            background-color: #ffffff;
            color: var(--primary);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        /* Map Container Workspace */
        .map-workspace {
            display: flex;
            flex: 1;
            overflow: hidden;
            width: 100%;
        }
        
        /* Sidebar Switcher */
        .sidebar {
            width: 320px;
            background-color: #ffffff;
            border-right: 1px solid var(--border);
            padding: 30px 20px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            overflow-y: auto;
            flex-shrink: 0;
        }
        
        .sidebar h2 {
            font-size: 18px;
            font-weight: 800;
            color: var(--text-main);
            letter-spacing: -0.5px;
        }
        
        .map-selector-btn {
            background: #f8fafc;
            border: 1px solid var(--border);
            padding: 16px;
            border-radius: 12px;
            text-align: left;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            flex-direction: column;
            gap: 5px;
            font-family: inherit;
        }
        
        .map-selector-btn:hover {
            border-color: var(--primary);
            background-color: #f1f5f9;
            transform: translateY(-2px);
        }
        
        .map-selector-btn.active {
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            border-color: var(--primary);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
        }
        
        .map-selector-btn .title {
            font-weight: 700;
            font-size: 13px;
            color: var(--text-main);
        }
        
        .map-selector-btn .desc {
            font-size: 11px;
            color: var(--text-muted);
            line-height: 1.3;
        }
        
        /* Map Viewer */
        .map-viewer {
            flex: 1;
            height: 100%;
            position: relative;
            background-color: #e2e8f0;
        }
        
        iframe {
            width: 100%;
            height: 100%;
            border: none;
            display: block;
        }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>Interactive GIS Map Explorer</h1>
        </div>
        <div class="nav-links">
            <a href="index.html" class="nav-button">Dashboard</a>
            <a href="maps.html" class="nav-button active">Interactive Maps</a>
            <a href="strategy.html" class="nav-button">Strategy</a>
        </div>
    </div>
    
    <div class="map-workspace">
        <div class="sidebar">
            <h2>Select Map Layer</h2>
            <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 10px;">
                Toggle between different GIS layers to analyze the components of education vulnerability.
            </p>
            
            <button class="map-selector-btn active" onclick="switchMap('evi_map.html', this)">
                <span class="title">Education Vulnerability Index (EVI)</span>
                <span class="desc">A composite spatial index showing overall risk intensity from 0 to 1.</span>
            </button>
            
            <button class="map-selector-btn" onclick="switchMap('cluster_map.html', this)">
                <span class="title">Risk Profile Clusters</span>
                <span class="desc">Grouping LGAs by KMeans (k=4) into Emergency, Expansion, Gap, and Stable zones.</span>
            </button>
            
            <button class="map-selector-btn" onclick="switchMap('mismatch_map.html', this)">
                <span class="title">Infrastructure Mismatch Ratio</span>
                <span class="desc">Ratio comparing school-age population volumes against physical school densities.</span>
            </button>
        </div>
        
        <div class="map-viewer">
            <iframe id="map-iframe" src="evi_map.html"></iframe>
        </div>
    </div>
    
    <script>
        function switchMap(mapUrl, element) {
            // Update iframe
            document.getElementById('map-iframe').src = mapUrl;
            
            // Update button styles
            const buttons = document.querySelectorAll('.map-selector-btn');
            buttons.forEach(btn => btn.classList.remove('active'));
            element.classList.add('active');
        }
    </script>
</body>
</html>
"""

with open(os.path.join(DOCS_DIR, "maps.html"), "w") as f:
    f.write(maps_html_content)
print("Saved docs/maps.html")

# 4. Write docs/strategy.html (Strategy page)
strategy_html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prioritisation Strategy - EVI Project</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --primary: #3b82f6;
            --primary-grad: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            --border: #e2e8f0;
        }
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            line-height: 1.6;
            padding: 0;
        }
        .header {
            background: var(--primary-grad);
            color: #ffffff;
            padding: 30px 5%;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }
        .header h1 {
            font-size: 24px;
            font-weight: 800;
            letter-spacing: -0.5px;
        }
        .nav-links {
            display: flex;
            gap: 15px;
        }
        .nav-button {
            background-color: rgba(255,255,255,0.15);
            color: #ffffff;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 14px;
            transition: all 0.2s ease;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .nav-button:hover {
            background-color: #ffffff;
            color: var(--primary);
        }
        .nav-button.active {
            background-color: #ffffff;
            color: var(--primary);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .container {
            max-width: 1000px;
            margin: 40px auto;
            padding: 0 20px;
        }
        .card {
            background: var(--card-bg);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.02);
            border: 1px solid var(--border);
            margin-bottom: 25px;
        }
        h2 {
            font-size: 20px;
            font-weight: 800;
            margin-top: 30px;
            margin-bottom: 15px;
            color: var(--text-main);
            border-left: 4px solid var(--primary);
            padding-left: 12px;
            letter-spacing: -0.5px;
        }
        h2:first-of-type {
            margin-top: 0;
        }
        h3 {
            font-size: 16px;
            font-weight: 700;
            margin-top: 25px;
            margin-bottom: 10px;
            color: var(--text-main);
        }
        p {
            font-size: 15px;
            color: #334155;
            margin-bottom: 15px;
        }
        ul {
            margin-bottom: 20px;
            padding-left: 20px;
        }
        li {
            font-size: 15px;
            color: #334155;
            margin-bottom: 8px;
        }
        .formula-box {
            background-color: #f1f5f9;
            padding: 20px;
            border-radius: 8px;
            font-family: monospace;
            font-size: 14px;
            margin: 20px 0;
            border: 1px solid var(--border);
            text-align: center;
            color: #0f172a;
            font-weight: bold;
        }
        .footer {
            text-align: center;
            padding: 40px;
            color: var(--text-muted);
            font-size: 12px;
            border-top: 1px solid var(--border);
            background-color: #ffffff;
            margin-top: 60px;
        }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>Education Bridge Initiative</h1>
        </div>
        <div class="nav-links">
            <a href="index.html" class="nav-button">Dashboard</a>
            <a href="maps.html" class="nav-button">Interactive Maps</a>
            <a href="strategy.html" class="nav-button active">Strategy</a>
        </div>
    </div>
    <div class="container">
        <div class="card">
            <h2 style="margin-bottom: 25px;">Prioritisation Strategy</h2>
            
            <h3>1. Context</h3>
            <p>The Education Bridge Initiative (EBI) operates in conflict-affected regions where education access is highly uneven and rapidly changing. While field teams possess strong contextual knowledge, the organisation’s current planning approach relies on fragmented and unevenly available information. As a result, EBI lacks a systematic, data-driven mechanism to prioritise interventions across regions, particularly when conflict dynamics shift quickly. </p>
            <p>This proposal addresses that gap by introducing a scalable, data-driven prioritisation framework that complements field knowledge with geospatial and predictive analytics.</p>
            
            <h3>2. Objectives</h3>
            <p>The project aims to:</p>
            <ul>
                <li><strong>Develop an Education Vulnerability Index (EVI)</strong> to identify areas with the greatest unmet education needs</li>
                <li><strong>Classify regions into risk profiles</strong> to support differentiated intervention strategies</li>
                <li><strong>Predict future education disruption risks</strong> using historical and real-time data</li>
                <li><strong>Deliver an interactive decision-support tool</strong> usable by non-technical staff</li>
                <li><strong>Enable rapid updates</strong> as new data becomes available</li>
            </ul>
            
            <h3>3. Approach</h3>
            <p>The proposed approach integrates geospatial analysis, statistical modelling, and machine learning into a unified prioritisation system.</p>
            
            <h3>3.1 Data Integration</h3>
            <p>The model combines three core datasets:</p>
            <ul>
                <li>Conflict event data (intensity, frequency, recency)</li>
                <li>Population distribution, with a focus on school-age children</li>
                <li>School infrastructure data</li>
            </ul>
            <p>These datasets are harmonised at the Local Government Area (LGA) level to enable consistent analysis.</p>
            
            <h3>3.2 Education Vulnerability Index (EVI)</h3>
            <p>An index is constructed to quantify education vulnerability:</p>
            <div class="formula-box">
                EVI = Conflict Intensity + Population Pressure - School Access
            </div>
            <p>All components are normalised and weighted to produce a comparable score across LGAs. The EVI allows EBI to:</p>
            <ul>
                <li>Rank areas by urgency</li>
                <li>Identify mismatches between population and school infrastructure</li>
                <li>Allocate resources more effectively</li>
            </ul>
            
            <h3>3.3 Risk Profiling (Clustering)</h3>
            <p>Using unsupervised machine learning (KMeans clustering), LGAs are grouped into distinct risk categories:</p>
            <ul>
                <li><strong>Emergency zones:</strong> high conflict, low access</li>
                <li><strong>Expansion zones:</strong> high population pressure, moderate access</li>
                <li><strong>Infrastructure gaps:</strong> low conflict but insufficient schools</li>
                <li><strong>Stable areas:</strong> relatively balanced conditions</li>
            </ul>
            <p>This classification enables tailored programmatic responses.</p>
            
            <h3>3.4 Predictive Modelling</h3>
            <p>A predictive model is developed to estimate the probability of education disruption in each LGA. The model uses:</p>
            <ul>
                <li>Conflict trends over time</li>
                <li>Population density</li>
                <li>School access indicators</li>
            </ul>
            <p>Outputs are expressed as probabilities, allowing EBI to anticipate emerging hotspots rather than reacting to crises after they occur.</p>
            
            <h3>3.5 Decision-Support Tool</h3>
            <p>All outputs are integrated into an interactive dashboard, including EVI maps, risk classification maps, and priority ranking tables. These tools are designed for usability by non-technical staff and can directly inform planning and resource allocation decisions.</p>
            
            <h3>3.6 Automation and Scalability</h3>
            <p>The system includes an automated pipeline that updates outputs as new data becomes available. The methodology relies exclusively on open data and modular code, ensuring it can be applied to other countries, adapted to varying data availability, and updated without rebuilding the system.</p>
            
            <h3>4. Proposed Activities</h3>
            <ul>
                <li>Data acquisition and validation</li>
                <li>Data cleaning and geospatial alignment</li>
                <li>Feature engineering and indicator construction</li>
                <li>Index development and validation</li>
                <li>Clustering and predictive modelling</li>
                <li>Dashboard and visualization development</li>
                <li>Automation pipeline creation</li>
            </ul>
            
            <h3>5. Deliverables</h3>
            <ul>
                <li>Education Vulnerability Index dataset (LGA level)</li>
                <li>Risk classification model and outputs</li>
                <li>Predictive model for disruption risk</li>
                <li>Interactive geospatial dashboard (GitHub Pages)</li>
                <li>Top-priority LGA ranking for intervention</li>
                <li>Open-source repository with full data and methodology</li>
            </ul>
        </div>
    </div>
    <div class="footer">
        © 2026 Education Vulnerability Index (EVI) Nigeria Project • Deployed via GitHub Pages.
    </div>
</body>
</html>
"""

with open(os.path.join(DOCS_DIR, "strategy.html"), "w") as f:
    f.write(strategy_html_content)
print("Saved docs/strategy.html")
print("Dashboard, Maps, and Strategy pages generated successfully!")
