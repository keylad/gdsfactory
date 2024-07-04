import pytest
from gdsfactory.components.bend_s import get_min_sbend_size
from gdsfactory.component_layout import _parse_coordinate

#tests for get_min_sbend_size
def test_get_min_sbend_size_x_none():
    result = get_min_sbend_size(size=(None, 10.0), cross_section="strip")
    assert isinstance(result, float)


def test_get_min_sbend_size_y_none():
    result = get_min_sbend_size(size=(10.0, None), cross_section="strip")
    assert isinstance(result, float)


def test_get_min_sbend_size_both_none():
    with pytest.raises(ValueError):
        get_min_sbend_size(size=(10.0, 10.0), cross_section="strip")


def test_get_min_sbend_size_min_radius_none():
    with pytest.raises(ValueError):
        get_min_sbend_size(size=(None, 10.0), cross_section="unknown_cross_section")


def test_get_min_sbend_size_small_size():
    result = get_min_sbend_size(size=(None, 1.0), cross_section="strip")
    assert result < 2.0


def test_get_min_sbend_size_large_size():
    result = get_min_sbend_size(size=(None, 100.0), cross_section="strip")
    assert result > 1.0


@pytest.mark.parametrize(
    "size, cross_section, expected",
    [
        ((None, 10.0), "strip", float),
        ((10.0, None), "strip", float),
        ((None, 5.0), "strip", float),
        ((None, 20.0), "strip", float),
    ],
)
def test_get_min_sbend_size_various_inputs(size, cross_section, expected):
    result = get_min_sbend_size(size=size, cross_section=cross_section)
    assert isinstance(result, expected)

#tests for parse_coordinate
def test_object_with_center():
    class MockObject:
        def __init__(self, center):
            self.center = center
            self.dcenter = (1.5, 2.5)

    obj = MockObject(center=True)
    result = _parse_coordinate(obj)
    assert result == obj.dcenter


def test_array_like_with_two_elements():
    coordinate = [1.0, 2.0]
    result = _parse_coordinate(coordinate)
    assert result == coordinate


def test_array_like_with_incorrect_number_of_elements():
    coordinate = [1.0, 2.0, 3.0]
    with pytest.raises(ValueError):
        _parse_coordinate(coordinate)
