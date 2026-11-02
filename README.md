# EBIOS Risk Assistant (`ebios-risk-assistant`)

A modular, Security-as-Code command-line tool written in Python to scaffold, validate, and compute cyber risk assessments following the official ANSSI EBIOS Risk Manager methodology (Workshops 1 to 5).

---

## Overview

The EBIOS Risk Manager (EBIOS RM) framework, standardized by the French National Cybersecurity Agency (ANSSI), provides a structured, iterative approach to risk analysis across five formal workshops. Traditional assessments often rely on disjointed spreadsheets or proprietary GRC platforms. 

`ebios-risk-assistant` introduces a declarative **Security-as-Code** workflow:
1. Define all organizational assets, threat actors, attack paths, and controls in a clean, human-readable YAML document.
2. Verify relational integrity and mathematical consistency across workshops.
3. Compute initial and residual risk scores using standard 4x4 likelihood and severity matrices.
4. Export professional executive reports in Markdown containing complete tabular records and automated Mermaid workflow diagrams.

---

## Methodology Alignment (ANSSI EBIOS RM 5-Workshop Structure)

The assistant natively enforces the sequential dependencies mandated by ANSSI:

| Workshop | Name | Methodological Focus | Key Artefacts & Tables |
| :--- | :--- | :--- | :--- |
| **Workshop 1** | Scope & Security Baseline | Establish assessment perimeter and technical baseline | Missions, Primary Assets (Business Values), Supporting Assets (Technical), Dreaded Events, Baseline Gap Analysis |
| **Workshop 2** | Risk Sources | Identify, characterize, and prioritize attackers | Threat Sources, Motivation, Resource Level, Sector Activity, Relevance rating |
| **Workshop 3** | Strategic Scenarios | Map macro-level threat paths through the ecosystem | Stakeholder Threat Rating formula, Strategic Attack Vectors |
| **Workshop 4** | Operational Scenarios | Deconstruct technical intrusion and exploitation paths | 4-Phase Cyber Kill Chain (Reconnaissance, Intrusion, Lateral Movement, Exploitation), Likelihood (1-4), Severity (1-4) |
| **Workshop 5** | Risk Treatment | Establish remediation strategy and evaluate residual risk | Risk Treatment Plan structured across 4 Security Pillars (Governance, Protection, Defense, Resilience), Residual Scoring |

---

## Project Architecture

```text
ebios-risk-assistant/
│
├── ebios_assistant.py         # Main CLI entrypoint (subcommands: init, new, audit)
├── requirements.txt           # Python dependencies (PyYAML)
├── README.md                  # Project documentation and guide
│
├── core/
│   ├── __init__.py
│   ├── creator.py             # Template generator and interactive terminal wizard
│   ├── engine.py              # Cross-workshop consistency validator & computation engine
│   ├── loader.py              # YAML structure and workshop schema validator
│   └── matrix.py              # 4x4 matrix calculator (Severity x Likelihood)
│
├── exporters/
│   ├── __init__.py
│   └── markdown_report.py     # Executive Markdown generator with tables and Mermaid diagrams
│
└── examples/
    └── sample_analysis.yaml   # Comprehensive end-to-end case study (Biotech / Industrial)
```

---

## Installation & Setup

### Prerequisites
- Python 3.10 or higher
- Git
- Compatible with macOS, Linux, and Windows

### Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/ebios-risk-assistant.git
   cd ebios-risk-assistant
   ```

2. Create and activate a local Python virtual environment:
   - On macOS / Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - On Windows:
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## CLI Usage Guide

The assistant features three subcommands: `init`, `new`, and `audit`.

### 1. Generating a Blank Assessment Template (`init`)
If you prefer drafting your analysis directly in your code editor (such as VS Code), generate a pre-formatted template with guidance comments:

```bash
python ebios_assistant.py init --out my_assessment.yaml
```

### 2. Interactive Terminal Wizard (`new`)
If starting from scratch and preferring an interactive setup, the wizard prompts you for core baseline items and generates the initial YAML structure:

```bash
python ebios_assistant.py new --out my_assessment.yaml
```

### 3. Validating and Auditing an Assessment (`audit`)
Execute cross-workshop integrity checks and compute risk scores:

```bash
# Terminal output only
python ebios_assistant.py audit examples/sample_analysis.yaml

# Generate an automated Markdown report named after the organization
python ebios_assistant.py audit examples/sample_analysis.yaml --report

# Generate a report with a custom filename
python ebios_assistant.py audit examples/sample_analysis.yaml --report AUDIT_REPORT.md
```

---

## Core Calculations & Scoring Standards

### Risk Matrix Calculation (Workshops 4 & 5)
Risk is evaluated on a discrete 4x4 matrix crossing Severity (1 to 4) and Likelihood (1 to 4):

$$\text{Risk Score} = \text{Severity} \times \text{Likelihood}$$

| Risk Score Range | Qualitative Level | Operational Significance |
| :---: | :---: | :--- |
| **1 - 3** | **Low** | Risk acceptable under standard operational baselines. |
| **4 - 6** | **Moderate** | Tolerable under monitoring; low priority mitigation. |
| **7 - 9** | **High** | Requires planned treatment and managerial oversight. |
| **10 - 16** | **Critical** | Unacceptable; demands immediate remediation or operational halt. |

### Ecosystem Stakeholder Threat Rating (Workshop 3)
Stakeholder risk exposure is calculated using the official ANSSI formula:

$$\text{Threat Level} = \frac{\text{Dependency} \times \text{Penetration}}{\text{Cyber Maturity} \times \text{Trust}}$$

- **Dependency (1-4):** Reliance of primary business processes on the third party.
- **Penetration (1-4):** Technical or physical access depth granted to the third party.
- **Cyber Maturity (1-4):** Assessed technical security posture of the partner.
- **Trust (1-4):** Contractual, legal, and operational assurance established.

---

## Continuous Integration & Security Automation

Because assessments are stored in declarative YAML files, `ebios-risk-assistant` can be integrated directly into CI/CD pipelines (e.g., GitHub Actions, GitLab CI) to prevent merging invalid risk architectures or untracked operational scenarios.

### Sample GitHub Action Workflow (`.github/workflows/ebios-audit.yml`)

```yaml
name: EBIOS RM Quality Gate

on:
  pull_request:
    paths:
      - '**/*.yaml'
      - '**/*.yml'

jobs:
  validate-risk-architecture:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install Dependencies
        run: pip install -r requirements.txt

      - name: Audit Reference Assessment
        run: python ebios_assistant.py audit examples/sample_analysis.yaml --report EBIOS_AUDIT.md
```

---

## License

This project is distributed under the MIT License. See `LICENSE` for further details.