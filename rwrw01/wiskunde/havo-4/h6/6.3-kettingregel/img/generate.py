"""Genereer matplotlib-PNG's voor 6.3 De kettingregel.

Verifieer alle punten en hellingen met assert-statements voordat de figuur wordt opgeslagen.
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


def fig1_drie_x_plus_1_kwadraat():
    """y = (3x+1)^2. Parabool met top bij x = -1/3, y = 0.
    Twee aanpakken:
      1) haakjes uitwerken: 9x^2 + 6x + 1  ->  f'(x) = 18x + 6
      2) kettingregel: 2(3x+1) * 3 = 6(3x+1) = 18x + 6
    """
    print("\nfig1_drie_x_plus_1_kwadraat -- y = (3x+1)^2")
    f = lambda x: (3 * x + 1) ** 2
    df_chain = lambda x: 2 * (3 * x + 1) * 3
    df_uitgewerkt = lambda x: 18 * x + 6
    # check op meerdere punten dat beide aanpakken hetzelfde geven
    for x in (-1.0, -1 / 3, 0.0, 0.5, 1.0):
        a = df_chain(x)
        b = df_uitgewerkt(x)
        assert abs(a - b) < 1e-9, f"x={x}: chain={a}, uitgewerkt={b}"
    # top bij x = -1/3, y = 0
    x_top = -1 / 3
    assert abs(f(x_top)) < 1e-9
    assert abs(df_chain(x_top)) < 1e-9
    print(f"  top bij x = -1/3, y = {f(x_top):.6f}")
    print(f"  f'(0) = {df_chain(0)}  (verwacht 6)")
    print(f"  f'(1) = {df_chain(1)}  (verwacht 24)")
    fig, ax = plt.subplots(figsize=(7, 5))
    xs = np.linspace(-1.5, 1.0, 200)
    ax.plot(xs, f(xs), color="#2563eb", lw=2.5, label="y = (3x + 1)²")
    ax.plot([x_top], [0], "o", color="#dc2626", markersize=8, zorder=5)
    ax.annotate("top: x = -⅓", xy=(x_top, 0), xytext=(-1.2, 1.5), fontsize=10, color="#7c2d12", fontweight="bold")
    style_axes(ax, (-1.5, 1.0), (-1, 16))
    ax.legend(loc="upper left", framealpha=0.95)
    ax.set_title("De grafiek van y = (3x + 1)²")
    out = OUT / "fig1-drie-x-plus-1-kwadraat.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


def fig2_kettingregel_vergelijking():
    """Visuele vergelijking goed/fout bij g(x) = 3(4x-1)^2.
    Goed:  g'(x) = 3*2*(4x-1)*4 = 24(4x-1) = 96x - 24
    Fout (binnenste afgeleide vergeten): 3*2*(4x-1) = 6(4x-1) = 24x - 6
    Toon beide grafieken naast g(x) zelf, zodat zichtbaar wordt dat de "fout" hellingen niet kloppen.
    """
    print("\nfig2_kettingregel_vergelijking -- g(x) = 3(4x-1)^2: goed vs fout")
    g = lambda x: 3 * (4 * x - 1) ** 2
    dg_goed = lambda x: 96 * x - 24
    dg_fout = lambda x: 24 * x - 6
    # check: haakjes uitgewerkt = 3(16x^2 - 8x + 1) = 48x^2 - 24x + 3
    for x in (-0.5, 0.0, 0.25, 0.5, 1.0):
        uitgewerkt = 48 * x * x - 24 * x + 3
        assert abs(g(x) - uitgewerkt) < 1e-9
        afgeleide = 96 * x - 24
        assert abs(dg_goed(x) - afgeleide) < 1e-9
    # numerieke afgeleide op x = 0.5 moet 24 zijn
    h = 1e-6
    num = (g(0.5 + h) - g(0.5 - h)) / (2 * h)
    print(f"  g'(0.5) numeriek = {num:.4f} (verwacht 24)")
    print(f"  goed:  g'(0.5) = {dg_goed(0.5)} (verwacht 24)")
    print(f"  fout:  g'(0.5) = {dg_fout(0.5)} (verwacht 6 -- KLOPT NIET)")
    assert abs(num - 24) < 1e-3
    assert dg_goed(0.5) == 24
    assert dg_fout(0.5) == 6
    fig, ax = plt.subplots(figsize=(7.5, 5))
    xs = np.linspace(-0.2, 0.7, 200)
    ax.plot(xs, dg_goed(xs), color="#15803d", lw=2.5, label="GOED: g'(x) = 96x − 24  (·4 meegenomen)")
    ax.plot(xs, dg_fout(xs), color="#dc2626", lw=2.5, ls="--", label="FOUT: 24x − 6  (·4 vergeten)")
    # markeer x = 0.5
    ax.plot([0.5], [dg_goed(0.5)], "o", color="#15803d", markersize=8, zorder=5)
    ax.plot([0.5], [dg_fout(0.5)], "o", color="#dc2626", markersize=8, zorder=5)
    ax.annotate("24", xy=(0.5, 24), xytext=(0.52, 26), fontsize=10, color="#166534", fontweight="bold")
    ax.annotate("6", xy=(0.5, 6), xytext=(0.52, 8), fontsize=10, color="#991b1b", fontweight="bold")
    style_axes(ax, (-0.2, 0.7), (-30, 50))
    ax.legend(loc="upper left", framealpha=0.95)
    ax.set_title("g(x) = 3(4x − 1)² — hellingen goed vs fout")
    out = OUT / "fig2-kettingregel-goed-fout.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


def fig3_breuk_kwadraat():
    """h(x) = 2/(½x - 3)^2 = 2(½x - 3)^(-2). Verticale asymptoot bij x = 6.
    h'(x) = 2 * (-2)(½x - 3)^(-3) * ½ = -2(½x - 3)^(-3) = -2/(½x - 3)^3
    Voor x_A = 4: ½*4 - 3 = -1, dus h(4) = 2/1 = 2, h'(4) = -2/(-1)^3 = 2.
    Raaklijn k: y = 2x + b door (4, 2): b = 2 - 8 = -6. k: y = 2x - 6.
    Snijpunt met x-as: 0 = 2x - 6 -> x = 3. Dus x_B = 3.  (zoals in C7c van het boek)
    """
    print("\nfig3_breuk_kwadraat -- h(x) = 2/(½x - 3)^2, raaklijn in A(4, 2)")
    h = lambda x: 2 / (0.5 * x - 3) ** 2
    dh = lambda x: -2 / (0.5 * x - 3) ** 3
    x_A = 4
    y_A = h(x_A)
    m = dh(x_A)
    b = y_A - m * x_A
    x_B = -b / m  # snijpunt met x-as: 0 = m*x + b
    print(f"  h(4) = {y_A} (verwacht 2)")
    print(f"  h'(4) = {m} (verwacht 2)")
    print(f"  k: y = {m}x + {b} (verwacht y = 2x - 6)")
    print(f"  x_B = {x_B} (verwacht 3)")
    assert y_A == 2.0
    assert m == 2.0
    assert b == -6.0
    assert x_B == 3.0
    fig, ax = plt.subplots(figsize=(7, 5))
    xs_left = np.linspace(-2, 5.7, 300)
    xs_right = np.linspace(6.3, 12, 300)
    ax.plot(xs_left, h(xs_left), color="#2563eb", lw=2.5, label="h(x) = 2 / (½x − 3)²")
    ax.plot(xs_right, h(xs_right), color="#2563eb", lw=2.5)
    ax.axvline(6, color="#94a3b8", lw=1, ls=":")
    ax.annotate("asymptoot x = 6", xy=(6, 4), xytext=(6.2, 4.3), fontsize=9, color="#475569")
    tx = np.linspace(1.5, 5, 50)
    ax.plot(tx, m * tx + b, color="#dc2626", lw=2, label="k: y = 2x − 6")
    ax.plot([x_A], [y_A], "o", color="#dc2626", markersize=8, zorder=5)
    ax.plot([x_B], [0], "o", color="#dc2626", markersize=8, zorder=5)
    ax.annotate("A(4, 2)", xy=(x_A, y_A), xytext=(x_A + 0.2, y_A + 0.5), fontsize=10, color="#7c2d12", fontweight="bold")
    ax.annotate("B(3, 0)", xy=(x_B, 0), xytext=(x_B - 1.5, -1.2), fontsize=10, color="#7c2d12", fontweight="bold")
    style_axes(ax, (-2, 12), (-5, 6))
    ax.legend(loc="upper right", framealpha=0.95)
    ax.set_title("Raaklijn k aan h(x) = 2/(½x − 3)²")
    out = OUT / "fig3-breuk-kwadraat.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


def fig4_wortel_6x_min_1():
    """f(x) = sqrt(6x - 1) = (6x - 1)^(1/2). Domein x >= 1/6.
    f'(x) = (1/2)(6x - 1)^(-1/2) * 6 = 3 / sqrt(6x - 1).
    Voorbeeld: f'(½) = 3/sqrt(2) ~= 2.121.
    """
    print("\nfig4_wortel_6x_min_1 -- f(x) = sqrt(6x - 1)")
    f = lambda x: np.sqrt(6 * x - 1)
    df = lambda x: 3 / np.sqrt(6 * x - 1)
    # numerieke check op x = 1
    h = 1e-6
    num = (f(1 + h) - f(1 - h)) / (2 * h)
    print(f"  f(1) = {f(1)} (verwacht sqrt(5) ~= 2.2360)")
    print(f"  f'(1) numeriek = {num:.5f}")
    print(f"  f'(1) analytisch = {df(1):.5f} (verwacht 3/sqrt(5) ~= 1.3416)")
    assert abs(num - df(1)) < 1e-4
    assert abs(f(1) - np.sqrt(5)) < 1e-9
    fig, ax = plt.subplots(figsize=(7, 5))
    xs = np.linspace(1 / 6, 5, 300)
    ax.plot(xs, f(xs), color="#2563eb", lw=2.5, label="f(x) = √(6x − 1)")
    # markeer beginpunt op x = 1/6
    ax.plot([1 / 6], [0], "o", color="#0f766e", markersize=8, zorder=5)
    ax.annotate("start: x = ⅙", xy=(1 / 6, 0), xytext=(0.3, -0.6), fontsize=9, color="#134e4a")
    style_axes(ax, (-0.5, 5), (-1, 6))
    ax.legend(loc="lower right", framealpha=0.95)
    ax.set_title("De grafiek van f(x) = √(6x − 1)")
    out = OUT / "fig4-wortel-6x-min-1.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


def fig5_wortel_3x_plus_1_met_raaklijn():
    """f(x) = sqrt(3x + 1) = (3x + 1)^(1/2). Domein x >= -1/3.
    f'(x) = (1/2)(3x + 1)^(-1/2) * 3 = 3 / (2 sqrt(3x + 1)).
    In x_A = 1: y_A = sqrt(4) = 2. helling = 3/(2*2) = 3/4.
    Raaklijn k: y = (3/4)x + b door (1, 2): b = 2 - 3/4 = 5/4.
    k: y = 3/4 x + 5/4.
    """
    print("\nfig5_wortel_3x_plus_1_met_raaklijn -- f(x) = sqrt(3x + 1), raaklijn in A(1, 2)")
    f = lambda x: np.sqrt(3 * x + 1)
    df = lambda x: 3 / (2 * np.sqrt(3 * x + 1))
    x_A = 1
    y_A = f(x_A)
    m = df(x_A)
    b = y_A - m * x_A
    print(f"  y_A = f(1) = {y_A} (verwacht 2)")
    print(f"  m = f'(1) = {m} (verwacht 0.75)")
    print(f"  b = {b} (verwacht 1.25)")
    assert y_A == 2.0
    assert m == 0.75
    assert b == 1.25
    fig, ax = plt.subplots(figsize=(7, 5))
    xs = np.linspace(-1 / 3, 6, 300)
    ax.plot(xs, f(xs), color="#2563eb", lw=2.5, label="f(x) = √(3x + 1)")
    tx = np.linspace(-0.5, 4, 50)
    ax.plot(tx, m * tx + b, color="#dc2626", lw=2, label="k: y = ¾x + 1¼")
    ax.plot([x_A], [y_A], "o", color="#dc2626", markersize=8, zorder=5)
    ax.annotate("A(1, 2)", xy=(x_A, y_A), xytext=(x_A + 0.2, y_A + 0.3), fontsize=10, color="#7c2d12", fontweight="bold")
    style_axes(ax, (-1, 6), (-1, 5))
    ax.legend(loc="lower right", framealpha=0.95)
    ax.set_title("Raaklijn k aan f(x) = √(3x + 1) in A(1, 2)")
    out = OUT / "fig5-wortel-raaklijn.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


if __name__ == "__main__":
    fig1_drie_x_plus_1_kwadraat()
    fig2_kettingregel_vergelijking()
    fig3_breuk_kwadraat()
    fig4_wortel_6x_min_1()
    fig5_wortel_3x_plus_1_met_raaklijn()
    print("\nKlaar.")
