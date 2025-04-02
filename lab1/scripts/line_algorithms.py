import math


class LineAlgorithm:
    def __init__(self, x0, y0, x1, y1, color="black"):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.color = color


class DDA(LineAlgorithm):
    def get_points(self):
        points = []
        dx = self.x1 - self.x0
        dy = self.y1 - self.y0
        steps = int(max(abs(dx), abs(dy)))
        if steps == 0:
            return [(self.x0, self.y0)]
        x_inc = dx / steps
        y_inc = dy / steps
        x, y = self.x0, self.y0
        for i in range(steps + 1):
            points.append((round(x), round(y), self.color))
            x += x_inc
            y += y_inc
        return points


class Bresenham(LineAlgorithm):
    def get_points(self):
        points = []
        x0, y0, x1, y1 = self.x0, self.y0, self.x1, self.y1
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            points.append((x0, y0, self.color))
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
        return points


class Wu(LineAlgorithm):
    def get_points(self):

        points = []
        x0, y0 = self.x0, self.y0
        x1, y1 = self.x1, self.y1

        if x0 == x1 and y0 == y1:
            return [(x0, y0, self.color)]

        dx = x1 - x0
        dy = y1 - y0
        steep = abs(dy) > abs(dx)

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            dx, dy = dy, dx

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
            dx, dy = -dx, -dy

        gradient = dy / dx if dx != 0 else 1.0

        def plot(x, y, intensity):
            intensity = max(0.0, min(intensity, 1.0))
            gray = int(255 * (1 - intensity))
            color = f"#{gray:02x}{gray:02x}{gray:02x}"
            if steep:
                points.append((y, x, color))
            else:
                points.append((x, y, color))

        xend = round(x0)
        yend = y0 + gradient * (xend - x0)
        xgap = self._rfpart(x0 + 0.5)
        xpxl1 = xend
        ypxl1 = math.floor(yend)
        plot(xpxl1, ypxl1, self._rfpart(yend) * xgap)
        plot(xpxl1, ypxl1 + 1, self._fpart(yend) * xgap)

        intery = yend + gradient

        xend = round(x1)
        yend = y1 + gradient * (xend - x1)
        xgap = self._fpart(x1 + 0.5)
        xpxl2 = xend
        ypxl2 = math.floor(yend)
        plot(xpxl2, ypxl2, self._rfpart(yend) * xgap)
        plot(xpxl2, ypxl2 + 1, self._fpart(yend) * xgap)

        for x in range(xpxl1 + 1, xpxl2):
            plot(x, math.floor(intery), self._rfpart(intery))
            plot(x, math.floor(intery) + 1, self._fpart(intery))
            intery += gradient

        return points

    @staticmethod
    def _fpart(x):
        return x - math.floor(x)

    @staticmethod
    def _rfpart(x):
        return 1 - Wu._fpart(x)