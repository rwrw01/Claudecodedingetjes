"""Genereer matplotlib-PNG's voor 6.4 Toepassingen van de afgeleide.

Verifieer alle punten, hellingen en oppervlakte-waarden met assert-statements
voordat de figuur wordt opgeslagen.
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


def fig1_loodrechte_lijnen():
    """Twee loodrechte lijnen: k: y = 2x - 2 en l: y = -1/2 x + 3.
    Snijpunt: 2x - 2 = -1/2 x + 3 -> 5/2 x = 5 -> x = 2, y = 2.
    Helling-product: 2 * (-1/2) = -1. -> k loodrecht op l.
    """
    print("\nfig1_loodrechte_lijnen -- k: y = 2x - 2 en l: y = -1/2 x + 3")
    mk, bk = 2, -2
    ml, bl = -0.5, 3
    # snijpunt
    x_s = (bl - bk) / (mk - ml)
    y_s = mk * x_s + bk
    print(f"  helling k = {mk}, helling l = {ml}, product = {mk*ml} (verwacht -1)")
    print(f"  snijpunt = ({x_s}, {y_s})  (verwacht (2, 2))")
    assert mk * ml == -1
    assert x_s == 2 and y_s == 2

    fig, ax = plt.subplots(figsize=(7, 5))
    xs = np.linspace(-2, 6, 200)
    ax.plot(xs, mk * xs + bk, color="#2563eb", lw=2.5, label="k: y = 2x - 2")
    ax.plot(xs, ml * xs + bl, color="#dc2626", lw=2.5, label="l: y = -½x + 3")
    ax.plot([x_s], [y_s], "o", color="#0f766e", markersize=9, zorder=5)
    ax.annotate(
        "snijpunt (2, 2)\nhelling-product = -1",
        xy=(x_s, y_s),
        xytext=(x_s + 0.4, y_s - 2),
        fontsize=10,
        color="#0f766e",
        fontweight="bold",
        arrowprops=dict(arrowstyle="->", color="#0f766e", lw=1),
    )
    style_axes(ax, (-2, 6), (-6, 6))
    ax.set_aspect("equal", adjustable="box")
    ax.legend(loc="upper left", framealpha=0.95)
    ax.set_title("Twee loodrechte lijnen — helling-product is -1")
    out = OUT / "fig1-loodrechte-lijnen.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


def fig2_rechthoek_onder_parabool():
    """y = 4 - x^2, rechthoek met P(p, 0) op x-as en Q(p, 4 - p^2) op grafiek.
    A(p) = p * (4 - p^2) = 4p - p^3 voor 0 < p < 2.
    dA/dp = 4 - 3p^2 = 0 -> p = 2/sqrt(3).
    A_max = (2/sqrt(3)) * (4 - 4/3) = (2/sqrt(3)) * (8/3) = 16 / (3*sqrt(3)).
    """
    print("\nfig2_rechthoek_onder_parabool -- y = 4 - x^2, rechthoek met P(p, 0), Q(p, 4-p^2)")
    f = lambda x: 4 - x**2
    p_opt = 2 / np.sqrt(3)
    A_max = 16 / (3 * np.sqrt(3))
    print(f"  p_opt = 2/sqrt(3) = {p_opt:.5f}  (verwacht ~1.15470)")
    print(f"  A_max = 16/(3*sqrt(3)) = {A_max:.5f}  (verwacht ~3.07920)")
    assert abs((4 - 3 * p_opt**2)) < 1e-9
    assert abs(p_opt * f(p_opt) - A_max) < 1e-9

    # Voor de visualisatie kiezen we p = 1.2 (dicht bij optimum, maar mooi rond).
    p_show = 1.2
    yQ_show = f(p_show)
    print(f"  visualisatie: p = {p_show}, Q = (1.2, {yQ_show})")
    fig, ax = plt.subplots(figsize=(7, 5))
    xs = np.linspace(-2.3, 2.3, 200)
    ax.plot(xs, f(xs), color="#2563eb", lw=2.5, label="y = 4 - x²")
    # rechthoek O-P-Q-R
    ax.fill(
        [0, p_show, p_show, 0],
        [0, 0, yQ_show, yQ_show],
        color="#fde68a",
        alpha=0.55,
        edgecolor="#b45309",
        linewidth=2,
    )
    # punten
    ax.plot([p_show], [0], "o", color="#dc2626", markersize=8, zorder=5)
    ax.plot([p_show], [yQ_show], "o", color="#dc2626", markersize=8, zorder=5)
    ax.plot([0], [yQ_show], "o", color="#dc2626", markersize=8, zorder=5)
    ax.plot([0], [0], "o", color="#dc2626", markersize=8, zorder=5)
    ax.annotate("O", xy=(0, 0), xytext=(-0.25, -0.45), fontsize=11, color="#7c2d12", fontweight="bold")
    ax.annotate("P(p, 0)", xy=(p_show, 0), xytext=(p_show + 0.1, -0.5), fontsize=11, color="#7c2d12", fontweight="bold")
    ax.annotate(
        "Q(p, 4 - p²)",
        xy=(p_show, yQ_show),
        xytext=(p_show + 0.1, yQ_show + 0.15),
        fontsize=11,
        color="#7c2d12",
        fontweight="bold",
    )
    ax.annotate(
        "oppervlakte\nA = p·(4 - p²)",
        xy=(p_show / 2, yQ_show / 2),
        ha="center",
        fontsize=10,
        color="#92400e",
        fontweight="bold",
    )
    style_axes(ax, (-2.3, 2.3), (-1, 5))
    ax.legend(loc="upper right", framealpha=0.95)
    ax.set_title("Rechthoek onder de parabool y = 4 - x²")
    out = OUT / "fig2-rechthoek-onder-parabool.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


def fig3_driehoek_OPQ():
    """y = -x^2 + 2x + 15, P(p, y_P) op grafiek, Q(p, 0). 0 < p < 5.
    Driehoek OPQ. Oppervlakte = 1/2 * |OQ| * |QP| = 1/2 * p * (-p^2 + 2p + 15)
    A(p) = 1/2 * (-p^3 + 2p^2 + 15p)
    dA/dp = 1/2 * (-3p^2 + 4p + 15) = 0 -> 3p^2 - 4p - 15 = 0
    -> p = (4 + sqrt(16 + 180)) / 6 = (4 + 14)/6 = 3.
    A(3) = 1/2 * 3 * (-9 + 6 + 15) = 1/2 * 3 * 12 = 18.
    """
    print("\nfig3_driehoek_OPQ -- y = -x^2 + 2x + 15, driehoek OPQ met P op grafiek, Q op x-as")
    f = lambda x: -x**2 + 2 * x + 15
    p_opt = 3
    A_opt = 0.5 * p_opt * f(p_opt)
    print(f"  p_opt = {p_opt}, f(3) = {f(3)} (verwacht 12)")
    print(f"  A_max = {A_opt} (verwacht 18)")
    assert f(3) == 12 and A_opt == 18

    fig, ax = plt.subplots(figsize=(7, 5))
    xs = np.linspace(-3.5, 5.5, 300)
    ax.plot(xs, f(xs), color="#2563eb", lw=2.5, label="y = -x² + 2x + 15")
    # driehoek
    yP = f(p_opt)
    ax.fill([0, p_opt, p_opt], [0, 0, yP], color="#bbf7d0", alpha=0.6, edgecolor="#15803d", linewidth=2)
    ax.plot([0], [0], "o", color="#dc2626", markersize=8, zorder=5)
    ax.plot([p_opt], [0], "o", color="#dc2626", markersize=8, zorder=5)
    ax.plot([p_opt], [yP], "o", color="#dc2626", markersize=8, zorder=5)
    ax.annotate("O", xy=(0, 0), xytext=(-0.5, -1.2), fontsize=11, color="#7c2d12", fontweight="bold")
    ax.annotate("Q(p, 0)", xy=(p_opt, 0), xytext=(p_opt + 0.15, -1.4), fontsize=11, color="#7c2d12", fontweight="bold")
    ax.annotate(
        "P(p, -p²+2p+15)",
        xy=(p_opt, yP),
        xytext=(p_opt + 0.2, yP + 0.5),
        fontsize=11,
        color="#7c2d12",
        fontweight="bold",
    )
    ax.annotate(
        "ΔOPQ\nA = ½·p·(-p²+2p+15)",
        xy=(p_opt / 2 + 0.3, yP / 3),
        ha="center",
        fontsize=10,
        color="#166534",
        fontweight="bold",
    )
    style_axes(ax, (-3.5, 5.5), (-3, 18))
    ax.legend(loc="upper left", framealpha=0.95)
    ax.set_title("Driehoek OPQ — maximale oppervlakte zoeken")
    out = OUT / "fig3-driehoek-OPQ.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


def fig4_verticale_afstand():
    """f(x) = x^2 + 4 en g(x) = x*sqrt(x) = x^(3/2). Voor p > 0 ligt A(p, p^2+4) op f en B(p, p^(3/2)) op g.
    f boven g (check: f(1) = 5, g(1) = 1).
    L(p) = (p^2 + 4) - p^(3/2)
    dL/dp = 2p - (3/2) * p^(1/2) = 0 -> p^(1/2) * (2 * p^(1/2) - 3/2) = 0
    -> sqrt(p) = 3/4 -> p = 9/16.
    Tweede afgeleide: 2 - (3/4) * p^(-1/2). Bij p = 9/16: 2 - (3/4)*(4/3) = 1 > 0 -> minimum.
    L_min = (9/16)^2 + 4 - (9/16)^(3/2)
          = 81/256 + 1024/256 - 108/256 = 997/256.
    Note: (9/16)^(3/2) = (sqrt(9/16))^3 = (3/4)^3 = 27/64 = 108/256.
    """
    print("\nfig4_verticale_afstand -- f(x) = x^2 + 4 en g(x) = x*sqrt(x)")
    f = lambda x: x**2 + 4
    g = lambda x: x * np.sqrt(x)
    p_opt = 9 / 16
    L_min_exact = 997 / 256
    L_min_calc = f(p_opt) - g(p_opt)
    print(f"  p_opt = 9/16 = {p_opt}")
    print(f"  f(9/16) = {f(p_opt)} (verwacht {81/256 + 4})")
    print(f"  g(9/16) = (3/4)^3 = {g(p_opt)} (verwacht {27/64})")
    print(f"  L_min = {L_min_calc:.6f}  (verwacht 997/256 = {L_min_exact:.6f})")
    # tweede afgeleide check
    second = 2 - (3 / 4) * p_opt ** (-0.5)
    print(f"  L''(9/16) = {second} (>0 dus minimum)")
    assert abs(L_min_calc - L_min_exact) < 1e-9
    assert second > 0

    # Voor visualisatie p = 1 (waar L = 5 - 1 = 4, mooie waarde). Plus p_opt = 9/16 als minimum.
    fig, ax = plt.subplots(figsize=(7, 5))
    xs = np.linspace(0.01, 2.5, 300)
    ax.plot(xs, f(xs), color="#2563eb", lw=2.5, label="f(x) = x² + 4")
    ax.plot(xs, g(xs), color="#15803d", lw=2.5, label="g(x) = x·√x")
    # toon x=p lijn op p = 0.9 (visueel goed plaatsbaar, niet exact het minimum)
    p_show = 0.9
    A_show = f(p_show)
    B_show = g(p_show)
    ax.plot([p_show, p_show], [B_show, A_show], color="#dc2626", lw=3, label=f"lijnstuk AB op x = p")
    ax.plot([p_show], [A_show], "o", color="#dc2626", markersize=8, zorder=5)
    ax.plot([p_show], [B_show], "o", color="#dc2626", markersize=8, zorder=5)
    ax.annotate("A(p, p²+4)", xy=(p_show, A_show), xytext=(p_show + 0.1, A_show + 0.3), fontsize=11, color="#7c2d12", fontweight="bold")
    ax.annotate("B(p, p·√p)", xy=(p_show, B_show), xytext=(p_show + 0.1, B_show - 0.5), fontsize=11, color="#7c2d12", fontweight="bold")
    ax.annotate(
        "L = f(p) - g(p)",
        xy=(p_show + 0.05, (A_show + B_show) / 2),
        xytext=(p_show + 0.45, (A_show + B_show) / 2),
        fontsize=11,
        color="#b91c1c",
        fontweight="bold",
        arrowprops=dict(arrowstyle="->", color="#b91c1c"),
    )
    style_axes(ax, (-0.3, 2.5), (-0.5, 9))
    ax.legend(loc="upper left", framealpha=0.95)
    ax.set_title("Verticale afstand L tussen twee grafieken op x = p")
    out = OUT / "fig4-verticale-afstand.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


def fig5_loodrecht_door_punt():
    """Lijn l: y = 3x - 2. Lijn k door A(6, 7) loodrecht op l.
    rc_l = 3, dus rc_k = -1/3. k: y = -1/3 x + b.
    Door A: 7 = -1/3 * 6 + b = -2 + b -> b = 9.
    k: y = -1/3 x + 9.
    """
    print("\nfig5_loodrecht_door_punt -- l: y = 3x - 2, k door A(6, 7) loodrecht op l")
    rc_l = 3
    rc_k = -1 / rc_l
    A = (6, 7)
    b_k = A[1] - rc_k * A[0]
    print(f"  rc_l = {rc_l}, rc_k = {rc_k} (verwacht -1/3 = {-1/3})")
    print(f"  rc_k * rc_l = {rc_k * rc_l} (verwacht -1)")
    print(f"  b_k = {b_k} (verwacht 9)")
    assert abs(rc_k * rc_l + 1) < 1e-9
    assert abs(b_k - 9) < 1e-9

    fig, ax = plt.subplots(figsize=(7, 5))
    xs = np.linspace(-2, 10, 200)
    ax.plot(xs, rc_l * xs - 2, color="#2563eb", lw=2.5, label="l: y = 3x - 2")
    ax.plot(xs, rc_k * xs + b_k, color="#dc2626", lw=2.5, label="k: y = -⅓x + 9")
    ax.plot([A[0]], [A[1]], "o", color="#0f766e", markersize=9, zorder=5)
    ax.annotate(
        f"A(6, 7)",
        xy=A,
        xytext=(A[0] + 0.2, A[1] + 0.8),
        fontsize=11,
        color="#0f766e",
        fontweight="bold",
    )
    style_axes(ax, (-2, 10), (-6, 12))
    ax.set_aspect("equal", adjustable="box")
    ax.legend(loc="lower right", framealpha=0.95)
    ax.set_title("Lijn k door A(6, 7), loodrecht op l")
    out = OUT / "fig5-loodrecht-door-punt.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


if __name__ == "__main__":
    fig1_loodrechte_lijnen()
    fig2_rechthoek_onder_parabool()
    fig3_driehoek_OPQ()
    fig4_verticale_afstand()
    fig5_loodrecht_door_punt()
    print("\nKlaar.")
