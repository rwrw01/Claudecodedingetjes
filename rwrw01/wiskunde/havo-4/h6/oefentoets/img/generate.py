"""Genereer matplotlib-PNG's voor de oefentoets H6 De afgeleide functie.

Deze toets is op Math-with-Menno-proefwerk-niveau: 4 opgaven, 39 punten, 50 minuten.
Cijfer-formule: cijfer = punten / 39 * 9 + 1.

Twee figuren:
  - fig-opg2: kubische f(x) = x^3 - 6x^2 + 9x + 2 met raaklijn k in A(4, 6) en
              twee parallelle raakpunten C(-1, -14) en D(5, 22) met helling 24,
              plus horizontale streep-lijnen op p=2 en p=6 (grens drie oplossingen).
  - fig-opg4: parabool y = -x^2 + 8x met driehoek PQR; P(p, y_P) op grafiek,
              Q(p, 0) op x-as, R(8, 0) vast. Max bij p = 8/3, A_max = 1024/27.

Alle berekeningen worden met asserts geverifieerd voordat de figuur wordt
geschreven, zodat de antwoorden in index.html en de plot 1-op-1 overeenkomen.
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


# ============================================================================
# WISKUNDIGE VERIFICATIE — alle 4 opgaven, vóór de figuren
# ============================================================================
def verify_opgaven():
    print("=== Wiskundige verificatie van de 4 opgaven ===")

    # ----------------------------------------------------------------------
    # Opgave 1 — differentiëren (3 deelvragen)
    # ----------------------------------------------------------------------
    print("\nOpg.1 — differentiëren")

    # 1a) f(x) = (4x - 3)^2 - 7x^3
    # Werk haakjes uit: f(x) = 16x^2 - 24x + 9 - 7x^3
    # f'(x) = 32x - 24 - 21x^2 = -21x^2 + 32x - 24
    # Numerieke check bij x = 2: (4*2-3)^2 - 7*8 = 25 - 56 = -31
    # f'(2) volgens formule: -21*4 + 32*2 - 24 = -84 + 64 - 24 = -44
    # Eindige-verschil check:
    h = 1e-7
    def f1a(x):
        return (4*x - 3)**2 - 7*x**3
    fp_num = (f1a(2 + h) - f1a(2 - h)) / (2*h)
    fp_formula = -21*4 + 32*2 - 24
    print(f"  1a) f'(2) formule = {fp_formula},  numeriek = {fp_num:.6f}")
    assert abs(fp_num - fp_formula) < 1e-4

    # 1b) g(x) = (x^3 + 4x) / cbrt(x)
    # Herschrijven: g(x) = x^(8/3) + 4 x^(2/3)
    # g'(x) = (8/3) x^(5/3) + (8/3) x^(-1/3)
    # = 8(x^2 + 1) / (3 cbrt(x))   na samenvoegen
    def g1b(x):
        return (x**3 + 4*x) / np.cbrt(x)
    def gp1b_formula(x):
        return (8.0/3.0) * x**(5.0/3.0) + (8.0/3.0) * x**(-1.0/3.0)
    gp_num = (g1b(8 + h) - g1b(8 - h)) / (2*h)
    print(f"  1b) g'(8) formule = {gp1b_formula(8):.6f},  numeriek = {gp_num:.6f}")
    assert abs(gp_num - gp1b_formula(8)) < 1e-3
    # Check alternatieve vorm 8(x^2+1)/(3 cbrt(x))
    alt_at_8 = 8*(64 + 1) / (3 * np.cbrt(8))
    print(f"      alt vorm 8(x^2+1)/(3 cbrt(x)) bij x=8: {alt_at_8:.6f}")
    assert abs(alt_at_8 - gp1b_formula(8)) < 1e-9

    # 1c) h(x) = 3 / sqrt(5x - 2) = 3 * (5x - 2)^(-1/2)
    # h'(x) = 3 * (-1/2) * (5x - 2)^(-3/2) * 5 = -15 / (2 * (5x-2)^(3/2))
    def h1c(x):
        return 3 / np.sqrt(5*x - 2)
    hp_num = (h1c(2 + h) - h1c(2 - h)) / (2*h)
    hp_formula = -15.0 / (2 * (5*2 - 2)**1.5)
    print(f"  1c) h'(2) formule = {hp_formula:.6f},  numeriek = {hp_num:.6f}")
    assert abs(hp_num - hp_formula) < 1e-4

    # ----------------------------------------------------------------------
    # Opgave 2 — kubische f(x) = x^3 - 6x^2 + 9x + 2
    # ----------------------------------------------------------------------
    print("\nOpg.2 — f(x) = x^3 - 6x^2 + 9x + 2")
    def f2(x):
        return x**3 - 6*x**2 + 9*x + 2
    def fp2(x):
        return 3*x**2 - 12*x + 9

    # a) raaklijn in A met x_A = 4
    # f(4) = 64 - 96 + 36 + 2 = 6
    # f'(4) = 48 - 48 + 9 = 9
    # k: y = 9x + b, door (4, 6) -> b = 6 - 36 = -30
    # B is snijpunt met y-as: (0, -30)
    assert f2(4) == 6
    assert fp2(4) == 9
    b_a = 6 - 9*4
    assert b_a == -30
    print(f"  a) A(4, {f2(4)}), helling f'(4) = {fp2(4)}, k: y = 9x - 30, B(0, {b_a})")

    # b) raaklijn evenwijdig met y = 24x - 7, dus helling 24
    # f'(x) = 24:  3x^2 - 12x + 9 = 24
    # 3x^2 - 12x - 15 = 0  ->  x^2 - 4x - 5 = 0  ->  (x - 5)(x + 1) = 0
    # x = -1 of x = 5
    # f(-1) = -1 - 6 - 9 + 2 = -14
    # f(5) = 125 - 150 + 45 + 2 = 22
    assert fp2(-1) == 24
    assert fp2(5) == 24
    assert f2(-1) == -14
    assert f2(5) == 22
    print(f"  b) C(-1, {f2(-1)}) en D(5, {f2(5)}), beide helling 24")

    # c) Drie oplossingen f(x) = p
    # Toppen: f'(x) = 0  ->  3(x-1)(x-3) = 0  ->  x = 1 of x = 3
    # f(1) = 1 - 6 + 9 + 2 = 6  (maximum, want grafiek stijgt-daalt-stijgt)
    # f(3) = 27 - 54 + 27 + 2 = 2  (minimum)
    # Drie oplossingen <=> 2 < p < 6
    assert fp2(1) == 0
    assert fp2(3) == 0
    assert f2(1) == 6
    assert f2(3) == 2
    # Verifieer numeriek: bij p = 4 zou f(x) = 4 drie oplossingen moeten hebben
    p_check = 4
    from numpy.polynomial import polynomial as P
    roots = np.roots([1, -6, 9, 2 - p_check])
    real_roots = [r.real for r in roots if abs(r.imag) < 1e-8]
    print(f"  c) f(x)=4 reele oplossingen: {sorted(real_roots)}  (verwacht 3)")
    assert len(real_roots) == 3
    print(f"     Drie oplossingen: 2 < p < 6")

    # ----------------------------------------------------------------------
    # Opgave 3 — wortelfunctie f(x) = sqrt(20 - 4x) + x/2 - 1
    # ----------------------------------------------------------------------
    print("\nOpg.3 — f(x) = sqrt(20 - 4x) + x/2 - 1")
    def f3(x):
        return np.sqrt(20 - 4*x) + x/2 - 1
    def fp3(x):
        # f'(x) = -4/(2 sqrt(20-4x)) + 1/2 = -2/sqrt(20-4x) + 1/2
        return -2/np.sqrt(20 - 4*x) + 0.5

    # a) Bereik algebraïsch
    # Domein: 20 - 4x >= 0  ->  x <= 5
    # f'(x) = 0:  2/sqrt(20-4x) = 1/2  ->  sqrt(20-4x) = 4  ->  20-4x = 16  ->  x = 1
    # f(1) = sqrt(16) + 1/2 - 1 = 4 - 1/2 = 7/2 = 3.5  (maximum)
    # x -> -oo: x/2 -> -oo, sqrt-term groeit als sqrt(-x) maar x/2 wint -> f -> -oo
    # Bij rand x = 5: f(5) = 0 + 5/2 - 1 = 3/2
    # Dus bereik: f <= 7/2,  d.w.z. (-oo, 7/2]
    assert abs(fp3(1)) < 1e-12
    assert abs(f3(1) - 3.5) < 1e-12
    assert abs(f3(5) - 1.5) < 1e-12
    print(f"  a) max f(1) = {f3(1)}, bereik = (-oo, 7/2]")

    # b) raaklijn in A met x_A = 4, A(4, 3)
    # f(4) = sqrt(4) + 2 - 1 = 2 + 1 = 3
    # f'(4) = -2/sqrt(4) + 1/2 = -1 + 1/2 = -1/2
    # k: y = -1/2 x + b,  door (4, 3): b = 3 + 2 = 5
    # k: y = -1/2 x + 5
    # Snijpunt met y-as: B(0, 5)
    # Loodrechte lijn l door B: helling = -1/(-1/2) = 2
    # l: y = 2x + 5
    # Snijpunt l met x-as: 0 = 2x + 5  ->  x = -5/2
    # Snijpunt heet C(-5/2, 0)
    assert abs(f3(4) - 3) < 1e-12
    assert abs(fp3(4) - (-0.5)) < 1e-12
    b_k = 3 - (-0.5)*4
    assert abs(b_k - 5) < 1e-12
    rc_l = -1 / (-0.5)
    assert rc_l == 2
    x_C = -5 / rc_l  # -5/2
    assert abs(x_C - (-2.5)) < 1e-12
    print(f"  b) A(4, 3), helling -1/2, k: y = -x/2 + 5, B(0, 5)")
    print(f"     l (loodrecht door B): y = 2x + 5, snijdt x-as in C(-5/2, 0)")

    # ----------------------------------------------------------------------
    # Opgave 4 — optimalisering, parabool y = -x^2 + 8x, driehoek PQR
    # ----------------------------------------------------------------------
    print("\nOpg.4 — y = -x^2 + 8x, driehoek PQR met R(8, 0)")
    # P(p, -p^2 + 8p) op de parabool, 0 < p < 8
    # Q(p, 0) op x-as recht onder P
    # R(8, 0) op x-as
    # Driehoek PQR: PQ verticaal (lengte -p^2 + 8p = p(8-p)), QR horizontaal (lengte 8 - p)
    # Hoek in Q is recht, dus A = 1/2 * (8 - p) * p(8 - p) = 1/2 * p * (8 - p)^2
    def A4(p):
        return 0.5 * p * (8 - p)**2
    # A'(p) = 1/2 * [(8-p)^2 + p * 2(8-p)(-1)]
    # = 1/2 * (8-p) * [(8-p) - 2p]
    # = 1/2 * (8-p) * (8 - 3p)
    # = 0  ->  p = 8 (rand, valt af) of p = 8/3
    p_max = 8/3
    # Numerieke afgeleide
    dA_num = (A4(p_max + h) - A4(p_max - h)) / (2*h)
    print(f"  A'(8/3) numeriek = {dA_num:.8f}  (verwacht 0)")
    assert abs(dA_num) < 1e-3
    A_max = A4(p_max)
    A_exact = 1024 / 27
    print(f"  A(8/3) = {A_max:.6f},  exact 1024/27 = {A_exact:.6f}")
    assert abs(A_max - A_exact) < 1e-9

    # Controle: A is groter bij p_max dan bij nabije waarden (echt een max)
    assert A4(p_max) > A4(p_max - 0.1)
    assert A4(p_max) > A4(p_max + 0.1)

    print("\nAlle wiskundige asserts gepasseerd.")


# ============================================================================
# Figuren
# ============================================================================
def fig_opg2():
    """Kubische f(x) = x^3 - 6x^2 + 9x + 2.
    Toon raaklijn k in A(4, 6) en de twee raakpunten C(-1, -14), D(5, 22)
    waar de helling gelijk is aan 24.
    """
    print("\nfig_opg2 -- f(x) = x^3 - 6x^2 + 9x + 2 met raaklijn k in A en parallelraakpunten C, D")

    def f(x):
        return x**3 - 6*x**2 + 9*x + 2

    yA = f(4)
    # k: y = 9x - 30
    def k(x):
        return 9*x - 30

    yC = f(-1)
    yD = f(5)
    # raaklijnen in C, D met helling 24:
    # in C: y = 24x + b, door (-1, -14):  b = -14 - 24*(-1) = -14 + 24 = 10
    # in D: y = 24x + b, door (5, 22):  b = 22 - 24*5 = 22 - 120 = -98
    def k_C(x):
        return 24*x + 10
    def k_D(x):
        return 24*x - 98

    fig, ax = plt.subplots(figsize=(7.4, 5.6))
    xs = np.linspace(-2, 6, 400)
    ax.plot(xs, f(xs), color="#0f766e", lw=2.5, label="f(x) = x³ − 6x² + 9x + 2")
    # raaklijn k beperken tot zichtbaar gebied
    xs_k = np.linspace(2.5, 6, 50)
    ax.plot(xs_k, k(xs_k), color="#dc2626", lw=2.2, label="k: y = 9x − 30")
    # twee parallelle raaklijnen — dun, gestippeld
    xs_p = np.linspace(-1.7, 0.2, 30)
    ax.plot(xs_p, k_C(xs_p), color="#7c3aed", lw=1.6, linestyle="--", alpha=0.85, label="raaklijnen helling 24")
    xs_p2 = np.linspace(4.4, 5.6, 30)
    ax.plot(xs_p2, k_D(xs_p2), color="#7c3aed", lw=1.6, linestyle="--", alpha=0.85)

    # markeren
    ax.plot([4], [yA], "o", color="#dc2626", markersize=9, zorder=5)
    ax.plot([0], [-30], "o", color="#dc2626", markersize=9, zorder=5)
    ax.plot([-1], [yC], "o", color="#7c3aed", markersize=8, zorder=5)
    ax.plot([5], [yD], "o", color="#7c3aed", markersize=8, zorder=5)

    ax.annotate("A(4, 6)", xy=(4, yA), xytext=(4.1, 9), fontsize=10, color="#7c2d12", fontweight="bold")
    ax.annotate("B(0, −30)", xy=(0, -30), xytext=(-1.9, -27), fontsize=10, color="#7c2d12", fontweight="bold")
    ax.annotate("C(−1, −14)", xy=(-1, yC), xytext=(-1.8, -18), fontsize=10, color="#4c1d95", fontweight="bold")
    ax.annotate("D(5, 22)", xy=(5, yD), xytext=(4.2, 24), fontsize=10, color="#4c1d95", fontweight="bold")

    style_axes(ax, (-2, 6), (-32, 30))
    ax.legend(loc="lower right", framealpha=0.95, fontsize=9)
    ax.set_title("Opgave 2 — raaklijn k in A en parallelle raakpunten C, D")
    out = OUT / "fig-opg2.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


def fig_opg4():
    """Parabool y = -x^2 + 8x met driehoek PQR.
    P(p, y_P) op grafiek, Q(p, 0), R(8, 0).
    Toon de driehoek bij de max-waarde p = 8/3.
    """
    print("\nfig_opg4 -- parabool y = -x^2 + 8x met driehoek PQR")

    def y(x):
        return -x**2 + 8*x

    p_max = 8/3
    P = (p_max, y(p_max))
    Q = (p_max, 0)
    R = (8, 0)

    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    xs = np.linspace(-1, 9, 400)
    ax.plot(xs, y(xs), color="#0f766e", lw=2.5, label="y = −x² + 8x")

    # vul de driehoek
    triangle = plt.Polygon([P, Q, R], closed=True, facecolor="#fde68a", edgecolor="#b45309", lw=2, alpha=0.7)
    ax.add_patch(triangle)
    ax.plot(*zip(P, Q, R, P), color="#b45309", lw=2)

    ax.plot(*P, "o", color="#dc2626", markersize=9, zorder=5)
    ax.plot(*Q, "o", color="#dc2626", markersize=9, zorder=5)
    ax.plot(*R, "o", color="#dc2626", markersize=9, zorder=5)

    ax.annotate("P(p, −p² + 8p)", xy=P, xytext=(p_max - 0.3, P[1] + 1.5), fontsize=10, color="#7c2d12", fontweight="bold")
    ax.annotate("Q(p, 0)", xy=Q, xytext=(p_max - 0.5, -2.2), fontsize=10, color="#7c2d12", fontweight="bold")
    ax.annotate("R(8, 0)", xy=R, xytext=(7.6, -2.2), fontsize=10, color="#7c2d12", fontweight="bold")

    style_axes(ax, (-1, 10), (-4, 18))
    ax.legend(loc="upper left", framealpha=0.95)
    ax.set_title("Opgave 4 — driehoek PQR op de parabool y = −x² + 8x")
    out = OUT / "fig-opg4.png"
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved -> {out.name}")


if __name__ == "__main__":
    verify_opgaven()
    fig_opg2()
    fig_opg4()
    print("\nKlaar - alle figuren gegenereerd en geverifieerd.")
