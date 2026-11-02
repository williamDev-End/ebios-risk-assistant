"""Loader and YAML structure validation for EBIOS RM assessments."""

from pathlib import Path
import yaml

REQUIRED_WORKSHOPS = [
    "workshop_1_baseline",
    "workshop_2_risk_sources",
    "workshop_3_strategic_scenarios",
    "workshop_4_operational_scenarios",
    "workshop_5_risk_treatment"
]

def load_ebios_study(filepath: str) -> dict:
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"Assessment file not found: {filepath}")

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not data or "workshops" not in data:
        raise ValueError("Invalid format: 'workshops' key not found at root level.")

    workshops = data["workshops"]
    for workshop in REQUIRED_WORKSHOPS:
        if workshop not in workshops:
            raise ValueError(f"Missing required workshop section: '{workshop}'")

    return data