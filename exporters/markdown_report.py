"""Générateur de rapport formel EBIOS RM (ANSSI) en Markdown avec graphiques Mermaid."""

def generate_markdown(data: dict, risk_results: list) -> str:
    ctx = data.get("context", {})
    ws = data.get("workshops", {})
    md = []

    org_name = ctx.get("organization", "Organisation Évaluée")
    target_name = ctx.get("target_name", "Système Cible")

    # En-tête officiel
    md.append(f"# Rapport d'Analyse de Risques EBIOS RM : {org_name}\n")
    md.append(f"- **Objet de l'étude :** {target_name}")
    md.append(f"- **Périmètre d'analyse :** {ctx.get('perimeter', 'Non précisé')}")
    md.append(f"- **Date de l'étude :** {ctx.get('date', 'N/A')}")
    md.append(f"- **Pilote de l'analyse :** {ctx.get('author', 'Non précisé')}\n")
    md.append("---\n")

    # Cartographie visuelle Mermaid
    md.append("## Cartographie Globale des Chemins d'Attaque\n")
    md.append("Le diagramme ci-dessous illustre l'alignement des 5 ateliers : de la source de menace jusqu'aux composants techniques cibles :\n")
    md.append("```mermaid")
    md.append("graph LR")
    md.append("    subgraph SR [Atelier 2 : Sources de Risques]")
    for rs in ws.get("workshop_2_risk_sources", {}).get("sources", []):
        md.append(f"        {rs['id']}[\"{rs['id']}: {rs['name']}\"]")
    md.append("    end")

    md.append("    subgraph SS [Atelier 3 : Scénarios Stratégiques]")
    for sc_s in ws.get("workshop_3_strategic_scenarios", {}).get("scenarios", []):
        md.append(f"        {sc_s['id']}[\"{sc_s['id']}: {sc_s['name']}\"]")
    md.append("    end")

    md.append("    subgraph SO [Atelier 4 : Scénarios Opérationnels]")
    for item in risk_results:
        sc = item["scenario"]
        md.append(f"        {sc['id']}[\"{sc['id']}: {sc['name']}<br/>Risque Brut : {item['baseline']['level']}\"]")
    md.append("    end")

    md.append("    subgraph BS [Atelier 1 : Biens Supports]")
    for sa in ws.get("workshop_1_baseline", {}).get("supporting_assets", []):
        md.append(f"        {sa['id']}[\"{sa['id']}: {sa['name']}\"]")
    md.append("    end")

    for sc_s in ws.get("workshop_3_strategic_scenarios", {}).get("scenarios", []):
        md.append(f"    {sc_s.get('source_id')} --> {sc_s['id']}")
    for item in risk_results:
        sc = item["scenario"]
        md.append(f"    {sc.get('strategic_scenario_id')} --> {sc['id']}")
        md.append(f"    {sc['id']} --> {sc.get('supporting_asset_id')}")

    md.append("```\n")
    md.append("---\n")

    # Atelier 1
    w1 = ws.get("workshop_1_baseline", {})
    md.append("## Atelier 1 : Cadrage et Socle de Sécurité\n")

    md.append("### 1.1 Missions de l'Organisation")
    for mission in w1.get("scope", {}).get("missions", []):
        md.append(f"- {mission}")
    md.append("")

    md.append("### 1.2 Cartographie des Actifs (Valeurs Métiers & Biens Supports)")
    md.append("| ID Valeur Métier | Intitulé de la Valeur Métier | Nature | Propriétaire Métier |")
    md.append("| :--- | :--- | :--- | :--- |")
    for pa in w1.get("primary_assets", []):
        md.append(f"| **{pa['id']}** | {pa['name']} | {pa.get('category', 'Processus')} | {pa.get('business_owner', '-')} |")
    md.append("")

    md.append("| ID Bien Support | Intitulé du Bien Support | Nature Technique | Responsable Technique |")
    md.append("| :--- | :--- | :--- | :--- |")
    for sa in w1.get("supporting_assets", []):
        md.append(f"| **{sa['id']}** | {sa['name']} | {sa.get('type', '-')} | {sa.get('technical_owner', '-')} |")
    md.append("")

    md.append("### 1.3 Événements Redoutés et Besoins de Sécurité")
    md.append("| ID Sinistre | Valeur Métier Liée | Description de l'Événement Redouté | Impacts Subis | Gravité (1 à 4) |")
    md.append("| :--- | :--- | :--- | :--- | :---: |")
    for de in w1.get("dreaded_events", []):
        md.append(f"| **{de['id']}** | `{de.get('primary_asset_id', '-')}` | {de['description']} | {de.get('impact_nature', '-')} | Niveau {de.get('severity', '-')} / 4 |")
    md.append("")

    md.append("### 1.4 Analyse des Écarts du Socle de Sécurité (Gap Analysis)")
    md.append("| Référentiel Évalué | Règle / Exigence Analysée | Statut de Conformité | Justification de l'Écart |")
    md.append("| :--- | :--- | :--- | :--- |")
    for gap in w1.get("security_baseline_gap_analysis", []):
        md.append(f"| **{gap['standard']}** | {gap['requirement']} | {gap['compliance_status']} | {gap['identified_gap']} |")
    md.append("\n---\n")

    # Atelier 2
    w2 = ws.get("workshop_2_risk_sources", {})
    md.append("## Atelier 2 : Sources de Risques (SR)\n")
    md.append("| ID Source | Profil de l'Attaquant | Motivation & Objectif | Ressources | Activité dans le Secteur | Pertinence |")
    md.append("| :--- | :--- | :--- | :---: | :---: | :---: |")
    for rs in w2.get("sources", []):
        md.append(f"| **{rs['id']}** | {rs['name']} | {rs.get('motivation', '-')} | {rs.get('resources', '-')} | {rs.get('activity_level', '-')} | **{rs.get('relevance', '-')}** |")
    md.append("\n---\n")

    # Atelier 3
    w3 = ws.get("workshop_3_strategic_scenarios", {})
    md.append("## Atelier 3 : Écosystème et Scénarios Stratégiques\n")

    md.append("### 3.1 Évaluation de la Menace des Tiers (Formule ANSSI)")
    md.append("Formule officielle : `Niveau de Menace = (Dépendance x Pénétration) / (Maturité Cyber x Confiance)`\n")
    md.append("| ID Tiers | Entité / Prestataire | Catégorie | Dép. (1-4) | Pén. (1-4) | Mat. (1-4) | Conf. (1-4) | Score Menace | Niveau de Menace |")
    md.append("| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |")
    for stk in w3.get("ecosystem_stakeholders", []):
        dep = stk.get("dependency", 1)
        pen = stk.get("penetration", 1)
        mat = stk.get("cyber_maturity", 1)
        tru = stk.get("trust", 1)
        score = (dep * pen) / max(1, (mat * tru))
        level = "Critique" if score >= 3.0 else ("Élevé" if score >= 2.0 else ("Modéré" if score >= 1.0 else "Faible"))
        md.append(f"| **{stk['id']}** | {stk['name']} | {stk.get('category', '-')} | {dep} | {pen} | {mat} | {tru} | {score:.2f} | **{level}** |")
    md.append("")

    md.append("### 3.2 Scénarios Stratégiques Retenus")
    md.append("| ID Scénario | Vecteur d'Attaque Stratégique | Source de Risque | Sinistre Visé | Gravité Héritée |")
    md.append("| :--- | :--- | :---: | :---: | :---: |")
    for sc_s in w3.get("scenarios", []):
        md.append(f"| **{sc_s['id']}** | {sc_s['name']} | `{sc_s.get('source_id', '-')}` | `{sc_s.get('dreaded_event_id', '-')}` | Niveau {sc_s.get('severity', 4)} / 4 |")
    md.append("\n---\n")

    # Atelier 4
    md.append("## Atelier 4 : Scénarios Opérationnels et Modèle d'Attaque\n")
    md.append("| ID Scénario | Scénario Opérationnel | Bien Support Ciblé | Gravité | Vraisemblance | Score Brut | Risque Brut |")
    md.append("| :--- | :--- | :---: | :---: | :---: | :---: | :---: |")
    for item in risk_results:
        sc = item["scenario"]
        b = item["baseline"]
        md.append(f"| **{sc['id']}** | {sc['name']} | `{sc['supporting_asset_id']}` | {b['severity']}/4 | {b['likelihood']}/4 | {b['score']}/16 | **{b['level']}** |")
    md.append("")

    md.append("### 4.1 Décomposition du Mode Opératoire en 4 Phases (Modèle ANSSI)")
    for item in risk_results:
        sc = item["scenario"]
        kc = sc.get("kill_chain", {})
        if kc:
            md.append(f"#### Mode Opératoire `{sc['id']}` : {sc['name']}")
            md.append(f"- **1. Connaître (Reconnaissance) :** {kc.get('reconnaissance', '-')}")
            md.append(f"- **2. Rentrer (Intrusion initiale) :** {kc.get('intrusion', '-')}")
            md.append(f"- **3. Trouver (Mouvement latéral) :** {kc.get('lateral_movement', '-')}")
            md.append(f"- **4. Exploiter (Action sur l'objectif) :** {kc.get('exploitation', '-')}\n")
    md.append("---\n")

    # Atelier 5
    md.append("## Atelier 5 : Plan de Traitement du Risque et Risque Résiduel\n")
    md.append("| Scénario Opérationnel | Risque Brut | Pilier ANSSI | Mesure de Traitement Retenue | Responsable | Échéance | Risque Résiduel | Gain |")
    md.append("| :--- | :---: | :---: | :--- | :--- | :---: | :---: | :---: |")
    for item in risk_results:
        sc = item["scenario"]
        b_level = item["baseline"]["level"]
        m = item["measure"]
        res = item["residual"]
        res_level = res["level"] if res else "Non traité"

        if m:
            action = m.get("action", "-")
            pillar = m.get("pillar", "Protection")
            owner = m.get("responsible", "-")
            date_target = m.get("deadline", "-")
            outcome = f"{b_level} -> {res_level}"
        else:
            action = "Aucune mesure planifiée"
            pillar = "Acceptation"
            owner = "-"
            date_target = "-"
            outcome = "Aucun"

        md.append(f"| **{sc['id']}** | {b_level} | {pillar} | {action} | {owner} | {date_target} | **{res_level}** | {outcome} |")

    return "\n".join(md)