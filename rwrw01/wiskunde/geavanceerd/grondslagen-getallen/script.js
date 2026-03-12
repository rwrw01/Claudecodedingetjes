// ==================== ASSOCIATIVITEIT SLIDER (P1) ====================
function updateAssoc() {
    const sliders = document.querySelectorAll('#assocDemo input[type=range]');
    const a = parseInt(sliders[0].value);
    const b = parseInt(sliders[1].value);
    const c = parseInt(sliders[2].value);
    document.getElementById('assocA').textContent = a;
    document.getElementById('assocB').textContent = b;
    document.getElementById('assocC').textContent = c;

    const left = a + (b + c);
    const right = (a + b) + c;
    const eq = left === right ? '=' : '≠';
    document.getElementById('assocResult').innerHTML =
        `${a} + (${b} + ${c}) = ${a} + ${b + c} = <strong>${left}</strong> &nbsp;&nbsp;` +
        `en &nbsp;&nbsp; (${a} + ${b}) + ${c} = ${a + b} + ${c} = <strong>${right}</strong> &nbsp;&nbsp;` +
        `<span style="color:${left === right ? '#16a34a' : '#ef4444'}">${eq} ✓</span>`;
}
updateAssoc();

// ==================== GETALLENLIJN (P10) ====================
function updateNumberLine() {
    const val = parseFloat(document.getElementById('nlSlider').value);
    document.getElementById('nlVal').textContent = val;
    const canvas = document.getElementById('numberLine');
    const ctx = canvas.getContext('2d');
    const w = canvas.width, h = canvas.height;
    ctx.clearRect(0, 0, w, h);

    const cx = w / 2, cy = h / 2;
    const scale = w / 22;

    // Lijn
    ctx.strokeStyle = '#94a3b8';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(10, cy);
    ctx.lineTo(w - 10, cy);
    ctx.stroke();

    // Streepjes en getallen
    ctx.fillStyle = '#64748b';
    ctx.font = '12px system-ui';
    ctx.textAlign = 'center';
    for (let i = -10; i <= 10; i++) {
        const x = cx + i * scale;
        ctx.beginPath();
        ctx.moveTo(x, cy - 6);
        ctx.lineTo(x, cy + 6);
        ctx.stroke();
        if (i % 2 === 0) {
            ctx.fillText(i, x, cy + 20);
        }
    }

    // Nul markeren
    ctx.fillStyle = '#1e293b';
    ctx.font = 'bold 13px system-ui';
    ctx.fillText('0', cx, cy + 20);

    // Punt markeren
    const px = cx + val * scale;
    ctx.beginPath();
    ctx.arc(px, cy, 8, 0, Math.PI * 2);
    ctx.fillStyle = '#2563eb';
    ctx.fill();
    ctx.fillStyle = 'white';
    ctx.font = 'bold 9px system-ui';
    ctx.textAlign = 'center';
    ctx.fillText('a', px, cy + 3);

    // Trichotomie resultaat
    let result;
    if (val > 0) result = 'a ∈ P (positief) → a > 0';
    else if (val < 0) result = '−a ∈ P (negatief) → a < 0';
    else result = 'a = 0 (nul)';
    document.getElementById('nlResult').textContent = result;
}
updateNumberLine();

