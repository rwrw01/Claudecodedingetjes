// Content script - draait op Microsoft login pagina's
// Detecteert het number matching scherm en stuurt het nummer naar de companion app

(function () {
  "use strict";

  const CHECK_INTERVAL_MS = 1000;
  const COMPANION_PORT = 8742;
  let lastSentNumber = null;
  let isWaitingForResponse = false;

  // Start observatie van de pagina
  function init() {
    console.log("[Garmin Auth] Content script geladen op:", window.location.href);
    // Check periodiek of het number matching scherm zichtbaar is
    setInterval(checkForNumberMatching, CHECK_INTERVAL_MS);
    // Ook observeren via MutationObserver voor snellere detectie
    observePageChanges();
  }

  // Zoek het 2-cijferige nummer op de Microsoft login pagina
  // Microsoft toont het nummer in een element met specifieke kenmerken
  function checkForNumberMatching() {
    // Microsoft number matching toont het nummer in de pagina tekst
    // Zoek naar patronen als "Enter the number: XX" of het nummer in een groot display

    // Methode 1: Zoek naar het nummer-display element
    const numberDisplay = findNumberDisplayElement();
    if (numberDisplay !== null && numberDisplay !== lastSentNumber) {
      console.log("[Garmin Auth] Number matching gedetecteerd:", numberDisplay);
      sendNumberToCompanion(numberDisplay);
      return;
    }

    // Methode 2: Zoek in de pagina tekst
    const bodyText = document.body.innerText;

    // Nederlands: "Voer het nummer in dat wordt weergegeven"
    // Engels: "Enter the number shown" / "Enter number"
    const patterns = [
      /(?:enter|voer)\s+(?:the\s+)?(?:number|nummer)\s*(?:shown|dat|:)?\s*(\d{2})/i,
      /number\s+matching[^]*?(\d{2})/i,
    ];

    for (const pattern of patterns) {
      const match = bodyText.match(pattern);
      if (match && match[1]) {
        const number = parseInt(match[1], 10);
        if (number >= 10 && number <= 99 && number !== lastSentNumber) {
          console.log(
            "[Garmin Auth] Nummer gevonden via tekstpatroon:",
            number
          );
          sendNumberToCompanion(number);
          return;
        }
      }
    }
  }

  // Zoek het nummer-display element op de Microsoft pagina
  function findNumberDisplayElement() {
    // Microsoft gebruikt specifieke CSS classes en data attributen
    // voor het number matching display
    const selectors = [
      // Standaard number matching display
      '[data-bind*="displaySign"]',
      ".display-sign-container",
      ".number-match-display",
      // Groot nummer in het midden van de pagina
      ".ext-sign-in-dialog .number-display",
      // Alternatieve selectors
      '[aria-label*="number"]',
      '[aria-label*="nummer"]',
    ];

    for (const selector of selectors) {
      const elements = document.querySelectorAll(selector);
      for (const el of elements) {
        const text = el.textContent.trim();
        const num = parseInt(text, 10);
        if (num >= 10 && num <= 99) {
          return num;
        }
      }
    }

    // Fallback: zoek naar grote nummers (font-size > 30px) in de pagina
    const allElements = document.querySelectorAll(
      "span, div, p, h1, h2, h3, strong"
    );
    for (const el of allElements) {
      const text = el.textContent.trim();
      if (/^\d{2}$/.test(text)) {
        const style = window.getComputedStyle(el);
        const fontSize = parseFloat(style.fontSize);
        // Groot nummer (>30px) is waarschijnlijk het matching nummer
        if (fontSize > 30) {
          return parseInt(text, 10);
        }
      }
    }

    return null;
  }

  // Observeer DOM wijzigingen voor snellere detectie
  function observePageChanges() {
    const observer = new MutationObserver(() => {
      checkForNumberMatching();
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true,
      characterData: true,
    });
  }

  // Stuur het nummer naar de companion app via lokaal netwerk
  async function sendNumberToCompanion(number) {
    if (isWaitingForResponse) return;

    lastSentNumber = number;
    isWaitingForResponse = true;

    // Laat de background script weten dat we een nummer hebben
    chrome.runtime.sendMessage({
      type: "NUMBER_DETECTED",
      number: number,
      url: window.location.href,
    });

    // Haal het companion app IP op uit opgeslagen instellingen
    const settings = await chrome.storage.sync.get([
      "companionHost",
      "companionPort",
    ]);
    const host = settings.companionHost || "localhost";
    const port = settings.companionPort || COMPANION_PORT;

    try {
      console.log(`[Garmin Auth] Verstuur nummer ${number} naar ${host}:${port}`);

      const response = await fetch(`http://${host}:${port}/auth-request`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type: "ms_auth",
          number: number,
          service: extractServiceName(),
          timestamp: Date.now(),
        }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log("[Garmin Auth] Companion app antwoord:", data);

        // Wacht op bevestiging van het horloge
        if (data.status === "sent_to_watch") {
          showNotification("Nummer verstuurd naar horloge", `Kies ${number} op je Garmin`);
          waitForWatchResponse(host, port);
        }
      } else {
        console.error("[Garmin Auth] Companion app fout:", response.status);
        showNotification("Fout", "Kan niet verbinden met companion app");
        isWaitingForResponse = false;
      }
    } catch (error) {
      console.error("[Garmin Auth] Verbindingsfout:", error);
      showNotification(
        "Niet verbonden",
        "Zorg dat de companion app draait op je telefoon"
      );
      isWaitingForResponse = false;
    }
  }

  // Wacht op antwoord van het Garmin horloge (via polling)
  async function waitForWatchResponse(host, port) {
    const maxWaitMs = 60000;
    const pollIntervalMs = 1000;
    const startTime = Date.now();

    const poll = async () => {
      if (Date.now() - startTime > maxWaitMs) {
        console.log("[Garmin Auth] Timeout - geen antwoord van horloge");
        showNotification("Verlopen", "Geen antwoord van horloge ontvangen");
        isWaitingForResponse = false;
        return;
      }

      try {
        const response = await fetch(`http://${host}:${port}/auth-response`, {
          method: "GET",
        });

        if (response.ok) {
          const data = await response.json();

          if (data.status === "approved") {
            console.log("[Garmin Auth] Horloge heeft bevestigd!");
            showNotification("Bevestigd!", "Inloggen goedgekeurd via Garmin");
            autoClickApproval();
            isWaitingForResponse = false;
            return;
          } else if (data.status === "denied") {
            console.log("[Garmin Auth] Horloge heeft geweigerd");
            showNotification("Geweigerd", "Inloggen geweigerd via Garmin");
            isWaitingForResponse = false;
            return;
          }
          // status === "pending" → blijf pollen
        }
      } catch {
        // Verbindingsfout → blijf proberen
      }

      setTimeout(poll, pollIntervalMs);
    };

    poll();
  }

  // Klik automatisch op de juiste knop na bevestiging van het horloge
  function autoClickApproval() {
    // Zoek de approve/bevestigen knop op de Microsoft pagina
    const approveSelectors = [
      'input[type="submit"][value*="Approve"]',
      'input[type="submit"][value*="Goedkeuren"]',
      'button[aria-label*="Approve"]',
      'button[aria-label*="approve"]',
      "#idSIButton9",
      'input[value="Yes"]',
      'input[value="Ja"]',
    ];

    for (const selector of approveSelectors) {
      const button = document.querySelector(selector);
      if (button) {
        console.log("[Garmin Auth] Auto-klik op approve knop:", selector);
        button.click();
        return;
      }
    }

    console.log(
      "[Garmin Auth] Geen approve knop gevonden - handmatig bevestigen"
    );
  }

  // Probeer de service naam te herkennen uit de pagina
  function extractServiceName() {
    // Zoek naar de app/service naam op de login pagina
    const selectors = [
      ".ext-sign-in-dialog .app-name",
      '[data-bind*="appName"]',
      ".banner-logo",
      "#loginHeader",
    ];

    for (const selector of selectors) {
      const el = document.querySelector(selector);
      if (el && el.textContent.trim()) {
        return el.textContent.trim();
      }
    }

    return "Microsoft";
  }

  // Toon een browser notificatie
  function showNotification(title, message) {
    chrome.runtime.sendMessage({
      type: "SHOW_NOTIFICATION",
      title: title,
      message: message,
    });
  }

  // Start!
  init();
})();
