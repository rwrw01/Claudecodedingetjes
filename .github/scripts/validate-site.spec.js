// @ts-check
// Navigatietest voor de live GitHub Pages site
// Hou rekening met deployment-vertraging: retries + wacht op networkidle
const { test, expect } = require('@playwright/test');

const BASE = 'https://rwrw01.github.io/Claudecodedingetjes';

test.describe('Homepage', () => {
  test('laadt correct', async ({ page }) => {
    const res = await page.goto(BASE + '/', { waitUntil: 'networkidle' });
    expect(res.status()).toBe(200);
    await expect(page.locator('header h1')).toContainText('Interactieve lesstof');
  });

  test('Schoollessen sectie aanwezig', async ({ page }) => {
    await page.goto(BASE + '/', { waitUntil: 'networkidle' });
    await expect(page.locator('.sc.blue')).toBeVisible();
    await expect(page.locator('.sc.blue strong')).toContainText('Schoollessen');
  });

  test('Leergangen sectie aanwezig', async ({ page }) => {
    await page.goto(BASE + '/', { waitUntil: 'networkidle' });
    await expect(page.locator('.sc.indigo')).toBeVisible();
    await expect(page.locator('.sc.indigo strong')).toContainText('Leergangen');
    await expect(page.locator('.sc.indigo')).toHaveAttribute('href', 'leergangen/');
  });

  test('klik op Leergangen geeft geen 404', async ({ page }) => {
    await page.goto(BASE + '/', { waitUntil: 'networkidle' });
    const [res] = await Promise.all([
      page.waitForResponse(r => r.url().includes('/leergangen/')),
      page.locator('.sc.indigo').click(),
    ]);
    expect(res.status()).toBe(200);
    await expect(page.locator('header h1')).toContainText('Leergangen');
  });
});

test.describe('Leergangen overzicht', () => {
  test('laadt correct (geen 404)', async ({ page }) => {
    const res = await page.goto(BASE + '/leergangen/', { waitUntil: 'networkidle' });
    expect(res.status()).toBe(200);
    await expect(page.locator('header h1')).toContainText('Leergangen');
  });

  test('geen gebroken links naar lege domein-paginas', async ({ page }) => {
    await page.goto(BASE + '/leergangen/', { waitUntil: 'networkidle' });
    const domainCards = page.locator('#domeinen a');
    const count = await domainCards.count();
    for (let i = 0; i < count; i++) {
      const href = await domainCards.nth(i).getAttribute('href');
      const res = await page.goto(BASE + '/leergangen/' + href, { waitUntil: 'networkidle' });
      expect(res.status(), `404 bij ${href}`).toBe(200);
      await page.goBack();
    }
  });

  test('colofon aanwezig', async ({ page }) => {
    await page.goto(BASE + '/leergangen/', { waitUntil: 'networkidle' });
    const footer = page.locator('footer');
    await expect(footer).toContainText('Ralph Wagter');
    await expect(footer).toContainText('EUPL');
  });

  test('/leergangen/ict/ geeft geen 404 als er lessen zijn, anders geen link', async ({ page }) => {
    await page.goto(BASE + '/leergangen/', { waitUntil: 'networkidle' });
    const ictLink = page.locator('#domeinen a[href="ict/"], #domeinen a[href*="ict"]');
    const ictLinked = await ictLink.count() > 0;
    if (ictLinked) {
      const res = await page.goto(BASE + '/leergangen/ict/', { waitUntil: 'networkidle' });
      expect(res.status(), '/leergangen/ict/ is gelinkt maar geeft 404').toBe(200);
    } else {
      // Goed: geen link als er geen lessen zijn, geen 404 mogelijk
      expect(ictLinked).toBe(false);
    }
  });
});

test.describe('Handleiding', () => {
  test('link aanwezig op homepage', async ({ page }) => {
    await page.goto(BASE + '/', { waitUntil: 'networkidle' });
    await expect(page.locator('a[href="handleiding.html"]')).toBeVisible();
  });
});
