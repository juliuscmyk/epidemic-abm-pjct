from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from epidemic_abm import EpidemicModel, SimulationConfig
from epidemic_abm.reporting import (
    aggregate_histories,
    summarize_history,
    write_csv,
    write_experiment_report,
)


OUTPUT_DIR = Path("outputs/experiments")
REPLICATES = 6


def main() -> None:
    base = SimulationConfig(steps=80)
    scenarios = {
        "baseline": replace(base, distancing_compliance=0.0),
        "moderate_distancing": replace(base, distancing_compliance=0.45),
        "high_distancing": replace(base, distancing_compliance=0.8),
        "high_transmission": replace(
            base, distancing_compliance=0.45, infection_probability=0.34
        ),
    }
    history_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []
    for scenario_index, (scenario, config) in enumerate(scenarios.items()):
        replicate_summaries = []
        for replicate in range(REPLICATES):
            model = EpidemicModel(replace(config, seed=1000 + scenario_index * 100 + replicate))
            model.run()
            for record in model.history:
                history_rows.append({"scenario": scenario, "replicate": replicate, **record})
            replicate_summaries.append(summarize_history(model.history))
        summary_rows.append(
            {
                "scenario": scenario,
                "runs": REPLICATES,
                "mean_peak_infected": round(
                    sum(row["peak_infected"] for row in replicate_summaries) / REPLICATES, 1
                ),
                "mean_peak_step": round(
                    sum(row["peak_step"] for row in replicate_summaries) / REPLICATES, 1
                ),
                "mean_attack_rate_percent": round(
                    sum(row["attack_rate_percent"] for row in replicate_summaries) / REPLICATES, 1
                ),
                "parameter_change": describe(scenario),
            }
        )

    mean_histories = aggregate_histories(history_rows)
    mean_rows = [record for rows in mean_histories.values() for record in rows]
    write_csv(OUTPUT_DIR / "all_histories.csv", history_rows)
    write_csv(OUTPUT_DIR / "mean_histories.csv", mean_rows)
    write_csv(OUTPUT_DIR / "scenario_summary.csv", summary_rows)
    write_experiment_report(OUTPUT_DIR / "experiment_report.html", mean_histories, summary_rows)
    print(f"Experiment report: {OUTPUT_DIR / 'experiment_report.html'}")
    print(f"Scenario summary: {OUTPUT_DIR / 'scenario_summary.csv'}")


def describe(scenario: str) -> str:
    descriptions = {
        "baseline": "0% distancing compliance",
        "moderate_distancing": "45% distancing compliance",
        "high_distancing": "80% distancing compliance",
        "high_transmission": "45% distancing, infection probability 0.34",
    }
    return descriptions[scenario]


if __name__ == "__main__":
    main()
