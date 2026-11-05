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
    action_rng = np.random.default_rng(CONFIG["seed"] + 1)
    rows = []
    action_records = []
    next_action_id = 1
    for i, pid in enumerate(ids):
        unresolved = 0
        recent_findings = []
        open_actions = []
        for j, period in enumerate(periods):
            recent_finding_count = sum(recent_findings[-6:])
            season = 1 + 0.08*np.sin(2*np.pi*j/12)
            cases = max(1, int(rng.normal(volume[i]*season, 8)))
            staff = max(1, int(rng.normal(staff0[i], 1.5)))
            caseload = cases/staff
            complaint_rate = max(0, rng.normal(
                0.018 + 0.004*max(caseload-10,0) - 0.004*quality[i], 0.008
            ))
            complaints = rng.poisson(cases*complaint_rate)
            late = max(0, int(rng.normal(
                1.5 + 0.8*unresolved + 0.7*recent_finding_count - quality[i], 3.5
            )))
            doc = float(np.clip(rng.normal(
                0.965 - 0.009*unresolved - 0.008*recent_finding_count + 0.01*quality[i], 0.02
            ), 0.75, 1.0))
            opened = rng.poisson(0.15 + 0.10*recent_finding_count)

            for _ in range(opened):
                severity = action_rng.choice(
                    ["low", "moderate", "high"],
                    p=[0.50, 0.35, 0.15],
                )
                opened_date = (
                    period.to_timestamp(how="start")
                    + pd.Timedelta(
                        days=int(action_rng.integers(0, 20))
                    )
                )
                due_days = {
                    "low": 90,
                    "moderate": 60,
                    "high": 30,
                }[severity]
                action = {
                    "action_id": next_action_id,
                    "provider_id": int(pid),
                    "opened_date": opened_date.date().isoformat(),
                    "due_date": (
                        opened_date + pd.Timedelta(days=due_days)
                    ).date().isoformat(),
                    "severity": severity,
                    "closed_date": None,
                }
                action_records.append(action)
                open_actions.append(action)
                next_action_id += 1

            closed = min(
                len(open_actions),
                rng.poisson(0.45 + 0.25*max(quality[i],0)),
            )

            open_actions.sort(
                key=lambda action: (
                    action["due_date"],
                    action["opened_date"],
                    action["action_id"],
                )
            )
            closing = open_actions[:closed]
            open_actions = open_actions[closed:]

            for action in closing:
                month_start = period.to_timestamp(how="start")
                close_date = (
                    month_start
                    + pd.Timedelta(
                        days=int(action_rng.integers(5, 28))
                    )
                )
                opened_timestamp = pd.Timestamp(action["opened_date"])
                if close_date < opened_timestamp:
                    close_date = opened_timestamp
                action["closed_date"] = close_date.date().isoformat()

            unresolved = len(open_actions)
            risk = -3.6 + 0.075*late + 3.0*max(0.93-doc,0) + 0.10*complaints + 0.16*unresolved + 0.12*recent_finding_count + 0.03*max(caseload-12,0)
            finding = rng.binomial(1, logistic(risk))
            recent_findings.append(finding)
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
    future_windows = pd.concat(
        [
            monthly.groupby("provider_id")["material_finding"].shift(-offset)
            for offset in (1, 2, 3)
        ],
        axis=1,
    )
    full_future_window = future_windows.notna().all(axis=1)
    monthly["future_material_finding"] = future_windows.max(
        axis=1,
        skipna=True,
    ).where(full_future_window)

    corrective_actions = pd.DataFrame(action_records)

    raw = ROOT / "data" / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    providers.to_csv(raw / "providers.csv", index=False)
    monthly.to_csv(raw / "provider_months.csv", index=False)
    corrective_actions.to_csv(
        raw / "corrective_actions.csv",
        index=False,
    )
    print(json.dumps({
        "providers": int(len(providers)),
        "provider_month_rows": int(len(monthly)),
        "material_findings": int(monthly["material_finding"].sum()),
        "corrective_actions": int(len(corrective_actions)),
        "open_corrective_actions": int(
            corrective_actions["closed_date"].isna().sum()
        )
    }, indent=2))

if __name__ == "__main__":
    main()
