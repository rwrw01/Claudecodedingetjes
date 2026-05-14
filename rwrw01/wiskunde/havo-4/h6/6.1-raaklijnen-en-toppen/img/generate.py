"""Genereer matplotlib-PNG's voor 6.1 Raaklijnen en toppen.

Verifieer alle punten en hellingen met print-statements voordat de figuur wordt opgeslagen.
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


def style_axes(ax, x_range, y_range):
    ax.axhline(0, color="#94a3b8", lw=1)
    ax.axvline(0, color="#94a3b8", lw=1)
    ax.set_xlim(*x_range)
    ax.set_ylim(*y_range)
    ax.set_xlabel("x")
    ax.set_ylabel("y")


def fig1_helling_ontdekken():
    """y = x^2 met raaklijnen op (1,1), (2,4), (3,9). GEEN helling-labels — Kasper moet zelf aflezen."""
    print("\nfig1_helling_ontdekken -- y = x^2 (ontdek-versie zonder helling-labels)")
    pts = [(1, 1, 2), (2, 4, 4), (3, 9, 6)]
    for x, y, m in pts:
        assert y == x * x, f"y={y} klopt niet met x^2={x*x}"
        assert m == 2 * x, f"m={m} klopt niet met 2x={2*x}"
        print(f"  punt ({x}, {y}): verwachte helling 2x = {m} (NIET op figuur)")
    fig, ax = plt.subplots(figsize=(7, 5))
    xs = np.linspace(-0.5, 3.7, 200)
    ax.plot(xs, xs**2, color="#2563eb", lw=2.5, label="y = x²")
    labels = ["A", "B", "C"]
    for (x, y, m), naam in zip(pts, labels):
        b = y - m * x
        tx = np.linspace(x - 1, x + 1, 50)
        ax.plot(tx, m * tx + b, color="#dc2626", lw=2, alpha=0.85)
        ax.plot([x], [y], "o", color="#dc2626", markersize=8, zorder=5)
        ax.annotate(
            f"{naam}({x}, {y})",
            xy=(x, y),
            xytext=(x + 0.2, y - 0.9),
            fontsize=10,
            color="#7c2d12",
            ha="left",
            fontweight="bold",
        )
    style_axes(ax, (-0.5, 3.7), (-2.5, 11))
    ax.legend(loc="upper left", framealpha=0.95)
    ax.set_title("y = x² met raaklijnen op de punten A, B en C")
    out = OUT / "fig1-helling-ontdekken.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


def fig2_raaklijn_in_A():
    """f(x) = -1/2 x^2 + 2x + 2, raaklijn in A(3, 3.5). f'(x)=-x+2, f'(3)=-1, k: y = -x + 6.5"""
    print("\nfig2_raaklijn_in_A — f(x) = -½x² + 2x + 2, raaklijn in A(3, 3½)")
    f = lambda x: -0.5 * x**2 + 2 * x + 2
    df = lambda x: -x + 2
    x_A = 3
    y_A = f(x_A)
    m = df(x_A)
    b = y_A - m * x_A
    print(f"  y_A = f(3) = {y_A}  (verwacht 3.5)")
    print(f"  f'(3) = {m}  (verwacht -1)")
    print(f"  b = {b}  (verwacht 6.5)")
    assert y_A == 3.5 and m == -1 and b == 6.5
    fig, ax = plt.subplots(figsize=(7, 5))
    xs = np.linspace(-2, 7, 200)
    ax.plot(xs, f(xs), color="#2563eb", lw=2.5, label="f(x) = -½x² + 2x + 2")
    tx = np.linspace(0.5, 5.5, 50)
    ax.plot(tx, m * tx + b, color="#dc2626", lw=2, label=f"k: y = -x + 6½")
    ax.plot([x_A], [y_A], "o", color="#dc2626", markersize=8, zorder=5)
    ax.annotate(f"A(3, 3½)", xy=(x_A, y_A), xytext=(x_A + 0.3, y_A + 0.4), fontsize=11, color="#7c2d12")
    style_axes(ax, (-2, 7), (-6, 6))
    ax.legend(loc="lower left", framealpha=0.95)
    ax.set_title("Raaklijn k in punt A op de grafiek van f")
    out = OUT / "fig2-raaklijn-in-A.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


def fig3_raaklijn_rc_gegeven():
    """f(x) = x^2 - 3x + 1, raaklijn met rc=2 in B(2.5, -0.25). f'(x)=2x-3=2 -> x=2.5"""
    print("\nfig3_raaklijn_rc_gegeven — f(x) = x² - 3x + 1, raaklijn met rc = 2")
    f = lambda x: x**2 - 3 * x + 1
    df = lambda x: 2 * x - 3
    x_B = 2.5
    y_B = f(x_B)
    m = df(x_B)
    b = y_B - m * x_B
    print(f"  f'(x) = 2x - 3 = 2  ->  x = {x_B}")
    print(f"  y_B = f({x_B}) = {y_B}  (verwacht -0.25 = -¼)")
    print(f"  m = {m} (verwacht 2)")
    print(f"  b = {b}")
    assert x_B == 2.5 and y_B == -0.25 and m == 2
    fig, ax = plt.subplots(figsize=(7, 5))
    xs = np.linspace(-1, 5, 200)
    ax.plot(xs, f(xs), color="#2563eb", lw=2.5, label="f(x) = x² - 3x + 1")
    tx = np.linspace(1, 4, 50)
    ax.plot(tx, m * tx + b, color="#dc2626", lw=2, label=f"raaklijn: y = 2x - 5¼")
    ax.plot([x_B], [y_B], "o", color="#dc2626", markersize=8, zorder=5)
    ax.annotate("B(2½, -¼)", xy=(x_B, y_B), xytext=(x_B + 0.3, y_B - 0.7), fontsize=11, color="#7c2d12")
    style_axes(ax, (-1, 5), (-3, 8))
    ax.legend(loc="upper left", framealpha=0.95)
    ax.set_title("Raaklijn met helling 2 in punt B")
    out = OUT / "fig3-raaklijn-rc-gegeven.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


