# EBIOS Risk Assistant (`ebios-risk-assistant`)

Assistant d'analyse de risques cybersécurité et générateur d'homologation automatisé basé sur la méthode officielle **ANSSI EBIOS Risk Manager** (Ateliers 1 à 5).

L'outil permet de modéliser des études EBIOS RM au format structuré YAML ou via un questionnaire interactif en ligne de commande, puis de compiler un **rapport exécutif PDF officiel de 4 pages calibré pour l'impression** via WeasyPrint.

---

## Fonctionnalités

- **Atelier 1 (Cadrage & Socle)** : Cartographie des missions, Valeurs Métiers (D/I/C), Biens Supports et analyse d'écarts de conformité (Gap Analysis).
- **Ateliers 2 & 3 (Sources de Risques & Écosystème)** : Caractérisation des attaquants, évaluation chiffrée de la menace des tiers via la formule officielle ANSSI :
  Niveau de Menace = (Dépendance x Pénétration) / (Maturité x Confiance)
  et formalisation des scénarios stratégiques.
- **Atelier 4 (Scénarios Opérationnels)** : Déroulé technique des modes opératoires selon la Kill Chain ANSSI en 4 phases (Connaître, Rentrer, Trouver, Exploiter).
- **Atelier 5 (Traitement du Risque)** : Double matrice cartésienne 4x4 (Risque Brut vs Risque Résiduel) avec pastilles de positionnement des scénarios et plan d'action rattaché aux 4 piliers de sécurité de l'ANSSI.
- **Export Exécutif PDF** : Rendu A4 paginé, sans dépendance bureautique lourde, prêt pour les comités d'homologation et de direction.

---

## Architecture du Projet

ebios-risk-assistant/
├── core/
│   ├── creator.py         # Questionnaire terminal interactif (scaffolding pas-à-pas)
│   ├── engine.py          # Moteur de validation logique et calcul des risques
│   ├── loader.py          # Chargement et validation de structure YAML
│   └── matrix.py          # Définition des grilles 4x4 et seuils de gravité/vraisemblance
├── exporters/
│   ├── markdown_report.py # Générateur de synthèse Markdown
│   └── pdf_report.py      # Moteur de rendu WeasyPrint PDF officiel ANSSI 4 pages
├── examples/
│   └── sample_analysis.yaml # Étude type complète (BioTech Pharma Solutions)
├── ebios_assistant.py     # Point d'entrée CLI principal
├── requirements.txt       # Dépendances Python
└── README.md

---

## Prérequis et Installation

### 1. Dépendances système (macOS)

WeasyPrint s'appuie sur les bibliothèques C pango, cairo et gobject. Sur macOS (Apple Silicon), installez-les via Homebrew :

brew install pango cairo libffi glib

### 2. Environnement virtuel Python

# Cloner le dépôt
git clone <URL_DU_DEPOT>
cd ebios-risk-assistant

# Créer et activer le venv
python3 -m venv .venv
source .venv/bin/activate

# Installer les paquets requis
pip install -r requirements.txt

---

## Utilisation

Si WeasyPrint ne localise pas automatiquement les bibliothèques Homebrew sous macOS, exportez la variable d'environnement :

export DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_FALLBACK_LIBRARY_PATH

### 1. Compiler un audit existant en rapport PDF
Valide la cohérence inter-ateliers et génère le rapport officiel :

python ebios_assistant.py audit examples/sample_analysis.yaml

### 2. Démarrer une nouvelle analyse interactive
Lance l'assistant en mode console pour guider la saisie pas-à-pas :

python ebios_assistant.py new

### 3. Générer un modèle vierge
Crée une structure YAML prête à être complétée manuellement :

python ebios_assistant.py init mon_etude.yaml

---

## Structure du Rapport PDF Généré (4 Pages)

1. Page 1 : Cadrage, Missions de l'organisation, Valeurs Métiers (D/I/C), Biens Supports et écarts du socle (Gap Analysis).
2. Page 2 : Sources de risques retenues, cotation de la menace de l'écosystème et scénarios stratégiques.
3. Page 3 : Scénarios opérationnels détaillés en Kill Chain 4 phases (Connaître, Rentrer, Trouver, Exploiter).
4. Page 4 : Matrices 4x4 brute et résiduelle avec marqueurs de scénarios (S1, S2) et plan de traitement rattaché aux piliers ANSSI.

---

## Licence

Projet sous licence MIT.