// ==================== ABSOLUTE WAARDE LIJN ====================
function updateAbsLine() {
    const val = parseFloat(document.getElementById('absSlider').value);
    document.getElementById('absVal').textContent = val;
    const canvas = document.getElementById('absLine');
    const ctx = canvas.getContext('2d');
    const w = canvas.width, h = canvas.height;
    ctx.clearRect(0, 0, w, h);

    const cx = w / 2, cy = h * 0.45;
    const scale = w / 22;

    // Lijn
    ctx.strokeStyle = '#94a3b8';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(10, cy);
    ctx.lineTo(w - 10, cy);
    ctx.stroke();

    // Streepjes
    ctx.fillStyle = '#64748b';
    ctx.font = '12px system-ui';
    ctx.textAlign = 'center';
    for (let i = -10; i <= 10; i++) {
        const x = cx + i * scale;
        ctx.beginPath();
        ctx.moveTo(x, cy - 6);
        ctx.lineTo(x, cy + 6);
        ctx.stroke();
        if (i % 2 === 0) ctx.fillText(i, x, cy + 20);
    }

    // Afstandsboog
    const px = cx + val * scale;
    const absVal = Math.abs(val);
    if (absVal > 0) {
        ctx.strokeStyle = '#e11d48';
        ctx.lineWidth = 2;
        ctx.setLineDash([4, 3]);
        const startX = Math.min(cx, px);
        const endX = Math.max(cx, px);
        ctx.beginPath();
        ctx.moveTo(startX, cy - 15);
        ctx.lineTo(endX, cy - 15);
        ctx.stroke();
        // Pijlpunten
        ctx.setLineDash([]);
        ctx.beginPath();
        ctx.moveTo(startX, cy - 20);
        ctx.lineTo(startX, cy - 10);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(endX, cy - 20);
        ctx.lineTo(endX, cy - 10);
        ctx.stroke();
        // Label
        ctx.fillStyle = '#e11d48';
        ctx.font = 'bold 13px system-ui';
        ctx.fillText('|a| = ' + absVal, (startX + endX) / 2, cy - 25);
    }

    // Punt 0
    ctx.beginPath();
    ctx.arc(cx, cy, 5, 0, Math.PI * 2);
    ctx.fillStyle = '#64748b';
    ctx.fill();

    // Punt a
    ctx.beginPath();
    ctx.arc(px, cy, 8, 0, Math.PI * 2);
    ctx.fillStyle = '#2563eb';
    ctx.fill();
    ctx.fillStyle = 'white';
    ctx.font = 'bold 9px system-ui';
    ctx.fillText('a', px, cy + 3);

    document.getElementById('absResult').textContent =
        `|${val}| = ${absVal} (afstand tot 0)`;
}
updateAbsLine();

// ==================== ONGELIJKHEID SLIDER ====================
function updateIneq() {
    const c = parseInt(document.getElementById('ineqSlider').value);
    document.getElementById('ineqC').textContent = c;
    const left = 2 * c;
    const right = 5 * c;
    let sign, color;
    if (c > 0) { sign = '<'; color = '#16a34a'; }
    else if (c < 0) { sign = '>'; color = '#ef4444'; }
    else { sign = '='; color = '#64748b'; }

    document.getElementById('ineqResult').innerHTML =
        `2 × ${c} = ${left} &nbsp; ${sign} &nbsp; 5 × ${c} = ${right} ` +
        `<span style="color:${color};font-weight:bold;">` +
        (c < 0 ? '← omgedraaid!' : c > 0 ? '← zelfde richting' : '← beide 0') +
        `</span>`;
}
updateIneq();

// ==================== PROBEER-ZELF VALIDATIE ====================
const tryAnswers = {
    tryP2: {
        check: v => v.trim() === '0',
        correct: 'Goed! 0 is het identiteitselement van optelling.',
        wrong: 'Niet juist. Welk getal verandert niets als je het ergens bij optelt?'
    },
    tryP3: {
        check: v => v.trim().replace(/\s/g, '') === '-8' || v.trim().replace(/\s/g, '') === '−8',
        correct: 'Goed! 8 + (−8) = 0.',
        wrong: 'Niet juist. Het tegenovergestelde van 8 is het getal dat bij 8 opgeteld 0 geeft.'
    },
    tryP7: {
        check: v => {
            const s = v.trim().replace(/\s/g, '');
            return s === '1/4' || s === '0.25' || s === '0,25';
        },
        correct: 'Goed! 4 × ¼ = 1.',
        wrong: 'Niet juist. Welk getal geeft 1 als je het met 4 vermenigvuldigt?'
    },
    tryProof1: {
        check: v => {
            const s = v.trim().toUpperCase().replace(/\s/g, '');
            return s === 'P9' || s === 'DISTRIBUTIVITEIT';
        },
        correct: 'Goed! P9 (distributiviteit) is de sleutel.',
        wrong: 'Niet juist. Welk axioma laat je a·(b+c) herschrijven als a·b + a·c?'
    },
    tryMinMin: {
        check: v => v.trim() === '21',
        correct: 'Goed! (−3)(−7) = 3 × 7 = 21. Min keer min is plus!',
        wrong: 'Niet juist. Probeer: (−3)(−7) = 3 · 7 = ?'
    }
};

function checkTry(id) {
    const input = document.getElementById(id);
    const val = input.value.trim();
    if (!val) return;
    const fb = document.getElementById(id + 'fb');
    const a = tryAnswers[id];
    if (a.check(val)) {
        fb.textContent = '✓ ' + a.correct;
        fb.style.color = '#166534';
        input.style.borderColor = '#22c55e';
    } else {
        fb.textContent = '✗ ' + a.wrong;
        fb.style.color = '#991b1b';
        input.style.borderColor = '#ef4444';
    }
}

