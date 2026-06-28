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
    print("Starting full EVINigeria ETL and Modeling Pipeline...")
    
    # Run the scripts sequentially
    run_script("scripts/clean_data.py")
    run_script("scripts/build_evi.py")
    run_script("scripts/clustering.py")
    run_script("scripts/prediction.py")
    
    print("\n==================================================")
    print("FULL PIPELINE EXECUTED SUCCESSFULLY!")
    print("==================================================")
