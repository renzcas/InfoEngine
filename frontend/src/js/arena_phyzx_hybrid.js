window.addEventListener("DOMContentLoaded", () => {
  const cyberOut = document.getElementById("cyber-telemetry");
  const canvas = document.getElementById("field-geometry");
  const ctx = canvas.getContext("2d");

  let pulse = 0;
  let pulseDir = 1;
  let hasCyber = false;
  let hasMatrix = false;
  let hasRiemann = false;

  function drawBackground() {
    const grd = ctx.createRadialGradient(200, 150, 10, 200, 150, 200);
    grd.addColorStop(0, "#050510");
    grd.addColorStop(1, "#000000");
    ctx.fillStyle = grd;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  }

  function render() {
    drawBackground();

    // Cyber pulse
    if (hasCyber) {
      ctx.beginPath();
      ctx.strokeStyle = "#00ff88";
      ctx.lineWidth = 2;
      ctx.arc(200, 150, 40 + pulse, 0, 2 * Math.PI);
      ctx.stroke();
    }

    // Matrix square
    if (hasMatrix) {
      ctx.fillStyle = "rgba(0, 150, 255, 0.3)";
      ctx.fillRect(150, 100, 100, 100);
    }

    // Riemann bars
    if (hasRiemann && window.__riemannZeros) {
      window.__riemannZeros.forEach((z, i) => {
        ctx.fillStyle = "rgba(255, 0, 200, 0.4)";
        ctx.fillRect(50 + i * 8, 20, 4, 260);
      });
    }

    pulse += pulseDir * 0.8;
    if (pulse > 20 || pulse < 0) pulseDir *= -1;

    requestAnimationFrame(render);
  }

  // Subscriptions
  window.EventBus.subscribe("cyber:telemetry", data => {
    cyberOut.textContent = JSON.stringify(data, null, 2);
    hasCyber = true;
  });

  window.EventBus.subscribe("matrix:eigen", () => {
    hasMatrix = true;
  });

  window.EventBus.subscribe("riemann:zeros", data => {
    window.__riemannZeros = data.zeros || [];
    hasRiemann = true;
  });

  render();
});
