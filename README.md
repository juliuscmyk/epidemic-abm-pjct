# Epidemic Spread ABM

This Applied AI project models epidemic spread with an agent-based simulation
implemented in **Mesa**, the Python ABM framework recommended in the brief.
Each person is an autonomous agent that moves on a two-dimensional wrapped grid,
meets nearby agents, can become infected, and later recovers. A configurable
distancing behavior changes movement and contact risk so experiments can compare
individual rules with population-level outcomes.

Mesa supplies the core ABM structure: the model subclasses `mesa.Model`, each
person subclasses `mesa.Agent`, the environment uses `mesa.space.MultiGrid`, and
state counts are recorded with `mesa.DataCollector`.

## Setup

Create and activate a virtual environment, then install the required framework:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Project files

- `epidemic_abm/model.py`: Mesa agents, Mesa grid environment, infection rule,
  recovery rule, and Mesa data collection.
- `epidemic_abm/reporting.py`: CSV output, animated demo, experiment report.
- `run_simulation.py`: one recorded simulation run for the demonstration.
- `run_experiments.py`: repeated parameter experiments and result aggregation.
- `Rationale.md`: rationale, design, analysis, and limitations.
- `tests/test_model.py`: small checks for population conservation and recovery.

## Run the demonstration

From this folder, run:

```powershell
python run_simulation.py
```

Open `outputs/single_run/simulation_demo.html` in a browser. The HTML file
contains a Play button and a step slider. In the grid:

- blue agents are susceptible,
- red agents are infected,
- green agents are recovered,
- a dark outline marks agents following distancing behavior.

The command also writes `outputs/single_run/history.csv`, which records state
counts at every simulation step.

## Run the experiments

```powershell
python run_experiments.py
```

Open `outputs/experiments/experiment_report.html`. The report compares four
scenarios across six seeded runs each:

| Scenario | Parameter change |
| --- | --- |
| `baseline` | 0% distancing compliance |
| `moderate_distancing` | 45% distancing compliance |
| `high_distancing` | 80% distancing compliance |
| `high_transmission` | 45% distancing and higher infection probability |

The experiment folder also contains:

- `all_histories.csv`: every repeated run,
- `mean_histories.csv`: mean state counts by scenario and step,
- `scenario_summary.csv`: peak infection and attack-rate summaries.

## Change parameters

`run_simulation.py` accepts command-line parameters. For example:

```powershell
python run_simulation.py --distancing-compliance 0.8 --infection-probability 0.22 --seed 5
```

Useful parameters are `--population`, `--grid-size`, `--initial-infected`,
`--infection-probability`, `--recovery-steps`, `--movement-probability`,
`--distancing-compliance`, `--steps`, and `--seed`.

## Test the model

```powershell
python -m unittest discover -s tests
```

## Demo flow for presentation

1. State the question: how do individual movement and distancing rules change an
   outbreak in a small population?
2. Run `python run_simulation.py`.
3. Open the animated demo and play the timeline from the first infections to the
   infection peak and recovery phase.
4. Open the experiment report and compare the baseline and high-distancing
   curves.
5. Explain that the results are simulation evidence under explicit assumptions,
   not a medical forecast.
