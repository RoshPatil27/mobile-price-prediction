const API_BASE = import.meta.env.VITE_API_BASE_URL || 'https://mobile-price-prediction-wnv1.onrender.com'

export async function predictPriceRange(specs) {
  const res = await fetch(`${API_BASE}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(specs),
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || `Request failed with status ${res.status}`)
  }

  return res.json()
}

export async function fetchModelInfo() {
  const res = await fetch(`${API_BASE}/model-info`)
  if (!res.ok) throw new Error('Failed to fetch model info')
  return res.json()
}
