from typing import List, Tuple

import numpy as np
from numpy.typing import NDArray
from python_tsp.exact import solve_tsp_dynamic_programming
from python_tsp.heuristics import solve_tsp_simulated_annealing

from gptravel.core.io.loggerconfig import logger
from gptravel.core.services.geocoder import Geocoder


class TSPSolver:
    def __init__(self, geocoder: Geocoder) -> None:
        self._geocoder = geocoder
        self._distance_matrix: NDArray[np.float64] = np.empty([2, 2])

    @property
    def distance_matrix(self) -> NDArray[np.float64]:
        return self._distance_matrix

    def solve(
        self, cities: List[str], open_problem: bool = False
    ) -> Tuple[List[str], float]:
        if len(cities) > 1:
            logger.debug("TSP solver: start")
            logger.debug("TSP solver: solve the problem for cities = %s", cities)
            logger.debug("TSP solver: open problem = %s", open_problem)
            if len(cities) < 10:
                solver = solve_tsp_dynamic_programming
                logger.debug("TSP solver: use dynamic programming")
            else:
                solver = solve_tsp_simulated_annealing
                logger.debug("TSP solver: use simulated annealing")
            self._distance_matrix = np.array(
                [
                    [
                        0.0
                        if i == j
                        else self._geocoder.location_distance(cities[i], cities[j])
                        for j in range(len(cities))
                    ]
                    for i in range(len(cities))
                ]
            )
            dist_mat = np.copy(self._distance_matrix)
            if open_problem:
                dist_mat[:, 0] = 0.0
            solution_indexes, solution_distance = solver(distance_matrix=dist_mat)
            return [cities[index] for index in solution_indexes], solution_distance
        logger.debug("TSP solver: only one city provided -- no computation needed")
        return cities, 0.0