// Commutativiteit check (P4)
function checkCommut() {
    const a = parseFloat(document.getElementById('tryP4a').value.replace(',', '.'));
    const b = parseFloat(document.getElementById('tryP4b').value.replace(',', '.'));
    const fb = document.getElementById('tryP4fb');
    if (isNaN(a) || isNaN(b)) { fb.textContent = 'Vul twee getallen in.'; fb.style.color = '#991b1b'; return; }
    fb.textContent = `✓ ${a} + ${b} = ${a + b}, en ${b} + ${a} = ${b + a}. Zelfde uitkomst!`;
    fb.style.color = '#166534';
}

// Distributiviteit check (P9)
function checkDistrib() {
    const a = document.getElementById('tryP9a').value.trim();
    const b = document.getElementById('tryP9b').value.trim();
    const c = document.getElementById('tryP9c').value.trim();
    const fb = document.getElementById('tryP9fb');
    if (!a || !b || !c) return;
    if (a === '35' && b === '15' && c === '50') {
        fb.textContent = '✓ Goed! 5·7 = 35, 5·3 = 15, en 35 + 15 = 50.';
        fb.style.color = '#166534';
    } else {
        fb.textContent = '✗ Niet juist. 5·7 = ?, 5·3 = ?, en hun som = ?';
        fb.style.color = '#991b1b';
    }
}

// Absolute waarde try
function checkAbsTry() {
    const a1 = document.getElementById('tryAbs1').value.trim();
    const a2 = document.getElementById('tryAbs2').value.trim();
    const a3 = document.getElementById('tryAbs3').value.trim();
    const fb = document.getElementById('tryAbsfb');
    if (a1 === '7' && a2 === '4' && a3 === '0') {
        fb.textContent = '✓ Goed! |−7| = 7, |4| = 4, |0| = 0.';
        fb.style.color = '#166534';
    } else {
        fb.textContent = '✗ Niet helemaal juist. Absolute waarde = afstand tot 0, altijd ≥ 0.';
        fb.style.color = '#991b1b';
    }
}

// Driehoeksongelijkheid check
function checkTriangle() {
    const val = document.getElementById('tryTriangle').value;
    const fb = document.getElementById('tryTrianglefb');
    if (val === 'same') {
        fb.textContent = '✓ Goed! Bij hetzelfde teken is er geen annulering, dus gelijkheid.';
        fb.style.color = '#166534';
    } else if (val) {
        fb.textContent = '✗ Niet juist. Denk na: wanneer is er geen annulering?';
        fb.style.color = '#991b1b';
    }
}