def fig4_top_via_afgeleide():
    """f(x) = x^3 - 3x^2 - 6x + 15. f'(x) = 3x^2 - 6x - 6 = 0 op x = 1 +/- sqrt(3).
    Maar voor 6.1 willen we een eenvoudig voorbeeld waar f'(x)=0 nette getallen geeft.
    Kies f(x) = x^3 - 6x^2 + 9x + 2. f'(x) = 3x^2 - 12x + 9 = 3(x-1)(x-3) = 0 -> x=1 (max), x=3 (min).
    f(1) = 1 - 6 + 9 + 2 = 6. f(3) = 27 - 54 + 27 + 2 = 2.
    """
    print("\nfig4_top_via_afgeleide — f(x) = x³ - 6x² + 9x + 2")
    f = lambda x: x**3 - 6 * x**2 + 9 * x + 2
    df = lambda x: 3 * x**2 - 12 * x + 9
    x_max = 1
    x_min = 3
    print(f"  f'(1) = {df(1)} (verwacht 0)")
    print(f"  f'(3) = {df(3)} (verwacht 0)")
    print(f"  f(1) = {f(1)} (max)")
    print(f"  f(3) = {f(3)} (min)")
    assert df(1) == 0 and df(3) == 0 and f(1) == 6 and f(3) == 2
    fig, ax = plt.subplots(figsize=(7, 5))
    xs = np.linspace(-0.5, 4.5, 300)
    ax.plot(xs, f(xs), color="#2563eb", lw=2.5, label="f(x) = x³ - 6x² + 9x + 2")
    for x_top, y_top, label in [(x_max, f(x_max), "max"), (x_min, f(x_min), "min")]:
        tx = np.linspace(x_top - 0.7, x_top + 0.7, 30)
        ax.plot(tx, [y_top] * len(tx), color="#dc2626", lw=2, alpha=0.85)
        ax.plot([x_top], [y_top], "o", color="#dc2626", markersize=9, zorder=5)
        ax.annotate(
            f"{label}: ({x_top}, {y_top})\nhelling = 0",
            xy=(x_top, y_top),
            xytext=(x_top + 0.25, y_top + (1.2 if label == "max" else -1.6)),
            fontsize=10,
            color="#7c2d12",
            ha="left",
        )
    style_axes(ax, (-0.5, 4.5), (-2, 10))
    ax.legend(loc="upper left", framealpha=0.95)
    ax.set_title("Toppen: waar de raaklijn horizontaal is (f'(x) = 0)")
    out = OUT / "fig4-toppen-horizontaal.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


