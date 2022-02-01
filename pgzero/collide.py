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
        l1x2_l1x1 = l1x2 - l1x1
        l1y2_l1y1 = l1y2 - l1y1

        determinant = (l2y2 - l2y1) * l1x2_l1x1 - (l2x2 - l2x1) * l1y2_l1y1

        # Simplify: Parallel lines are never considered to be intersecting
        if determinant == 0:
            return False

        uA = ((l2x2 - l2x1) * (l1y1 - l2y1) - (l2y2 - l2y1) * (l1x1 - l2x1)) \
            / determinant
        if uA < 0 or uA > 1:
            return False

        uB = (l1x2_l1x1 * (l1y1 - l2y1) - l1y2_l1y1 * (l1x1 - l2x1)) \
            / determinant
        if uB < 0 or uB > 1:
            return False

        return True

    @staticmethod
    def line_lines(l1x1, l1y1, l1x2, l1y2, l2):
        l1x2_l1x1 = l1x2 - l1x1
        l1y2_l1y1 = l1y2 - l1y1

        i = 0
        for li in l2:
            determinant = (li[3] - li[1]) * l1x2_l1x1 - (li[2] - li[0]) * l1y2_l1y1

            # Simplify: Parallel lines are never considered to be intersecting
            if determinant == 0:
                i += 1
                continue

            uA = ((li[2] - li[0]) * (l1y1 - li[1]) - (li[3] - li[1]) * (l1x1 - li[0]))\
                / determinant
            uB = (l1x2_l1x1 * (l1y1 - li[1]) - l1y2_l1y1 * (l1x1 - li[0])) / determinant
            if 0 <= uA <= 1 and 0 <= uB <= 1:
                return i

            i += 1

        return -1

    @staticmethod
    def line_line_XY(l1x1, l1y1, l1x2, l1y2, l2x1, l2y1, l2x2, l2y2):
        determinant = (l2y2 - l2y1) * (l1x2 - l1x1) - (l2x2 - l2x1) * (l1y2 - l1y1)

        # Simplify: Parallel lines are never considered to be intersecting
        if determinant == 0:
            return (None, None)

        uA = ((l2x2 - l2x1) * (l1y1 - l2y1) - (l2y2 - l2y1) * (l1x1 - l2x1))\
            / determinant
        uB = ((l1x2 - l1x1) * (l1y1 - l2y1) - (l1y2 - l1y1) * (l1x1 - l2x1))\
            / determinant

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
    def line_rect(x1, y1, x2, y2, rx, ry, w, h):
        if Collide.rect_points(rx, ry, w, h, [(x1, y1), (x2, y2)]) != -1:
            return True

        half_w = w / 2
        half_h = h / 2
        rect_lines = [
            [rx - half_w, ry - half_h, rx - half_w, ry + half_h],
            [rx - half_w, ry - half_h, rx + half_w, ry - half_h],
            [rx + half_w, ry + half_h, rx - half_w, ry + half_h],
            [rx + half_w, ry + half_h, rx + half_w, ry - half_h],
        ]
        if Collide.line_lines(x1, y1, x2, y2, rect_lines) != -1:
            return True

        return False

    @staticmethod
    def line_rect_XY(x1, y1, x2, y2, rx, ry, w, h):
        if Collide.rect_point(rx, ry, w, h, x1, y1):
            return (x1, y1)

        half_w = w / 2
        half_h = h / 2
        rect_lines = [
            [rx - half_w, ry - half_h, rx - half_w, ry + half_h],
            [rx - half_w, ry - half_h, rx + half_w, ry - half_h],
            [rx + half_w, ry + half_h, rx - half_w, ry + half_h],
            [rx + half_w, ry + half_h, rx + half_w, ry - half_h],
        ]
        XYs = []
        for li in rect_lines:
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

        if rx > -half_width and rx < half_width and ry > -half_height\
           and ry < half_height:
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
        dSquare = (x2 - x1) ** 2 + (y2 - y1) ** 2

        if dSquare < rSquare:
            return True

        return False

    @staticmethod
    def circle_points(x, y, radius, points):
        rSquare = radius ** 2

        i = 0
        for point in points:
            try:
                px = point[0]
                py = point[1]
            except KeyError:
                px = point.x
                py = point.y
            dSquare = (px - x) ** 2 + (py - y) ** 2

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
        dSquare = (x2 - x1) ** 2 + (y2 - y1) ** 2

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
            px < x - half_w or
            px > x + half_w or
            py < y - half_h or
            py > y + half_h
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

        i = 0
        for point in points:
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
            i += 1

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

    @staticmethod
    def obb_point(x, y, w, h, angle, px, py):
        half_width = w / 2
        half_height = h / 2
        b_radius_sq = half_width ** 2 + half_height ** 2
        tx = px - x
        ty = py - y

        if tx ** 2 + ty ** 2 > b_radius_sq:
            return False

        r_angle = math.radians(angle)
        costheta = math.cos(r_angle)
        sintheta = math.sin(r_angle)

        rx = tx * costheta - ty * sintheta
        ry = ty * costheta + tx * sintheta

        if rx > -half_width and rx < half_width\
           and ry > -half_height and ry < half_height:
            return True

        return False

    @staticmethod
    def obb_points(x, y, w, h, angle, points):
        half_width = w / 2
        half_height = h / 2
        r_angle = math.radians(angle)
        costheta = math.cos(r_angle)
        sintheta = math.sin(r_angle)

        i = 0
        for point in points:
            try:
                px = point[0]
                py = point[1]
            except KeyError:
                px = point.x
                py = point.y

            tx = px - x
            ty = py - y
            rx = tx * costheta - ty * sintheta
            ry = ty * costheta + tx * sintheta

            if (rx > -half_width and rx < half_width and
                    ry > -half_height and ry < half_height):
                return i
            i += 1

        return -1

    @staticmethod
    def obb_line(x, y, w, h, angle, lx1, ly1, lx2, ly2):
        half_width = w / 2
        half_height = h / 2
        r_angle = math.radians(angle)
        costheta = math.cos(r_angle)
        sintheta = math.sin(r_angle)

        tx = lx1 - x
        ty = ly1 - y
        rx = tx * costheta - ty * sintheta
        ry = ty * costheta + tx * sintheta

        if (rx > -half_width and rx < half_width and
           ry > -half_height and ry < half_height):
            return True

        tx = lx2 - x
        ty = ly2 - y
        rx = tx * costheta - ty * sintheta
        ry = ty * costheta + tx * sintheta

        if (rx > -half_width and rx < half_width and
                ry > -half_height and ry < half_height):
            return True

        wc = half_width * costheta
        hs = half_height * sintheta
        hc = half_height * costheta
        ws = half_width * sintheta
        p = [
            [x + wc + hs, y + hc - ws],
            [x - wc + hs, y + hc + ws],
            [x + wc - hs, y - hc - ws],
            [x - wc - hs, y - hc + ws],
        ]
        obb_lines = [
            [p[0][0], p[0][1], p[1][0], p[1][1]],
            [p[1][0], p[1][1], p[3][0], p[3][1]],
            [p[3][0], p[3][1], p[2][0], p[2][1]],
            [p[2][0], p[2][1], p[0][0], p[0][1]]
        ]

        if Collide.line_lines(lx1, ly1, lx2, ly2, obb_lines) != -1:
            return True

        return False

    @staticmethod
    def obb_lines(x, y, w, h, angle, lines):
        half_width = w / 2
        half_height = h / 2
        r_angle = math.radians(angle)
        costheta = math.cos(r_angle)
        sintheta = math.sin(r_angle)

        wc = half_width * costheta
        hs = half_height * sintheta
        hc = half_height * costheta
        ws = half_width * sintheta
        p = [
            [x + wc + hs, y + hc - ws],
            [x - wc + hs, y + hc + ws],
            [x + wc - hs, y - hc - ws],
            [x - wc - hs, y - hc + ws],
        ]
        obb_lines = [
            [p[0][0], p[0][1], p[1][0], p[1][1]],
            [p[1][0], p[1][1], p[3][0], p[3][1]],
            [p[3][0], p[3][1], p[2][0], p[2][1]],
            [p[2][0], p[2][1], p[0][0], p[0][1]]
        ]

        i = 0
        for li in lines:
            tx = li[0] - x
            ty = li[1] - y
            rx = tx * costheta - ty * sintheta
            ry = ty * costheta + tx * sintheta

            if (rx > -half_width and rx < half_width and
                    ry > -half_height and ry < half_height):
                return i

            tx = li[2] - x
            ty = li[3] - y
            rx = tx * costheta - ty * sintheta
            ry = ty * costheta + tx * sintheta

            if (rx > -half_width and rx < half_width and
                    ry > -half_height and ry < half_height):
                return i

            if Collide.line_lines(li[0], li[1], li[2], li[3], obb_lines) != -1:
                return i

            i += 1

        return -1

    @staticmethod
    def obb_circle(x, y, w, h, angle, cx, cy, radius):
        half_width = w / 2
        half_height = h / 2
        tx = cx - x
        ty = cy - y

        if tx ** 2 + ty ** 2 > (half_height + half_width + radius) ** 2:
            return False

        r_angle = math.radians(angle)
        costheta = math.cos(r_angle)
        sintheta = math.sin(r_angle)

        rx = tx * costheta - ty * sintheta
        ry = ty * costheta + tx * sintheta

        if (rx < -half_width - radius
                or rx > half_width + radius
                or ry < -half_height - radius
                or ry > half_height + radius):
            return False

        if ((rx <= half_width and rx >= -half_width) or
                (ry <= half_height and ry >= -half_height)):
            return True

        dx = abs(rx) - half_width
        dy = abs(ry) - half_height
        dist_squared = dx ** 2 + dy ** 2
        if dist_squared > radius ** 2:
            return False

        return True

    @staticmethod
    def obb_circles(x, y, w, h, angle, circles):
        half_width = w / 2
        half_height = h / 2
        r_angle = math.radians(angle)
        costheta = math.cos(r_angle)
        sintheta = math.sin(r_angle)

        i = 0
        for circle in circles:
            tx = circle[0] - x
            ty = circle[1] - y

            rx = tx * costheta - ty * sintheta
            ry = ty * costheta + tx * sintheta

            if (rx < -half_width - circle[2]
                    or rx > half_width + circle[2]
                    or ry < -half_height - circle[2]
                    or ry > half_height + circle[2]):
                i += 1
                continue

            if ((rx <= half_width and rx >= -half_width) or
                    (ry <= half_height and ry >= -half_height)):
                return i

            dx = abs(rx) - half_width
            dy = abs(ry) - half_height
            dist_squared = dx ** 2 + dy ** 2
            if dist_squared > circle[2] ** 2:
                i += 1
                continue

            return i

        return -1

    @staticmethod
    def obb_rect(x, y, w, h, angle, rx, ry, rw, rh):
        half_width = w / 2
        half_height = h / 2
        tx = rx - x
        ty = ry - y

        if tx ** 2 + ty ** 2 > (half_height + half_width + rw + rh) ** 2:
            return False

        r_angle = math.radians(angle)
        costheta = math.cos(r_angle)
        sintheta = math.sin(r_angle)

        tx2 = tx * costheta - ty * sintheta
        ty2 = ty * costheta + tx * sintheta

        if (tx2 > -half_width and tx2 < half_width and
                ty2 > -half_height and ty2 < half_height):
            return True

        wc = half_width * costheta
        hs = half_height * sintheta
        hc = half_height * costheta
        ws = half_width * sintheta
        p = [
            [wc + hs, hc - ws],
            [-wc + hs, hc + ws],
            [wc - hs, -hc - ws],
            [-wc - hs, -hc + ws],
        ]
        obb_lines = [
            [p[0][0], p[0][1], p[1][0], p[1][1]],
            [p[1][0], p[1][1], p[3][0], p[3][1]],
            [p[3][0], p[3][1], p[2][0], p[2][1]],
            [p[2][0], p[2][1], p[0][0], p[0][1]]
        ]
        h_rw = rw / 2
        h_rh = rh / 2
        rect_lines = [
            [tx - h_rw, ty - h_rh, tx - h_rw, ty + h_rh],
            [tx + h_rw, ty - h_rh, tx + h_rw, ty + h_rh],
            [tx - h_rw, ty - h_rh, tx + h_rw, ty - h_rh],
            [tx - h_rw, ty + h_rh, tx + h_rw, ty + h_rh]
        ]

        for obb_p in p:
            if (obb_p[0] > tx - h_rw and obb_p[0] < tx + h_rw and
                    obb_p[1] > ty - h_rh and obb_p[1] < ty + h_rh):
                return True

        for obb_line in obb_lines:
            l1x1 = obb_line[0]
            l1y1 = obb_line[1]
            l1x2 = obb_line[2]
            l1y2 = obb_line[3]
            l1x2_l1x1 = l1x2 - l1x1
            l1y2_l1y1 = l1y2 - l1y1

            for rect_line in rect_lines:
                l2x1 = rect_line[0]
                l2y1 = rect_line[1]
                l2x2 = rect_line[2]
                l2y2 = rect_line[3]

                determinant = (l2y2 - l2y1) * l1x2_l1x1 - (l2x2 - l2x1) * l1y2_l1y1

                # Simplify: Parallel lines are never considered to be intersecting
                if determinant == 0:
                    continue

                uA = ((l2x2 - l2x1) * (l1y1 - l2y1) - (l2y2 - l2y1) * (l1x1 - l2x1)) \
                    / determinant
                if uA < 0 or uA > 1:
                    continue

                uB = (l1x2_l1x1 * (l1y1 - l2y1) - l1y2_l1y1 * (l1x1 - l2x1))\
                    / determinant
                if uB < 0 or uB > 1:
                    continue

                return True

        return False

    @staticmethod
    def obb_rects(x, y, w, h, angle, rects):
        half_width = w / 2
        half_height = h / 2
        r_angle = math.radians(angle)
        costheta = math.cos(r_angle)
        sintheta = math.sin(r_angle)

        i = 0
        for rect in rects:
            rx = rect[0]
            ry = rect[1]
            rw = rect[2]
            rh = rect[3]

            tx = rx - x
            ty = ry - y

            if tx ** 2 + ty ** 2 > (half_height + half_width + rw + rh) ** 2:
                i += 1
                continue

            tx2 = tx * costheta - ty * sintheta
            ty2 = ty * costheta + tx * sintheta

            if (tx2 > -half_width and tx2 < half_width and
                    ty2 > -half_height and ty2 < half_height):
                return i

            wc = half_width * costheta
            hs = half_height * sintheta
            hc = half_height * costheta
            ws = half_width * sintheta
            p = [
                [wc + hs, hc - ws],
                [-wc + hs, hc + ws],
                [wc - hs, -hc - ws],
                [-wc - hs, -hc + ws],
            ]
            obb_lines = [
                [p[0][0], p[0][1], p[1][0], p[1][1]],
                [p[1][0], p[1][1], p[3][0], p[3][1]],
                [p[3][0], p[3][1], p[2][0], p[2][1]],
                [p[2][0], p[2][1], p[0][0], p[0][1]]
            ]
            h_rw = rw / 2
            h_rh = rh / 2
            rect_lines = [
                [tx - h_rw, ty - h_rh, tx - h_rw, ty + h_rh],
                [tx + h_rw, ty - h_rh, tx + h_rw, ty + h_rh],
                [tx - h_rw, ty - h_rh, tx + h_rw, ty - h_rh],
                [tx - h_rw, ty + h_rh, tx + h_rw, ty + h_rh]
            ]

            for obb_p in p:
                if (obb_p[0] > tx - h_rw and obb_p[0] < tx + h_rw and
                        obb_p[1] > ty - h_rh and obb_p[1] < ty + h_rh):
                    return i

            for obb_line in obb_lines:
                l1x1 = obb_line[0]
                l1y1 = obb_line[1]
                l1x2 = obb_line[2]
                l1y2 = obb_line[3]
                l1x2_l1x1 = l1x2 - l1x1
                l1y2_l1y1 = l1y2 - l1y1

                for rect_line in rect_lines:
                    l2x1 = rect_line[0]
                    l2y1 = rect_line[1]
                    l2x2 = rect_line[2]
                    l2y2 = rect_line[3]

                    determinant = (l2y2 - l2y1) * l1x2_l1x1 - (l2x2 - l2x1) * l1y2_l1y1

                    # Simplify: Parallel lines are never considered to be intersecting
                    if determinant == 0:
                        continue

                    uA = ((l2x2 - l2x1) * (l1y1 - l2y1) - (l2y2 - l2y1)
                          * (l1x1 - l2x1)) / determinant
                    if uA < 0 or uA > 1:
                        continue

                    uB = (l1x2_l1x1 * (l1y1 - l2y1) - l1y2_l1y1 * (l1x1 - l2x1))\
                        / determinant
                    if uB < 0 or uB > 1:
                        continue

                    return i

            i += 1

        return -1
