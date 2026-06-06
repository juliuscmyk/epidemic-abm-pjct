from __future__ import annotations

import argparse
from pathlib import Path

from epidemic_abm import EpidemicModel, SimulationConfig
from epidemic_abm.reporting import summarize_history, write_csv, write_demo_html


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run one epidemic ABM simulation.")
    parser.add_argument("--population", type=int, default=180)
    parser.add_argument("--grid-size", type=int, default=16)
    parser.add_argument("--initial-infected", type=int, default=5)
    parser.add_argument("--infection-probability", type=float, default=0.30)
    parser.add_argument("--recovery-steps", type=int, default=14)
    parser.add_argument("--movement-probability", type=float, default=0.92)
    parser.add_argument("--distancing-compliance", type=float, default=0.35)
    parser.add_argument("--steps", type=int, default=80)
    parser.add_argument("--seed", type=int, default=21)
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/single_run"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = SimulationConfig(
        population=args.population,
        width=args.grid_size,
        height=args.grid_size,
        initial_infected=args.initial_infected,
        infection_probability=args.infection_probability,
        recovery_steps=args.recovery_steps,
        movement_probability=args.movement_probability,
        distancing_compliance=args.distancing_compliance,
        steps=args.steps,
        seed=args.seed,
    )
    model = EpidemicModel(config)
    snapshots = model.run(capture_snapshots=True)
    summary = summarize_history(model.history)
    write_csv(args.output_dir / "history.csv", model.history)
    write_demo_html(args.output_dir / "simulation_demo.html", model.config_dict(), snapshots, summary)
    print(f"History: {args.output_dir / 'history.csv'}")
    print(f"Animated demo: {args.output_dir / 'simulation_demo.html'}")
    print("Summary:", summary)


if __name__ == "__main__":
    main()
