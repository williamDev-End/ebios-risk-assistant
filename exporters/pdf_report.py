"""Générateur exécutif PDF officiel EBIOS RM (ANSSI) via WeasyPrint."""

from pathlib import Path
from weasyprint import HTML

def render_matrix_table(title: str, scenario_points: list[dict], is_residual: bool = False) -> str:
    """Génère une matrice 4x4 rigoureusement calibrée en tableau HTML."""
    scores = {
        4: [4, 8, 12, 16],
        3: [3, 6, 9, 12],
        2: [2, 4, 6, 8],
        1: [1, 2, 3, 4]
    }
    
    html = f"""
    <div class="matrix-wrapper">
        <div class="matrix-title">{title}</div>
        <table class="table-matrix">
            <colgroup>
                <col style="width: 14mm;">
                <col style="width: 16mm;">
                <col style="width: 16mm;">
                <col style="width: 16mm;">
                <col style="width: 16mm;">
            </colgroup>
            <thead>
                <tr>
                    <th class="th-axis">G \\ V</th>
                    <th class="th-col">V1</th>
                    <th class="th-col">V2</th>
                    <th class="th-col">V3</th>
                    <th class="th-col">V4</th>
                </tr>
            </thead>
            <tbody>
    """
    for g in [4, 3, 2, 1]:
        html += f"<tr><th class=\"th-row\">G{g}</th>"
        for v in [1, 2, 3, 4]:
            score = scores[g][v - 1]
            if score <= 3:
                color_class = "c-low"
            elif score <= 6:
                color_class = "c-mod"
            elif score <= 9:
                color_class = "c-high"
            else:
                color_class = "c-crit"
            
            active_labels = []
            for sp in scenario_points:
                key = "residual" if is_residual else "baseline"
                s_data = sp.get(key) or {}
                if s_data.get("severity") == g and s_data.get("likelihood") == v:
                    active_labels.append(sp.get("label", "•"))
            
            if active_labels:
                markers = f"<div class=\"cell-markers\">{' '.join(active_labels)}</div>"
                cell_class = f"cell-score {color_class} cell-active"
            else:
                markers = ""
                cell_class = f"cell-score {color_class}"
                
            html += f"<td class=\"{cell_class}\"><span class=\"score-num\">{score}</span>{markers}</td>"
        html += "</tr>"
        
    html += """
            </tbody>
        </table>
    </div>
    """
    return html


