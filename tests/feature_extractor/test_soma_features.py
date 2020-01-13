import unittest

import numpy as np
import math
from neuron_morphology.features import soma
from neuron_morphology.constants import (
    SOMA, AXON, APICAL_DENDRITE, BASAL_DENDRITE)
from neuron_morphology.morphology import Morphology
from neuron_morphology.feature_extractor.data import Data

def basic_nodes():
    """
    This morphology looks like:
    S -10-> A -10-> A
    |
    3-> AD -3-> AD
    """
    return [
        {
            "id": 0,
            "parent_id": -1,
            "type": SOMA,
            "x": 0,
            "y": 0,
            "z": 100,
            "radius": 5
        },
        {
            "id": 1,
            "parent_id": 0,
            "type": AXON,
            "x": 0,
            "y": 0,
            "z": 110,
            "radius": 1
        },
        {
            "id": 2,
            "parent_id": 1,
            "type": AXON,
            "x": 0,
            "y": 0,
            "z": 120,
            "radius": 1
        },
        {
            "id": 3,
            "parent_id": 0,
            "type": APICAL_DENDRITE,
            "x": 0,
            "y": 3,
            "z": 100,
            "radius": 1
        },
        {
            "id": 4,
            "parent_id": 3,
            "type": APICAL_DENDRITE,
            "x": 0,
            "y": 6,
            "z": 100,
            "radius": 1
        },
    ]


class MorphSomaTest(unittest.TestCase):
    def setUp(self):
        self.morphology = Morphology(
            basic_nodes(),
            node_id_cb=lambda node: node["id"],
            parent_id_cb=lambda node: node["parent_id"],
        )
        self.data = Data(self.morphology, relative_soma_depth= 0.25)

class TestSomaFeatures(MorphSomaTest):
    
    def test_soma_surface(self):
        obtained = soma.calculate_soma_surface(self.data)
        self.assertEqual(obtained, 4.0 * math.pi * 5 * 5)

    def test_relative_soma_depth(self):
        obtained = soma.calculate_relative_soma_depth(self.data)
        self.assertEqual(obtained, 0.25)

    def test_stem_exit_and_distance(self):
        obtained = soma.calculate_stem_exit_and_distance(self.data, [AXON])
        self.assertEqual(obtained, (0.5, 0))
