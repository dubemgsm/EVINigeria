import subprocess
import sys

def run_script(script_path):
    print(f"\n==================================================")
    print(f"RUNNING: {script_path}")
    print(f"==================================================")
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    
    # Print stdout
    if result.stdout:
        print(result.stdout)
    
    # Print stderr if there were warnings or errors
    if result.stderr:
        print("Warnings/Errors:")
        print(result.stderr)
        
    if result.returncode != 0:
        print(f"ERROR: {script_path} failed with return code {result.returncode}")
        sys.exit(result.returncode)
    else:
        print(f"SUCCESS: {script_path} finished successfully.")

if __name__ == "__main__":
    print("Starting full EVINigeria Automated Pipeline Update...")
    
    # 1. Clean and clip raw data
    run_script("scripts/clean_data.py")
    
    # 2. Recalculate EVI and engineering features
    run_script("scripts/build_evi.py")
    
    # 3. Re-run KMeans clustering
    run_script("scripts/clustering.py")
    
    # 4. Update predictive disruption risk model
    run_script("scripts/prediction.py")
    
    # 5. Re-generate Leaflet interactive HTML maps
    run_script("scripts/visualize.py")
    
    # 6. Re-compile HTML dashboard and switcher
    run_script("scripts/generate_dashboard.py")
    
    print("\n==================================================")
    print("ALL OUTPUTS AND DASHBOARDS UPDATED SUCCESSFULLY!")
    print("==================================================")
