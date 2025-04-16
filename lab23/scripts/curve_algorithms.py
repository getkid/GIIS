import math


class CurveAlgorithm:
    def __init__(self, x0, y0, x1, y1, color="green"):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.color = color


class Circle(CurveAlgorithm):
    def get_points(self):
        points = []
        radius = int(math.sqrt((self.x1 - self.x0) ** 2 + (self.y1 - self.y0) ** 2))
        x, y = 0, radius
        d = 3 - 2 * radius
        while x <= y:
            for dx, dy in [(x, y), (-x, y), (x, -y), (-x, -y), (y, x), (-y, x), (y, -x), (-y, -x)]:
                points.append((self.x0 + dx, self.y0 + dy, self.color))
            if d < 0:
                d += 4 * x + 6
            else:
                d += 4 * (x - y) + 10
                y -= 1
            x += 1
        return points


class Ellipse(CurveAlgorithm):
    def get_points(self):
        points = []
        a = abs(self.x1 - self.x0) // 2
        b = abs(self.y1 - self.y0) // 2
        xc, yc = self.x0, self.y0
        x, y = 0, b
        d1 = b * b - a * a * b + 0.25 * a * a
        dx = 2 * b * b * x
        dy = 2 * a * a * y

        while dx < dy:
            points.extend([(xc + x, yc + y, self.color), (xc - x, yc + y, self.color),
                           (xc + x, yc - y, self.color), (xc - x, yc - y, self.color)])
            if d1 < 0:
                x += 1
                dx += 2 * b * b
                d1 += dx + b * b
            else:
                x += 1
                y -= 1
                dx += 2 * b * b
                dy -= 2 * a * a
                d1 += dx - dy + b * b
        d2 = b * b * (x + 0.5) * (x + 0.5) + a * a * (y - 1) * (y - 1) - a * a * b * b

        while y >= 0:
            points.extend([(xc + x, yc + y, self.color), (xc - x, yc + y, self.color),
                           (xc + x, yc - y, self.color), (xc - x, yc - y, self.color)])
            if d2 > 0:
                y -= 1
                dy -= 2 * a * a
                d2 += a * a - dy
            else:
                y -= 1
                x += 1
                dx += 2 * b * b
                dy -= 2 * a * a
                d2 += dx - dy + a * a
        return points


class Hyperbola(CurveAlgorithm):
    #  y = b * sqrt(1 + (x/a) ** 2)
    def get_points(self):
        points = []
        a = max(abs(self.x1 - self.x0), 1)
        b = max(abs(self.y1 - self.y0) // 2, 1)
        for x in range(-a, a + 1):
            try:
                y = int(b * math.sqrt(1 + (x / a) ** 2))
                points.extend([(self.x0 + x, self.y0 + y, self.color), (self.x0 + x, self.y0 - y, self.color)])
            except ValueError:
                continue
        return points


class Parabola(CurveAlgorithm):
    # y = x ** 2 / 4 * p
    def get_points(self):
        points = []
        p = max(abs(self.y1 - self.y0) // 2, 1)
        for x in range(-abs(self.x1 - self.x0), abs(self.x1 - self.x0) + 1):
            try:
                y = int((x ** 2) / (4 * p))
                points.append((self.x0 + x, self.y0 + y, self.color))
            except ValueError:
                continue
        return points
