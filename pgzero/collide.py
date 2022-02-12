import math


def distance_to(from_x, from_y, to_x, to_y):
    dx = to_x - from_x
    dy = to_y - from_y
    return math.sqrt(dx**2 + dy**2)


def distance_to_squared(from_x, from_y, to_x, to_y):
    dx = to_x - from_x
    dy = to_y - from_y
    return dx**2 + dy**2


class Collide():
    @staticmethod
    def line_line(l1x1, l1y1, l1x2, l1y2, l2x1, l2y1, l2x2, l2y2):
        pt = Collide.line_line_XY(l1x1, l1y1, l1x2, l1y2, l2x1, l2y1, l2x2, l2y2)
        return all(pt)

    @staticmethod
    def line_lines(l1x1, l1y1, l1x2, l1y2, lines):
        for i, line in enumerate(lines):
            l2x1, l2y1, l2x2, l2y2 = line
            if Collide.line_line(l1x1, l1y1, l1x2, l1y2, l2x1, l2y1, l2x2, l2y2):
                return i
        return -1

    @staticmethod
    def line_line_XY(l1x1, l1y1, l1x2, l1y2, l2x1, l2y1, l2x2, l2y2):
        determinant = (l2y2-l2y1)*(l1x2-l1x1) - (l2x2-l2x1)*(l1y2-l1y1)

        # Simplify: Parallel lines are never considered to be intersecting
        if determinant == 0:
            return (None, None)

        uA = ((l2x2-l2x1)*(l1y1-l2y1) - (l2y2-l2y1)*(l1x1-l2x1)) / determinant
        uB = ((l1x2-l1x1)*(l1y1-l2y1) - (l1y2-l1y1)*(l1x1-l2x1)) / determinant

        if 0 <= uA <= 1 and 0 <= uB <= 1:
            ix = l1x1 + uA * (l1x2 - l1x1)
            iy = l1y1 + uA * (l1y2 - l1y1)
            return (ix, iy)

        return (None, None)

    @staticmethod
    def line_line_dist(l1x1, l1y1, l1x2, l1y2, l2x1, l2y1, l2x2, l2y2):
        ix, iy = Collide.line_line_XY(l1x1, l1y1, l1x2, l1y2, l2x1, l2y1, l2x2, l2y2)
        if ix is not None:
            return distance_to(l1x1, l1y1, ix, iy)
        return None

    @staticmethod
    def line_line_dist_squared(l1x1, l1y1, l1x2, l1y2, l2x1, l2y1, l2x2, l2y2):
        ix, iy = Collide.line_line_XY(l1x1, l1y1, l1x2, l1y2, l2x1, l2y1, l2x2, l2y2)
        if ix is not None:
            return distance_to_squared(l1x1, l1y1, ix, iy)
        return None

    @staticmethod
    def line_circle(x1, y1, x2, y2, cx, cy, radius):
        r_sq = radius ** 2

        dist_sq = (x1 - cx) ** 2 + (y1 - cy) ** 2
        if dist_sq <= r_sq:
            return True

        dist_sq = (x2 - cx) ** 2 + (y2 - cy) ** 2
        if dist_sq <= r_sq:
            return True

        dx = x2 - x1
        dy = y2 - y1
        l_sq = dx ** 2 + dy ** 2
        dot = (((cx - x1) * dx) + ((cy - y1) * dy)) / l_sq

        ix = x1 + dot * dx
        if (ix < x1) == (ix < x2):
            return False

        iy = y1 + dot * dy
        if (iy < y1) == (iy < y2):
            return False

        dist_sq = (ix - cx) ** 2 + (iy - cy) ** 2
        if dist_sq <= r_sq:
            return True

        return False

    @staticmethod
    def line_circle_XY(x1, y1, x2, y2, cx, cy, radius):
        if Collide.circle_point(cx, cy, radius, x1, y1):
            return (x1, y1)

        x1 -= cx
        y1 -= cy
        x2 -= cx
        y2 -= cy

        if x2 < x1:
            x_min, x_max = x2, x1
        else:
            x_min, x_max = x1, x2

        if y2 < y1:
            y_min, y_max = y2, y1
        else:
            y_min, y_max = y1, y2

        # Coefficients of circle
        c_r2 = radius ** 2

        # Simplify if dx == 0: Vertical line
        dx = x2 - x1
        if dx == 0:
            d = c_r2 - x1**2
            if d < 0:
                return (None, None)
            elif d == 0:
                i = 0
            else:
                i = math.sqrt(d)

            iy = None
            if y_min <= i <= y_max:
                iy = i

            if y_min <= -i <= y_max:
                if iy is None or abs(i - y1) > abs(-i - y1):
                    iy = -i

            if iy:
                return (x1 + cx, iy + cy)
            return (None, None)

        # Gradient of line
        l_m = (y2 - y1) / dx

        # Simplify if l_m == 0: Horizontal line
        if l_m == 0:
            d = c_r2 - y1**2
            if d < 0:
                return (None, None)
            elif d == 0:
                i = 0
            else:
                i = math.sqrt(d)
            ix = None
            if x_min <= i <= x_max:
                ix = i

            if x_min <= -i <= x_max:
                if ix is None or abs(i - x1) > abs(-i - x1):
                    ix = -i

            if ix:
                return (ix + cx, y1 + cy)
            return (None, None)

        # y intercept
        l_c = y1 - l_m * x1

        # Coefficients of quadratic
        a = 1 + l_m**2
        b = 2 * l_c * l_m
        c = l_c**2 - c_r2

        # Calculate discriminant and solve quadratic
        discriminant = b**2 - 4 * a * c
        if discriminant < 0:
            return (None, None)

        if discriminant == 0:
            d_root = 0
        else:
            d_root = math.sqrt(discriminant)

        ix = None
        i1 = (-b + d_root) / (2 * a)
        if x_min <= i1 <= x_max:
            ix = i1

        i2 = (-b - d_root) / (2 * a)
        if x_min <= i2 <= x_max:
            if ix is None or abs(i1 - x1) > abs(i2 - x1):
                ix = i2

        if ix:
            return (ix + cx, l_m * ix + l_c + cy)

        return (None, None)

    @staticmethod
    def line_circle_dist(x1, y1, x2, y2, cx, cy, radius):
        ix, iy = Collide.line_circle_XY(x1, y1, x2, y2, cx, cy, radius)
        if ix is not None:
            return distance_to(x1, y1, ix, iy)
        return None

    @staticmethod
    def line_circle_dist_squared(x1, y1, x2, y2, cx, cy, radius):
        ix, iy = Collide.line_circle_XY(x1, y1, x2, y2, cx, cy, radius)
        if ix is not None:
            return distance_to_squared(x1, y1, ix, iy)
        return None

    @staticmethod
    def _rect_lines(rx, ry, w, h):
        half_w = w / 2
        half_h = h / 2
        rect_lines = [
            [rx - half_w, ry - half_h, rx - half_w, ry + half_h],
            [rx - half_w, ry - half_h, rx + half_w, ry - half_h],
            [rx + half_w, ry + half_h, rx - half_w, ry + half_h],
            [rx + half_w, ry + half_h, rx + half_w, ry - half_h],
        ]
        return rect_lines

    @staticmethod
    def line_rect(x1, y1, x2, y2, rx, ry, w, h):
        if Collide.rect_points(rx, ry, w, h, [(x1, y1), (x2, y2)]) != -1:
            return True

        rect_lines = Collide._rect_lines(rx, ry, w, h)
        if Collide.line_lines(x1, y1, x2, y2, rect_lines) != -1:
            return True

        return False

    @staticmethod
    def line_rect_XY(x1, y1, x2, y2, rx, ry, w, h):
        if Collide.rect_point(rx, ry, w, h, x1, y1):
            return (x1, y1)

        rect_lines = Collide._rect_lines(rx, ry, w, h)

        XYs = []
        for line in rect_lines:
            ix, iy = Collide.line_line_XY(x1, y1, x2, y2,
                                          line[0], line[1], line[2], line[3])
            if ix is not None:
                XYs.append((ix, iy))

        length = len(XYs)
        if length == 0:
            return (None, None)
        elif length == 1:
            return XYs[0]

        ix, iy = XYs[0]
        shortest_dist = (ix - x1) ** 2 + (iy - y1) ** 2
        for XY in XYs:
            dist = (XY[0] - x1) ** 2 + (XY[1] - y1) ** 2
            if dist < shortest_dist:
                ix, iy = XY
                shortest_dist = dist

        return (ix, iy)

    @staticmethod
    def line_rect_dist(x1, y1, x2, y2, rx, ry, w, h):
        ix, iy = Collide.line_rect_XY(x1, y1, x2, y2, rx, ry, w, h)
        if ix is not None:
            return distance_to(x1, y1, ix, iy)
        return None

    @staticmethod
    def line_rect_dist_squared(x1, y1, x2, y2, rx, ry, w, h):
        ix, iy = Collide.line_rect_XY(x1, y1, x2, y2, rx, ry, w, h)
        if ix is not None:
            return distance_to_squared(x1, y1, ix, iy)
        return None

    @staticmethod
    def line_obb_XY(x1, y1, x2, y2, ox, oy, w, h, angle):
        half_width = w / 2
        half_height = h / 2
        r_angle = math.radians(angle)
        costheta = math.cos(r_angle)
        sintheta = math.sin(r_angle)

        tx = x1 - ox
        ty = y1 - oy
        rx = tx * costheta - ty * sintheta
        ry = ty * costheta + tx * sintheta

        if (rx > -half_width and rx < half_width and
                ry > -half_height and ry < half_height):
            return (x1, y1)

        wc = half_width * costheta
        hs = half_height * sintheta
        hc = half_height * costheta
        ws = half_width * sintheta
        p = [
            [ox + wc + hs, oy + hc - ws],
            [ox - wc + hs, oy + hc + ws],
            [ox + wc - hs, oy - hc - ws],
            [ox - wc - hs, oy - hc + ws],
        ]
        obb_lines = [
            [p[0][0], p[0][1], p[1][0], p[1][1]],
            [p[1][0], p[1][1], p[3][0], p[3][1]],
            [p[3][0], p[3][1], p[2][0], p[2][1]],
            [p[2][0], p[2][1], p[0][0], p[0][1]]
        ]

        XYs = []
        for li in obb_lines:
            ix, iy = Collide.line_line_XY(x1, y1, x2, y2, li[0], li[1], li[2], li[3])
            if ix is not None:
                XYs.append((ix, iy))

        length = len(XYs)
        if length == 0:
            return (None, None)
        elif length == 1:
            return XYs[0]

        ix, iy = XYs[0]
        shortest_dist = (ix - x1) ** 2 + (iy - y1) ** 2
        for XY in XYs:
            dist = (XY[0] - x1) ** 2 + (XY[1] - y1) ** 2
            if dist < shortest_dist:
                ix, iy = XY
                shortest_dist = dist

        return (ix, iy)

    @staticmethod
    def line_obb_dist(x1, y1, x2, y2, ox, oy, w, h, angle):
        ix, iy = Collide.line_obb_XY(x1, y1, x2, y2, ox, oy, w, h, angle)
        if ix is not None:
            return distance_to(x1, y1, ix, iy)
        return None

    @staticmethod
    def line_obb_dist_squared(x1, y1, x2, y2, ox, oy, w, h, angle):
        ix, iy = Collide.obb_line_XY(x1, y1, x2, y2, ox, oy, w, h, angle)
        if ix is not None:
            return distance_to_squared(x1, y1, ix, iy)
        return None

    @staticmethod
    def circle_point(x1, y1, radius, x2, y2):
        rSquare = radius ** 2
        dSquare = (x2 - x1)**2 + (y2 - y1)**2

        if dSquare < rSquare:
            return True

        return False

    @staticmethod
    def circle_points(x, y, radius, points):
        rSquare = radius ** 2

        i = 0
        for i, point in enumerate(points):
            try:
                px = point[0]
                py = point[1]
            except KeyError:
                px = point.x
                py = point.y
            dSquare = (px - x)**2 + (py - y)**2

            if dSquare < rSquare:
                return i
            i += 1

        return -1

    @staticmethod
    def circle_line(cx, cy, radius, x1, y1, x2, y2):
        return Collide.line_circle(x1, y1, x2, y2, cx, cy, radius)

    @staticmethod
    def circle_circle(x1, y1, r1, x2, y2, r2):
        rSquare = (r1 + r2) ** 2
        dSquare = (x2 - x1)**2 + (y2 - y1)**2

        if dSquare < rSquare:
            return True

        return False

    @staticmethod
    def circle_rect(cx, cy, cr, rx, ry, rw, rh):
        h_w = rw / 2
        h_h = rh / 2
        rect_l = rx - h_w
        rect_t = ry - h_h

        if cx < rect_l:
            dx2 = (cx - rect_l) ** 2
        elif cx > (rect_l + rw):
            dx2 = (cx - rect_l - rw) ** 2
        else:
            dx2 = 0

        if cy < rect_t:
            dy2 = (cy - rect_t) ** 2
        elif cy > (rect_t + rh):
            dy2 = (cy - rect_t - rh) ** 2
        else:
            dy2 = 0

        dist2 = dx2 + dy2

        if dist2 < (cr ** 2):
            return True

        return False

    @staticmethod
    def rect_point(x, y, w, h, px, py):
        half_w = w / 2
        half_h = h / 2

        if (
            px < x - half_w
            or px > x + half_w
            or py < y - half_h
            or py > y + half_h
        ):
            return False

        return True

    @staticmethod
    def rect_points(x, y, w, h, points):
        half_w = w / 2
        half_h = h / 2
        min_x = x - half_w
        max_x = x + half_w
        min_y = y - half_h
        max_y = y + half_h

        for i, point in enumerate(points):
            try:
                px = point[0]
                py = point[1]
            except KeyError:
                px = point.x
                py = point.y
            if (
                px >= min_x
                and px <= max_x
                and py >= min_y
                and py <= max_y
            ):
                return i

        return -1

    @staticmethod
    def rect_line(x, y, w, h, lx1, ly1, lx2, ly2):
        return Collide.line_rect(lx1, ly1, lx2, ly2, x, y, w, h)

    @staticmethod
    def rect_circle(rx, ry, rw, rh, cx, cy, cr):
        return Collide.circle_rect(cx, cy, cr, rx, ry, rw, rh)

    @staticmethod
    def rect_rect(x1, y1, w1, h1, x2, y2, w2, h2):
        h_w1 = w1 / 2
        h_h1 = h1 / 2
        h_w2 = w2 / 2
        h_h2 = h2 / 2

        if (
            x2 - h_w2 > x1 + h_w1
            or x2 + h_w2 < x1 - h_w1
            or y2 - h_h2 > y1 + h_h1
            or y2 + h_h2 < y1 - h_h1
        ):
            return False

        return True

    class Obb:
        def __init__(self, x, y, w, h, angle):
            self.x = x
            self.y = y
            self.angle = angle
            self.width = w
            self.height = h
            self.half_w = w / 2
            self.half_h = h / 2
            self.b_radius_sq = self.half_w ** 2 + self.half_h ** 2
            r_angle = math.radians(angle)
            self.costheta = math.cos(r_angle)
            self.sintheta = math.sin(r_angle)
            self._lines = None
            self._points = None

        def transform_point(self, px, py):
            tx = px - self.x
            ty = py - self.y
            rx = tx * self.costheta - ty * self.sintheta
            ry = ty * self.costheta + tx * self.sintheta
            return (rx, ry)

        def contains(self, px, py):
            rx, ry = self.transform_point(px, py)
            tx = px - self.x
            ty = py - self.y

            if tx ** 2 + ty ** 2 > self.b_radius_sq:
                return False
            return (rx > -self.half_w and rx < self.half_w
                    and ry > -self.half_h and ry < self.half_h)

        def collideline(self, lx1, ly1, lx2, ly2):
            if self.contains(lx1, ly1) or self.contains(lx2, ly2):
                return True

            if Collide.line_lines(lx1, ly1, lx2, ly2, self.lines()) != -1:
                return True

            return False

        def collidecircle(self, cx, cy, radius):
            return Collide.circle_rect(*self.transform_point(cx, cy), radius,
                                       0, 0, self.width, self.height)

        def colliderect(self, rx, ry, rw, rh):
            tx = rx - self.x
            ty = ry - self.y

            if tx ** 2 + ty ** 2 > (self.half_h + self.half_w + rw + rh) ** 2:
                return False

            if self.contains(rx, ry):
                return True

            if Collide.rect_point(rx, ry, rw, rh, self.x, self.y):
                return True

            if Collide.rect_points(rx, ry, rw, rh, self.points()) != -1:
                return True

            h_rw = rw / 2
            h_rh = rh / 2
            rect_points = [
                [rx - h_rw, ry - h_rh], [rx + h_rw, ry - h_rh],
                [rx + h_rw, ry + h_rh], [rx - h_rw, ry + h_rh]
            ]
            for point in rect_points:
                if self.contains(*point):
                    return True

        def collideobb(self, x, y, w, h, angle):
            tx, ty = self.transform_point(x, y)
            return Collide.Obb(tx, ty, w, h, angle - self.angle)\
                .colliderect(0, 0, self.width, self.height)

        def points(self):
            if self._points is not None:
                return self._points

            wc = self.half_w * self.costheta
            hs = self.half_h * self.sintheta
            hc = self.half_h * self.costheta
            ws = self.half_w * self.sintheta
            self._points = [
                [self.x + wc + hs, self.y + hc - ws],
                [self.x - wc + hs, self.y + hc + ws],
                [self.x - wc - hs, self.y - hc + ws],
                [self.x + wc - hs, self.y - hc - ws],
            ]
            return self._points

        def lines(self):
            if self._lines is not None:
                return self._lines

            p = self.get_points()
            self._lines = [
                [p[0][0], p[0][1], p[1][0], p[1][1]],
                [p[1][0], p[1][1], p[2][0], p[2][1]],
                [p[3][0], p[3][1], p[3][0], p[3][1]],
                [p[3][0], p[3][1], p[0][0], p[0][1]]
            ]
            return self._lines

    @staticmethod
    def obb_point(x, y, w, h, angle, px, py):
        obb = Collide.Obb(x, y, w, h, angle)
        return obb.contains(px, py)

    @staticmethod
    def obb_points(x, y, w, h, angle, points):
        obb = Collide.Obb(x, y, w, h, angle)
        for i, point in enumerate(points):
            try:
                px, py = point[0], point[1]
            except KeyError:
                px, py = point.x, point.y
            if obb.contains(px, py):
                return i

        return -1

    @staticmethod
    def obb_line(x, y, w, h, angle, lx1, ly1, lx2, ly2):
        obb = Collide.Obb(x, y, w, h, angle)
        return obb.collideline(lx1, ly1, lx2, ly2)

    @staticmethod
    def obb_lines(x, y, w, h, angle, lines):
        obb = Collide.Obb(x, y, w, h, angle)
        for i, line in enumerate(lines):
            if obb.collideline(*line):
                return i
        return -1

    @staticmethod
    def obb_circle(x, y, w, h, angle, cx, cy, radius):
        obb = Collide.Obb(x, y, w, h, angle)
        return obb.collidecircle(cx, cy, radius)

    @staticmethod
    def obb_circles(x, y, w, h, angle, circles):
        obb = Collide.Obb(x, y, w, h, angle)
        for i, circle in enumerate(circles):
            if obb.collidecircle(*circle):
                return i
        return -1

    @staticmethod
    def obb_rect(x, y, w, h, angle, rx, ry, rw, rh):
        obb = Collide.Obb(x, y, w, h, angle)
        return obb.colliderect(rx, ry, rw, rh)

    @staticmethod
    def obb_rects(x, y, w, h, angle, rects):
        obb = Collide.Obb(x, y, w, h, angle)
        for i, circle in enumerate(rects):
            if obb.colliderect(*rects):
                return i
        return -1

    @staticmethod
    def obb_obb(x, y, w, h, angle, x2, y2, w2, h2, angle2):
        obb = Collide.Obb(x, y, w, h, angle)
        return obb.collideobb(x2, y2, w2, h2, angle2)
