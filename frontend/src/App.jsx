import { useEffect, useState } from 'react'
import SpecForm from './components/SpecForm'
import ResultPanel from './components/ResultPanel'
import { DEFAULT_SPECS } from './specConfig'
import { fetchModelInfo, predictPriceRange } from './api'
import ModelComparison from './components/ModelComparison'
import ModelMetrics from './components/ModelMetrics'
import Modal from './components/Modal'

export default function App() {
  const [specs, setSpecs] = useState(DEFAULT_SPECS)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const [modelInfo, setModelInfo] = useState(null)
  const [apiOnline, setApiOnline] = useState(null)

  // Controls which modal (if any) is open: null | 'comparison' | 'metrics'
  const [activeModal, setActiveModal] = useState(null)

  useEffect(() => {
    fetchModelInfo()
      .then((info) => {
        setModelInfo(info)
        setApiOnline(true)
      })
      .catch(() => setApiOnline(false))
  }, [])

  function handleChange(key, value) {
    setSpecs((prev) => ({ ...prev, [key]: value }))
  }

  async function handleSubmit() {
    setLoading(true)
    setError(null)
    try {
      const res = await predictPriceRange(specs)
      setResult(res)
    } catch (err) {
      setError(err.message)
      setResult(null)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="app__header">
        <div className="app__brand">
          <span className="app__logo" aria-hidden="true">
            <svg viewBox="0 0 24 24" width="22" height="22">
              <rect x="6" y="2" width="12" height="20" rx="2.5" fill="none" stroke="currentColor" strokeWidth="1.6" />
              <circle cx="12" cy="18" r="0.9" fill="currentColor" />
            </svg>
          </span>
          <div>
            {/* <h1>SpecSense</h1> */}
            <h1>Mobile price-range predictor</h1>
          </div>
        </div>

        <div className="app__header-right">
          {modelInfo && (
            <div className="app__model-buttons">
              <button
                type="button"
                className="app__model-btn"
                onClick={() => setActiveModal('metrics')}
              >
                Selected Model
              </button>
              <button
                type="button"
                className="app__model-btn"
                onClick={() => setActiveModal('comparison')}
              >
                Compare Models
              </button>
            </div>
          )}

          <div className={`app__status ${apiOnline ? 'is-online' : apiOnline === false ? 'is-offline' : ''}`}>
            <span className="app__status-dot" />
            {apiOnline === null && 'Checking API…'}
            {apiOnline === true && modelInfo && `Model online · ${modelInfo.best_model}`}
            {apiOnline === false && 'API offline — start the FastAPI backend'}
          </div>
        </div>
      </header>

      <main className="app__main">
        <section className="app__intro">
          <h2>Estimate a phone's price tier from its specs</h2>
          <p>
            Adjust the 20 hardware specifications below — RAM, battery, display, camera, and
            connectivity — and the trained classifier will estimate which of four price
            tiers the device falls into.
          </p>
        </section>

        <div className="app__grid">
          <SpecForm specs={specs} onChange={handleChange} onSubmit={handleSubmit} loading={loading} />
          <aside className="app__sidebar">
            <ResultPanel result={result} error={error} loading={loading} />
          </aside>
        </div>
      </main>

      <footer className="app__footer">
        <p>
          Trained on a 2,000-device dataset modeled after the Kaggle "Mobile Price Classification"
          challenge · FastAPI backend · React frontend
        </p>
      </footer>

      {activeModal === 'metrics' && (
        <Modal title="Selected Model" onClose={() => setActiveModal(null)}>
          <ModelMetrics modelInfo={modelInfo} />
        </Modal>
      )}

      {activeModal === 'comparison' && (
        <Modal title="Model Performance Comparison" onClose={() => setActiveModal(null)}>
          <ModelComparison modelInfo={modelInfo} />
        </Modal>
      )}
    </div>
  )
}