from opentidalfarm import *
import pytest

class TestTurbines(object):

    def test_BumpTurbine(self):
        turbine = BumpTurbine(diameter=20., minimum_distance=20., thrust_coefficient=0.8,
                              controls=Controls(position=True, friction=True))

        # Test properties
        assert turbine.diameter == 20.
        assert turbine.minimum_distance == 20.
        assert turbine.friction == 0.8*pi/2./turbine._unit_bump_int
        assert turbine.radius == 10.

        # Test controls
        assert turbine.controls.position
        assert turbine.controls.friction
        assert not turbine.controls.dynamic_friction

        # Test parameterisation
        assert turbine.bump
        assert not turbine.smeared


    def test_SmearedTurbine(self):
        turbine = SmearedTurbine(friction=21.0)

        # Test properties
        with pytest.raises(ValueError): turbine.diameter
        with pytest.raises(ValueError): turbine.minimum_distance
        assert turbine.friction == 21.
        with pytest.raises(ValueError): turbine.radius

        # Test controls
        assert not turbine.controls.position
        assert turbine.controls.friction
        assert not turbine.controls.dynamic_friction

        # Test parameterisation
        assert not turbine.bump
        assert turbine.smeared
