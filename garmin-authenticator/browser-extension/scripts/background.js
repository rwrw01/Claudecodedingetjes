// Background service worker
// Beheert notificaties en communicatie tussen content scripts en popup

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "NUMBER_DETECTED") {
    // Toon badge op extensie icoon
    chrome.action.setBadgeText({ text: String(message.number) });
    chrome.action.setBadgeBackgroundColor({ color: "#0078D4" });

    // Sla op voor de popup
    chrome.storage.local.set({
      lastNumber: message.number,
      lastTimestamp: Date.now(),
      lastUrl: message.url,
    });
  }

  if (message.type === "SHOW_NOTIFICATION") {
    chrome.notifications.create({
      type: "basic",
      iconUrl: "icons/icon128.png",
      title: message.title,
      message: message.message,
      priority: 2,
    });
  }

  if (message.type === "AUTH_COMPLETE") {
    // Wis badge na bevestiging
    chrome.action.setBadgeText({ text: "" });
  }
});
