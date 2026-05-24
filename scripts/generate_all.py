import os
import sys
import subprocess

def run_script(script_path):
    print(f"\n==================================================")
    print(f"Exécution de : {script_path}")
    print(f"==================================================")
    
    # Resolve the python executable being used currently to maintain environment
    python_executable = sys.executable
    
    result = subprocess.run([python_executable, script_path], capture_output=False, text=True)
    if result.returncode != 0:
        print(f"Erreur lors de l'exécution de {script_path} (code de retour: {result.returncode})")
        return False
    return True

def main():
    # Base directory is the project root (assumed to run from there)
    scripts = [
        "scripts/generate_base.py",
        "scripts/generate_solo.py",
        "scripts/generate_trames_d_ombres.py",
        "scripts/generate_trames_d_ombres_solo.py"
    ]
    
    success = True
    for script in scripts:
        if not os.path.exists(script):
            print(f"Script introuvable : {script}")
            success = False
            continue
            
        if not run_script(script):
            success = False
            
    if success:
        print("\nTous les PDFs ont été générés avec succès dans le dossier 'Générations' !")
    else:
        print("\nCertains scripts de génération ont rencontré des erreurs. Veuillez vérifier les logs ci-dessus.")
        sys.exit(1)

if __name__ == "__main__":
    main()
