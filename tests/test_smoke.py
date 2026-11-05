from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_required_project_files_exist():
    required = [
        "README.md",
        "config/simulation.json",
        "docs/RESEARCH_DESIGN.md",
        "sql/01_schema.sql",
        "sql/02_compliance_kpis.sql",
        "sql/03_exception_monitor.sql",
        "src/generate_synthetic_data.py",
    ]
    for path in required:
        assert (ROOT / path).exists()