// ==================== OEFENOPGAVEN VALIDATIE ====================
const answers = {
    1: {
        check: v => v.trim() === '1',
        correct: '✓ Goed! x = 1.',
        wrong: '✗ Denk na: als bx = b en b ≠ 0, wat is x dan?'
    },
    2: {
        check: v => {
            const s = v.trim().replace(/\s/g, '').toLowerCase();
            return s.includes('p²') || s.includes('p^2') || s.includes('p2') ||
                   s.includes('distributiviteit') || s.includes('p9');
        },
        correct: '✓ Goed! Werk (p−q)(p+q) uit met distributiviteit.',
        wrong: '✗ Probeer (p−q)(p+q) uit te werken met P9.'
    },
    3: {
        check: v => {
            const s = v.trim().toLowerCase();
            return s.includes('4') || s.includes('deel') || s.includes('nul') ||
                   s.includes('a-b') || s.includes('a−b') || s.includes('0');
        },
        correct: '✓ Goed! In stap 4 delen we door (a−b) = 0. Dat mag niet (P7)!',
        wrong: '✗ Kijk nog eens naar stap 4. Waardoor wordt er gedeeld?'
    },
    4: {
        check: v => {
            const s = v.trim().toUpperCase().replace(/\s/g, '');
            return s.includes('P7') || s.includes('P5') || s.includes('INVERSE');
        },
        correct: '✓ Goed! De sleutel is P7 (inverse) en P5 (associativiteit).',
        wrong: '✗ Denk na over de inverse van het product bc.'
    },
    5: {
        check: v => {
            const s = v.trim().toLowerCase().replace(/\s/g, '');
            return s.includes('b⁻¹') || s.includes('b^-1') || s.includes('inverse') ||
                   s.includes('definitie') || s.includes('a·b');
        },
        correct: '✓ Goed! Schrijf de breuken als vermenigvuldigingen met inversen.',
        wrong: '✗ Begin met: a/b = a · b⁻¹ (definitie van deling).'
    },
    6: {
        check: v => {
            const s = v.trim().replace(/\s/g, '').replace(',', '.');
            return s === 'x<2' || s === 'x<2' || s.includes('<2');
        },
        correct: '✓ Goed! x < 2.',
        wrong: '✗ Tel 2x op bij beide kanten en trek 3 af.'
    },
    7: {
        check: v => {
            const s = v.trim().replace(/\s/g, '');
            return (s.includes('<-2') || s.includes('<−2')) && (s.includes('>2'));
        },
        correct: '✓ Goed! x < −2 of x > 2.',
        wrong: '✗ Herschrijf als x² > 4 en ontbind in factoren.'
    },
    8: {
        check: v => {
            const s = v.trim().toUpperCase().replace(/\s/g, '');
            return s.includes('P11') || s.includes('P3') || s.includes('OPTELLEN');
        },
        correct: '✓ Goed! Tel −a en −b op bij beide kanten (P11-gevolg + P3).',
        wrong: '✗ Tip: tel −a − b op bij beide kanten van a < b.'
    },
    9: {
        check: v => {
            const s = v.trim().toLowerCase().replace(/\s/g, '');
            return s.includes('vermenigvuldig') || s.includes('p12') || s.includes('a>0');
        },
        correct: '✓ Goed! Vermenigvuldig a < 1 met a (mag want a > 0).',
        wrong: '✗ Wat gebeurt er als je a < 1 vermenigvuldigt met a?'
    },
    10: {
        check: v => {
            const s = v.trim().toLowerCase();
            return s.includes('negatief') || s.includes('−') || s.includes('-');
        },
        correct: '✓ Goed! De uitdrukking is negatief, dus het antwoord is √2 + √7 − √3 − √5.',
        wrong: '✗ Bereken eerst of √3 + √5 groter of kleiner is dan √2 + √7.'
    },
    11: {
        check: v => {
            const s = v.trim().replace(/\s/g, '');
            return s.includes('1<x<7') || s.includes('1<x<7') ||
                   (s.includes('1') && s.includes('7'));
        },
        correct: '✓ Goed! 1 < x < 7.',
        wrong: '✗ |x−4| < 3 betekent −3 < x−4 < 3. Tel 4 op.'
    },
    12: {
        check: v => {
            const s = v.trim();
            return s === '2' || s.includes('twee') || s.includes('2 gevallen');
        },
        correct: '✓ Goed! Twee gevallen: beide ≥ 0 of beide ≤ 0.',
        wrong: '✗ Hoeveel gevallen onderscheid je? (Tip: hetzelfde teken kan twee dingen zijn.)'
    }
};

function checkAnswer(n) {
    const val = document.getElementById('ans' + n).value;
    if (!val.trim()) return;
    const fb = document.getElementById('fb' + n);
    const a = answers[n];
    if (a.check(val)) {
        fb.className = 'feedback correct';
        fb.textContent = a.correct;
    } else {
        fb.className = 'feedback wrong';
        fb.textContent = a.wrong;
    }
    const solBtn = document.getElementById('solbtn' + n);
    if (solBtn) solBtn.classList.remove('locked');
}

function toggleHint(n) {
    const hint = document.getElementById('hint' + n);
    hint.style.display = hint.style.display === 'block' ? 'none' : 'block';
}

function toggleSolution(n) {
    const sol = document.getElementById('sol' + n);
    sol.style.display = sol.style.display === 'block' ? 'none' : 'block';
}

// ==================== MINI-OEFENINGEN VALIDATIE ====================

// --- Blok A: Optelling (P1-P4) ---
function checkMiniA1() {
    const a = document.getElementById('miniA1a').value.trim();
    const b = document.getElementById('miniA1b').value.trim();
    const c = document.getElementById('miniA1c').value.trim();
    const d = document.getElementById('miniA1d').value.trim();
    const fb = document.getElementById('miniA1fb');
    if (a === '13' && b === '7' && c === '3' && d === '7') {
        fb.textContent = '✓ Goed! Beide manieren geven 7. Dat is P1: associativiteit!';
        fb.style.color = '#166534';
    } else {
        fb.textContent = '✗ Reken stap voor stap: 9 + 4 = 13, −6 + 13 = 7, en −6 + 9 = 3, 3 + 4 = 7.';
        fb.style.color = '#991b1b';
    }
}