def generate_pdf_report(data: dict, risk_results: list, output_filepath: str) -> str:
    ctx = data.get("context", {})
    ws = data.get("workshops", {})

    org = ctx.get("organization", "Organisation Évaluée")
    target = ctx.get("target_name", "Système Cible")
    perimeter = ctx.get("perimeter", "Périmètre Opérationnel")
    author = ctx.get("author", "Équipe Cybersécurité")
    date_str = ctx.get("date", "02/11/2026")

    w1 = ws.get("workshop_1_baseline", {})
    w2 = ws.get("workshop_2_risk_sources", {})
    w3 = ws.get("workshop_3_strategic_scenarios", {})
    w5 = ws.get("workshop_5_risk_treatment", {})

    html_template = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Rapport EBIOS RM - {org}</title>
    <style>
        @page {{
            size: A4 portrait;
            margin: 14mm 14mm 16mm 14mm;
            @bottom-left {{
                content: "ANSSI EBIOS RM — Diffusion Restreinte : {org}";
                font-size: 8pt;
                color: #64748b;
            }}
            @bottom-right {{
                content: "Page " counter(page) " / " counter(pages);
                font-size: 8pt;
                color: #64748b;
            }}
        }}
        *, *::before, *::after {{ box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            color: #1e293b;
            font-size: 8.5pt;
            line-height: 1.4;
            margin: 0;
            padding: 0;
        }}
        .page-break {{ page-break-before: always; }}
        .header-banner {{
            border-bottom: 2px solid #002e6c;
            padding-bottom: 5px;
            margin-bottom: 10px;
        }}
        .doc-category {{
            font-size: 8pt;
            font-weight: 700;
            color: #002e6c;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}
        h1 {{
            font-size: 14pt;
            color: #0f172a;
            margin: 2px 0 0 0;
            font-weight: 700;
        }}
        .meta-grid {{
            display: flex;
            justify-content: space-between;
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-left: 4px solid #002e6c;
            padding: 6px 12px;
            margin-bottom: 10px;
        }}
        .meta-grid p {{ margin: 2px 0; font-size: 8.5pt; }}
        h2 {{
            font-size: 9.5pt;
            color: #002e6c;
            background: #f1f5f9;
            border-left: 3px solid #002e6c;
            padding: 4px 8px;
            margin: 10px 0 5px 0;
            text-transform: uppercase;
        }}
        h3 {{
            font-size: 8.5pt;
            color: #334155;
            margin: 8px 0 4px 0;
            text-transform: uppercase;
        }}
        .missions-box {{
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            padding: 6px 12px;
            margin-bottom: 8px;
            font-size: 8pt;
        }}
        .missions-box ul {{ margin: 2px 0; padding-left: 18px; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 8pt;
            margin-bottom: 8px;
        }}
        th, td {{
            border: 1px solid #cbd5e1;
            padding: 4px 6px;
            text-align: left;
            vertical-align: middle;
        }}
        th {{
            background: #f8fafc;
            color: #002e6c;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 7.5pt;
        }}
        .text-center {{ text-align: center; }}
        .badge {{
            display: inline-block;
            padding: 2px 5px;
            font-weight: 700;
            font-size: 7pt;
            border-radius: 2px;
            text-transform: uppercase;
        }}
        .badge-faible {{ background-color: #dcfce7; color: #166534; }}
        .badge-modéré {{ background-color: #fef9c3; color: #854d0e; }}
        .badge-élevé {{ background-color: #ffedd5; color: #9a3412; }}
        .badge-critique {{ background-color: #fee2e2; color: #991b1b; }}

        /* Kill Chain Styles */
        .chain-box {{
            margin-bottom: 10px;
            border: 1px solid #cbd5e1;
            background: #ffffff;
        }}
        .chain-title {{
            background: #f1f5f9;
            padding: 4px 8px;
            font-size: 8pt;
            font-weight: 700;
            color: #002e6c;
            border-bottom: 1px solid #cbd5e1;
        }}
        .table-killchain {{
            width: 100%;
            border-collapse: collapse;
            table-layout: fixed;
            margin-bottom: 0;
        }}
        .table-killchain th {{
            background: #ffffff;
            color: #002e6c;
            border-bottom: 2px solid #002e6c;
            padding: 3px 6px;
            font-size: 7.5pt;
        }}
        .table-killchain td {{
            background: #f8fafc;
            padding: 5px 6px;
            font-size: 7.5pt;
            vertical-align: top;
            height: 52px;
        }}

        /* Matrices 4x4 */
        .matrices-flex {{
            display: flex;
            gap: 16px;
            margin: 8px 0 10px 0;
        }}
        .matrix-wrapper {{
            flex: 1;
            border: 1px solid #cbd5e1;
            padding: 6px;
            background: #ffffff;
        }}
        .matrix-title {{
            font-size: 8pt;
            font-weight: 700;
            color: #002e6c;
            text-align: center;
            margin-bottom: 6px;
            text-transform: uppercase;
        }}
        .table-matrix {{
            width: 78mm;
            margin: 0 auto;
            border-collapse: collapse;
            table-layout: fixed;
        }}
        .table-matrix th, .table-matrix td {{
            border: 1px solid #94a3b8;
            text-align: center;
            padding: 1px 0;
            height: 24px;
            vertical-align: middle;
            box-sizing: border-box;
        }}
        .th-axis {{ background: #e2e8f0; font-size: 6.5pt; font-weight: 700; }}
        .th-col, .th-row {{ background: #f1f5f9; font-size: 7pt; font-weight: 700; color: #002e6c; }}
        
        .score-num {{ 
            display: block; 
            font-size: 7pt; 
            font-weight: 700;
            line-height: 1;
            color: #1e293b; 
        }}
        
        .cell-markers {{
            display: inline-block;
            font-size: 5.5pt;
            font-weight: 800;
            color: #ffffff;
            background: #002e6c;
            border-radius: 2px;
            padding: 0 2px;
            line-height: 1.1;
            margin-top: 1px;
            white-space: nowrap;
        }}
        .c-low {{ background-color: #dcfce7; }}
        .c-mod {{ background-color: #fef9c3; }}
        .c-high {{ background-color: #fed7aa; }}
        .c-crit {{ background-color: #fee2e2; }}
        .cell-active {{
            outline: 2px solid #002e6c;
            outline-offset: -1px;
        }}
        .matrix-legend {{
            font-size: 7.5pt;
            color: #475569;
            margin-bottom: 8px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <!-- PAGE 1 : ATELIER 1 -->
    <header class="header-banner">
        <div class="doc-category">ANSSI — Méthode EBIOS Risk Manager</div>
        <div style="display: flex; justify-content: space-between; align-items: flex-end;">
            <h1>Dossier d'Homologation et d'Analyse de Risques</h1>
            <span class="badge badge-critique">Diffusion Restreinte</span>
        </div>
    </header>

    <div class="meta-grid">
        <div>
            <p><strong>Organisation :</strong> {org}</p>
            <p><strong>Cible :</strong> {target}</p>
            <p><strong>Périmètre :</strong> {perimeter}</p>
        </div>
        <div>
            <p><strong>Date de l'étude :</strong> {date_str}</p>
            <p><strong>Pilote :</strong> {author}</p>
            <p><strong>Statut :</strong> Finalisé post-Atelier 5</p>
        </div>
    </div>

    <h2>Atelier 1 : Cadrage, Actifs & Socle de Sécurité</h2>
    
    <h3>1.1 Missions Principales de l'Organisation</h3>
    <div class="missions-box">
        <ul>"""

    for m in w1.get("scope", {}).get("missions", []):
        html_template += f"<li>{m}</li>"

    html_template += """
        </ul>
    </div>

    <h3>1.2 Cartographie des Valeurs Métiers et Événements Redoutés</h3>
    <table>
        <thead>
            <tr>
                <th style="width: 10%;">ID</th>
                <th style="width: 25%;">Valeur Métier</th>
                <th class="text-center" style="width: 12%;">D / I / C</th>
                <th style="width: 40%;">Événement Redouté</th>
                <th class="text-center" style="width: 13%;">Gravité</th>
            </tr>
        </thead>
        <tbody>"""

    for pa in w1.get("primary_assets", []):
        crit = pa.get("security_criteria", {})
        d = crit.get("availability", "-")
        i = crit.get("integrity", "-")
        c = crit.get("confidentiality", "-")
        matched_de = next((de for de in w1.get("dreaded_events", []) if de.get("primary_asset_id") == pa["id"]), {})
        sev = matched_de.get("severity", "-")
        badge_cls = "badge-critique" if sev == 4 else ("badge-élevé" if sev == 3 else "badge-modéré")
        html_template += f"""
            <tr>
                <td><strong>{pa['id']}</strong></td>
                <td>{pa['name']}</td>
                <td class="text-center"><strong>{d} / {i} / {c}</strong></td>
                <td>{matched_de.get('description', '-')}</td>
                <td class="text-center"><span class="badge {badge_cls}">Niveau {sev}</span></td>
            </tr>"""

    html_template += """
        </tbody>
    </table>

    <h3>1.3 Biens Supports Associés</h3>
    <table>
        <thead>
            <tr>
                <th style="width: 10%;">ID</th>
                <th style="width: 35%;">Bien Support</th>
                <th style="width: 30%;">Nature Technique</th>
                <th style="width: 25%;">Responsable Technique</th>
            </tr>
        </thead>
        <tbody>"""

    for sa in w1.get("supporting_assets", []):
        html_template += f"""
            <tr>
                <td><strong>{sa['id']}</strong></td>
                <td>{sa['name']}</td>
                <td>{sa.get('type', '-')}</td>
                <td>{sa.get('technical_owner', '-')}</td>
            </tr>"""

    html_template += """
        </tbody>
    </table>

    <h3>1.4 Analyse des Écarts du Socle de Sécurité (Gap Analysis)</h3>
    <table>
        <thead>
            <tr>
                <th style="width: 25%;">Référentiel</th>
                <th style="width: 35%;">Exigence Analysée</th>
                <th style="width: 20%;">Conformité</th>
                <th style="width: 20%;">Écart Identifié</th>
            </tr>
        </thead>
        <tbody>"""

    for gap in w1.get("security_baseline_gap_analysis", []):
        status = gap.get("compliance_status", "-")
        is_full = "sans restriction" in status.lower()
        badge_cls = "badge-faible" if is_full else "badge-modéré"
        html_template += f"""
            <tr>
                <td><strong>{gap['standard']}</strong></td>
                <td>{gap['requirement']}</td>
                <td><span class="badge {badge_cls}">{status}</span></td>
                <td>{gap.get('identified_gap', 'Aucun')}</td>
            </tr>"""

    html_template += """
        </tbody>
    </table>

    <!-- PAGE 2 : ATELIERS 2 & 3 -->
    <div class="page-break"></div>
    <header class="header-banner">
        <div class="doc-category">ANSSI — Méthode EBIOS Risk Manager</div>
        <h1>Ateliers 2 & 3 : Sources de Risques et Scénarios Stratégiques</h1>
    </header>

    <h2>Atelier 2 : Sources de Risques Retenues</h2>
    <table>
        <thead>
            <tr>
                <th style="width: 10%;">ID</th>
                <th style="width: 25%;">Profil de l'Attaquant</th>
                <th style="width: 35%;">Motivation & Objectif</th>
                <th class="text-center" style="width: 15%;">Ressources</th>
                <th class="text-center" style="width: 15%;">Activité</th>
            </tr>
        </thead>
        <tbody>"""

    for rs in w2.get("sources", []):
        html_template += f"""
            <tr>
                <td><strong>{rs['id']}</strong></td>
                <td>{rs['name']}</td>
                <td>{rs.get('motivation', '-')}</td>
                <td class="text-center">{rs.get('resources', '-')}</td>
                <td class="text-center">{rs.get('activity_level', '-')}</td>
            </tr>"""

    html_template += """
        </tbody>
    </table>

    <h2>Atelier 3 : Cartographie de l'Écosystème & Menace des Tiers</h2>
    <p style="font-size: 7.5pt; color: #64748b; margin-top: -3px; margin-bottom: 6px;">
        Formule officielle ANSSI : <code>Niveau de Menace = (Dépendance x Pénétration) / (Maturité x Confiance)</code>
    </p>
    <table>
        <thead>
            <tr>
                <th style="width: 10%;">ID</th>
                <th style="width: 30%;">Partie Prenante (Tiers)</th>
                <th style="width: 20%;">Catégorie</th>
                <th class="text-center" style="width: 20%;">Dép / Pén / Mat / Conf</th>
                <th class="text-center" style="width: 20%;">Menace Calculée</th>
            </tr>
        </thead>
        <tbody>"""

    for stk in w3.get("ecosystem_stakeholders", []):
        dep, pen = stk.get("dependency", 1), stk.get("penetration", 1)
        mat, tru = stk.get("cyber_maturity", 1), stk.get("trust", 1)
        score = (dep * pen) / max(1, (mat * tru))
        level = "Critique" if score >= 3.0 else ("Élevé" if score >= 2.0 else ("Modéré" if score >= 1.0 else "Faible"))
        badge_cls = f"badge-{level.lower()}"
        html_template += f"""
            <tr>
                <td><strong>{stk['id']}</strong></td>
                <td>{stk['name']}</td>
                <td>{stk.get('category', '-')}</td>
                <td class="text-center">{dep} / {pen} / {mat} / {tru}</td>
                <td class="text-center"><span class="badge {badge_cls}">Score {score:.2f} ({level})</span></td>
            </tr>"""

    html_template += """
        </tbody>
    </table>

    <h2>Atelier 3 : Scénarios Stratégiques Retenus</h2>
    <table>
        <thead>
            <tr>
                <th style="width: 10%;">ID</th>
                <th style="width: 30%;">Scénario Stratégique</th>
                <th style="width: 15%;">Attaquant</th>
                <th style="width: 30%;">Vecteur d'Attaque</th>
                <th class="text-center" style="width: 15%;">Gravité</th>
            </tr>
        </thead>
        <tbody>"""

    for sc_s in w3.get("scenarios", []):
        html_template += f"""
            <tr>
                <td><strong>{sc_s['id']}</strong></td>
                <td>{sc_s['name']}</td>
                <td><code>{sc_s.get('source_id', '-')}</code></td>
                <td>{sc_s.get('attack_path', '-')}</td>
                <td class="text-center"><span class="badge badge-critique">Niveau {sc_s.get('severity', 4)}</span></td>
            </tr>"""

    html_template += """
        </tbody>
    </table>

    <!-- PAGE 3 : ATELIER 4 -->
    <div class="page-break"></div>
    <header class="header-banner">
        <div class="doc-category">ANSSI — Méthode EBIOS Risk Manager</div>
        <h1>Atelier 4 : Scénarios Opérationnels & Modes Opératoires</h1>
    </header>

    <h2>Décomposition des Modes Opératoires en 4 Phases (Kill Chain ANSSI)</h2>"""

    # Préparation des points pour les matrices
    scenario_points = []
    for idx, item in enumerate(risk_results, 1):
        sc = item["scenario"]
        label = f"S{idx}"
        scenario_points.append({
            "label": label,
            "id": sc["id"],
            "name": sc["name"],
            "baseline": item.get("baseline", {}),
            "residual": item.get("residual", {})
        })

        kc = sc.get("kill_chain", {})
        b = item["baseline"]
        html_template += f"""
    <div class="chain-box">
        <div class="chain-title">
            <strong>[{label}] {sc['id']} : {sc['name']}</strong> &bull; Bien Support : <code>{sc.get('supporting_asset_id', '-')}</code> &bull; Score Brut : <strong>G{b['severity']} &times; V{b['likelihood']} ({b['level']})</strong>
        </div>
        <table class="table-killchain">
            <thead>
                <tr>
                    <th style="width: 25%;">1. Connaître (Reconnaissance)</th>
                    <th style="width: 25%;">2. Rentrer (Intrusion initiale)</th>
                    <th style="width: 25%;">3. Trouver (Mouvement latéral)</th>
                    <th style="width: 25%;">4. Exploiter (Action finale)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>{kc.get('reconnaissance', '-')}</td>
                    <td>{kc.get('intrusion', '-')}</td>
                    <td>{kc.get('lateral_movement', '-')}</td>
                    <td>{kc.get('exploitation', '-')}</td>
                </tr>
            </tbody>
        </table>
    </div>"""

    # PAGE 4 : ATELIER 5
    matrix_brute_html = render_matrix_table("Matrice des Risques Bruts", scenario_points, is_residual=False)
    matrix_residuelle_html = render_matrix_table("Matrice des Risques Résiduels", scenario_points, is_residual=True)

    legend_items = " &nbsp;|&nbsp; ".join([f"<strong>{sp['label']}</strong> = {sp['id']} ({sp['name'][:28]}...)" for sp in scenario_points])

    html_template += f"""
    <!-- PAGE 4 : ATELIER 5 -->
    <div class="page-break"></div>
    <header class="header-banner">
        <div class="doc-category">ANSSI — Méthode EBIOS Risk Manager</div>
        <h1>Atelier 5 : Matrice des Risques 4x4 & Plan de Traitement</h1>
    </header>

    <h2>Évaluation Matricielle des Risques (Brut vs Résiduel)</h2>
    <div class="matrix-legend">Légende des scénarios : {legend_items}</div>
    <div class="matrices-flex">
        {matrix_brute_html}
        {matrix_residuelle_html}
    </div>

    <h2>Plan d'Action et Traitement du Risque</h2>
    <table>
        <thead>
            <tr>
                <th style="width: 8%;">ID</th>
                <th style="width: 14%;">Scénario</th>
                <th style="width: 12%;">Pilier</th>
                <th style="width: 36%;">Mesure de Sécurité</th>
                <th style="width: 16%;">Responsable & Échéance</th>
                <th class="text-center" style="width: 14%;">Évolution</th>
            </tr>
        </thead>
        <tbody>"""

    # Résolution robuste des mesures (depuis risk_results ou directement w5.measures)
    raw_measures = w5.get("measures", [])
    for item in risk_results:
        sc = item["scenario"]
        m = item.get("measure")
        
        # Si la mesure n'est pas attachée dans item, on la cherche dans les données YAML brutes
        if not m:
            m = next((rm for rm in raw_measures if rm.get("operational_scenario_id") == sc["id"]), None)

        b_lvl = item['baseline']['level']
        res_info = item.get('residual')
        r_lvl = res_info['level'] if res_info else 'Non traité'
        badge_cls = f"badge-{r_lvl.lower()}"

        if m:
            m_id = m.get("id", "MES")
            pillar = m.get("pillar", "Protection")
            action = m.get("action", "-")
            resp = f"{m.get('responsible', '-')}<br/><span style='color:#64748b;'>{m.get('deadline', '-')}</span>"
        else:
            m_id = "-"
            pillar = "Acceptation"
            action = "Risque accepté sans mesure spécifique"
            resp = "-"

        html_template += f"""
            <tr>
                <td><strong>{m_id}</strong></td>
                <td><code>{sc['id']}</code></td>
                <td><strong>{pillar}</strong></td>
                <td>{action}</td>
                <td>{resp}</td>
                <td class="text-center"><span class="badge {badge_cls}">{b_lvl} &rarr; {r_lvl}</span></td>
            </tr>"""

    html_template += """
        </tbody>
    </table>
</body>
</html>"""

    HTML(string=html_template).write_pdf(output_filepath)
    return output_filepath