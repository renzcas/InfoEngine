window.addEventListener("DOMContentLoaded", () => {
  const cyberOut = document.getElementById("cyber-telemetry");
  const canvas = document.getElementById("field-geometry");
  const ctx = canvas.getContext("2d");

  window.EventBus.subscribe("cyber:telemetry", data => {
    cyberOut.textContent = JSON.stringify(data, null, 2);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.beginPath();
    ctx.arc(200, 150, 50, 0, 2 * Math.PI);
    ctx.stroke();
  });

  window.EventBus.subscribe("matrix:eigen", data => {
    ctx.fillStyle = "rgba(0, 150, 255, 0.3)";
    ctx.fillRect(150, 100, 100, 100);
  });
});
