# Project Rationale

## Title

**Epidemic Spread Simulation with Adaptive Distancing Agents using Mesa**

## 1. Problem definition

Infectious diseases can spread through many local interactions before the overall
pattern is obvious. This project investigates a realistic question for an
agent-based model: **how can individual movement and distancing behavior change
the spread of infection in a small population?**

The project objectives are:

1. Represent people as autonomous agents with health states and behaviors.
2. Represent a shared environment where contact emerges from movement.
3. Compare epidemic outcomes under different transmission and distancing
   parameters.
4. Visualize both a single run and repeated experimental results.

The expected outcome is not a real epidemiological forecast. The expected
outcome is a clear simulation showing that local rules can create different
system-level infection curves.

## 2. Justification of ABM approach

Agent-based modeling is suitable because infection is caused by local encounters
between individual people. A single average equation would hide variation in
movement, compliance, and accidental co-location. In this model, each person
agent follows a small rule set, while infection peaks and final attack rates
emerge from many interactions over time.

The implementation uses Mesa, a Python framework for agent-based modeling. Mesa
is appropriate because it provides the model, agent, grid, and data-collection
components needed by this problem while keeping the rules executable and
inspectable.

## 3. System design

### Agents

There is one agent type: `Person`.

Each person has:

- a grid position,
- a health state: susceptible, infected, or recovered,
- an infection duration counter,
- a distancing-compliance flag.

### Environment

The environment is a Mesa `MultiGrid`. It is configured as a two-dimensional
wrapped grid, meaning that an agent leaving one edge re-enters at the opposite
edge. Several agents may occupy the same cell. Sharing a cell represents a
contact opportunity.

### Interaction rules

At every simulation step:

1. Agents decide whether to move to a neighboring grid cell.
2. Infected agents may isolate and skip movement.
3. Distancing agents move less often.
4. Susceptible agents sharing a cell with infected agents face infection risk.
5. Distancing agents receive reduced contact risk.
6. Infected agents recover after a fixed number of steps.

When more infected agents share a cell, infection risk increases using:

`1 - (1 - infection_probability) ^ infected_contacts`

This keeps the rule intuitive: repeated exposure increases risk without forcing
infection deterministically.

### Assumptions and constraints

- Health states follow a simple SIR structure: susceptible, infected, recovered.
- Recovered agents do not become infected again during the same run.
- The grid cell is an abstract contact area, not a real physical distance.
- Distancing behavior is fixed for a run rather than learned over time.
- No age, symptoms, vaccination, death, or hospital capacity is modeled.

## 4. Implementation

The implementation is organized into:

- a Mesa model module for agent and environment behavior,
- a reporting module for CSV, HTML, and chart output,
- a single-run script for the animated demonstration,
- an experiment script for repeated scenario comparison.

`EpidemicModel` subclasses Mesa `Model`, `PersonAgent` subclasses Mesa `Agent`,
the environment uses Mesa `MultiGrid`, and state counts are collected with Mesa
`DataCollector`. The demonstration records every time step and produces an
interactive HTML grid. The experiment runner exports raw CSV data and a report
that plots mean infected agents per scenario.

## 5. Experimentation and results

### Experimental scenarios

The experiment runner compares:

| Scenario | Purpose |
| --- | --- |
| Baseline | No agents follow distancing behavior. |
| Moderate distancing | 45% of agents reduce movement and contact risk. |
| High distancing | 80% of agents reduce movement and contact risk. |
| High transmission | Transmission probability rises while distancing stays moderate. |

Each scenario is repeated with six seeds. This avoids depending on one lucky or
unlucky random run.

### Collected metrics

The system records:

- susceptible, infected, and recovered counts by step,
- peak infected population,
- step of the infection peak,
- attack rate, calculated as the percentage infected at least once by the end.

### Result interpretation

The experiment report in `outputs/experiments/experiment_report.html` should be
used as the final visual evidence. In the regenerated Mesa experiment set,
baseline mean peak infection is 75.8 agents, while high distancing reduces the
mean peak to 27.2 agents. The attack rate drops from 89.6% in the baseline
scenario to 45.6% in the high-distancing scenario. The high-transmission
scenario tests whether stronger disease pressure can offset moderate behavioral
protection.

Because random movement matters, results should be discussed as repeated
simulation outcomes under the chosen parameter values.

## 6. Critical analysis

### Strengths

- The model directly demonstrates autonomous Mesa agents and emergent behavior.
- Rules are transparent and parameters are easy to vary.
- Seeded repeated experiments support reproducible comparisons.
- CSV outputs and HTML visuals make the system easy to inspect.

### Limitations

- Contact is simplified to co-location in a grid cell.
- Recovery time is fixed for every infected agent.
- Agents do not adapt their beliefs from outbreak observations.
- Parameter values are illustrative rather than fitted to real disease data.

### Future improvements

- Add household, workplace, and public-space locations.
- Give agents changing beliefs or risk perception.
- Add vaccination or quarantine policies.
- Calibrate parameters with external epidemiological data.
- Compare the ABM results with a mathematical SIR baseline.

## 7. Conclusion

This project satisfies the ABM objective by using Mesa to define agents, an
environment, interaction protocols, parameter experiments, visual output, and a
critical analysis. It demonstrates the central Applied AI idea that simple
intelligent agent behaviors can produce measurable collective outcomes.
