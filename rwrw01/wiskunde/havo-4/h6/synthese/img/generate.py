"""Genereer matplotlib-PNG's voor de synthese-pagina H6.

Drie figuren — één per moeilijke opgave waar Kasper een visuele anker bij kan gebruiken.
Alle punten en hellingen worden geverifieerd met asserts voor de figuur wordt opgeslagen.
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


def fig1_opg1_raaklijn_loodrecht():
    """Opg.1 — f(x) = 1/3 x^3 - 1/2 x^2 - 2x + 1.
    Raaklijn k in A(4, 19/3) met helling 10. Loodrechte lijn l door A met helling -1/10
    snijdt y-as in B(0, 101/15).
    """
    print("\nfig1_opg1_raaklijn_loodrecht -- f(x) = 1/3 x^3 - 1/2 x^2 - 2x + 1")
    f = lambda x: (1 / 3) * x**3 - 0.5 * x**2 - 2 * x + 1
    df = lambda x: x**2 - x - 2
    x_A = 4
    y_A = f(x_A)
    rc_k = df(x_A)
    rc_l = -1 / rc_k
    b_l = y_A - rc_l * x_A
    print(f"  y_A = f(4) = {y_A:.6f}  (verwacht 19/3 = {19/3:.6f})")
    print(f"  rc_k = f'(4) = {rc_k}  (verwacht 10)")
    print(f"  rc_l = -1/rc_k = {rc_l}  (verwacht -0.1)")
    print(f"  b_l = {b_l:.6f}  (verwacht 101/15 = {101/15:.6f})")
    assert abs(y_A - 19 / 3) < 1e-9
    assert rc_k == 10
    assert rc_l == -0.1
    assert abs(b_l - 101 / 15) < 1e-9

    # Belangrijk: 1:1 as-schaal vereist anders zijn loodrechte lijnen visueel scheef.
    fig, ax = plt.subplots(figsize=(6, 10))
    xs = np.linspace(-1, 5, 300)
    ax.plot(xs, f(xs), color="#2563eb", lw=2.5, label="f(x) = ⅓x³ - ½x² - 2x + 1")
    # Raaklijn k -- alleen rond A tonen want helling = 10 (heel steil)
    tx = np.linspace(3.4, 4.6, 30)
    b_k = y_A - rc_k * x_A
    ax.plot(tx, rc_k * tx + b_k, color="#dc2626", lw=2, label="k: y = 10x - 33⅔  (raaklijn)")
    # Loodrechte lijn l -- helling = -1/10 (heel vlak)
    tx_l = np.linspace(-0.5, 5, 50)
    ax.plot(tx_l, rc_l * tx_l + b_l, color="#7c2d12", lw=2, ls="--", label="l: y = -0,1x + 101/15  (loodrecht op k)")
    # Punten
    ax.plot([x_A], [y_A], "o", color="#dc2626", markersize=9, zorder=5)
    ax.annotate("A(4, 19/3)", xy=(x_A, y_A), xytext=(x_A + 0.3, y_A - 1.2), fontsize=11, color="#7c2d12", fontweight="bold")
    ax.plot([0], [b_l], "s", color="#7c2d12", markersize=9, zorder=5)
    ax.annotate("B(0, 101/15)", xy=(0, b_l), xytext=(0.3, b_l + 0.7), fontsize=11, color="#7c2d12", fontweight="bold")

    ax.set_aspect("equal", adjustable="box")
    style_axes(ax, (-2, 6), (-4, 12))
    ax.legend(loc="upper left", framealpha=0.95, fontsize=9)
    ax.set_title("Opg.1 — raaklijn k in A en loodrechte l door A snijdt y-as in B")
    out = OUT / "fig1-opg1-raaklijn-loodrecht.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


def fig2_opg2_geen_oplossing():
    """Opg.2 — f(x) = (x^2 - 3x + 4)/x = x - 3 + 4/x. Twee toppen: lokaal max bij (-2, -7),
    lokaal min bij (2, 1). Voor -7 < p < 1: lijn y=p snijdt grafiek niet."""
    print("\nfig2_opg2_geen_oplossing -- f(x) = (x^2 - 3x + 4)/x")
    f = lambda x: (x**2 - 3 * x + 4) / x
    df = lambda x: 1 - 4 / x**2
    # Verifieer toppen
    for x_top, naam, verwacht_y in [(2, "min", 1), (-2, "max", -7)]:
        print(f"  f'({x_top}) = {df(x_top)} (verwacht 0)")
        print(f"  f({x_top}) = {f(x_top)} (verwacht {verwacht_y}) — {naam}")
        assert df(x_top) == 0
        assert f(x_top) == verwacht_y

    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    # twee takken vanwege asymptoot x=0
    xs_links = np.linspace(-7, -0.15, 200)
    xs_rechts = np.linspace(0.15, 7, 200)
    ax.plot(xs_links, f(xs_links), color="#2563eb", lw=2.5, label="f(x) = (x² - 3x + 4) / x")
    ax.plot(xs_rechts, f(xs_rechts), color="#2563eb", lw=2.5)

    # "verboden" p-bereik: -7 < p < 1
    ax.axhspan(-7, 1, color="#fef3c7", alpha=0.55, label="-7 < p < 1: lijn y=p snijdt grafiek niet")
    ax.axhline(-7, color="#ca8a04", lw=1, ls=":")
    ax.axhline(1, color="#ca8a04", lw=1, ls=":")

    # toppen markeren
    ax.plot([2], [1], "o", color="#dc2626", markersize=9, zorder=5)
    ax.annotate("min (2, 1)", xy=(2, 1), xytext=(2.3, 1.6), fontsize=11, color="#7c2d12", fontweight="bold")
    ax.plot([-2], [-7], "o", color="#dc2626", markersize=9, zorder=5)
    ax.annotate("max (-2, -7)", xy=(-2, -7), xytext=(-1.8, -8.5), fontsize=11, color="#7c2d12", fontweight="bold")

    style_axes(ax, (-7, 7), (-14, 14))
    ax.legend(loc="upper left", framealpha=0.95, fontsize=9)
    ax.set_title("Opg.2 — voor welke p heeft f(x) = p geen oplossing?")
    out = OUT / "fig2-opg2-geen-oplossing.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


def fig3_opg3_wortel_top():
    """Opg.3 — f(x) = sqrt(8x + 12 - x^2). Top bij x=4 (want 8-2*4=0).
    Domein: [4 - 2*sqrt(7), 4 + 2*sqrt(7)]. Max f(4) = sqrt(28) = 2*sqrt(7)."""
    print("\nfig3_opg3_wortel_top -- f(x) = sqrt(8x + 12 - x^2)")
    import math

    f = lambda x: np.sqrt(np.maximum(8 * x + 12 - x**2, 0))

    x_top = 4
    print(f"  f'(4) telt 8 - 2*4 = {8 - 2 * 4} (verwacht 0)")
    print(f"  f(4) = sqrt(28) = {f(4):.6f}  (verwacht 2*sqrt(7) = {2 * math.sqrt(7):.6f})")
    assert abs(f(4) - 2 * math.sqrt(7)) < 1e-9

    dom_links = 4 - 2 * math.sqrt(7)
    dom_rechts = 4 + 2 * math.sqrt(7)
    print(f"  Domein: [{dom_links:.6f}, {dom_rechts:.6f}]")
    assert abs(f(dom_links)) < 1e-9
    assert abs(f(dom_rechts)) < 1e-9

    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    xs = np.linspace(dom_links, dom_rechts, 300)
    ax.plot(xs, f(xs), color="#2563eb", lw=2.5, label="f(x) = √(8x + 12 - x²)")

    # Top
    ax.plot([x_top], [f(x_top)], "o", color="#dc2626", markersize=9, zorder=5)
    ax.annotate(
        f"top (4, 2√7)",
        xy=(x_top, f(x_top)),
        xytext=(x_top + 0.3, f(x_top) + 0.4),
        fontsize=11,
        color="#7c2d12",
        fontweight="bold",
    )
    # Horizontale raaklijn in de top
    tx = np.linspace(x_top - 1.5, x_top + 1.5, 30)
    ax.plot(tx, [f(x_top)] * len(tx), color="#dc2626", lw=2, alpha=0.85, label="horizontale raaklijn (helling = 0)")

    # Domein-randen
    ax.axvline(dom_links, color="#7c2d12", lw=1, ls=":", alpha=0.6)
    ax.axvline(dom_rechts, color="#7c2d12", lw=1, ls=":", alpha=0.6)
    ax.annotate(f"x = 4 - 2√7\n≈ -1,29", xy=(dom_links, 0.2), xytext=(dom_links + 0.2, 1.5), fontsize=9, color="#7c2d12")
    ax.annotate(f"x = 4 + 2√7\n≈ 9,29", xy=(dom_rechts, 0.2), xytext=(dom_rechts - 2.6, 1.5), fontsize=9, color="#7c2d12")

    style_axes(ax, (-3, 11), (-1, 7))
    ax.legend(loc="upper right", framealpha=0.95, fontsize=9)
    ax.set_title("Opg.3 — wortelfunctie met top bij x = 4 en domein [4-2√7, 4+2√7]")
    out = OUT / "fig3-opg3-wortel-top.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


if __name__ == "__main__":
    fig1_opg1_raaklijn_loodrecht()
    fig2_opg2_geen_oplossing()
    fig3_opg3_wortel_top()
    print("\nKlaar.")
