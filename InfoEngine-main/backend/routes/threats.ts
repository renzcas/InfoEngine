// backend/routes/threats.ts

router.get("/threats/:alertId/explain", async (req, res) => {
  const { alertId } = req.params;

  const alert = await loadAlert(alertId);
  const flow = await loadFlow(alert.flow_id);
  const packets = await loadPacketsForFlow(alert.flow_id);

  const explanation = explainThreat({ alert, flow, packets });

  res.json(explanation);
});