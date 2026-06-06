import unittest

from epidemic_abm import EpidemicModel, SimulationConfig


class EpidemicModelTests(unittest.TestCase):
    def test_population_is_conserved(self):
        model = EpidemicModel(SimulationConfig(population=30, steps=15, seed=8))
        model.run()

        for record in model.history:
            self.assertEqual(
                record["susceptible"] + record["infected"] + record["recovered"],
                30,
            )

    def test_zero_initial_infected_stops_without_new_cases(self):
        model = EpidemicModel(
            SimulationConfig(population=20, initial_infected=0, steps=30, seed=11)
        )
        model.run()

        self.assertEqual(len(model.history), 2)
        self.assertEqual(model.history[-1]["infected"], 0)
        self.assertEqual(model.history[-1]["susceptible"], 20)

    def test_infected_agents_recover(self):
        model = EpidemicModel(
            SimulationConfig(
                population=1,
                initial_infected=1,
                infection_probability=0,
                movement_probability=0,
                recovery_steps=3,
                steps=5,
            )
        )
        model.run()

        self.assertEqual(model.history[-1]["infected"], 0)
        self.assertEqual(model.history[-1]["recovered"], 1)


if __name__ == "__main__":
    unittest.main()
