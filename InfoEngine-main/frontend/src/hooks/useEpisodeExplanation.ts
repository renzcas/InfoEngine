// frontend/src/hooks/useEpisodeExplanation.ts
import { useState } from "react";

export function useEpisodeExplanation(episodeId?: string) {
  const [explanation, setExplanation] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchExplanation = async () => {
    if (!episodeId) return;
    setLoading(true);
    const res = await fetch(`/api/episodes/${episodeId}/explain`);
    const data = await res.json();
    setExplanation(data);
    setLoading(false);
  };

  return { explanation, loading, fetchExplanation };
}