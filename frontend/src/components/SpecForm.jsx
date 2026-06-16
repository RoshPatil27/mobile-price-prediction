import { SECTIONS } from '../specConfig'

function Slider({ field, value, onChange }) {
  return (
    <label className="field">
      <div className="field__head">
        <span className="field__label">{field.label}</span>
        <span className="field__value">
          {value}
          {field.unit ? <span className="field__unit"> {field.unit}</span> : null}
        </span>
      </div>
      <input
        type="range"
        min={field.min}
        max={field.max}
        step={field.step}
        value={value}
        onChange={(e) => onChange(field.key, parseFloat(e.target.value))}
      />
    </label>
  )
}

function Toggle({ field, value, onChange }) {
  return (
    <label className="toggle">
      <span className="toggle__label">{field.label}</span>
      <button
        type="button"
        className={`toggle__switch ${value ? 'is-on' : ''}`}
        role="switch"
        aria-checked={value === 1}
        onClick={() => onChange(field.key, value ? 0 : 1)}
      >
        <span className="toggle__knob" />
      </button>
    </label>
  )
}

export default function SpecForm({ specs, onChange, onSubmit, loading }) {
  return (
    <form
      className="spec-form"
      onSubmit={(e) => {
        e.preventDefault()
        onSubmit()
      }}
    >
      {SECTIONS.map((section) => (
        <fieldset className="spec-section" key={section.title}>
          <legend>
            <span className="spec-section__title">{section.title}</span>
            <span className="spec-section__desc">{section.description}</span>
          </legend>

          <div className="spec-section__grid">
            {section.fields.map((field) =>
              field.type === 'toggle' ? (
                <Toggle key={field.key} field={field} value={specs[field.key]} onChange={onChange} />
              ) : (
                <Slider key={field.key} field={field} value={specs[field.key]} onChange={onChange} />
              )
            )}
          </div>
        </fieldset>
      ))}

      <button type="submit" className="predict-btn" disabled={loading}>
        {loading ? 'Analyzing…' : 'Run Prediction'}
      </button>
    </form>
  )
}
