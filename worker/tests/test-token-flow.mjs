import { chromium } from "playwright";

const HUB_URL =
  "https://rwrw01.github.io/Claudecodedingetjes/rwrw01/wiskunde/havo-4/h6/?t=ksp_cd737e4b5930353846c658dadfe6f89bb338b2ce";

const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext();
const page = await ctx.newPage();

const logs = [];
page.on("console", (msg) => logs.push(`[${msg.type()}] ${msg.text()}`));
page.on("pageerror", (err) => logs.push(`[pageerror] ${err.message}`));

console.log("Stap 1: open hub-pagina met token in URL");
await page.goto(HUB_URL, { waitUntil: "networkidle" });
const hubLocal = await page.evaluate(() => ({
  token: localStorage.getItem("kasper-token"),
  search: location.search,
}));
console.log("  hub localStorage kasper-token:", hubLocal.token);
console.log("  hub URL search:", hubLocal.search);

console.log("\nStap 2: klik op de 6.1-card");
await page.click("a[href='6.1-raaklijnen-en-toppen/']");
await page.waitForLoadState("networkidle");
const subLocal = await page.evaluate(() => ({
  token: localStorage.getItem("kasper-token"),
  search: location.search,
  href: location.href,
}));
console.log("  6.1 localStorage kasper-token:", subLocal.token);
console.log("  6.1 URL search:", subLocal.search);
console.log("  6.1 URL href:", subLocal.href);

console.log("\nStap 3: open chat widget en bekijk wat er gebeurt");
await page.click(".chat-fab");
await page.waitForTimeout(2500);
const chatText = await page.locator("#chatMessages").innerText();
console.log("  chat messages content (eerste 400 chars):");
console.log("  " + chatText.replace(/\n/g, "\n  ").slice(0, 400));

console.log("\nStap 4: console-output van pagina");
for (const l of logs) console.log("  " + l);

await browser.close();
