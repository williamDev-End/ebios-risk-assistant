"""CLI principale pour EBIOS Risk Assistant — Export PDF Officiel."""

import argparse
import sys
import re
from pathlib import Path
from core.loader import load_ebios_study
from core.engine import validate_study_consistency, compute_all_risks
from core.creator import generate_blank_template, run_interactive_wizard
from exporters.pdf_report import generate_pdf_report

def sanitize_filename(name: str) -> str:
    clean = re.sub(r"[^\w\s-]", "", name).strip().replace(" ", "_")
    return clean.upper()

def run_audit(study_file: str):
    print("[*] Chargement de l'étude EBIOS RM...")
    try:
        data = load_ebios_study(study_file)
    except Exception as e:
        print(f"[!] Erreur de lecture : {e}")
        sys.exit(1)

    print("[*] Validation de la cohérence logique inter-ateliers...")
    errors = validate_study_consistency(data)
    if errors:
        print(f"[!] Échec de validation ({len(errors)} erreur(s)) :")
        for err in errors:
            print(f"    - {err}")
        sys.exit(1)
    print("[+] Cohérence logique validée avec succès.")

    risks = compute_all_risks(data)
    ctx = data.get("context", {})
    org = ctx.get("organization") or ctx.get("target_name") or "RAPPORT"

    # Nommage automatique du PDF au nom de l'entreprise
    pdf_filename = f"EBIOS_RM_RAPPORT_{sanitize_filename(org)}.pdf"
    
    print("[*] Génération du PDF officiel ANSSI (tableaux, matrices 4x4, chaînes d'attaque)...")
    generate_pdf_report(data, risks, pdf_filename)
    print(f"\n[+] PDF officiel prêt : {Path(pdf_filename).resolve()}")

def main():
    parser = argparse.ArgumentParser(description="Assistant EBIOS Risk Manager (ANSSI) — Générateur PDF.")
    subparsers = parser.add_subparsers(dest="command", help="Sous-commandes disponibles")

    # new : questionnaire pas à pas
    new_parser = subparsers.add_parser("new", help="Lancer le questionnaire interactif pas à pas.")
    new_parser.add_argument("--out", default="etude_ebios.yaml", help="Fichier YAML d'enregistrement.")

    # audit : génère le PDF à partir du fichier
    audit_parser = subparsers.add_parser("audit", help="Auditer un fichier existant et produire le PDF officiel.")
    audit_parser.add_argument("study_file", help="Chemin vers le fichier YAML.")

    # init : modèle vierge
    init_parser = subparsers.add_parser("init", help="Générer un fichier modèle YAML vierge.")
    init_parser.add_argument("--out", default="modele_ebios.yaml", help="Fichier de sortie.")

    args = parser.parse_args()

    if args.command == "new":
        saved_yaml = run_interactive_wizard(args.out)
        print(f"\n[+] Données enregistrées dans : {saved_yaml}")
        run_audit(saved_yaml)
        return

    if args.command == "audit":
        run_audit(args.study_file)
        return

    if args.command == "init":
        path = generate_blank_template(args.out)
        print(f"[+] Modèle YAML généré : {path}")
        return

    parser.print_help()

if __name__ == "__main__":
    main()