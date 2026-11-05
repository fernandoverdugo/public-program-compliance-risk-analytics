import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "config" / "simulation.json").read_text())

def logistic(x):
    return 1 / (1 + np.exp(-x))

def main():
    rng = np.random.default_rng(CONFIG["seed"])
    n = CONFIG["providers"]
    months = CONFIG["months"]
    ids = np.arange(1, n + 1)
    ptype = rng.choice(CONFIG["provider_types"], size=n, p=[0.55,0.30,0.15])
    region = rng.choice(CONFIG["regions"], size=n)
    volume = rng.lognormal(4.2, 0.45, size=n)
    staff0 = np.maximum(3, np.round(volume / rng.uniform(8,15,size=n))).astype(int)
    quality = rng.normal(0,1,size=n)

    providers = pd.DataFrame({
        "provider_id": ids,
        "provider_type": ptype,
        "region": region,
        "baseline_monthly_cases": np.round(volume).astype(int),
        "baseline_staff": staff0,
    })

    periods = pd.period_range(CONFIG["start_month"], periods=months, freq="M")
    rows = []
    for i, pid in enumerate(ids):
        unresolved = 0
        prior_findings = 0
        for j, period in enumerate(periods):
            season = 1 + 0.08*np.sin(2*np.pi*j/12)
            cases = max(1, int(rng.normal(volume[i]*season, 8)))
            staff = max(1, int(rng.normal(staff0[i], 1.5)))
            caseload = cases/staff
            complaint_rate = max(0, rng.normal(
                0.018 + 0.004*max(caseload-10,0) - 0.004*quality[i], 0.008
            ))
            complaints = rng.poisson(cases*complaint_rate)
            late = max(0, int(rng.normal(
                1.5 + 1.2*unresolved + 0.4*prior_findings - quality[i], 3.5
            )))
            doc = float(np.clip(rng.normal(
                0.965 - 0.012*unresolved - 0.006*prior_findings + 0.01*quality[i], 0.02
            ), 0.75, 1.0))
            opened = rng.poisson(0.15 + 0.15*prior_findings)
            closed = min(unresolved + opened, rng.poisson(0.35 + 0.25*max(quality[i],0)))
            unresolved = max(0, unresolved + opened - closed)
            risk = -3.1 + 0.085*late + 3.2*max(0.93-doc,0) + 0.11*complaints + 0.18*unresolved + 0.10*prior_findings + 0.035*max(caseload-12,0)
            finding = rng.binomial(1, logistic(risk))
            prior_findings += finding
            rows.append({
                "provider_id": int(pid),
                "month": str(period),
                "case_volume": cases,
                "staff_count": staff,
                "caseload_per_staff": round(caseload,3),
                "complaints": int(complaints),
                "complaint_rate": round(complaint_rate,5),
                "report_days_late": late,
                "documentation_complete_rate": round(doc,5),
                "unresolved_corrective_actions": int(unresolved),
                "material_finding": int(finding),
            })

    monthly = pd.DataFrame(rows).sort_values(["provider_id","month"])
    monthly["future_material_finding"] = (
        monthly.groupby("provider_id")["material_finding"]
        .transform(lambda s: s.shift(-1).rolling(3, min_periods=1).max())
    )

    raw = ROOT / "data" / "raw"
    providers.to_csv(raw / "providers.csv", index=False)
    monthly.to_csv(raw / "provider_months.csv", index=False)
    print(json.dumps({
        "providers": int(len(providers)),
        "provider_month_rows": int(len(monthly)),
        "material_findings": int(monthly["material_finding"].sum())
    }, indent=2))

if __name__ == "__main__":
    main()
