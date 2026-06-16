export default function ModelMetrics({ modelInfo }) {
  if (!modelInfo) return null

  const best = modelInfo.results[modelInfo.best_model]

  return (
    <div className="metrics-card">
      <h2>Selected Model</h2>

      <div className="metric-grid">
        <div>
          <span>Model</span>
          <strong>{modelInfo.best_model}</strong>
        </div>

        <div>
          <span>Accuracy</span>
          <strong>
            {(best["Accuracy"] * 100).toFixed(2)}%
          </strong>
        </div>

        <div>
          <span>Precision</span>
          <strong>
            {(best["Precision (macro)"] * 100).toFixed(2)}%
          </strong>
        </div>

        <div>
          <span>Recall</span>
          <strong>
            {(best["Recall (macro)"] * 100).toFixed(2)}%
          </strong>
        </div>

        <div>
          <span>F1 Score</span>
          <strong>
            {(best["F1 (macro)"] * 100).toFixed(2)}%
          </strong>
        </div>

        <div>
          <span>Cross Validation</span>
          <strong>
            {(best["CV Accuracy (5-fold)"] * 100).toFixed(2)}%
          </strong>
        </div>
      </div>
    </div>
  )
}