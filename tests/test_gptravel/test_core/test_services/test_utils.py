import os

import numpy as np
import pytest

from gptravel.core.services.utils import (
    is_location_a_country,
    remove_consecutive_duplicates,
    theil_diversity_entropy_index,
)


def test_entropy_score():
    input_list = [0.2, 0.2, 0.2, 0.2, 0.2]
    expected_output = 0.0
    assert np.isclose(
        theil_diversity_entropy_index(input_list), expected_output, rtol=1e-6
    )

    input_list = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    input_list = [item / sum(input_list) for item in input_list]
    expected_output = 0.0
    assert np.isclose(
        theil_diversity_entropy_index(input_list), expected_output, rtol=1e-6
    )

    input_list = [100, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    input_list = [item / sum(input_list) for item in input_list]
    expected_output = 0.7634496077289633
    assert np.isclose(
        theil_diversity_entropy_index(input_list), expected_output, rtol=1e-6
    )

    input_list = [100, 0.0, 0.0, 0, 0.0]
    expected_output = 1.0
    assert np.isclose(
        theil_diversity_entropy_index(input_list), expected_output, rtol=1e-6
    )

    input_list = [0.9, 0.05, 0.05, 0.01, 0.01]
    expected_output = 0.6913428710325702
    assert np.isclose(
        theil_diversity_entropy_index(input_list), expected_output, rtol=1e-6
    )

    input_list = [0.2, 0.3, 0.1, 0.2, 0.2]
    expected_output = 0.03251123511643821
    assert np.isclose(
        theil_diversity_entropy_index(input_list), expected_output, rtol=1e-6
    )


@pytest.mark.skipif(
    os.getenv("HUGGING_FACE_KEY", "") == "", reason="no api key available"
)
def test_is_location_a_country():
    assert is_location_a_country("Thailand")
    assert not is_location_a_country("Bangkok")
    assert is_location_a_country("United States")
    assert not is_location_a_country("Milan")
    assert is_location_a_country("Russia")


def test_remove_consecutive_duplicates():
    assert remove_consecutive_duplicates([]) == []
    assert remove_consecutive_duplicates([1]) == [1]
    assert remove_consecutive_duplicates([1, 1, 1, 1]) == [1]
    assert remove_consecutive_duplicates([1, 2, 3, 4]) == [1, 2, 3, 4]
    assert remove_consecutive_duplicates([1, 1, 2, 2, 3, 4, 4]) == [1, 2, 3, 4]
    assert remove_consecutive_duplicates([1, 1, 2, 2, 3, 4, 4, 1]) == [1, 2, 3, 4, 1]
    assert remove_consecutive_duplicates([1, 1, 2, 2, 3, 4, 4, 1, 1]) == [1, 2, 3, 4, 1]
    assert remove_consecutive_duplicates([1, 1, 2, 2, 3, 4, 1, 4, 1]) == [
        1,
        2,
        3,
        4,
        1,
        4,
        1,
    ]
    assert remove_consecutive_duplicates([1, "a", "a", 2, 2, "b", "c", "c", 4]) == [
        1,
        "a",
        2,
        "b",
        "c",
        4,
    ]
