// frontend/src/pages/EpisodePage.tsx
import { useEpisodeExplanation } from "../hooks/useEpisodeExplanation";
import { EpisodeExplanationPanel } from "../panels/EpisodeExplanationPanel";

const EpisodePage: React.FC = () => {
  const { episodeId } = useParams();
  const { events, setEventsForEpisode } = useEventsForEpisode(episodeId);
  const { explanation, loading, fetchExplanation } =
    useEpisodeExplanation(episodeId);

  useEffect(() => {
    fetch(`/api/episodes/${episodeId}/events`)
      .then(res => res.json())
      .then(data => setEventsForEpisode(episodeId, data));
  }, [episodeId]);

  return (
    <div className="episode-layout">
      <div className="episode-header">
        <h1>Episode {episodeId}</h1>
        <button onClick={fetchExplanation} disabled={loading}>
          {loading ? "Explaining..." : "Explain This Episode"}
        </button>
      </div>

      <EpisodeSummaryPanel events={events} />
      <FlowsPanel events={events} />
      <TimelinePanel events={events} />
      <AlertsPanel events={events} />

      {explanation && (
        <EpisodeExplanationPanel explanation={explanation} />
      )}
    </div>
  );
};