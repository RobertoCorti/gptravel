from typing import List, Union

import numpy as np


def entropy_score(input_list: List[Union[int, float]]) -> float:
    input_list_vec = np.array(input_list)
    entropy = np.sum(-np.log2(input_list) * input_list)
    max_entropy = np.log2(len(input_list_vec))
    out = entropy / max_entropy
    return 0.0 if np.isnan(out) else out
