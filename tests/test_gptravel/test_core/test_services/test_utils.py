import numpy as np
import pytest

from gptravel.core.services.utils import entropy_score


def test_entropy_score():
    input_list = [0.2, 0.2, 0.2, 0.2, 0.2]
    expected_output = 1.0
    assert np.isclose(entropy_score(input_list), expected_output, rtol=1e-6)

    input_list = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    input_list = [item / sum(input_list) for item in input_list]
    expected_output = 1.0
    assert np.isclose(entropy_score(input_list), expected_output, rtol=1e-6)

    input_list = [100, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    input_list = [item / sum(input_list) for item in input_list]
    expected_output = 0.23655039227103675
    assert np.isclose(entropy_score(input_list), expected_output, rtol=1e-6)

    input_list = [0.001, 0.5, 0.00001, 0.5, 0.0001]
    expected_output = 0.4356123921987464
    assert np.isclose(entropy_score(input_list), expected_output, rtol=1e-6)

    input_list = [0.9, 0.05, 0.05, 0.01, 0.01]
    expected_output = 0.30228012612889454
    assert np.isclose(entropy_score(input_list), expected_output, rtol=1e-6)

    input_list = [0.2, 0.3, 0.1, 0.2, 0.2]
    expected_output = 0.9674887648835616
    assert np.isclose(entropy_score(input_list), expected_output, rtol=1e-6)


if __name__=="__main__":
    test_entropy_score()