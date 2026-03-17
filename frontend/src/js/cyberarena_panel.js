window.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("ping-cyber");
  const out = document.getElementById("cyber-output");

  btn.onclick = async () => {
    const res = await fetch("http://localhost:5000/cyber/ping");
    const data = await res.json();
    out.textContent = JSON.stringify(data, null, 2);

    // broadcast telemetry
    window.EventBus.publish("cyber:telemetry", data);
  };
});
