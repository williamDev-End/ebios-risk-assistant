"""Calculs et matrices de risques EBIOS RM (Échelle officielle ANSSI)."""

RISK_LEVELS = {
    "Faible": {"min": 1, "max": 3},
    "Modéré": {"min": 4, "max": 6},
    "Élevé": {"min": 7, "max": 9},
    "Critique": {"min": 10, "max": 16}
}

SEVERITY_LABELS = {
    1: "1 - Négligeable",
    2: "2 - Modéré",
    3: "3 - Majeur",
    4: "4 - Critique"
}

LIKELIHOOD_LABELS = {
    1: "1 - Très peu vraisemblable",
    2: "2 - Peu vraisemblable",
    3: "3 - Vraisemblable",
    4: "4 - Très vraisemblable"
}

def calculate_risk_level(severity: int, likelihood: int) -> dict:
    """Calcule le score et le niveau qualitatif selon la matrice 4x4 ANSSI."""
    score = severity * likelihood

    if score <= 3:
        level = "Faible"
    elif score <= 6:
        level = "Modéré"
    elif score <= 9:
        level = "Élevé"
    else:
        level = "Critique"

    return {
        "severity": severity,
        "severity_label": SEVERITY_LABELS.get(severity, str(severity)),
        "likelihood": likelihood,
        "likelihood_label": LIKELIHOOD_LABELS.get(likelihood, str(likelihood)),
        "score": score,
        "level": level
    }