"""F4 cipher:

caduceus(t) -> (x, y)

A single continuous, closed, period-1000 parametric curve tracing a caduceus:
vertical staff + finial, two feathered wings, two snakes helixed around the
staff with heads at the top.

Connector runs are retraces along already-drawn ink, so the pen never shows
a stray line.
"""


from __future__ import annotations

import math

TAU = 2.0 * math.pi

# --- geometry constants -------------------------------------------------
Y_BOT, Y_TOP = -1.15, 1.15  # staff extent
Y_WING = 0.86  # wing root height on the staff
Y_S0, Y_S1 = -0.80, 0.58  # snake extent
A = 0.28  # helix half-width
TURNS = 2.75  # snake wraps (ends at +/-A)
R_KNOB = 0.06
R_HEAD = 0.07
WING_LEN, WING_RISE, WING_DROP = 0.95, 0.30, 0.28


def _lerp(a, b, u):
    return a + (b - a) * u


def _circle(cx, cy, r, a0, u, sweep=TAU):
    a = a0 + sweep * u
    return (cx + r * math.cos(a), cy + r * math.sin(a))


def _wing(u, side):
    """u in [0,1]: out along the leading edge, back along a scalloped trailing
    edge. side = +1 right, -1 left. Starts and ends at the wing root."""
    if u <= 0.5:  # leading edge, root -> tip
        p = u / 0.5
        x = WING_LEN * p
        y = Y_WING + WING_RISE * math.sin(0.5 * math.pi * p)
    else:  # trailing edge, tip -> root
        q = 1.0 - (u - 0.5) / 0.5
        x = WING_LEN * q
        y = (Y_WING
             + WING_RISE * math.sin(0.5 * math.pi * q)
             - WING_DROP * math.sin(math.pi * q)
             + 0.05 * math.sin(math.pi * q) * math.sin(6.0 * math.pi * q))
    return (side * x, y)


def _snake(u, side):
    """u in [0,1] from tail (staff center, bottom) to head (side*A, top)."""
    return (side * A * math.sin(TURNS * TAU * u), _lerp(Y_S0, Y_S1, u))


# --- segment table: (t_start, t_end, callable(u) -> (x, y)) -------------
_SEGMENTS = [
    (0, 90, lambda u: (0.0, _lerp(Y_BOT, Y_TOP, u))),  # staff up
    (90, 140, lambda u: _circle(0.0, Y_TOP + R_KNOB, R_KNOB,
     -math.pi / 2, u)),  # finial
    (140, 170, lambda u: (0.0, _lerp(Y_TOP, Y_WING, u))),  # down to wings
    (170, 280, lambda u: _wing(u, +1)),  # right wing
    (280, 390, lambda u: _wing(u, -1)),  # left wing
    (390, 420, lambda u: (0.0, _lerp(Y_WING, Y_S0, u))),  # down to snakes
    (420, 530, lambda u: _snake(u, +1)),  # snake 1 up
    (530, 570, lambda u: _circle(-A - 0.6 * R_HEAD, Y_S1 + 0.8 * R_HEAD,
     R_HEAD, math.atan2(-0.8, 0.6), u)),  # head 1
    (570, 680, lambda u: _snake(1.0 - u, +1)),  # snake 1 back down
    (680, 790, lambda u: _snake(u, -1)),  # snake 2 up
    (790, 830, lambda u: _circle(A + 0.6 * R_HEAD, Y_S1 + 0.8 * R_HEAD,
     R_HEAD, math.atan2(-0.8, -0.6), u)),  # head 2
    (830, 940, lambda u: _snake(1.0 - u, -1)),  # snake 2 back down
    (940, 1000, lambda u: (0.0, _lerp(Y_S0, Y_BOT, u))),  # close the loop
]


def caduceus(t):
    """Map t (any real) to a point (x, y) on the caduceus. Period = 1000."""
    t = t % 1000.0
    for t0, t1, f in _SEGMENTS:
        if t < t1:
            return f((t - t0) / (t1 - t0))
    return _SEGMENTS[-1][2](1.0)


if __name__ == "__main__":
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    pts = [caduceus(i) for i in range(1001)]
    xs, ys = zip(*pts)
    fig, ax = plt.subplots(figsize=(4, 7))
    ax.plot(xs, ys, lw=2.2, color="#1b3a5c", marker=',')
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig("preview.png", dpi=110, bbox_inches="tight")
    # continuity check
    worst = 0.0
    for i in range(1000):
        p, q = pts[i], pts[i + 1]
        d = math.hypot(q[0] - p[0], q[1] - p[1])
        worst = max(worst, d)
    print("max step:", worst)
    print("t=0 ", caduceus(0.0), " t=1000 ", caduceus(1000.0))


def f4_cipher(value: int) -> tuple(int, int):
    """Map an integer to .

    Args:
        value: The integer to encode (e.g. a locker number or subset sum).

    Returns:
        The ASCII code point of the mapped character.
    """
    return caduceus(value)
