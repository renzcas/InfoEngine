window.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("compute-eigen");
  const input = document.getElementById("matrix-input");
  const out = document.getElementById("matrix-output");

  btn.onclick = async () => {
    try {
      // Parse matrix from textarea
      const matrix = JSON.parse(input.value);

      // Send to backend
      const res = await fetch("http://localhost:5000/matrix/eigen", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ matrix })
      });

      const data = await res.json();

      // Display result
      out.textContent = JSON.stringify(data, null, 2);

      // Broadcast eigenvalues to all other panels
      window.EventBus.publish("matrix:eigen", data);

    } catch (err) {
      out.textContent = "Invalid matrix or backend error.";
    }
  };
});
