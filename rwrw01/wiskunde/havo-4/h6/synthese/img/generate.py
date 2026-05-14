"""Genereer matplotlib-PNG's voor de synthese-pagina H6.

Per opgave een visueel anker. Alle punten en hellingen worden geverifieerd
met asserts voor de figuur wordt opgeslagen.
"""

from pathlib import Path
import math

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
    """Kies een leesbare tick-stap (1, 2, 5, 10) op basis van het bereik."""
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
    """Opg.1 (walkthrough) — f(x) = 1/3 x^3 - 1/2 x^2 - 2x + 1.
    Raaklijn k in A(4, 19/3) met helling 10. Loodrechte lijn l door A
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
    assert abs(y_A - 19 / 3) < 1e-9
    assert rc_k == 10
    assert rc_l == -0.1
    assert abs(b_l - 101 / 15) < 1e-9

    fig, ax = plt.subplots(figsize=(6, 10))
    xs = np.linspace(-1, 5, 300)
    ax.plot(xs, f(xs), color="#2563eb", lw=2.5, label="f(x) = 1/3 x^3 - 1/2 x^2 - 2x + 1")
    tx = np.linspace(3.4, 4.6, 30)
    b_k = y_A - rc_k * x_A
    ax.plot(tx, rc_k * tx + b_k, color="#dc2626", lw=2, label="k: y = 10x - 33 2/3  (raaklijn)")
    tx_l = np.linspace(-0.5, 5, 50)
    ax.plot(tx_l, rc_l * tx_l + b_l, color="#7c2d12", lw=2, ls="--", label="l: y = -0,1x + 101/15  (loodrecht)")
    ax.plot([x_A], [y_A], "o", color="#dc2626", markersize=9, zorder=5)
    ax.annotate("A(4, 19/3)", xy=(x_A, y_A), xytext=(x_A + 0.3, y_A - 1.2), fontsize=11, color="#7c2d12", fontweight="bold")
    ax.plot([0], [b_l], "s", color="#7c2d12", markersize=9, zorder=5)
    ax.annotate("B(0, 101/15)", xy=(0, b_l), xytext=(0.3, b_l + 0.7), fontsize=11, color="#7c2d12", fontweight="bold")

    ax.set_aspect("equal", adjustable="box")
    style_axes(ax, (-2, 6), (-4, 12))
    ax.legend(loc="upper left", framealpha=0.95, fontsize=9)
    ax.set_title("Opg.1 — raaklijn k en loodrechte l door A")
    out = OUT / "fig1-opg1-raaklijn-loodrecht.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


def fig2_opg2_aantal_oplossingen():
    """Opg.2 — derdegraads f(x) = x^3 - 6x^2 + 9x + 2.
    Toppen: lokaal max in (1, 6), lokaal min in (3, 2).
    Voor welke p heeft f(x) = p precies één oplossing?
    Antwoord: p < 2 of p > 6.
    """
    print("\nfig2_opg2_aantal_oplossingen -- f(x) = x^3 - 6x^2 + 9x + 2")
    f = lambda x: x**3 - 6 * x**2 + 9 * x + 2
    df = lambda x: 3 * x**2 - 12 * x + 9

    # Verifieer toppen
    assert df(1) == 0
    assert df(3) == 0
    assert f(1) == 6
    assert f(3) == 2
    print("  f(1) = 6 (lokaal max), f(3) = 2 (lokaal min) -- OK")

    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    xs = np.linspace(-1, 5, 300)
    ax.plot(xs, f(xs), color="#2563eb", lw=2.5, label="f(x) = x^3 - 6x^2 + 9x + 2")

    # Het "1 oplossing"-gebied: p < 2 of p > 6 (gele zones)
    ax.axhspan(8, 10, color="#fef3c7", alpha=0.55)
    ax.axhspan(-4, 2, color="#fef3c7", alpha=0.55, label="p < 2 of p > 6: precies 1 oplossing")
    # Het "3 oplossingen"-gebied: 2 < p < 6
    ax.axhspan(2, 6, color="#dcfce7", alpha=0.55, label="2 < p < 6: 3 oplossingen")
    ax.axhline(2, color="#16a34a", lw=1, ls=":")
    ax.axhline(6, color="#16a34a", lw=1, ls=":")

    # Toppen markeren
    ax.plot([1], [6], "o", color="#dc2626", markersize=9, zorder=5)
    ax.annotate("max (1, 6)", xy=(1, 6), xytext=(-0.9, 6.7), fontsize=11, color="#7c2d12", fontweight="bold")
    ax.plot([3], [2], "o", color="#dc2626", markersize=9, zorder=5)
    ax.annotate("min (3, 2)", xy=(3, 2), xytext=(3.2, 0.5), fontsize=11, color="#7c2d12", fontweight="bold")

    style_axes(ax, (-1, 5), (-4, 10))
    ax.legend(loc="upper left", framealpha=0.95, fontsize=9)
    ax.set_title("Opg.2 — aantal oplossingen van f(x) = p")
    out = OUT / "fig2-opg2-aantal-oplossingen.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


def fig3_opg3_bereik_wortel():
    """Opg.3 — f(x) = sqrt(10 + 6x - x^2).
    Top bij x = 3 (want 6 - 2*3 = 0). f(3) = sqrt(19).
    Domein-randen: 3 - sqrt(19) en 3 + sqrt(19).
    Bereik: [0, sqrt(19)].
    """
    print("\nfig3_opg3_bereik_wortel -- f(x) = sqrt(10 + 6x - x^2)")
    f_inner = lambda x: 10 + 6 * x - x**2
    f = lambda x: np.sqrt(np.maximum(f_inner(x), 0))

    # Verifieer top
    x_top = 3
    y_top = f(x_top)
    print(f"  f(3) = {y_top}, sqrt(19) = {math.sqrt(19)}")
    assert abs(y_top - math.sqrt(19)) < 1e-9
    # Binnenste afgeleide 6-2x=0 bij x=3
    assert (6 - 2 * x_top) == 0

    dom_links = 3 - math.sqrt(19)
    dom_rechts = 3 + math.sqrt(19)
    # Controleer dat de randen exact nul opleveren (binnen tolerantie)
    assert abs(f_inner(dom_links)) < 1e-9
    assert abs(f_inner(dom_rechts)) < 1e-9
    print(f"  Domein: [{dom_links:.4f}, {dom_rechts:.4f}]")
    print(f"  Bereik: [0, {y_top:.4f}]")

    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    xs = np.linspace(dom_links, dom_rechts, 300)
    ax.plot(xs, f(xs), color="#2563eb", lw=2.5, label="f(x) = sqrt(10 + 6x - x^2)")

    # Top
    ax.plot([x_top], [y_top], "o", color="#dc2626", markersize=9, zorder=5)
    ax.annotate("top (3, sqrt 19)", xy=(x_top, y_top), xytext=(x_top + 0.3, y_top + 0.4),
                fontsize=11, color="#7c2d12", fontweight="bold")
    tx = np.linspace(x_top - 1.5, x_top + 1.5, 30)
    ax.plot(tx, [y_top] * len(tx), color="#dc2626", lw=2, alpha=0.85,
            label="horizontale raaklijn (helling = 0)")

    # Bereik gemarkeerd op y-as
    ax.axhspan(0, y_top, xmin=0, xmax=0.04, color="#fde68a", alpha=0.8)
    ax.annotate("bereik:\n0 <= y <= sqrt 19", xy=(-2, y_top / 2), fontsize=10, color="#7c2d12", fontweight="bold")

    # Domein-randen
    ax.axvline(dom_links, color="#7c2d12", lw=1, ls=":", alpha=0.6)
    ax.axvline(dom_rechts, color="#7c2d12", lw=1, ls=":", alpha=0.6)
    ax.annotate(f"x = 3 - sqrt 19\nca. -1,36", xy=(dom_links, 0.2), xytext=(dom_links + 0.2, 1.4),
                fontsize=9, color="#7c2d12")
    ax.annotate(f"x = 3 + sqrt 19\nca. 7,36", xy=(dom_rechts, 0.2), xytext=(dom_rechts - 2.6, 1.4),
                fontsize=9, color="#7c2d12")

    style_axes(ax, (-3, 9), (-1, 6))
    ax.legend(loc="upper right", framealpha=0.95, fontsize=9)
    ax.set_title("Opg.3 — bereik van een wortelfunctie")
    out = OUT / "fig3-opg3-bereik-wortel.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


def fig4_opg4_raken_elkaar():
    """Opg.4 — f(x) = 0.5 x^2 + 1 en g(x) = 2x - 1.
    Beide functies raken elkaar in (2, 3): f(2) = g(2) = 3 EN f'(2) = g'(2) = 2.
    """
    print("\nfig4_opg4_raken_elkaar -- f(x) = 0.5 x^2 + 1, g(x) = 2x - 1")
    f = lambda x: 0.5 * x**2 + 1
    df = lambda x: x
    g = lambda x: 2 * x - 1
    dg = lambda x: 2

    # Bewijs-asserts: gelijk in (2, 3) en gelijke helling 2
    assert f(2) == g(2) == 3
    assert df(2) == dg(2) == 2
    # Verifieer ook algebraisch via (x-2)^2 = 0
    # f(x) - g(x) = 0.5 x^2 - 2x + 2 = 0.5 (x-2)^2
    for x in [0, 1, 2, 3, 4]:
        verschil = f(x) - g(x)
        verwacht = 0.5 * (x - 2) ** 2
        assert abs(verschil - verwacht) < 1e-9
    print("  Raakpunt (2, 3) -- f(2)=g(2)=3 en f'(2)=g'(2)=2  OK")

    fig, ax = plt.subplots(figsize=(7.5, 6))
    xs = np.linspace(-1, 5, 300)
    ax.plot(xs, f(xs), color="#2563eb", lw=2.5, label="f(x) = 0,5 x^2 + 1")
    ax.plot(xs, g(xs), color="#16a34a", lw=2.5, label="g(x) = 2x - 1")

    # Raakpunt
    ax.plot([2], [3], "o", color="#dc2626", markersize=10, zorder=5)
    ax.annotate("raakpunt (2, 3)", xy=(2, 3), xytext=(2.3, 3.6),
                fontsize=11, color="#7c2d12", fontweight="bold")

    # Verticale stippellijn x=2
    ax.axvline(2, color="#7c2d12", lw=1, ls=":", alpha=0.5)

    ax.set_aspect("equal", adjustable="box")
    style_axes(ax, (-1, 5), (-2, 8))
    ax.legend(loc="upper left", framealpha=0.95, fontsize=10)
    ax.set_title("Opg.4 — f en g raken elkaar in (2, 3)")
    out = OUT / "fig4-opg4-raken-elkaar.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


def fig5_opg5_parallel_raakpunten():
    """Opg.5 — f(x) = 1/3 x^3 - 4x.
    Vraag: parallel met y = 5x + 7 (helling 5).
    f'(x) = x^2 - 4 = 5 -> x^2 = 9 -> x = 3 of x = -3.
    Raakpunten: (3, -3) en (-3, 3).
    Raaklijnen: y = 5x - 18 (in (3,-3)) en y = 5x + 18 (in (-3,3)).
    """
    print("\nfig5_opg5_parallel_raakpunten -- f(x) = 1/3 x^3 - 4x, helling = 5")
    f = lambda x: (1 / 3) * x**3 - 4 * x
    df = lambda x: x**2 - 4

    # Asserts
    assert df(3) == 5
    assert df(-3) == 5
    assert f(3) == -3
    assert f(-3) == 3
    # Raaklijnen
    raaklijn_a = lambda x: 5 * x - 18
    raaklijn_b = lambda x: 5 * x + 18
    assert raaklijn_a(3) == -3
    assert raaklijn_b(-3) == 3
    print("  Raakpunten (3, -3) en (-3, 3), beide helling 5 -- OK")

    fig, ax = plt.subplots(figsize=(7.5, 6.5))
    xs = np.linspace(-5, 5, 300)
    ax.plot(xs, f(xs), color="#2563eb", lw=2.5, label="f(x) = 1/3 x^3 - 4x")

    # De gegeven lijn (referentielijn helling 5)
    xs_ref = np.linspace(-2.5, 0, 30)
    ax.plot(xs_ref, 5 * xs_ref + 7, color="#94a3b8", lw=1.8, ls="--",
            label="referentielijn y = 5x + 7 (helling 5)")

    # Beide raaklijnen
    xs_a = np.linspace(1.5, 4.5, 30)
    ax.plot(xs_a, raaklijn_a(xs_a), color="#dc2626", lw=2,
            label="raaklijn in (3, -3): y = 5x - 18")
    xs_b = np.linspace(-4.5, -1.5, 30)
    ax.plot(xs_b, raaklijn_b(xs_b), color="#b45309", lw=2,
            label="raaklijn in (-3, 3): y = 5x + 18")

    # Raakpunten markeren
    ax.plot([3], [-3], "o", color="#dc2626", markersize=10, zorder=5)
    ax.annotate("(3, -3)", xy=(3, -3), xytext=(3.2, -4.2),
                fontsize=11, color="#7c2d12", fontweight="bold")
    ax.plot([-3], [3], "o", color="#b45309", markersize=10, zorder=5)
    ax.annotate("(-3, 3)", xy=(-3, 3), xytext=(-4.4, 3.6),
                fontsize=11, color="#7c2d12", fontweight="bold")

    style_axes(ax, (-6, 6), (-10, 10))
    ax.legend(loc="upper left", framealpha=0.95, fontsize=9)
    ax.set_title("Opg.5 — raakpunten met helling 5 (parallel met y = 5x + 7)")
    out = OUT / "fig5-opg5-parallel-raakpunten.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


if __name__ == "__main__":
    fig1_opg1_raaklijn_loodrecht()
    fig2_opg2_aantal_oplossingen()
    fig3_opg3_bereik_wortel()
    fig4_opg4_raken_elkaar()
    fig5_opg5_parallel_raakpunten()
    print("\nKlaar.")
