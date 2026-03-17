window.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("load-zeta");
  const out = document.getElementById("riemann-output");
  const canvas = document.getElementById("riemann-spectrum");
  const ctx = canvas.getContext("2d");

  btn.onclick = async () => {
    const res = await fetch("http://localhost:5000/physics/zeta_spectrum");
    const data = await res.json();
    out.textContent = JSON.stringify(data, null, 2);

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    (data.zeros || []).forEach((z, i) => {
      const x = i * 10 + 10;
      const y = canvas.height / 2;
      ctx.fillRect(x, y - 5, 4, 10);
    });
  };
});
