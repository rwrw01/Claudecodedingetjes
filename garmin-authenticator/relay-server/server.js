// Garmin Authenticator - Cloud Relay Server
//
// WebSocket relay die de browser extensie verbindt met de companion app
// Werkt via internet - geen lokaal netwerk nodig
//
// Deploy gratis op: Railway, Render, Fly.io, of zelf hosten
//
// Flow:
// 1. Browser extensie (laptop) stuurt nummer via WebSocket
// 2. Relay stuurt door naar companion app (telefoon)
// 3. Companion app stuurt naar Garmin horloge via Bluetooth
// 4. Horloge antwoord gaat terug via dezelfde keten

const { WebSocketServer } = require("ws");
const http = require("http");
const crypto = require("crypto");

const PORT = process.env.PORT || 8742;

// Simpele HTTP server voor health checks
const httpServer = http.createServer((req, res) => {
  if (req.url === "/health") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(
      JSON.stringify({
        status: "ok",
        channels: channels.size,
        uptime: process.uptime(),
      })
    );
    return;
  }

  // Landing page
  res.writeHead(200, { "Content-Type": "text/html" });
  res.end(`
    <!DOCTYPE html>
    <html>
    <head><title>Garmin Auth Relay</title></head>
    <body style="font-family:sans-serif;text-align:center;padding:40px;background:#1a1a2e;color:#fff">
      <h1>Garmin Authenticator Relay</h1>
      <p>WebSocket relay server draait.</p>
      <p style="color:#4CAF50">Status: Online</p>
    </body>
    </html>
  `);
});

// WebSocket server
const wss = new WebSocketServer({ server: httpServer });

// Channels: elke gebruiker heeft een uniek kanaal
// Een kanaal heeft een browser-client en een phone-client
const channels = new Map();

wss.on("connection", (ws, req) => {
  let clientChannel = null;
  let clientRole = null;

  console.log("[Relay] Nieuwe verbinding");

  ws.on("message", (data) => {
    let msg;
    try {
      msg = JSON.parse(data.toString());
    } catch {
      ws.send(JSON.stringify({ error: "Ongeldig JSON bericht" }));
      return;
    }

    // Registratie: client meldt zich aan bij een kanaal
    if (msg.type === "register") {
      const channelId = msg.channelId;
      const role = msg.role; // "browser" of "phone"

      if (!channelId || !role) {
        ws.send(JSON.stringify({ error: "channelId en role zijn verplicht" }));
        return;
      }

      if (!channels.has(channelId)) {
        channels.set(channelId, { browser: null, phone: null });
      }

      const channel = channels.get(channelId);
      channel[role] = ws;
      clientChannel = channelId;
      clientRole = role;

      console.log(`[Relay] ${role} geregistreerd op kanaal ${channelId.substring(0, 8)}...`);

      // Laat de andere kant weten dat er verbinding is
      const otherRole = role === "browser" ? "phone" : "browser";
      if (channel[otherRole] && channel[otherRole].readyState === 1) {
        channel[otherRole].send(
          JSON.stringify({
            type: "peer_connected",
            role: role,
          })
        );
        ws.send(
          JSON.stringify({
            type: "peer_connected",
            role: otherRole,
          })
        );
      }

      ws.send(JSON.stringify({ type: "registered", channelId, role }));
      return;
    }

    // Auth request: browser stuurt nummer naar telefoon
    if (msg.type === "ms_auth") {
      if (!clientChannel || clientRole !== "browser") {
        ws.send(JSON.stringify({ error: "Niet geregistreerd als browser" }));
        return;
      }

      const channel = channels.get(clientChannel);
      if (channel && channel.phone && channel.phone.readyState === 1) {
        channel.phone.send(
          JSON.stringify({
            type: "ms_auth",
            number: msg.number,
            service: msg.service || "Microsoft",
            timestamp: Date.now(),
          })
        );
        ws.send(JSON.stringify({ type: "ack", status: "sent_to_phone" }));
        console.log(
          `[Relay] Nummer ${msg.number} doorgestuurd naar telefoon`
        );
      } else {
        ws.send(
          JSON.stringify({
            type: "error",
            message: "Telefoon niet verbonden",
          })
        );
      }
      return;
    }

    // Auth response: telefoon stuurt antwoord van horloge terug naar browser
    if (msg.type === "ms_auth_response") {
      if (!clientChannel || clientRole !== "phone") {
        ws.send(JSON.stringify({ error: "Niet geregistreerd als phone" }));
        return;
      }

      const channel = channels.get(clientChannel);
      if (channel && channel.browser && channel.browser.readyState === 1) {
        channel.browser.send(
          JSON.stringify({
            type: "ms_auth_response",
            approved: msg.approved,
            timestamp: Date.now(),
          })
        );
        console.log(
          `[Relay] Antwoord doorgestuurd: ${msg.approved ? "bevestigd" : "geweigerd"}`
        );
      }
      return;
    }
  });

  ws.on("close", () => {
    if (clientChannel && clientRole) {
      const channel = channels.get(clientChannel);
      if (channel) {
        channel[clientRole] = null;

        // Laat de andere kant weten
        const otherRole = clientRole === "browser" ? "phone" : "browser";
        if (channel[otherRole] && channel[otherRole].readyState === 1) {
          channel[otherRole].send(
            JSON.stringify({
              type: "peer_disconnected",
              role: clientRole,
            })
          );
        }

        // Verwijder kanaal als beide weg zijn
        if (!channel.browser && !channel.phone) {
          channels.delete(clientChannel);
        }
      }
      console.log(`[Relay] ${clientRole} losgekoppeld van kanaal ${clientChannel.substring(0, 8)}...`);
    }
  });

  ws.on("error", (err) => {
    console.error("[Relay] WebSocket fout:", err.message);
  });

  // Ping/pong om verbinding actief te houden
  ws.isAlive = true;
  ws.on("pong", () => {
    ws.isAlive = true;
  });
});

// Heartbeat: verwijder dode verbindingen
const heartbeat = setInterval(() => {
  wss.clients.forEach((ws) => {
    if (ws.isAlive === false) {
      return ws.terminate();
    }
    ws.isAlive = false;
    ws.ping();
  });
}, 30000);

wss.on("close", () => {
  clearInterval(heartbeat);
});

// Genereer een nieuw kanaal-ID (voor eerste keer setup)
function generateChannelId() {
  return crypto.randomBytes(16).toString("hex");
}

// Start server
httpServer.listen(PORT, () => {
  console.log(`[Relay] Garmin Auth Relay draait op poort ${PORT}`);
  console.log(`[Relay] Health check: http://localhost:${PORT}/health`);
  console.log(`[Relay] WebSocket: ws://localhost:${PORT}`);
});