function checkMiniA2() {
    const a = document.getElementById('miniA2a').value.trim().replace('−', '-');
    const b = document.getElementById('miniA2b').value.trim();
    const fb = document.getElementById('miniA2fb');
    if (a === '3' && b === '0') {
        fb.textContent = '✓ Goed! Het tegenovergestelde van −3 is 3, want −3 + 3 = 0 (P3).';
        fb.style.color = '#166534';
        document.getElementById('miniA2echo').textContent = '3';
    } else {
        fb.textContent = '✗ Het tegenovergestelde is het getal waarmee je op 0 uitkomt (P3).';
        fb.style.color = '#991b1b';
    }
}

function checkMiniA3() {
    const a = document.getElementById('miniA3a').value.trim().replace('−', '-');
    const b = document.getElementById('miniA3b').value.trim();
    const fb = document.getElementById('miniA3fb');
    if ((a === '-5' || a === '(-5)') && b === '7') {
        fb.textContent = '✓ Goed! 12 − 5 = 12 + (−5) = 7. Aftrekken is optellen in vermomming!';
        fb.style.color = '#166534';
    } else {
        fb.textContent = '✗ P3 zegt: a − b = a + (−b). Dus 12 − 5 = 12 + (−5) = ?';
        fb.style.color = '#991b1b';
    }
}

// --- Blok B: Vermenigvuldiging (P5-P9) ---
function checkMiniB1() {
    const a = document.getElementById('miniB1a').value.trim();
    const b = document.getElementById('miniB1b').value.trim();
    const c = document.getElementById('miniB1c').value.trim().toUpperCase().replace(/\s/g, '');
    const fb = document.getElementById('miniB1fb');
    if (a === '12' && b === '36' && c === 'P5') {
        fb.textContent = '✓ Goed! 3 · 12 = 36 en 6 · 6 = 36. P5: associativiteit van vermenigvuldiging.';
        fb.style.color = '#166534';
    } else if (b === '36' && c === 'P5') {
        fb.textContent = '✓ Bijna! De uitkomst klopt (36) en het axioma klopt (P5). Vul ook de tussenstap in.';
        fb.style.color = '#166534';
    } else {
        fb.textContent = '✗ Reken: 2 · 6 = 12, dan 3 · 12 = 36. Welk axioma gaat over haakjes bij vermenigvuldiging?';
        fb.style.color = '#991b1b';
    }
}

function checkMiniB2() {
    const a = document.getElementById('miniB2a').value.trim().replace(/\s/g, '');
    const b = document.getElementById('miniB2b').value.trim();
    const fb = document.getElementById('miniB2fb');
    if ((a === '3/2' || a === '1.5' || a === '1,5') && b === '1') {
        fb.textContent = '✓ Goed! ⅔ · 3/2 = 1. De inverse van ⅔ is 3/2 (P7).';
        fb.style.color = '#166534';
        document.getElementById('miniB2echo').textContent = '3/2';
    } else {
        fb.textContent = '✗ De inverse van a/b is b/a, want (a/b) · (b/a) = 1.';
        fb.style.color = '#991b1b';
    }
}

function checkMiniB3() {
    const a = document.getElementById('miniB3a').value.trim().replace('−', '-');
    const b = document.getElementById('miniB3b').value.trim();
    const c = document.getElementById('miniB3c').value.trim().replace('−', '-');
    const d = document.getElementById('miniB3d').value.trim();
    const fb = document.getElementById('miniB3fb');
    if ((a === '-3' || a === '−3') && b === '32' && (c === '-12' || c === '−12') && d === '20') {
        fb.textContent = '✓ Goed! 4 · 8 + 4 · (−3) = 32 + (−12) = 20. Dat is P9!';
        fb.style.color = '#166534';
    } else {
        fb.textContent = '✗ P9: 4 · (8 − 3) = 4 · 8 + 4 · (−3) = 32 + (−12) = 20.';
        fb.style.color = '#991b1b';
    }
}

// --- Blok C: Orde-axioma's (P10-P12) ---
function checkMiniC1() {
    const a = document.getElementById('miniC1a').value;
    const b = document.getElementById('miniC1b').value;
    const c = document.getElementById('miniC1c').value;
    const fb = document.getElementById('miniC1fb');
    if (a === 'neg' && b === 'nul' && c === 'pos') {
        fb.textContent = '✓ Goed! −4 is negatief, 0 is nul, 7 is positief. Precies één optie per getal (P10).';
        fb.style.color = '#166534';
    } else {
        fb.textContent = '✗ Denk aan trichotomie: elk getal is positief, nul, of negatief — precies één van de drie.';
        fb.style.color = '#991b1b';
    }
}

