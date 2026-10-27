"""Reproduce all core analytical artifacts without cloud access or an API key."""
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
for step in ['generate_data.py','build_dataset.py','build_operations.py','reconcile_orders.py','validate_data.py','run_analysis.py']:
    subprocess.run([sys.executable,str(ROOT/'scripts'/step)],check=True,cwd=ROOT)
subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],check=True,cwd=ROOT)
for step in ['package_docs.py','prepare_powerbi.py','prepare_operations_model.py','render_previews.py','ai_summary.py','finalize_submission.py']:
    subprocess.run([sys.executable,str(ROOT/'scripts'/step)],check=True,cwd=ROOT)
print('Analytical artifacts rebuilt. Cloud report is refreshed separately; Excel export is optional.')
