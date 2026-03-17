window.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("ping-cyber");
  const out = document.getElementById("cyber-output");

  // One-shot HTTP ping
  btn.onclick = async () => {
    const res = await fetch("http://localhost:5000/cyber/ping");
    const data = await res.json();
    out.textContent = JSON.stringify(data, null, 2);
    window.EventBus.publish("cyber:telemetry", data);
  };

  // Live WebSocket telemetry
  const ws = new WebSocket("ws://localhost:5000/cyber/stream");

  ws.onmessage = evt => {
    try {
      const data = JSON.parse(evt.data);
      out.textContent = JSON.stringify(data, null, 2);
      window.EventBus.publish("cyber:telemetry", data);
    } catch {
      // ignore parse errors
    }
  };
});
