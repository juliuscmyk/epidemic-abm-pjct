from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum

from mesa import Agent as MesaAgent
from mesa import DataCollector, Model
from mesa.space import MultiGrid


class HealthState(str, Enum):
    SUSCEPTIBLE = "susceptible"
    INFECTED = "infected"
    RECOVERED = "recovered"


@dataclass
class SimulationConfig:
    population: int = 180
    width: int = 16
    height: int = 16
    initial_infected: int = 5
    infection_probability: float = 0.30
    recovery_steps: int = 14
    movement_probability: float = 0.92
    distancing_compliance: float = 0.35
    distancing_movement_reduction: float = 0.58
    distancing_contact_reduction: float = 0.45
    infected_isolation_probability: float = 0.18
    steps: int = 80
    seed: int = 21

    def validate(self) -> None:
        if self.population < 1:
            raise ValueError("population must be positive")
        if self.width < 1 or self.height < 1:
            raise ValueError("grid dimensions must be positive")
        if not 0 <= self.initial_infected <= self.population:
            raise ValueError("initial_infected must be within population")
        if self.recovery_steps < 1 or self.steps < 1:
            raise ValueError("recovery_steps and steps must be positive")
        probability_fields = (
            "infection_probability",
            "movement_probability",
            "distancing_compliance",
            "distancing_movement_reduction",
            "distancing_contact_reduction",
            "infected_isolation_probability",
        )
        for field_name in probability_fields:
            value = getattr(self, field_name)
            if not 0 <= value <= 1:
                raise ValueError(f"{field_name} must be between 0 and 1")


class PersonAgent(MesaAgent):
    """Mesa agent representing one person in the epidemic model."""

    def __init__(self, model: "EpidemicModel", distancing: bool):
        super().__init__(model)
        self.distancing = distancing
        self.state = HealthState.SUSCEPTIBLE
        self.infected_steps = 0

    def snapshot(self) -> dict[str, int | str | bool]:
        x, y = self.pos
        return {
            "id": self.unique_id,
            "x": x,
            "y": y,
            "state": self.state.value,
            "distancing": self.distancing,
        }


class EpidemicModel(Model):
    """Mesa MultiGrid ABM where mobile people exchange infection on contact."""

    def __init__(self, config: SimulationConfig):
        config.validate()
        super().__init__(rng=config.seed)
        self.config = config
        self.step_number = 0
        self.grid = MultiGrid(config.width, config.height, torus=True)
        self.person_agents: list[PersonAgent] = []

        for _ in range(config.population):
            agent = PersonAgent(
                self,
                distancing=self.random.random() < config.distancing_compliance,
            )
            self.person_agents.append(agent)
            self.grid.place_agent(
                agent,
                (
                    self.random.randrange(config.width),
                    self.random.randrange(config.height),
                ),
            )

        for agent in self.random.sample(self.person_agents, config.initial_infected):
            agent.state = HealthState.INFECTED

        self.datacollector = DataCollector(
            model_reporters={
                "susceptible": "susceptible_count",
                "infected": "infected_count",
                "recovered": "recovered_count",
            }
        )
        self.history = [self._count_states()]
        self.datacollector.collect(self)

    def run(self, capture_snapshots: bool = False) -> list[dict[str, object]]:
        snapshots = [self.snapshot()] if capture_snapshots else []
        for _ in range(self.config.steps):
            self.step()
            if capture_snapshots:
                snapshots.append(self.snapshot())
            if self.history[-1]["infected"] == 0:
                break
        return snapshots

    def step(self) -> dict[str, int]:
        self._move_agents()
        newly_infected = self._find_new_infections()
        self._advance_infections(newly_infected)
        self.step_number += 1
        record = self._count_states()
        self.history.append(record)
        self.datacollector.collect(self)
        return record

    def snapshot(self) -> dict[str, object]:
        return {
            "step": self.step_number,
            "counts": self.history[-1],
            "agents": [agent.snapshot() for agent in self.person_agents],
        }

    def config_dict(self) -> dict[str, int | float]:
        return asdict(self.config)

    @property
    def susceptible_count(self) -> int:
        return self.history[-1]["susceptible"] if self.history else 0

    @property
    def infected_count(self) -> int:
        return self.history[-1]["infected"] if self.history else 0

    @property
    def recovered_count(self) -> int:
        return self.history[-1]["recovered"] if self.history else 0

    def _move_agents(self) -> None:
        directions = (
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        )
        for agent in self.person_agents:
            if (
                agent.state == HealthState.INFECTED
                and self.random.random() < self.config.infected_isolation_probability
            ):
                continue
            movement_probability = self.config.movement_probability
            if agent.distancing:
                movement_probability *= 1 - self.config.distancing_movement_reduction
            if self.random.random() >= movement_probability:
                continue
            dx, dy = self.random.choice(directions)
            x, y = agent.pos
            self.grid.move_agent(
                agent,
                (
                    (x + dx) % self.config.width,
                    (y + dy) % self.config.height,
                ),
            )

    def _find_new_infections(self) -> set[int]:
        new_infections: set[int] = set()
        occupied_positions = {agent.pos for agent in self.person_agents}
        for pos in occupied_positions:
            colocated_agents = self.grid.get_cell_list_contents([pos])
            infected_count = sum(
                agent.state == HealthState.INFECTED for agent in colocated_agents
            )
            if infected_count == 0:
                continue
            base_risk = 1 - (1 - self.config.infection_probability) ** infected_count
            for agent in colocated_agents:
                if agent.state != HealthState.SUSCEPTIBLE:
                    continue
                risk = base_risk
                if agent.distancing:
                    risk *= 1 - self.config.distancing_contact_reduction
                if self.random.random() < risk:
                    new_infections.add(agent.unique_id)
        return new_infections

    def _advance_infections(self, new_infections: set[int]) -> None:
        for agent in self.person_agents:
            if agent.unique_id in new_infections:
                agent.state = HealthState.INFECTED
                agent.infected_steps = 0
                continue
            if agent.state != HealthState.INFECTED:
                continue
            agent.infected_steps += 1
            if agent.infected_steps >= self.config.recovery_steps:
                agent.state = HealthState.RECOVERED

    def _count_states(self) -> dict[str, int]:
        counts = {state.value: 0 for state in HealthState}
        for agent in self.person_agents:
            counts[agent.state.value] += 1
        return {"step": self.step_number, **counts}


Agent = PersonAgent
