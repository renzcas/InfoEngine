import { useEffect, useState } from "react";

type SurpriseEntropyState = {
  surprise: number;
  entropy: number;
  panic: number;
  reward: number;
  coherence: number;
  anomaly: number;
  timestamp: number | null;
};

export function SurpriseEntropyPanel() {
  const [state, setState] = useState<SurpriseEntropyState | null>(null);

  useEffect(() => {
    const fetchState = async () => {
      const res = await fetch("/organ/mind/surprise_entropy/state/last");
      const data = await res.json();
      setState(data);
    };
    fetchState();
    const id = setInterval(fetchState, 2000);
    return () => clearInterval(id);
  }, []);

  if (!state) return <div>Loading surprise/entropy state…</div>;

  return (
    <div>
      <h2>Surprise–Entropy</h2>
      <p>Surprise: {state.surprise.toFixed(3)}</p>
      <p>Entropy: {state.entropy.toFixed(3)}</p>
      <p>Panic: {state.panic.toFixed(3)}</p>
      <p>Reward: {state.reward.toFixed(3)}</p>
      <p>Coherence: {state.coherence.toFixed(3)}</p>
      <p>Anomaly: {state.anomaly.toFixed(3)}</p>
    </div>
  );
}
