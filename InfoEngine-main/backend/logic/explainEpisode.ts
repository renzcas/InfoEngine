// backend/logic/explainEpisode.ts
export function explainEpisode({ episode, flows, alerts, labs, lineage }) {
  const protocols = Array.from(
    new Set(flows.flatMap(f => f.protocols || []))
  );

  const threats = alerts.map(a => ({
    type: a.type,
    severity: a.severity,
    reason: a.reason,
    flow_id: a.flow_id,
    extra: a.extra || {},
  }));

  const summary = buildSummary({ episode, protocols, threats });

  const timeline = buildTimeline({ flows, alerts });

  const key_entities = extractEntities({ flows });

  const labsForEpisode = labs.map(l => ({
    lab_id: l.lab_id,
    status: l.status,
    focus: l.title,
  }));

  return {
    episode_id: episode.id,
    summary,
    timeline,
    key_entities,
    protocols,
    threats,
    labs: labsForEpisode,
    lineage,
    next_actions: buildNextActions({ threats, labs: labsForEpisode, lineage }),
  };
}