import { PRICE_TIERS } from '../specConfig'

function Gauge({ result }) {
  const predicted = result ? PRICE_TIERS[result.price_range] : null
  // Marker sits within the predicted tier's 25%-wide segment; confidence
  // pushes it further to the right within that segment.
  const markerPct = result ? result.price_range * 25 + result.confidence * 25 : 0

  return (
    <div className="gauge">
      <div className="gauge__track">
        {PRICE_TIERS.map((tier) => (
          <div
            key={tier.value}
            className="gauge__segment"
            style={{ background: tier.color, opacity: predicted && predicted.value === tier.value ? 1 : 0.28 }}
          />
        ))}
        {result && (
          <div className="gauge__marker" style={{ left: `${markerPct}%`, background: predicted.color }} />
        )}
      </div>
      <div className="gauge__ticks">
        {PRICE_TIERS.map((tier) => (
          <span key={tier.value} className="gauge__tick" style={{ color: predicted?.value === tier.value ? tier.color : undefined }}>
            {tier.short}
          </span>
        ))}
      </div>
    </div>
  )
}

export default function ResultPanel({ result, error, loading }) {
  const predicted = result ? PRICE_TIERS[result.price_range] : null

  return (
    <div className="result-panel">
      <div className="result-panel__header">
        <span className="result-panel__eyebrow">Predicted Tier</span>
        {predicted ? (
          <h2 className="result-panel__title" style={{ color: predicted.color }}>
            {predicted.label}
          </h2>
        ) : (
          <h2 className="result-panel__title result-panel__title--placeholder">Awaiting input</h2>
        )}
        {result && <p className="result-panel__confidence">Confidence: {(result.confidence * 100).toFixed(1)}%</p>}
      </div>

      <Gauge result={result} />

      {error && <p className="result-panel__error">{error}</p>}

      {result && (
        <div className="probs">
          <h3>Class probabilities</h3>
          {PRICE_TIERS.map((tier) => {
            const p = result.probabilities[tier.label] ?? 0
            return (
              <div className="probs__row" key={tier.value}>
                <span className="probs__label">{tier.label}</span>
                <div className="probs__bar">
                  <div className="probs__fill" style={{ width: `${p * 100}%`, background: tier.color }} />
                </div>
                <span className="probs__value">{(p * 100).toFixed(1)}%</span>
              </div>
            )
          })}
        </div>
      )}

      {!result && !error && (
        <p className="result-panel__hint">
          Adjust the specifications on the left, then run a prediction to see where this device lands
          on the price spectrum — from 0 (Low Cost) to 3 (Very High Cost).
        </p>
      )}

      {loading && <p className="result-panel__hint">Sending specs to the model…</p>}
    </div>
  )
}
