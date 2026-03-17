async function fetchIdeals(n) {
  const res = await fetch("http://localhost:5000/algebra/ideals", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ n })
  });
  return res.json();
}

function drawSpectrum(ideals) {
  const canvas = document.getElementById("spectrum");
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  ideals.forEach((ideal, i) => {
    const h = ideal.elements.length * 10;
    ctx.fillStyle = `hsl(${i * 40}, 80%, 60%)`;
    ctx.fillRect(i * 40 + 20, canvas.height - h, 30, h);
  });
}

window.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("compute-ideals");
  const out = document.getElementById("ideals-output");

  let lastEigen = null;
  window.EventBus.subscribe("matrix:eigen", data => {
    lastEigen = data;
  });

  btn.onclick = async () => {
    const n = Number(document.getElementById("mod-n").value);
    if (!lastEigen) {
      out.textContent = "No eigenvalues yet. Go to Matrix panel first.";
      return;
    }

    const gens = lastEigen.eigenvalues.map(v => Math.abs(Math.round(v)) % n);
    const data = await fetchIdeals(n);

    const ideals = data.ideals.filter(id => gens.includes(id.generator));
    out.textContent = JSON.stringify(ideals, null, 2);
    drawSpectrum(ideals);
  };
});
