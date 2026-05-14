import { chromium } from "playwright";

const URL =
  "https://rwrw01.github.io/Claudecodedingetjes/rwrw01/wiskunde/havo-4/h6/6.1-raaklijnen-en-toppen/?t=ksp_cd737e4b5930353846c658dadfe6f89bb338b2ce";

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
await page.goto(URL, { waitUntil: "networkidle" });
await page.click(".chat-fab");
await page.waitForFunction(
  () => {
    const msgs = document.querySelectorAll(".msg.assistant");
    return msgs.length > 0 && msgs[0].innerHTML.length > 50;
  },
  { timeout: 15000 }
);
await page.waitForTimeout(1500);

const result = await page.evaluate(() => {
  const msg = document.querySelector(".msg.assistant");
  return {
    innerHTML: msg.innerHTML,
    strongCount: msg.querySelectorAll("strong").length,
    strongTexts: Array.from(msg.querySelectorAll("strong")).map((s) => s.textContent),
  };
});
console.log("Aantal <strong>-elementen:", result.strongCount);
console.log("Tekst in <strong>:", result.strongTexts);
console.log("\nHTML snippet (eerste 500 chars):");
console.log(result.innerHTML.slice(0, 500));

await browser.close();
