export default function ModelComparison({ modelInfo }) {
  if (!modelInfo?.results) return null

  const models = Object.entries(modelInfo.results).sort(
    (a, b) => b[1]["Accuracy"] - a[1]["Accuracy"]
  )

  return (
    <div className="comparison-card">
      <h2>Model Performance Comparison</h2>

      {models.map(([name, metrics]) => (
        <>
        <div key={name} className="comparison-row">
          <div className="comparison-label">
            {name}

            {name === modelInfo.best_model && (
              <span className="best-model">
                🏆 Best
              </span>
            )}
          </div>
            <header>Accuracy</header>
          <div className="comparison-bar">
            
            <div
              className="comparison-fill"
              style={{
                width: `${metrics["Accuracy"] * 100}%`
              }}
            />
            </div>

        <span>
            {(metrics["Accuracy"] * 100).toFixed(2)}%
          </span>
          <div></div>
            <header className="header_acc">Precision</header>
            <div className="comparison-bar">
            
            <div
              className="comparison-fill"
              style={{
                width: `${metrics["Precision (macro)"] * 100}%`
              }}
            />
          </div>

        <span>
            {(metrics["Precision (macro)"] * 100).toFixed(2)}%
          </span>


        </div>
        <hr />
        </>
      ))}
    </div>
  )
}