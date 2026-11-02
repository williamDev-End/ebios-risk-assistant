"""Logical validation engine across the 5 EBIOS RM workshops."""

from core.matrix import calculate_risk_level

def validate_study_consistency(data: dict) -> list[str]:
    """Validates structural cross-references between all workshops."""
    errors = []
    ws = data["workshops"]

    # Workshop 1 IDs
    sa_ids = {sa["id"] for sa in ws["workshop_1_baseline"].get("supporting_assets", [])}

    # Workshop 2 IDs
    rs_ids = {rs["id"] for rs in ws["workshop_2_risk_sources"].get("sources", [])}

    # Workshop 3 validation
    sc_s_ids = set()
    for sc in ws["workshop_3_strategic_scenarios"].get("scenarios", []):
        sc_s_ids.add(sc["id"])
        if sc.get("source_id") not in rs_ids:
            errors.append(f"Strategic Scenario '{sc['id']}': unknown source_id '{sc.get('source_id')}'.")

    # Workshop 4 validation
    sc_o_ids = set()
    for sc in ws["workshop_4_operational_scenarios"].get("scenarios", []):
        sc_o_ids.add(sc["id"])
        if sc.get("strategic_scenario_id") not in sc_s_ids:
            errors.append(f"Operational Scenario '{sc['id']}': strategic_scenario_id '{sc.get('strategic_scenario_id')}' not found.")
        if sc.get("supporting_asset_id") not in sa_ids:
            errors.append(f"Operational Scenario '{sc['id']}': supporting_asset_id '{sc.get('supporting_asset_id')}' not found.")

    # Workshop 5 validation
    for mes in ws["workshop_5_risk_treatment"].get("mesures", []):
        if mes.get("operational_scenario_id") not in sc_o_ids:
            errors.append(f"Measure '{mes['id']}': operational_scenario_id '{mes.get('operational_scenario_id')}' not found.")

    return errors

def compute_all_risks(data: dict) -> list[dict]:
    workshops = data.get("workshops", {})
    w4 = workshops.get("workshop_4_operational_scenarios", {})
    w5 = workshops.get("workshop_5_risk_treatment", {})

    scenarios = w4.get("scenarios", [])
    measures = w5.get("measures", [])

    results = []
    for sc in scenarios:
        sc_id = sc.get("id")
        sev = sc.get("severity", 1)
        lik = sc.get("likelihood", 1)
        baseline_risk = calculate_risk_level(sev, lik)

        # Recherche de la mesure associée au scénario
        matched_measure = next(
            (m for m in measures if m.get("operational_scenario_id") == sc_id),
            None
        )

        residual_risk = None
        if matched_measure and "residual_risk" in matched_measure:
            res_meta = matched_measure["residual_risk"]
            r_sev = res_meta.get("severity", sev)
            r_lik = res_meta.get("likelihood", lik)
            residual_risk = calculate_risk_level(r_sev, r_lik)

        results.append({
            "scenario": sc,
            "baseline": baseline_risk,
            "measure": matched_measure,
            "residual": residual_risk
        })

    return results