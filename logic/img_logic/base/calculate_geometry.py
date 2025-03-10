import numpy as np


class GeometryCalculation:
    @classmethod
    def decide_radious(cls, Lu_x, Lu_y, porosity, num_vertices) -> float:
        return np.sqrt(
            (2 * porosity * Lu_x * Lu_y)
            / (num_vertices * np.sin((2 * np.pi) / num_vertices))
        )
