window.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("compute-eigen");
  const input = document.getElementById("matrix-input");
  const out = document.getElementById("matrix-output");

  btn.onclick = async () => {
    const matrix = JSON.parse(input.value);
    const res = await fetch("http://localhost:5000/matrix/eigen", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ matrix })
    });
    const data = await res.json();
    out.textContent = JSON.stringify(data, null, 2);

    window.EventBus.publish("matrix:eigen", data);
  };
});
