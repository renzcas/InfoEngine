window.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("ping-infophyzx");
  const out = document.getElementById("infophyzx-output");

  btn.onclick = async () => {
    const res = await fetch("http://localhost:5000/infophyzx/ping");
    out.textContent = JSON.stringify(await res.json(), null, 2);
  };
});