function checkMiniC2() {
    const a = document.getElementById('miniC2a').value.trim().replace('−', '-');
    const b = document.getElementById('miniC2b').value.trim().replace('−', '-');
    const c = document.getElementById('miniC2c').value;
    const fb = document.getElementById('miniC2fb');
    if ((a === '-8' || a === '−8') && (b === '-18' || b === '−18') && c === '>') {
        fb.textContent = '✓ Goed! −8 > −18. De ongelijkheid draait om bij vermenigvuldiging met een negatief getal!';
        fb.style.color = '#166534';
    } else {
        fb.textContent = '✗ 4 · (−2) = −8, 9 · (−2) = −18. En −8 is groter dan −18! Het teken draait om.';
        fb.style.color = '#991b1b';
    }
}

function checkMiniC3() {
    const a = document.getElementById('miniC3a').value.trim();
    const b = document.getElementById('miniC3b').value;
    const fb = document.getElementById('miniC3fb');
    if (a === '25' && b === 'pos') {
        fb.textContent = '✓ Goed! (−5)² = 25 > 0. Het kwadraat van elk getal ≠ 0 is positief (P12 + min×min=plus).';
        fb.style.color = '#166534';
    } else {
        fb.textContent = '✗ (−5)² = (−5) · (−5). Min keer min is plus! Dus (−5)² = 25.';
        fb.style.color = '#991b1b';
    }
}

// --- Blok D: Absolute waarde ---
function checkMiniD1() {
    const a = document.getElementById('miniD1a').value.trim();
    const b = document.getElementById('miniD1b').value.trim();
    const c = document.getElementById('miniD1c').value.trim();
    const d = document.getElementById('miniD1d').value.trim();
    const fb = document.getElementById('miniD1fb');
    if (a === '9' && b === '3' && c === '2' && d === '10') {
        fb.textContent = '✓ Goed! 9 + 3 − 2 = 10.';
        fb.style.color = '#166534';
    } else {
        fb.textContent = '✗ |−9| = 9, |3| = 3, |−2| = 2. Dus 9 + 3 − 2 = 10.';
        fb.style.color = '#991b1b';
    }
}

function checkMiniD2() {
    const a = document.getElementById('miniD2a').value.trim();
    const b = document.getElementById('miniD2b').value.trim();
    const c = document.getElementById('miniD2c').value.trim();
    const d = document.getElementById('miniD2d').value.trim();
    const e = document.getElementById('miniD2e').value.trim();
    const f = document.getElementById('miniD2f').value;
    const fb = document.getElementById('miniD2fb');
    if (a === '3' && b === '3' && c === '8' && d === '5' && e === '13' && f === 'ja') {
        fb.textContent = '✓ Goed! |3| = 3 ≤ 13 = 8 + 5. De driehoeksongelijkheid klopt!';
        fb.style.color = '#166534';
    } else {
        fb.textContent = '✗ 8 + (−5) = 3, dus |3| = 3. En |8| + |−5| = 8 + 5 = 13. Is 3 ≤ 13?';
        fb.style.color = '#991b1b';
    }
}

function checkMiniD3() {
    const a = document.getElementById('miniD3a').value.trim().replace('−', '-');
    const b = document.getElementById('miniD3b').value.trim().replace('−', '-');
    const fb = document.getElementById('miniD3fb');
    const vals = [a, b].sort();
    if ((vals[0] === '-7' && vals[1] === '3') || (vals[0] === '−7' && vals[1] === '3')) {
        fb.textContent = '✓ Goed! x + 2 = 5 → x = 3, of x + 2 = −5 → x = −7.';
        fb.style.color = '#166534';
    } else {
        fb.textContent = '✗ |x + 2| = 5 betekent: x + 2 = 5 óf x + 2 = −5. Los beide op.';
        fb.style.color = '#991b1b';
    }
}

// ==================== ENTER KEY SUPPORT ====================
document.querySelectorAll('.try-input, .try-it input[type=text], .mini-ex input[type=text]').forEach(input => {
    input.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            const btn = this.closest('.try-it, .mini-ex')?.querySelector('button') ||
                        this.parentElement.querySelector('button');
            if (btn) btn.click();
        }
    });
});

document.querySelectorAll('.exercise input[type=text]').forEach(input => {
    input.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            const btn = this.parentElement.querySelector('button');
            if (btn) btn.click();
        }
    });
});
