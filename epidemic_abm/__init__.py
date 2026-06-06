"""Epidemic agent-based model package."""

from .model import Agent, EpidemicModel, HealthState, PersonAgent, SimulationConfig

__all__ = ["Agent", "PersonAgent", "EpidemicModel", "HealthState", "SimulationConfig"]
