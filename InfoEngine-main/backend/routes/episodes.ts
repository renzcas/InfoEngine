// backend/routes/episodes.ts
router.get("/episodes/:episodeId/explain", async (req, res) => {
  const { episodeId } = req.params;

  const episode = await loadEpisode(episodeId);
  const flows = await loadFlowsForEpisode(episodeId);
  const packets = await loadPacketsForEpisode(episodeId);
  const alerts = await loadAlertsForEpisode(episodeId);   // dns_tunneling, http_anomaly, etc.
  const labs = await loadLabsForEpisode(episodeId);
  const lineage = await loadLineageForEpisode(episodeId);

  const explanation = explainEpisode({
    episode,
    flows,
    packets,
    alerts,
    labs,
    lineage,
  });

  res.json(explanation);
});