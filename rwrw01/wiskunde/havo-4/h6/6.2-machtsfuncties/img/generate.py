"""Genereer matplotlib-PNG's voor 6.2 De afgeleide van machtsfuncties.

Verifieer alle waarden en hellingen met assert + print VOORDAT de figuur wordt opgeslagen.
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


def fig1_negatieve_exponent():
    """y = 1/x^2 en y' = -2/x^3 samen in 1 figuur.

    Voor x > 0: y = 1/x^2 dalend (van +oneindig naar 0). y' = -2/x^3 is negatief (dus onder x-as).
    Voor x < 0: y = 1/x^2 stijgend richting 0 (van rechts naar links). y' = -2/x^3 is positief.

    Toont: afgeleide is negatief precies daar waar de functie daalt.
    """
    print("\nfig1_negatieve_exponent -- y = 1/x^2 en y' = -2/x^3")
    f = lambda x: 1.0 / (x * x)
    df = lambda x: -2.0 / (x ** 3)

    # Verificatie op een paar punten
    for x in (-2.0, -1.0, -0.5, 0.5, 1.0, 2.0):
        y = f(x)
        m = df(x)
        expected_y = 1.0 / (x ** 2)
        expected_m = -2.0 / (x ** 3)
        assert abs(y - expected_y) < 1e-12
        assert abs(m - expected_m) < 1e-12
        # Teken-controle: f daalt voor x>0, dus df<0 ; f stijgt voor x<0, dus df>0
        if x > 0:
            assert m < 0, f"f'({x}) moet negatief zijn (functie daalt rechts)"
        else:
            assert m > 0, f"f'({x}) moet positief zijn (functie stijgt links)"
        print(f"  x={x:>5}:  f(x)={y:8.4f}   f'(x)={m:8.4f}")

    fig, ax = plt.subplots(figsize=(7.5, 5.2))
    # Linker tak en rechter tak apart plotten om de asymptoot bij x=0 te vermijden
    xs_l = np.linspace(-3.5, -0.35, 300)
    xs_r = np.linspace(0.35, 3.5, 300)
    ax.plot(xs_l, f(xs_l), color="#2563eb", lw=2.5, label="f(x) = 1/x²  =  x⁻²")
    ax.plot(xs_r, f(xs_r), color="#2563eb", lw=2.5)
    ax.plot(xs_l, df(xs_l), color="#dc2626", lw=2.2, ls="--", label="f'(x) = −2/x³  =  −2x⁻³")
    ax.plot(xs_r, df(xs_r), color="#dc2626", lw=2.2, ls="--")
    ax.axvline(0, color="#94a3b8", lw=1)
    ax.axhline(0, color="#94a3b8", lw=1)
    ax.set_xlim(-3.7, 3.7)
    ax.set_ylim(-6, 6)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(loc="upper right", framealpha=0.95)
    ax.set_title("f(x) = 1/x² (blauw) en de afgeleide f'(x) = −2/x³ (rood, gestippeld)")
    out = OUT / "fig1-omgekeerd-kwadraat.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


def fig2_wortel_raaklijn():
    """f(x) = sqrt(x). f'(x) = 1/(2*sqrt(x)). Op x=4: f(4)=2, f'(4)=1/4. Raaklijn k: y = (1/4)x + 1."""
    print("\nfig2_wortel_raaklijn -- f(x) = sqrt(x), raaklijn in (4, 2)")
    f = lambda x: np.sqrt(x)
    df = lambda x: 1.0 / (2.0 * np.sqrt(x))

    x_A = 4.0
    y_A = float(f(x_A))
    m = float(df(x_A))
    b = y_A - m * x_A
    print(f"  y_A = f(4) = {y_A}  (verwacht 2)")
    print(f"  f'(4) = {m}  (verwacht 0.25)")
    print(f"  b = {b}  (verwacht 1)")
    assert y_A == 2.0
    assert m == 0.25
    assert b == 1.0

    fig, ax = plt.subplots(figsize=(7.5, 5))
    xs = np.linspace(0.001, 9.5, 400)
    ax.plot(xs, f(xs), color="#2563eb", lw=2.5, label="f(x) = √x  =  x^(½)")
    tx = np.linspace(0.5, 8.5, 50)
    ax.plot(tx, m * tx + b, color="#dc2626", lw=2, label="k: y = ¼x + 1")
    ax.plot([x_A], [y_A], "o", color="#dc2626", markersize=9, zorder=5)
    ax.annotate("A(4, 2)", xy=(x_A, y_A), xytext=(x_A + 0.3, y_A - 0.55), fontsize=11, color="#7c2d12", fontweight="bold")
    style_axes(ax, (-0.5, 9.5), (-0.5, 4.5))
    ax.legend(loc="lower right", framealpha=0.95)
    ax.set_title("Raaklijn aan f(x) = √x in het punt A(4, 2)")
    out = OUT / "fig2-wortel-raaklijn.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


def fig3_extreme_waarden_twee_takken():
    """f(x) = (x^2 + 16)/(4x) = (1/4)x + 4/x.

    f'(x) = 1/4 - 4/x^2 = 0  ->  x^2 = 16  ->  x = +/-4
    f(-4) = (16+16)/(-16) = 32/-16 = -2  -> dit is MAXIMUM van de linker tak
    f( 4) = (16+16)/( 16) = 32/ 16 = +2  -> dit is MINIMUM van de rechter tak

    Let op: het maximum (-2) is KLEINER dan het minimum (+2) -- twee aparte takken.
    """
    print("\nfig3_extreme_waarden -- f(x) = (x²+16)/(4x)")
    f = lambda x: (x * x + 16) / (4 * x)
    df = lambda x: 0.25 - 4.0 / (x * x)

    for x in (-4.0, 4.0):
        assert abs(df(x)) < 1e-12, f"f'({x}) = {df(x)}, verwacht 0"
    y_max = f(-4)
    y_min = f(4)
    print(f"  f'(-4) = {df(-4)} (verwacht 0)")
    print(f"  f'( 4) = {df( 4)} (verwacht 0)")
    print(f"  f(-4) = {y_max}  (max van linker tak, verwacht -2)")
    print(f"  f( 4) = {y_min}  (min van rechter tak, verwacht  2)")
    assert y_max == -2.0 and y_min == 2.0
    # En de "max" is hier kleiner dan de "min" -- bevestig
    assert y_max < y_min
    print(f"  LET OP: max ({y_max}) < min ({y_min}) want het zijn twee takken.")

    fig, ax = plt.subplots(figsize=(7.5, 5.2))
    xs_l = np.linspace(-10, -0.4, 400)
    xs_r = np.linspace(0.4, 10, 400)
    ax.plot(xs_l, f(xs_l), color="#2563eb", lw=2.5, label="f(x) = (x² + 16)/(4x)")
    ax.plot(xs_r, f(xs_r), color="#2563eb", lw=2.5)
    # Toppen markeren
    ax.plot([-4], [-2], "o", color="#dc2626", markersize=9, zorder=5)
    ax.plot([4], [2], "o", color="#dc2626", markersize=9, zorder=5)
    # Horizontale lijntjes door de toppen
    for x_top, y_top, lab in [(-4, -2, "max f(−4) = −2"), (4, 2, "min f(4) = 2")]:
        tx = np.linspace(x_top - 1.2, x_top + 1.2, 30)
        ax.plot(tx, [y_top] * len(tx), color="#dc2626", lw=2, alpha=0.85)
        offset_y = -1.0 if x_top < 0 else 1.0
        ax.annotate(
            lab,
            xy=(x_top, y_top),
            xytext=(x_top + 0.4, y_top + offset_y),
            fontsize=10,
            color="#7c2d12",
            fontweight="bold",
        )
    ax.axvline(0, color="#94a3b8", lw=1)
    ax.axhline(0, color="#94a3b8", lw=1)
    ax.set_xlim(-10, 10)
    ax.set_ylim(-8, 8)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(loc="upper left", framealpha=0.95)
    ax.set_title("Twee aparte takken — max (−4, −2) en min (4, 2). Max < min!")
    out = OUT / "fig3-twee-takken.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


def fig4_x_maal_wortelx():
    """f(x) = x*sqrt(x) = x^(3/2). f'(x) = (3/2) * x^(1/2) = (3/2)*sqrt(x).

    Raaklijn op x=1: f(1)=1, f'(1)=1.5. k: y = 1.5x - 0.5.
    """
    print("\nfig4_x_maal_wortelx -- f(x) = x*sqrt(x), raaklijn op x=1")
    f = lambda x: x * np.sqrt(x)
    df = lambda x: 1.5 * np.sqrt(x)

    x_A = 1.0
    y_A = float(f(x_A))
    m = float(df(x_A))
    b = y_A - m * x_A
    print(f"  y_A = f(1) = {y_A} (verwacht 1)")
    print(f"  f'(1) = {m} (verwacht 1.5)")
    print(f"  b = {b} (verwacht -0.5)")
    assert y_A == 1.0 and m == 1.5 and b == -0.5

    fig, ax = plt.subplots(figsize=(7.5, 5))
    xs = np.linspace(0.001, 4.5, 400)
    ax.plot(xs, f(xs), color="#2563eb", lw=2.5, label="f(x) = x·√x  =  x^(3/2)")
    tx = np.linspace(-0.2, 3.0, 50)
    ax.plot(tx, m * tx + b, color="#dc2626", lw=2, label="k: y = 1½x − ½")
    ax.plot([x_A], [y_A], "o", color="#dc2626", markersize=9, zorder=5)
    ax.annotate("A(1, 1)", xy=(x_A, y_A), xytext=(x_A + 0.15, y_A - 0.7), fontsize=11, color="#7c2d12", fontweight="bold")
    style_axes(ax, (-0.5, 4.5), (-2, 9))
    ax.legend(loc="upper left", framealpha=0.95)
    ax.set_title("Raaklijn aan f(x) = x·√x in het punt A(1, 1)")
    out = OUT / "fig4-x-wortel-x.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


def fig5_opgave_c_synthese():
    """Opg. C uit toetsstijl: f(x) = (x^2 + 1) / (x * sqrt(x)).

    Herschrijven:
      f(x) = (x^2 + 1) * x^(-3/2)
           = x^2 * x^(-3/2)  +  1 * x^(-3/2)
           = x^(1/2)  +  x^(-3/2)
           = sqrt(x) + 1/(x*sqrt(x))

    Afgeleide:
      f'(x) = (1/2) x^(-1/2)  +  (-3/2) x^(-5/2)
            = 1/(2 sqrt(x))  -  3/(2 x^2 sqrt(x))

    f'(1) = 1/2 - 3/2 = -1.
    f(1) = 1 + 1 = 2.

    We tonen f met de raaklijn op x=1.
    """
    print("\nfig5_opgave_c -- f(x) = (x^2+1) / (x*sqrt(x)), raaklijn op x = 1")
    f = lambda x: np.sqrt(x) + 1.0 / (x * np.sqrt(x))
    # alternatieve check: (x^2+1) / (x*sqrt(x))
    f_check = lambda x: (x * x + 1) / (x * np.sqrt(x))
    df = lambda x: 1.0 / (2 * np.sqrt(x)) - 3.0 / (2 * (x * x) * np.sqrt(x))

    # Numerieke consistentie van de herleiding
    for x in (0.5, 1.0, 2.0, 4.0):
        a = float(f(x))
        b = float(f_check(x))
        assert abs(a - b) < 1e-10, f"Herleiding fout bij x={x}: {a} vs {b}"

    x_A = 1.0
    y_A = float(f(x_A))
    m = float(df(x_A))
    print(f"  f(1) = {y_A} (verwacht 2)")
    print(f"  f'(1) = {m} (verwacht -1)")
    assert y_A == 2.0
    assert m == -1.0
    b_lin = y_A - m * x_A
    print(f"  raaklijn k: y = {m}x + {b_lin}  -> y = -x + 3")

    fig, ax = plt.subplots(figsize=(7.5, 5.2))
    xs = np.linspace(0.18, 5.0, 400)
    ax.plot(xs, f(xs), color="#2563eb", lw=2.5, label="f(x) = (x² + 1)/(x·√x)")
    tx = np.linspace(-0.2, 3.5, 50)
    ax.plot(tx, m * tx + b_lin, color="#dc2626", lw=2, label="k: y = −x + 3")
    ax.plot([x_A], [y_A], "o", color="#dc2626", markersize=9, zorder=5)
    ax.annotate("A(1, 2)", xy=(x_A, y_A), xytext=(x_A + 0.2, y_A + 0.4), fontsize=11, color="#7c2d12", fontweight="bold")
    style_axes(ax, (-0.5, 5.0), (-0.5, 6))
    ax.legend(loc="upper right", framealpha=0.95)
    ax.set_title("Synthese-opgave C: f(x) = (x²+1)/(x·√x) met raaklijn op x = 1")
    out = OUT / "fig5-synthese-opgave-c.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


if __name__ == "__main__":
    fig1_negatieve_exponent()
    fig2_wortel_raaklijn()
    fig3_extreme_waarden_twee_takken()
    fig4_x_maal_wortelx()
    fig5_opgave_c_synthese()
    print("\nKlaar.")