def fig5_aantonen_top():
    """f(x) = x^4 + 2x^3 - 2x + 3. f'(x) = 4x^3 + 6x^2 - 2.
    Boekvoorbeeld: bewijs extreme waarde bij x = 1/2.
    f'(1/2) = 4*(1/8) + 6*(1/4) - 2 = 0.5 + 1.5 - 2 = 0.
    """
    print("\nfig5_aantonen_top -- f(x) = x^4 + 2x^3 - 2x + 3 (toon top bij x = 1/2)")
    f = lambda x: x**4 + 2 * x**3 - 2 * x + 3
    df = lambda x: 4 * x**3 + 6 * x**2 - 2
    x_top = 0.5
    print(f"  f'(½) = {df(0.5)} (verwacht 0)")
    print(f"  f(½) = {f(0.5)} (waarde van de top)")
    assert df(0.5) == 0.0
    fig, ax = plt.subplots(figsize=(7, 5))
    xs = np.linspace(-2.5, 1.5, 300)
    ax.plot(xs, f(xs), color="#2563eb", lw=2.5, label="f(x) = x⁴ + 2x³ - 2x + 3")
    ax.plot([x_top], [f(x_top)], "o", color="#dc2626", markersize=9, zorder=5)
    tx = np.linspace(x_top - 0.5, x_top + 0.5, 30)
    ax.plot(tx, [f(x_top)] * len(tx), color="#dc2626", lw=2, alpha=0.85)
    ax.annotate(
        f"top bij x = ½\nf(½) = {f(x_top):.3f}",
        xy=(x_top, f(x_top)),
        xytext=(x_top + 0.15, f(x_top) - 1.8),
        fontsize=10,
        color="#7c2d12",
    )
    style_axes(ax, (-2.5, 1.5), (-1, 8))
    ax.legend(loc="upper left", framealpha=0.95)
    ax.set_title("Bewijs van een top: laat zien dat f'(½) = 0")
    out = OUT / "fig5-aantonen-top.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


def fig6_twee_raakpunten():
    """f(x) = x^3 - 3x^2 - 6x + 15, raaklijnen met rc = 3 in TWEE punten A(-1, 17) en B(3, -3).
    f'(x) = 3x^2 - 6x - 6 = 3  ->  x^2 - 2x - 3 = 0  ->  (x+1)(x-3) = 0
    """
    print("\nfig6_twee_raakpunten -- f(x) = x^3 - 3x^2 - 6x + 15, raaklijnen met helling 3")
    f = lambda x: x**3 - 3 * x**2 - 6 * x + 15
    df = lambda x: 3 * x**2 - 6 * x - 6
    rc = 3
    for x in (-1, 3):
        assert df(x) == rc, f"f'({x}) = {df(x)}, verwacht {rc}"
    y_A = f(-1)
    y_B = f(3)
    print(f"  A(-1, {y_A})  -- verwacht 17")
    print(f"  B( 3, {y_B})  -- verwacht -3")
    assert y_A == 17 and y_B == -3
    fig, ax = plt.subplots(figsize=(7, 5))
    xs = np.linspace(-3, 5, 300)
    ax.plot(xs, f(xs), color="#2563eb", lw=2.5, label="f(x) = x³ - 3x² - 6x + 15")
    for x_p, y_p, lab in [(-1, 17, "A"), (3, -3, "B")]:
        b = y_p - rc * x_p
        tx = np.linspace(x_p - 1.5, x_p + 1.5, 50)
        ax.plot(tx, rc * tx + b, color="#dc2626", lw=2, alpha=0.85)
        ax.plot([x_p], [y_p], "o", color="#dc2626", markersize=8, zorder=5)
        ax.annotate(f"{lab}({x_p}, {y_p})", xy=(x_p, y_p), xytext=(x_p + 0.25, y_p + 1.5), fontsize=10, color="#7c2d12", fontweight="bold")
    style_axes(ax, (-3, 5), (-10, 22))
    ax.legend(loc="upper left", framealpha=0.95)
    ax.set_title("Twee raakpunten met dezelfde helling 3")
    out = OUT / "fig6-twee-raakpunten.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


if __name__ == "__main__":
    fig1_helling_ontdekken()
    fig2_raaklijn_in_A()
    fig3_raaklijn_rc_gegeven()
    fig4_top_via_afgeleide()
    fig5_aantonen_top()
    fig6_twee_raakpunten()
    print("\nKlaar.")
