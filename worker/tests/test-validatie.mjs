import { chromium } from "playwright";

const URL =
  "https://rwrw01.github.io/Claudecodedingetjes/rwrw01/wiskunde/havo-4/h6/6.3-kettingregel/?t=ksp_cd737e4b5930353846c658dadfe6f89bb338b2ce";

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
await page.goto(URL, { waitUntil: "networkidle" });
await page.click(".chat-fab");

async function readLastAssistantMessage() {
  return await page.evaluate(() => {
    const msgs = document.querySelectorAll(".msg.assistant");
    return msgs.length > 0 ? msgs[msgs.length - 1].innerText : null;
  });
}

async function waitForNewAssistantMessage(prevCount) {
  await page.waitForFunction(
    (count) => {
      const msgs = document.querySelectorAll(".msg.assistant");
      return msgs.length > count && msgs[msgs.length - 1].innerText.length > 50;
    },
    prevCount,
    { timeout: 30000 }
  );
  // Wait for streaming to finish
  let stable = "";
  for (let i = 0; i < 20; i++) {
    await page.waitForTimeout(500);
    const current = await readLastAssistantMessage();
    if (current === stable && current && current.length > 50) break;
    stable = current ?? "";
  }
}

async function send(text) {
  const before = await page.locator(".msg.assistant").count();
  await page.fill(".chat-input", text);
  await page.click(".chat-send");
  await waitForNewAssistantMessage(before);
}

// Wait for initial greeting
await page.waitForFunction(
  () => document.querySelectorAll(".msg.assistant").length > 0,
  { timeout: 15000 }
);
await page.waitForTimeout(3000);
console.log("--- 1. Opening van tutor ---");
console.log(await readLastAssistantMessage());

console.log("\n--- 2. Kasper antwoordt FOUT: '12x+6' (met kettingregel-fout) ---");
await send("uitkomst (met kettingregel) = 12x+6");
console.log(await readLastAssistantMessage());

console.log("\n--- 3. Kasper vraagt 'maar klopt het antwoord?' ---");
await send("maar klopt het antwoord?");
console.log(await readLastAssistantMessage());

await browser.close();
