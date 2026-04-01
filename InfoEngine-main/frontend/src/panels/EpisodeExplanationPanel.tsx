// frontend/src/panels/EpisodeExplanationPanel.tsx

type Props = {
  explanation: any;
};

export const EpisodeExplanationPanel: React.FC<Props> = ({ explanation }) => {
  const { summary, timeline, threats, labs, lineage, next_actions } =
    explanation;

  return (
    <div className="panel episode-explanation-panel">
      <h2>Episode Explanation</h2>
      <p>{summary}</p>

      <h3>Timeline</h3>
      <ul>
        {timeline.map((t: string, i: number) => (
          <li key={i}>{t}</li>
        ))}
      </ul>

      <h3>Threats</h3>
      <ul>
        {threats.map((th: any, i: number) => (
          <li key={i}>
            <strong>{th.type}</strong> — {th.reason} (severity {th.severity})
          </li>
        ))}
      </ul>

      <h3>Labs</h3>
      <ul>
        {labs.map((l: any) => (
          <li key={l.lab_id}>
            {l.lab_id}: {l.focus} ({l.status})
          </li>
        ))}
      </ul>

      <h3>Lineage</h3>
      <p>
        Parent: {lineage.parent || "none"} | Children:{" "}
        {lineage.children?.join(", ") || "none"}
      </p>

      <h3>Suggested next actions</h3>
      <ul>
        {next_actions.map((a: string, i: number) => (
          <li key={i}>{a}</li>
        ))}
      </ul>
    </div>
  );
};