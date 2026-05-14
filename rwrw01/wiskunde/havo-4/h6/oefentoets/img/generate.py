"""Genereer matplotlib-PNG's voor de oefentoets H6 De afgeleide functie.

Drie figuren, één per opgave die een schets nodig heeft:
  - fig-opg1: kubische functie met raaklijn k door A(2, 41/3), snijdt y-as in B(0, -19/3).
  - fig-opg5: wortelfunctie met max in (-2, 4) en raaklijn in A(7, 5/2) die x-as snijdt in B(17, 0).
  - fig-opg6: parabool y = 16 - x^2 met driehoek OPQ (driehoek met max-oppervlakte bij p = 4/sqrt(3)).

Alle berekeningen worden met asserts geverifieerd vóór de figuur wordt geschreven.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).parent
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "figure.dpi": 110,
        "savefig.dpi": 130,
        "savefig.bbox": "tight",
    }
)


def _nice_step(span):
    """Kies een leesbare tick-stap (1, 2, 5, 10) op basis van het bereik. Geen 0.5-stappen."""
    if span <= 6:
        return 1
    if span <= 14:
        return 2
    if span <= 30:
        return 5
    return 10


def style_axes(ax, x_range, y_range):
    from matplotlib.ticker import MultipleLocator
    ax.axhline(0, color="#94a3b8", lw=1)
    ax.axvline(0, color="#94a3b8", lw=1)
    ax.set_xlim(*x_range)
    ax.set_ylim(*y_range)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.xaxis.set_major_locator(MultipleLocator(_nice_step(x_range[1] - x_range[0])))
    ax.yaxis.set_major_locator(MultipleLocator(_nice_step(y_range[1] - y_range[0])))


# --------------------------------------------------------------------------
# Opgave 1 — raaklijn in A(2, 41/3) aan f(x) = 1/3 x^3 + 1/2 x^2 + 4x + 1
# --------------------------------------------------------------------------
def fig_opg1():
    """Verificatie:
      f(x)  = 1/3 x^3 + 1/2 x^2 + 4x + 1
      f(2)  = 8/3 + 2 + 8 + 1 = 8/3 + 11 = 41/3
      f'(x) = x^2 + x + 4
      f'(2) = 4 + 2 + 4 = 10
      Raaklijn k: y = 10x + b door A(2, 41/3) -> b = 41/3 - 20 = -19/3
      B(0, -19/3) (snijpunt met y-as)
    """
    print("\nfig_opg1 -- f(x) = 1/3 x^3 + 1/2 x^2 + 4x + 1, raaklijn in A(2, 41/3)")

    def f(x):
        return (1 / 3) * x**3 + (1 / 2) * x**2 + 4 * x + 1

    def fprime(x):
        return x**2 + x + 4

    yA = f(2)
    helling = fprime(2)
    yB = yA - helling * 2  # b van y = 10x + b
    print(f"  f(2)  = {yA}  (verwacht 41/3 = {41/3})")
    print(f"  f'(2) = {helling}  (verwacht 10)")
    print(f"  B(0, {yB})  (verwacht -19/3 = {-19/3})")
    assert abs(yA - 41 / 3) < 1e-9
    assert helling == 10
    assert abs(yB - (-19 / 3)) < 1e-9

    fig, ax = plt.subplots(figsize=(7, 5.5))
    xs = np.linspace(-3, 4, 300)
    ax.plot(xs, f(xs), color="#0f766e", lw=2.5, label="f(x) = ⅓x³ + ½x² + 4x + 1")
    # raaklijn k op het zichtbare bereik
    xs_k = np.linspace(-1, 4, 100)
    ax.plot(xs_k, helling * xs_k + yB, color="#dc2626", lw=2.2, label="k: y = 10x − 19/3")
    # markeer A en B
    ax.plot([2], [yA], "o", color="#dc2626", markersize=9, zorder=5)
    ax.plot([0], [yB], "o", color="#dc2626", markersize=9, zorder=5)
    ax.annotate(
        "A(2, 41/3)",
        xy=(2, yA),
        xytext=(2.2, yA - 3),
        fontsize=10,
        color="#7c2d12",
        fontweight="bold",
    )
    ax.annotate(
        "B(0, −19/3)",
        xy=(0, yB),
        xytext=(0.3, yB - 1.5),
        fontsize=10,
        color="#7c2d12",
        fontweight="bold",
    )
    style_axes(ax, (-3, 4), (-10, 20))
    ax.legend(loc="upper left", framealpha=0.95)
    ax.set_title("Opgave 1 — raaklijn k aan f in punt A")
    out = OUT / "fig-opg1.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


# --------------------------------------------------------------------------
# Opgave 5 — f(x) = sqrt(3x + 15) - 1/2 x  met max en raaklijn in A(7, 5/2)
# --------------------------------------------------------------------------
def fig_opg5():
    """Verificatie:
      f(x)   = sqrt(3x + 15) - x/2,    domein 3x + 15 >= 0  ->  x >= -5
      f(-5)  = 0 - (-5/2) = 5/2
      f(-2)  = sqrt(9) - (-1) = 3 + 1 = 4  (max)
      f(7)   = sqrt(36) - 7/2 = 6 - 3.5 = 2.5 = 5/2
      f'(x)  = 3 / (2 sqrt(3x+15)) - 1/2
      f'(-2) = 3 / 6 - 1/2 = 0  -> max
      f'(7)  = 3 / 12 - 1/2 = 1/4 - 1/2 = -1/4
      Raaklijn k: y = -x/4 + b door A(7, 5/2)  ->  b = 5/2 + 7/4 = 17/4
      x-as: 0 = -x/4 + 17/4  ->  x = 17.  B(17, 0).
    """
    print("\nfig_opg5 -- f(x) = sqrt(3x + 15) - x/2")

    def f(x):
        return np.sqrt(3 * x + 15) - x / 2

    def fprime(x):
        return 3 / (2 * np.sqrt(3 * x + 15)) - 1 / 2

    yA = f(7)
    helling = fprime(7)
    bk = yA - helling * 7
    xB = bk / (-helling)  # 0 = m x + b  ->  x = -b/m
    ymax = f(-2)
    print(f"  f(-2)  = {ymax}    (verwacht 4 — max)")
    print(f"  f(7)   = {yA}    (verwacht 5/2)")
    print(f"  f'(7)  = {helling}  (verwacht -1/4)")
    print(f"  b van k= {bk}    (verwacht 17/4 = {17/4})")
    print(f"  x_B    = {xB}    (verwacht 17)")
    assert abs(ymax - 4) < 1e-9
    assert abs(yA - 2.5) < 1e-9
    assert abs(helling - (-0.25)) < 1e-9
    assert abs(bk - 17 / 4) < 1e-9
    assert abs(xB - 17) < 1e-9

    fig, ax = plt.subplots(figsize=(7.4, 5))
    xs = np.linspace(-5, 18, 400)
    ax.plot(xs, f(xs), color="#0f766e", lw=2.5, label="f(x) = √(3x+15) − ½x")
    xs_k = np.linspace(2, 18, 50)
    ax.plot(xs_k, helling * xs_k + bk, color="#dc2626", lw=2.2, label="k: y = −¼x + 17/4")
    ax.plot([-2], [ymax], "o", color="#7c3aed", markersize=9, zorder=5)
    ax.plot([7], [yA], "o", color="#dc2626", markersize=9, zorder=5)
    ax.plot([xB], [0], "o", color="#dc2626", markersize=9, zorder=5)
    ax.annotate("max (−2, 4)", xy=(-2, ymax), xytext=(-1, 4.4), fontsize=10, color="#5b21b6", fontweight="bold")
    ax.annotate("A(7, 5/2)", xy=(7, yA), xytext=(7.3, 2.9), fontsize=10, color="#7c2d12", fontweight="bold")
    ax.annotate("B(17, 0)", xy=(xB, 0), xytext=(15.4, 0.5), fontsize=10, color="#7c2d12", fontweight="bold")
    style_axes(ax, (-6, 19), (-1, 6))
    ax.legend(loc="upper right", framealpha=0.95)
    ax.set_title("Opgave 5 — max van f en raaklijn k in A")
    out = OUT / "fig-opg5.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


# --------------------------------------------------------------------------
# Opgave 6 — parabool y = 16 - x^2 met driehoek OPQ; max bij p = 4/sqrt(3)
# --------------------------------------------------------------------------
def fig_opg6():
    """Verificatie:
      y(x)  = 16 - x^2,  parabool opent omlaag, top in (0, 16), nulpunten x = +-4
      P(p, 16 - p^2),  Q(p, 0),  O(0, 0)
      A(p)  = 1/2 * p * (16 - p^2) = 8p - 1/2 p^3
      dA/dp = 8 - 3/2 p^2 = 0  ->  p^2 = 16/3  ->  p = 4/sqrt(3) ~ 2.309
      A_max = 8*(4/sqrt(3)) - 1/2*(4/sqrt(3))^3
            = 32/sqrt(3) - 1/2 * 64/(3 sqrt(3))
            = 32/sqrt(3) - 32/(3 sqrt(3))
            = (96 - 32) / (3 sqrt(3))
            = 64 / (3 sqrt(3)) = 64 sqrt(3) / 9 ~ 12.3168
    """
    print("\nfig_opg6 -- parabool y = 16 - x^2 met driehoek OPQ")

    def y(x):
        return 16 - x**2

    def A(p):
        return 0.5 * p * (16 - p**2)

    p_max = 4 / np.sqrt(3)
    A_max = A(p_max)
    A_exact = 64 * np.sqrt(3) / 9
    print(f"  p_max = {p_max}  (verwacht 4/sqrt(3) = {4/np.sqrt(3)})")
    print(f"  A_max = {A_max}  (verwacht 64 sqrt(3)/9 = {A_exact})")
    print(f"  A_max ~ {round(A_max, 2)}  (verwacht 12,32)")
    assert abs(p_max**2 - 16 / 3) < 1e-9
    assert abs(A_max - A_exact) < 1e-9
    assert round(A_max, 2) == 12.32

    fig, ax = plt.subplots(figsize=(7, 5.5))
    xs = np.linspace(-4.5, 4.5, 300)
    ax.plot(xs, y(xs), color="#0f766e", lw=2.5, label="y = 16 − x²")

    # Driehoek met p = p_max
    P = (p_max, y(p_max))
    Q = (p_max, 0)
    O = (0, 0)
    triangle = plt.Polygon([O, P, Q], closed=True, facecolor="#fde68a", edgecolor="#b45309", lw=2, alpha=0.7)
    ax.add_patch(triangle)
    ax.plot(*zip(O, P, Q, O), color="#b45309", lw=2)

    ax.plot(*O, "o", color="#1f2937", markersize=8, zorder=5)
    ax.plot(*P, "o", color="#dc2626", markersize=9, zorder=5)
    ax.plot(*Q, "o", color="#dc2626", markersize=9, zorder=5)
    ax.annotate("O(0, 0)", xy=O, xytext=(-1.1, -1.5), fontsize=10, color="#1f2937", fontweight="bold")
    ax.annotate("P(p, 16 − p²)", xy=P, xytext=(p_max + 0.2, P[1] + 0.5), fontsize=10, color="#7c2d12", fontweight="bold")
    ax.annotate("Q(p, 0)", xy=Q, xytext=(p_max + 0.2, -1.6), fontsize=10, color="#7c2d12", fontweight="bold")

    style_axes(ax, (-5, 5), (-3, 18))
    ax.legend(loc="upper right", framealpha=0.95)
    ax.set_title("Opgave 6 — driehoek OPQ onder de parabool")
    out = OUT / "fig-opg6.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


if __name__ == "__main__":
    fig_opg1()
    fig_opg5()
    fig_opg6()
    print("\nKlaar — alle figuren gegenereerd en geverifieerd.")
