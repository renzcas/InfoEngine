// frontend/src/pages/EpisodePage.tsx

const EpisodePage: React.FC = () => {
  const { episodeId } = useParams();
  const { events, setEventsForEpisode } = useEventsForEpisode(episodeId);

  useEffect(() => {
    fetch(`/api/episodes/${episodeId}/events`)
      .then(res => res.json())
      .then(data => setEventsForEpisode(episodeId, data));
  }, [episodeId]);

  return (
    <div className="episode-layout">
      <EpisodeSummaryPanel events={events} />
      <FlowsPanel events={events} />
      <TimelinePanel events={events} />
      <AlertsPanel events={events} />
    </div>
  );
};