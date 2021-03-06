# Copyright (c) 2019 fortiss GmbH
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


import unittest
import os
import numpy as np
from modules.runtime.scenario.scenario_generation.deterministic \
  import DeterministicScenarioGeneration
from modules.runtime.scenario.scenario_generation.scenario_generation \
  import ScenarioGeneration
from bark.world.goal_definition import GoalDefinition, GoalDefinitionPolygon
from modules.runtime.commons.parameters import ParameterServer
from modules.runtime.runtime import Runtime
from modules.runtime.viewer.matplotlib_viewer import MPViewer

class ScenarioGenerationTests(unittest.TestCase):
  def test_uniform_vehicle_distribution_default_params(self):
    param_server = ParameterServer(
      filename="modules/runtime/tests/data/deterministic_scenario_test.json")
    scenario_generation = DeterministicScenarioGeneration(num_scenarios=2,
                                                          random_seed=0,
                                                          params=param_server)
    scenario_generation.dump_scenario_list("test.scenario")
    self.assertEqual(len(scenario_generation._scenario_list), 2)
    self.assertEqual(len(scenario_generation._scenario_list[0]._agent_list), 2)

    # assert scenario generation
    agent0 = scenario_generation._scenario_list[0]._agent_list[0]
    np.testing.assert_array_equal(agent0.state, np.array([0., 0., 0., 0., 5.0]))
    self.assertEqual(agent0.id, 0)
    self.assertEqual(str(agent0.behavior_model), "bark.behavior.BehaviorConstantVelocity")
    self.assertEqual(str(agent0.dynamic_model), "bark.dynamic.SingleTrackModel")
    self.assertEqual(str(agent0.execution_model), "bark.dynamic.ExecutionModelInterpolate")
    agent1 = scenario_generation._scenario_list[0]._agent_list[1]
    #np.testing.assert_array_equal(agent1.state, np.array([0., 10., 0., 0., 5.0]))
    self.assertEqual(agent1.id, 1)
    self.assertEqual(str(agent1.behavior_model), "bark.behavior.BehaviorIDMClassic")
    
    # TODO(@hart): make sure the map is not reloaded for rl-performance
    for _ in range(0, 10):
      _ = scenario_generation.get_next_scenario()

    # loading serialized scenarios
    scenario_loader = ScenarioGeneration()
    scenario_loader.load_scenario_list("test.scenario")
    self.assertEqual(len(scenario_loader._scenario_list), 2)
    self.assertEqual(len(scenario_loader._scenario_list[0]._agent_list),
                     len(scenario_generation._scenario_list[0]._agent_list))
    self.assertEqual(
      str(scenario_loader._scenario_list[0]._agent_list[0].behavior_model),
      "bark.behavior.BehaviorConstantVelocity")
    #np.testing.assert_array_equal(scenario_loader._scenario_list[0]._agent_list[0].state,
    #  np.array([0., 0., 0., 0., 5.0]))

    self.assertEqual(
      str(scenario_loader._scenario_list[0]._agent_list[1].behavior_model),
      "bark.behavior.BehaviorIDMClassic")
    #np.testing.assert_array_equal(scenario_loader._scenario_list[0]._agent_list[1].state,
    #  np.array([0., 10., 0., 0., 5.0]))


if __name__ == '__main__':
  unittest.main()