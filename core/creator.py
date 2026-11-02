"""Assistant interactif en français pour l'analyse EBIOS Risk Manager (ANSSI)."""

from datetime import datetime
from pathlib import Path
import yaml

def ask_choice(prompt: str, options: list[str], default: str) -> str:
    """Invite l'utilisateur à choisir parmi une liste d'options."""
    opts_str = "/".join(options)
    val = input(f"{prompt} [{opts_str}] (défaut : {default}) : ").strip()
    return val if val in options else default

def ask_int_scale(prompt: str, explanation: str, default: int = 3) -> int:
    """Invite pour une échelle de 1 à 4 avec explication contextuelle."""
    print(f"  -> Guide : {explanation}")
    raw = input(f"  {prompt} [1=Faible, 2=Modéré, 3=Élevé, 4=Critique] (défaut : {default}) : ").strip()
    try:
        val = int(raw)
        return val if 1 <= val <= 4 else default
    except ValueError:
        return default

def generate_blank_template(filepath: str) -> str:
    """Génère un squelette YAML vierge et documenté selon la méthode EBIOS RM."""
    current_date = datetime.now().strftime("%d/%m/%Y")
    template_content = f"""context:
  organization: "Nom de l'Organisation"
  target_name: "Système ou Produit Évalué"
  perimeter: "Périmètre de l'étude"
  author: "Responsable de l'analyse"
  date: "{current_date}"

workshops:
  workshop_1_baseline:
    scope:
      missions:
        - "Assurer la continuité de service"
    primary_assets:
      - id: "VM-01"
        name: "Valeur Métier 1"
        category: "Processus"
        business_owner: "Direction Métier"
        security_criteria:
          availability: 3     # Échelle ANSSI : 1 (Faible) à 4 (Critique)
          integrity: 3
          confidentiality: 2
    supporting_assets:
      - id: "BS-01"
        name: "Bien Support 1"
        type: "Logiciel"
        technical_owner: "Équipe IT"
    dreaded_events:
      - id: "ER-01"
        primary_asset_id: "VM-01"
        description: "Sinistre majeur redouté"
        impact_nature: "Préjudice financier et réputationnel"
        severity: 3          # Échelle : 1 à 4
    security_baseline_gap_analysis:
      - standard: "Guide d'hygiène ANSSI"
        requirement: "Règle 8 : Comptes d'administration dédiés"
        compliance_status: "Appliqué sans restriction"
        identified_gap: "Aucun"

  workshop_2_risk_sources:
    sources:
      - id: "SR-01"
        name: "Groupe Cybercriminel"
        motivation: "Gain financier et extorsion"
        resources: "Moyen"
        activity_level: "Élevée"
        relevance: "Élevée"

  workshop_3_strategic_scenarios:
    ecosystem_stakeholders:
      - id: "PP-01"
        name: "Prestataire Informatique"
        category: "Prestataire IT"
        dependency: 3        # Échelle : 1 à 4
        penetration: 3       # Échelle : 1 à 4
        cyber_maturity: 2    # Échelle : 1 à 4
        trust: 2             # Échelle : 1 à 4
    scenarios:
      - id: "SC-S01"
        name: "Intrusion directe en périphérie réseau"
        source_id: "SR-01"
        dreaded_event_id: "ER-01"
        attack_path: "Attaque directe via interface exposée"
        severity: 3

  workshop_4_operational_scenarios:
    scenarios:
      - id: "SC-O01"
        name: "Exploitation d'une vulnérabilité et exfiltration"
        strategic_scenario_id: "SC-S01"
        supporting_asset_id: "BS-01"
        kill_chain:
          reconnaissance: "Reconnaissance OSINT"
          intrusion: "Exploitation d'un service exposé"
          lateral_movement: "Élévation de privilèges"
          exploitation: "Exfiltration des bases de données"
        severity: 3          # Échelle : 1 à 4
        likelihood: 2        # Échelle : 1 à 4

  workshop_5_risk_treatment:
    measures:
      - id: "MES-01"
        operational_scenario_id: "SC-O01"
        pillar: "Protection"
        action: "Authentification multifacteur et segmentation réseau"
        responsible: "Équipe Sécurité"
        deadline: "2027-T1"
        residual_risk:
          severity: 2
          likelihood: 1
"""
    dest = Path(filepath)
    dest.write_text(template_content, encoding="utf-8")
    return str(dest.resolve())

