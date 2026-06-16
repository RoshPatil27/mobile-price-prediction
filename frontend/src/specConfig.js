// Field definitions for every spec the model expects.
// `type: 'range'` renders a slider, `type: 'toggle'` renders a switch.

export const DEFAULT_SPECS = {
  battery_power: 1500,
  blue: 1,
  clock_speed: 2.2,
  dual_sim: 1,
  fc: 5,
  four_g: 1,
  int_memory: 32,
  m_dep: 0.5,
  mobile_wt: 150,
  n_cores: 4,
  pc: 10,
  px_height: 800,
  px_width: 1200,
  ram: 2048,
  sc_h: 13,
  sc_w: 7,
  talk_time: 10,
  three_g: 1,
  touch_screen: 1,
  wifi: 1,
}

export const SECTIONS = [
  {
    title: '01 — Power & Performance',
    description: 'The specs that drive the strongest signal in the model.',
    fields: [
      { key: 'ram', label: 'RAM', unit: 'MB', type: 'range', min: 256, max: 4000, step: 16 },
      { key: 'battery_power', label: 'Battery capacity', unit: 'mAh', type: 'range', min: 500, max: 2000, step: 10 },
      { key: 'clock_speed', label: 'Clock speed', unit: 'GHz', type: 'range', min: 0.5, max: 3.0, step: 0.1 },
      { key: 'n_cores', label: 'CPU cores', unit: '', type: 'range', min: 1, max: 8, step: 1 },
      { key: 'int_memory', label: 'Internal storage', unit: 'GB', type: 'range', min: 2, max: 64, step: 1 },
    ],
  },
  {
    title: '02 — Display',
    description: 'Screen resolution, size, and physical build.',
    fields: [
      { key: 'px_width', label: 'Resolution width', unit: 'px', type: 'range', min: 500, max: 1998, step: 1 },
      { key: 'px_height', label: 'Resolution height', unit: 'px', type: 'range', min: 0, max: 1960, step: 1 },
      { key: 'sc_w', label: 'Screen width', unit: 'cm', type: 'range', min: 0, max: 18, step: 1 },
      { key: 'sc_h', label: 'Screen height', unit: 'cm', type: 'range', min: 5, max: 19, step: 1 },
      { key: 'm_dep', label: 'Depth / thickness', unit: 'cm', type: 'range', min: 0.1, max: 1.0, step: 0.1 },
      { key: 'mobile_wt', label: 'Weight', unit: 'g', type: 'range', min: 80, max: 200, step: 1 },
      { key: 'touch_screen', label: 'Touch screen', type: 'toggle' },
    ],
  },
  {
    title: '03 — Cameras',
    description: 'Front and rear camera resolution.',
    fields: [
      { key: 'pc', label: 'Primary camera', unit: 'MP', type: 'range', min: 0, max: 20, step: 1 },
      { key: 'fc', label: 'Front camera', unit: 'MP', type: 'range', min: 0, max: 20, step: 1 },
    ],
  },
  {
    title: '04 — Connectivity & Battery Life',
    description: 'Network capability and how long the device lasts.',
    fields: [
      { key: 'talk_time', label: 'Talk time', unit: 'hrs', type: 'range', min: 2, max: 20, step: 1 },
      { key: 'three_g', label: '3G', type: 'toggle' },
      { key: 'four_g', label: '4G', type: 'toggle' },
      { key: 'wifi', label: 'WiFi', type: 'toggle' },
      { key: 'blue', label: 'Bluetooth', type: 'toggle' },
      { key: 'dual_sim', label: 'Dual SIM', type: 'toggle' },
    ],
  },
]

export const PRICE_TIERS = [
  { value: 0, label: 'Low Cost', color: '#34d399', short: 'Budget' },
  { value: 1, label: 'Medium Cost', color: '#60a5fa', short: 'Mid-range' },
  { value: 2, label: 'High Cost', color: '#fbbf24', short: 'Premium' },
  { value: 3, label: 'Very High Cost', color: '#f472b6', short: 'Flagship' },
]
