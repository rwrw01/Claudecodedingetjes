// @ts-check
const { test, expect } = require('@playwright/test');

const LESSON_FILE = process.env.LESSON_FILE;
if (!LESSON_FILE) throw new Error('LESSON_FILE env var vereist');

test.describe('Les validatie', () => {

  test.beforeEach(async ({ page }) => {
    const jsErrors = [];
    page.on('pageerror', err => jsErrors.push(err.message));
    page.on('console', msg => { if (msg.type() === 'error') jsErrors.push(msg.text()); });
    await page.goto('file:///' + LESSON_FILE.replace(/\\/g, '/'));
    page._jsErrors = jsErrors;
  });

  test('1. Geen JS-fouten', async ({ page }) => {
    await page.waitForTimeout(500);
    expect(page._jsErrors || [], `JS-fouten: ${(page._jsErrors||[]).join(', ')}`).toHaveLength(0);
  });

  test('2. Minimaal 3 sliders', async ({ page }) => {
    const count = await page.locator('input[type="range"]').count();
    expect(count, `Sliders: ${count} — verwacht >=3`).toBeGreaterThanOrEqual(3);
  });

  test('3. Minimaal 1 SVG-diagram', async ({ page }) => {
    const count = await page.locator('svg').count();
    expect(count, `SVG: ${count} — verwacht >=1`).toBeGreaterThanOrEqual(1);
  });

  test('4. Minimaal 8 oefeningen met invulveld', async ({ page }) => {
    const count = await page.locator('input[type="text"], input:not([type])').count();
    expect(count, `Invulvelden: ${count} — verwacht >=8`).toBeGreaterThanOrEqual(8);
  });

  test('5. Hint-knoppen aanwezig', async ({ page }) => {
    const count = await page.locator('button:has-text("Hint"), button:has-text("hint")').count();
    expect(count, `Hint-knoppen: ${count} — verwacht >=4`).toBeGreaterThanOrEqual(4);
  });

  test('6. Uitleg-knoppen aanwezig', async ({ page }) => {
    const count = await page.locator('button:has-text("Leg uit"), button:has-text("uitleg"), button:has-text("Uitleg"), button:has-text("📖")').count();
    expect(count, `Uitleg-knoppen: ${count} — verwacht >=4`).toBeGreaterThanOrEqual(4);
  });

  test('7. Hint toont zich na klikken', async ({ page }) => {
    const hintBtn = page.locator('button:has-text("Hint"), button:has-text("hint")').first();
    await hintBtn.scrollIntoViewIfNeeded();
    await hintBtn.click();
    await page.waitForTimeout(300);
    const hintContent = page.locator('.hint-box, [id^="hint-"]:visible, [class*="hint"]:visible');
    const visible = await hintContent.count();
    expect(visible, 'Hint-inhoud niet zichtbaar na klikken').toBeGreaterThanOrEqual(1);
  });

  test('8. Uitlegknop verschijnt na fout antwoord', async ({ page }) => {
    const input = page.locator('input[type="text"], input:not([type])').first();
    await input.scrollIntoViewIfNeeded();
    await input.fill('99999');
    const checkBtn = page.locator('button:has-text("Controleer"), button:has-text("Check"), button:has-text("Nakijken")').first();
    await checkBtn.click();
    await page.waitForTimeout(400);
    const uitlegZichtbaar = page.locator('[id^="uitleg-"]:visible, .uitleg-stappen:visible, button:has-text("Leg uit"):visible, button:has-text("📖"):visible');
    const count = await uitlegZichtbaar.count();
    expect(count, 'Uitleg niet zichtbaar na fout antwoord').toBeGreaterThanOrEqual(1);
  });

  test('9. HTML volledig', async ({ page }) => {
    const html = await page.content();
    expect(html).toContain('</html>');
    expect(html).toContain('</script>');
    const bodyIdx = html.lastIndexOf('</body>');
    const htmlIdx = html.lastIndexOf('</html>');
    expect(bodyIdx).toBeLessThan(htmlIdx);
  });

  test('10. Colofon met Ralph en EUPL', async ({ page }) => {
    const footer = page.locator('footer');
    const text = await footer.textContent();
    expect(text.toLowerCase()).toContain('ralph');
    expect(text.toLowerCase()).toContain('eupl');
  });

});