def run_interactive_wizard(filepath: str) -> str:
    print("=" * 72)
    print("      EBIOS RISK MANAGER (ANSSI) - QUESTIONNAIRE D'ÉVALUATION")
    print("=" * 72)
    print("Ce questionnaire recueille les éléments requis pour les 5 ateliers.")
    print("Le livrable produit respecte la terminologie officielle de l'ANSSI.\n")

    current_date = datetime.now().strftime("%d/%m/%Y")

    # Étape 0 : Cadrage général
    print("----------------------------------------------------------------------")
    print("ÉTAPE 0 : CONTEXTE GÉNÉRAL ET CADRAGE")
    print("----------------------------------------------------------------------")
    org = input("Nom de l'organisation / Entreprise (ex: BioTech Pharma) : ").strip() or "Entreprise Évaluée"
    target = input("Système, service ou produit cible (ex: Ligne de production) : ").strip() or "Système Cible"
    perimeter = input("Périmètre d'analyse (ex: Réseau industriel et serveurs centraux) : ").strip() or "Périmètre Opérationnel"
    author = input("Pilote de l'analyse / Responsable : ").strip() or "Équipe Cybersécurité"
    date_str = input(f"Date de l'analyse (JJ/MM/AAAA, défaut : {current_date}) : ").strip() or current_date

    # Atelier 1 : Cadrage et socle de sécurité
    print("\n----------------------------------------------------------------------")
    print("ATELIER 1 : CADRAGE, VALEURS MÉTIERS ET ÉVÉNEMENTS REDOUTÉS")
    print("----------------------------------------------------------------------")

    # Missions
    missions = []
    print("\n[Missions de l'organisation]")
    while True:
        m = input(f"  Mission #{len(missions) + 1} (laisser vide pour terminer) : ").strip()
        if not m:
            if not missions:
                missions.append(f"Garantir la continuité d'activité et la conformité de {target}")
            break
        missions.append(m)

    # Valeurs métiers (Actifs primaires)
    primary_assets = []
    print("\n--- 1.1 Valeurs Métiers (Processus clés ou informations critiques) ---")
    while True:
        idx = len(primary_assets) + 1
        pa_id = f"VM-{idx:02d}"
        print(f"\n[Valeur Métier {pa_id}]")
        name = input("  Intitulé de la Valeur Métier (ex: Données de R&D, Pilotage de la production) : ").strip()
        if not name:
            name = f"Valeur Métier {idx}"
        cat = ask_choice("  Nature de l'actif", ["Processus", "Information"], "Processus")
        owner = input("  Propriétaire métier (ex: Directeur Médical, Responsable Logistique) : ").strip() or "Direction Métier"

        print("  Besoins de sécurité de la Valeur Métier (Échelle ANSSI de 1 à 4) :")
        d_val = ask_int_scale("Disponibilité (D) - Impact en cas d'indisponibilité", "1=Tolère plusieurs jours d'arrêt, 4=Interruption fatale", 3)
        i_val = ask_int_scale("Intégrité (I) - Impact en cas d'altération", "1=Erreur tolérée sans impact, 4=Altération critique / toxique", 3)
        c_val = ask_int_scale("Confidentialité (C) - Impact en cas de divulgation", "1=Donnée publique, 4=Secret stratégique / vital", 2)

        primary_assets.append({
            "id": pa_id,
            "name": name,
            "category": cat,
            "business_owner": owner,
            "security_criteria": {"availability": d_val, "integrity": i_val, "confidentiality": c_val}
        })

        if input("\nAjouter une autre Valeur Métier ? (o/n, défaut : n) : ").strip().lower() != "o":
            break

    # Biens supports
    supporting_assets = []
    print("\n--- 1.2 Biens Supports (Actifs techniques supportant les valeurs métiers) ---")
    while True:
        idx = len(supporting_assets) + 1
        sa_id = f"BS-{idx:02d}"
        print(f"\n[Bien Support {sa_id}]")
        name = input("  Intitulé du Bien Support (ex: Serveur ERP, Automates PLC, Contrôleur de domaine) : ").strip()
        if not name:
            name = f"Bien Support {idx}"
        sa_type = input("  Nature technique (Matériel, Logiciel, Réseau, Personnel) : ").strip() or "Logiciel"
        tech_owner = input("  Responsable technique (ex: Administrateur Système, RSSI) : ").strip() or "Équipe IT"

        supporting_assets.append({
            "id": sa_id,
            "name": name,
            "type": sa_type,
            "technical_owner": tech_owner
        })

        if input("\nAjouter un autre Bien Support ? (o/n, défaut : n) : ").strip().lower() != "o":
            break

    # Événements redoutés
    dreaded_events = []
    print("\n--- 1.3 Événements Redoutés (Sinistres affectant les valeurs métiers) ---")
    for pa in primary_assets:
        idx = len(dreaded_events) + 1
        de_id = f"ER-{idx:02d}"
        print(f"\n[Événement Redouté pour '{pa['name']}']")
        desc = input(f"  Description du sinistre sur {pa['name']} (ex: Arrêt prolongé supérieur à 48h) : ").strip()
        if not desc:
            desc = f"Atteinte grave à {pa['name']}"
        impact = input("  Conséquences métier (ex: Pertes d'exploitation directes, sanctions CNIL) : ").strip() or "Préjudice financier et réputationnel"
        sev = ask_int_scale("  Gravité du sinistre", "1=Négligeable, 2=Modérée, 3=Majeure, 4=Critique pour l'organisation", 3)

        dreaded_events.append({
            "id": de_id,
            "primary_asset_id": pa["id"],
            "description": desc,
            "impact_nature": impact,
            "severity": sev
        })

    # Atelier 2 : Sources de risques
    print("\n----------------------------------------------------------------------")
    print("ATELIER 2 : SOURCES DE RISQUES (SR)")
    print("----------------------------------------------------------------------")
    risk_sources = []
    while True:
        idx = len(risk_sources) + 1
        rs_id = f"SR-{idx:02d}"
        print(f"\n[Source de Risque {rs_id}]")
        name = input("  Profil de l'attaquant (ex: Groupe Cybercriminel, Concurrent, Employé malveillant) : ").strip()
        if not name:
            name = f"Attaquant {idx}"
        mot = input("  Motivation principale (ex: Extorsion financière, Espionnage, Sabotage) : ").strip() or "Gain financier"
        res = ask_choice("  Niveau de ressources", ["Faible", "Moyen", "Élevé"], "Moyen")
        act = ask_choice("  Activité dans le secteur", ["Faible", "Moyenne", "Élevée"], "Élevée")

        risk_sources.append({
            "id": rs_id,
            "name": name,
            "motivation": mot,
            "resources": res,
            "activity_level": act,
            "relevance": "Élevée"
        })

        if input("\nAjouter une autre Source de Risque ? (o/n, défaut : n) : ").strip().lower() != "o":
            break

    # Atelier 3 : Écosystème & Scénarios stratégiques
    print("\n----------------------------------------------------------------------")
    print("ATELIER 3 : ÉCOSYSTÈME ET SCÉNARIOS STRATÉGIQUES")
    print("----------------------------------------------------------------------")
    stakeholders = []
    if input("L'organisation s'appuie-t-elle sur des tiers (prestataires IT, fournisseurs) ? (o/n, défaut : o) : ").strip().lower() != "n":
        while True:
            idx = len(stakeholders) + 1
            stk_id = f"PP-{idx:02d}"
            print(f"\n[Partie Prenante {stk_id}]")
            stk_name = input("  Nom du tiers (ex: Infogéreur d'infrastructure, Prestataire maintenance) : ").strip()
            if not stk_name:
                stk_name = f"Prestataire {idx}"
            cat = input("  Catégorie (Prestataire IT, Fournisseur, Sous-traitant, Partenaire) : ").strip() or "Prestataire IT"
            print("  Cotation de la menace selon la formule ANSSI :")
            dep = ask_int_scale("Dépendance (Le tiers est-il remplaçable ?)", "1=Facilement remplaçable, 4=Indispensable et unique", 3)
            pen = ask_int_scale("Pénétration (Niveau d'accès au système d'information)", "1=Aucun accès direct, 4=Privilèges d'administration", 3)
            mat = ask_int_scale("Maturité cyber (Niveau de sécurité du tiers)", "1=Faible / Non documenté, 4=Certifié ISO 27001", 2)
            tru = ask_int_scale("Confiance (Garanties contractuelles et organisationnelles)", "1=Faible confiance, 4=Confiance vérifiée par audit", 2)

            stakeholders.append({
                "id": stk_id,
                "name": stk_name,
                "category": cat,
                "dependency": dep,
                "penetration": pen,
                "cyber_maturity": mat,
                "trust": tru
            })

            if input("\nAjouter une autre Partie Prenante ? (o/n, défaut : n) : ").strip().lower() != "o":
                break

    # Scénarios stratégiques
    strategic_scenarios = []
    print("\n--- Scénarios Stratégiques (Chemins d'attaque macroscopiques) ---")
    while True:
        idx = len(strategic_scenarios) + 1
        sc_s_id = f"SC-S{idx:02d}"
        print(f"\n[Scénario Stratégique {sc_s_id}]")
        name = input("  Intitulé (ex: Rançonnage via attaque directe, Espionnage via rebond infogéreur) : ").strip()
        if not name:
            name = f"Scénario Stratégique {idx}"

        print("  Sélectionnez la Source de Risque associée :")
        for s in risk_sources:
            print(f"    - {s['id']} : {s['name']}")
        source_id = input(f"  ID de la Source de Risque (défaut : {risk_sources[0]['id']}) : ").strip() or risk_sources[0]["id"]

        print("  Sélectionnez l'Événement Redouté visé :")
        for d in dreaded_events:
            print(f"    - {d['id']} : {d['description']} (Gravité : {d['severity']})")
        de_id = input(f"  ID de l'Événement Redouté (défaut : {dreaded_events[0]['id']}) : ").strip() or dreaded_events[0]["id"]

        matched_de = next((d for d in dreaded_events if d["id"] == de_id), dreaded_events[0])
        inherited_sev = matched_de["severity"]

        path_desc = input("  Vecteur d'attaque (ex: Intrusion directe en périphérie / Rebond VPN tiers) : ").strip() or "Intrusion directe"

        strategic_scenarios.append({
            "id": sc_s_id,
            "name": name,
            "source_id": source_id,
            "dreaded_event_id": de_id,
            "attack_path": path_desc,
            "severity": inherited_sev
        })

        if input("\nAjouter un autre Scénario Stratégique ? (o/n, défaut : n) : ").strip().lower() != "o":
            break

    # Ateliers 4 & 5 : Scénarios opérationnels & Traitement du risque
    print("\n----------------------------------------------------------------------")
    print("ATELIERS 4 & 5 : MODES OPÉRATOIRES TECHNIQUES ET TRAITEMENT DU RISQUE")
    print("----------------------------------------------------------------------")
    operational_scenarios = []
    measures = []

    for sc_s in strategic_scenarios:
        idx = len(operational_scenarios) + 1
        sc_o_id = f"SC-O{idx:02d}"
        print(f"\n[Mode Opératoire pour '{sc_s['name']}']")
        op_name = input("  Intitulé technique du scénario (ex: Exploitation vulnérabilité VPN et mouvement latéral) : ").strip() or f"Scénario Opérationnel {idx}"

        print("  Sélectionnez le Bien Support ciblé :")
        for sa in supporting_assets:
            print(f"    - {sa['id']} : {sa['name']}")
        sa_id = input(f"  ID du Bien Support (défaut : {supporting_assets[0]['id']}) : ").strip() or supporting_assets[0]["id"]

        print("\n  Décomposition du mode opératoire en 4 phases (Modèle ANSSI) :")
        recon = input("    1. Connaître (Reconnaissance) - ex: Énumération Shodan, cartographie réseau : ").strip() or "Reconnaissance OSINT"
        intru = input("    2. Rentrer (Intrusion initiale) - ex: Exploitation service exposé, phishing : ").strip() or "Exploitation d'une interface externe"
        lat = input("    3. Trouver (Mouvement latéral) - ex: Élévation de privilèges, compromission AD : ").strip() or "Élévation de privilèges"
        expl = input("    4. Exploiter (Action finale) - ex: Déploiement rançongiciel, exfiltration : ").strip() or "Action finale sur l'objectif"

        lik = ask_int_scale("Vraisemblance technique du mode opératoire", "1=Quasi impossible, 4=Facile et très automatisé", 3)
        sev = sc_s["severity"]

        operational_scenarios.append({
            "id": sc_o_id,
            "name": op_name,
            "strategic_scenario_id": sc_s["id"],
            "supporting_asset_id": sa_id,
            "kill_chain": {
                "reconnaissance": recon,
                "intrusion": intru,
                "lateral_movement": lat,
                "exploitation": expl
            },
            "severity": sev,
            "likelihood": lik
        })

        # Atelier 5 : Mesure de sécurité
        mes_id = f"MES-{idx:02d}"
        print(f"\n[Mesure de Sécurité {mes_id} pour traiter ce risque]")
        pillar = ask_choice("  Pilier ANSSI", ["Protection", "Défense", "Résilience", "Gouvernance"], "Protection")
        act = input("  Mesure concrète (ex: MFA obligatoire, segmentation réseau, EDR) : ").strip() or "MFA et segmentation réseau"
        owner = input("  Responsable de mise en œuvre (ex: Équipe Réseau, RSSI) : ").strip() or "Équipe Sécurité"
        deadline = input("  Échéance de réalisation (ex: 2027-T1) : ").strip() or "2027-T1"
        res_sev = ask_int_scale("Gravité Résiduelle après mesure", "1=Dommage négligeable, 4=Dommage toujours critique", max(1, sev - 2))
        res_lik = ask_int_scale("Vraisemblance Résiduelle après mesure", "1=Attaque devenue très peu vraisemblable, 4=Toujours très probable", 1)

        measures.append({
            "id": mes_id,
            "operational_scenario_id": sc_o_id,
            "pillar": pillar,
            "action": act,
            "responsible": owner,
            "deadline": deadline,
            "residual_risk": {
                "severity": res_sev,
                "likelihood": res_lik
            }
        })

    data = {
        "context": {
            "organization": org,
            "target_name": target,
            "perimeter": perimeter,
            "author": author,
            "date": date_str
        },
        "workshops": {
            "workshop_1_baseline": {
                "scope": {"missions": missions},
                "primary_assets": primary_assets,
                "supporting_assets": supporting_assets,
                "dreaded_events": dreaded_events,
                "security_baseline_gap_analysis": [
                    {
                        "standard": "Guide d'hygiène ANSSI",
                        "requirement": "Règle 8 : Comptes d'administration dédiés et nominatifs",
                        "compliance_status": "Appliqué sans restriction",
                        "identified_gap": "Aucun"
                    }
                ]
            },
            "workshop_2_risk_sources": {
                "sources": risk_sources
            },
            "workshop_3_strategic_scenarios": {
                "ecosystem_stakeholders": stakeholders,
                "scenarios": strategic_scenarios
            },
            "workshop_4_operational_scenarios": {
                "scenarios": operational_scenarios
            },
            "workshop_5_risk_treatment": {
                "measures": measures
            }
        }
    }

    dest = Path(filepath)
    with open(dest, "w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

    return str(dest.resolve())