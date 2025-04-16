import math


def create_matrix(rows, cols, data):
    return [data[i * cols:(i + 1) * cols] for i in range(rows)]


def matrix_mult(a, b):
    rows_a, cols_a = len(a), len(a[0])
    rows_b, cols_b = len(b), len(b[0])
    if cols_a != rows_b:
        raise ValueError("Matrices cannot be multiplied")
    result = create_matrix(rows_a, cols_b, [0] * (rows_a * cols_b))
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += a[i][k] * b[k][j]
    return result


def my_linspace(start, stop, num):
    if num == 1:
        return [start]
    step = (stop - start) / (num - 1)
    return [start + i * step for i in range(num)]


class ParametricAlgorithm:
    def __init__(self, x0, y0, x1, y1, color="red"):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.color = color


class HermiteAlgorithm(ParametricAlgorithm):
    def get_points(self):
        dx = self.x1 - self.x0
        dy = self.y1 - self.y0
        distance = math.sqrt(dx * dx + dy * dy)
        if distance == 0:
            return [(self.x0, self.y0, self.color)]
        k = distance / 3.0
        tx = -dy / distance * k
        ty = dx / distance * k

        m_hermite = [
            [2, -2, 1, 1],
            [-3, 3, -2, -1],
            [0, 0, 1, 0],
            [1, 0, 0, 0]
        ]
        vec_x = [self.x0, self.x1, tx, ty]
        vec_y = [self.y0, self.y1, tx, ty]

        mat_px = create_matrix(4, 1, vec_x)
        mat_py = create_matrix(4, 1, vec_y)

        coeffs_x = matrix_mult(m_hermite, mat_px)
        coeffs_y = matrix_mult(m_hermite, mat_py)

        t_values = my_linspace(0, 1, 100)
        points = []
        for t in t_values:
            t_vector = [t ** 3, t ** 2, t, 1]
            x = sum(t_vector[i] * coeffs_x[i][0] for i in range(4))
            y = sum(t_vector[i] * coeffs_y[i][0] for i in range(4))
            points.append((int(round(x)), int(round(y)), self.color))
        return points


class BezierAlgorithm(ParametricAlgorithm):
    def get_points(self):
        dx = self.x1 - self.x0
        dy = self.y1 - self.y0
        distance = math.sqrt(dx * dx + dy * dy)
        if distance == 0:
            return [(self.x0, self.y0, self.color)]
        k = distance / 3.0

        offset_x = -dy / distance * k
        offset_y = dx / distance * k

        p0x, p0y = self.x0, self.y0
        p3x, p3y = self.x1, self.y1
        p1x = self.x0 + dx / 3.0 + offset_x
        p1y = self.y0 + dy / 3.0 + offset_y
        p2x = self.x0 + 2 * dx / 3.0 + offset_x
        p2y = self.y0 + 2 * dy / 3.0 + offset_y

        m_bezier = [
            [-1, 3, -3, 1],
            [3, -6, 3, 0],
            [-3, 3, 0, 0],
            [1, 0, 0, 0]
        ]

        vec_x = [p0x, p1x, p2x, p3x]
        vec_y = [p0y, p1y, p2y, p3y]

        mat_px = create_matrix(4, 1, vec_x)
        mat_py = create_matrix(4, 1, vec_y)

        coeffs_x = matrix_mult(m_bezier, mat_px)
        coeffs_y = matrix_mult(m_bezier, mat_py)

        t_values = my_linspace(0, 1, 100)
        points = []
        for t in t_values:
            t_vector = [t ** 3, t ** 2, t, 1]
            x = sum(t_vector[i] * coeffs_x[i][0] for i in range(4))
            y = sum(t_vector[i] * coeffs_y[i][0] for i in range(4))
            points.append((int(round(x)), int(round(y)), self.color))
        return points


class BSplineAlgorithm(ParametricAlgorithm):

    def get_points(self):
        dx = self.x1 - self.x0
        dy = self.y1 - self.y0
        distance = math.sqrt(dx * dx + dy * dy)
        if distance == 0:
            return [(self.x0, self.y0, self.color)]
        k = distance / 3.0
        offset_x = -dy / distance * k
        offset_y = dx / distance * k

        p0x, p0y = self.x0, self.y0
        p3x, p3y = self.x1, self.y1
        p1x = self.x0 + dx / 3.0 + offset_x
        p1y = self.y0 + dy / 3.0 + offset_y
        p2x = self.x0 + 2 * dx / 3.0 + offset_x
        p2y = self.y0 + 2 * dy / 3.0 + offset_y

        m_bspline = [
            [-1 / 6, 3 / 6, -3 / 6, 1 / 6],
            [3 / 6, -6 / 6, 3 / 6, 0],
            [-3 / 6, 0, 3 / 6, 0],
            [1 / 6, 4 / 6, 1 / 6, 0]
        ]

        vec_x = [p0x, p1x, p2x, p3x]
        vec_y = [p0y, p1y, p2y, p3y]

        mat_px = create_matrix(4, 1, vec_x)
        mat_py = create_matrix(4, 1, vec_y)

        coeffs_x = matrix_mult(m_bspline, mat_px)
        coeffs_y = matrix_mult(m_bspline, mat_py)

        t_values = my_linspace(0, 1, 100)
        points = []
        for t in t_values:
            t_vector = [t ** 3, t ** 2, t, 1]
            x = sum(t_vector[i] * coeffs_x[i][0] for i in range(4))
            y = sum(t_vector[i] * coeffs_y[i][0] for i in range(4))
            points.append((int(round(x)), int(round(y)), self.color))
        return points
