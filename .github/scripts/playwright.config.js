// @ts-check
const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: '.',
  timeout: 30000,
  retries: 0,
  reporter: [['list']],
  use: {
    headless: true,
    locale: 'nl-NL',
  },
  projects: [
    { name: 'chromium', use: { browserName: 'chromium' } },
  ],
});
