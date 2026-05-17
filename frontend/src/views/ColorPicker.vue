<template>
  <div class="color-picker">
    <div class="page-header">
      <div class="page-icon">
        <Icon name="palette" :size="28" />
      </div>
      <div class="page-title">
        <h1>颜色选择器</h1>
        <p>可视化选择颜色，支持 HEX/RGB/HSL 格式转换</p>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h2>选择颜色</h2>
      </div>
      <div class="color-selection">
        <div class="color-preview" :style="{ backgroundColor: hexColor }"></div>
        <div class="color-inputs">
          <div class="input-group">
            <label>HEX</label>
            <input
              v-model="hexColor"
              type="text"
              maxlength="7"
              placeholder="#000000"
              class="input-field"
              @input="updateFromHex"
            />
          </div>
          <div class="rgb-inputs">
            <div class="input-group">
              <label>R</label>
              <input
                v-model.number="rgbColor.r"
                type="number"
                min="0"
                max="255"
                class="input-field small-input"
                @input="updateFromRgb"
              />
            </div>
            <div class="input-group">
              <label>G</label>
              <input
                v-model.number="rgbColor.g"
                type="number"
                min="0"
                max="255"
                class="input-field small-input"
                @input="updateFromRgb"
              />
            </div>
            <div class="input-group">
              <label>B</label>
              <input
                v-model.number="rgbColor.b"
                type="number"
                min="0"
                max="255"
                class="input-field small-input"
                @input="updateFromRgb"
              />
            </div>
          </div>
          <div class="hsl-inputs">
            <div class="input-group">
              <label>H</label>
              <input
                v-model.number="hslColor.h"
                type="number"
                min="0"
                max="360"
                class="input-field small-input"
                @input="updateFromHsl"
              />
            </div>
            <div class="input-group">
              <label>S</label>
              <input
                v-model.number="hslColor.s"
                type="number"
                min="0"
                max="100"
                class="input-field small-input"
                @input="updateFromHsl"
              />
            </div>
            <div class="input-group">
              <label>L</label>
              <input
                v-model.number="hslColor.l"
                type="number"
                min="0"
                max="100"
                class="input-field small-input"
                @input="updateFromHsl"
              />
            </div>
          </div>
        </div>
      </div>
      <div class="color-sliders">
        <div class="slider-group">
          <label>红 ({{ rgbColor.r }})</label>
          <input
            v-model.number="rgbColor.r"
            type="range"
            min="0"
            max="255"
            class="color-slider slider-red"
            @input="updateFromRgb"
          />
        </div>
        <div class="slider-group">
          <label>绿 ({{ rgbColor.g }})</label>
          <input
            v-model.number="rgbColor.g"
            type="range"
            min="0"
            max="255"
            class="color-slider slider-green"
            @input="updateFromRgb"
          />
        </div>
        <div class="slider-group">
          <label>蓝 ({{ rgbColor.b }})</label>
          <input
            v-model.number="rgbColor.b"
            type="range"
            min="0"
            max="255"
            class="color-slider slider-blue"
            @input="updateFromRgb"
          />
        </div>
      </div>
      <div class="native-picker">
        <input
          ref="colorPickerRef"
          type="color"
          :value="hexColor"
          @input="updateFromNativePicker"
          class="native-color-input"
        />
        <span>点击左侧方块选择颜色</span>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h2>常用颜色</h2>
      </div>
      <div class="preset-colors">
        <button
          v-for="color in presetColors"
          :key="color.hex"
          class="color-btn"
          :style="{ backgroundColor: color.hex }"
          :title="color.name"
          @click="selectPresetColor(color.hex)"
        ></button>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h2>配色方案</h2>
      </div>
      <div class="color-schemes">
        <div class="scheme">
          <h3>互补色</h3>
          <div class="scheme-colors">
            <div class="scheme-color" :style="{ backgroundColor: hexColor }" @click="copyToClipboard(hexColor)"></div>
            <div class="scheme-color" :style="{ backgroundColor: complementaryColor }" @click="copyToClipboard(complementaryColor)"></div>
          </div>
        </div>
        <div class="scheme">
          <h3>类似色</h3>
          <div class="scheme-colors">
            <div class="scheme-color" :style="{ backgroundColor: analogousColors[0] }" @click="copyToClipboard(analogousColors[0])"></div>
            <div class="scheme-color" :style="{ backgroundColor: hexColor }" @click="copyToClipboard(hexColor)"></div>
            <div class="scheme-color" :style="{ backgroundColor: analogousColors[1] }" @click="copyToClipboard(analogousColors[1])"></div>
          </div>
        </div>
        <div class="scheme">
          <h3>三角色</h3>
          <div class="scheme-colors">
            <div class="scheme-color" :style="{ backgroundColor: triadicColors[0] }" @click="copyToClipboard(triadicColors[0])"></div>
            <div class="scheme-color" :style="{ backgroundColor: hexColor }" @click="copyToClipboard(hexColor)"></div>
            <div class="scheme-color" :style="{ backgroundColor: triadicColors[1] }" @click="copyToClipboard(triadicColors[1])"></div>
          </div>
        </div>
        <div class="scheme">
          <h3>单色方案</h3>
          <div class="scheme-colors">
            <div class="scheme-color" v-for="(color, index) in monochromaticColors" :key="index" :style="{ backgroundColor: color }" @click="copyToClipboard(color)"></div>
          </div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h2>对比度检查</h2>
      </div>
      <div class="contrast-check">
        <div class="contrast-preview" :style="{ backgroundColor: hexColor, color: contrastTextColor }">
          <span>示例文本</span>
        </div>
        <div class="contrast-info">
          <p><strong>对比度：</strong> {{ contrastRatio.toFixed(2) }}:1</p>
          <p class="contrast-level" :class="contrastLevelClass">
            {{ contrastLevelText }}
          </p>
        </div>
      </div>
    </div>

    <div class="action-buttons">
      <button @click="copyHex" class="btn-primary">
        <Icon name="copy" :size="18" />
        复制 HEX
      </button>
      <button @click="copyRgb" class="btn-secondary">
        <Icon name="copy" :size="18" />
        复制 RGB
      </button>
      <button @click="copyHsl" class="btn-secondary">
        <Icon name="copy" :size="18" />
        复制 HSL
      </button>
      <button @click="randomColor" class="btn-warning">
        <Icon name="refresh" :size="18" />
        随机颜色
      </button>
    </div>

    <div v-if="successMessage" class="alert alert-success">
      <Icon name="check" :size="20" />
      <span>{{ successMessage }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Icon from '../components/Icon.vue'

const hexColor = ref('#3b82f6')
const rgbColor = ref({ r: 59, g: 130, b: 246 })
const hslColor = ref({ h: 217, s: 91, l: 60 })
const successMessage = ref('')

const presetColors = [
  { name: '红色', hex: '#ef4444' },
  { name: '橙色', hex: '#f97316' },
  { name: '黄色', hex: '#eab308' },
  { name: '绿色', hex: '#22c55e' },
  { name: '青色', hex: '#06b6d4' },
  { name: '蓝色', hex: '#3b82f6' },
  { name: '紫色', hex: '#8b5cf6' },
  { name: '粉色', hex: '#ec4899' },
  { name: '黑色', hex: '#000000' },
  { name: '白色', hex: '#ffffff' },
  { name: '灰色', hex: '#6b7280' },
  { name: '深蓝', hex: '#1e3a8a' }
]

const complementaryColor = computed(() => {
  const h = (hslColor.value.h + 180) % 360
  return hslToHex(h, hslColor.value.s, hslColor.value.l)
})

const analogousColors = computed(() => {
  const h1 = (hslColor.value.h + 30) % 360
  const h2 = (hslColor.value.h - 30 + 360) % 360
  return [
    hslToHex(h1, hslColor.value.s, hslColor.value.l),
    hslToHex(h2, hslColor.value.s, hslColor.value.l)
  ]
})

const triadicColors = computed(() => {
  const h1 = (hslColor.value.h + 120) % 360
  const h2 = (hslColor.value.h + 240) % 360
  return [
    hslToHex(h1, hslColor.value.s, hslColor.value.l),
    hslToHex(h2, hslColor.value.s, hslColor.value.l)
  ]
})

const monochromaticColors = computed(() => {
  const colors = []
  const lValues = [20, 35, 50, 65, 80]
  lValues.forEach(l => {
    colors.push(hslToHex(hslColor.value.h, hslColor.value.s, l))
  })
  return colors
})

const luminance = computed(() => {
  const [r, g, b] = [rgbColor.value.r, rgbColor.value.g, rgbColor.value.b].map(c => {
    c = c / 255
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4)
  })
  return 0.2126 * r + 0.7152 * g + 0.0722 * b
})

const contrastRatio = computed(() => {
  const l1 = luminance.value
  const l2 = 1.0
  const lighter = Math.max(l1, l2)
  const darker = Math.min(l1, l2)
  return (lighter + 0.05) / (darker + 0.05)
})

const contrastTextColor = computed(() => {
  return luminance.value > 0.5 ? '#000000' : '#ffffff'
})

const contrastLevelClass = computed(() => {
  const ratio = contrastRatio.value
  if (ratio >= 7) return 'contrast-excellent'
  if (ratio >= 4.5) return 'contrast-good'
  if (ratio >= 3) return 'contrast-moderate'
  return 'contrast-poor'
})

const contrastLevelText = computed(() => {
  const ratio = contrastRatio.value
  if (ratio >= 7) return 'AAA 级 - 优秀对比度'
  if (ratio >= 4.5) return 'AA 级 - 良好对比度'
  if (ratio >= 3) return '一般对比度'
  return '对比度不足'
})

function hexToRgb(hex) {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : { r: 0, g: 0, b: 0 }
}

function rgbToHex(r, g, b) {
  return '#' + [r, g, b].map(x => {
    const hex = Math.round(Math.max(0, Math.min(255, x))).toString(16)
    return hex.length === 1 ? '0' + hex : hex
  }).join('')
}

function rgbToHsl(r, g, b) {
  r /= 255
  g /= 255
  b /= 255
  const max = Math.max(r, g, b)
  const min = Math.min(r, g, b)
  let h, s, l = (max + min) / 2

  if (max === min) {
    h = s = 0
  } else {
    const d = max - min
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min)
    switch (max) {
      case r: h = ((g - b) / d + (g < b ? 6 : 0)) / 6; break
      case g: h = ((b - r) / d + 2) / 6; break
      case b: h = ((r - g) / d + 4) / 6; break
    }
  }

  return {
    h: Math.round(h * 360),
    s: Math.round(s * 100),
    l: Math.round(l * 100)
  }
}

function hslToHex(h, s, l) {
  h /= 360
  s /= 100
  l /= 100
  let r, g, b

  if (s === 0) {
    r = g = b = l
  } else {
    const hue2rgb = (p, q, t) => {
      if (t < 0) t += 1
      if (t > 1) t -= 1
      if (t < 1/6) return p + (q - p) * 6 * t
      if (t < 1/2) return q
      if (t < 2/3) return p + (q - p) * (2/3 - t) * 6
      return p
    }
    const q = l < 0.5 ? l * (1 + s) : l + s - l * s
    const p = 2 * l - q
    r = hue2rgb(p, q, h + 1/3)
    g = hue2rgb(p, q, h)
    b = hue2rgb(p, q, h - 1/3)
  }

  return rgbToHex(r * 255, g * 255, b * 255)
}

function updateFromHex() {
  let hex = hexColor.value
  if (!hex.startsWith('#')) {
    hex = '#' + hex
  }
  if (/^#[0-9A-Fa-f]{6}$/.test(hex)) {
    const rgb = hexToRgb(hex)
    rgbColor.value = rgb
    hslColor.value = rgbToHsl(rgb.r, rgb.g, rgb.b)
  }
}

function updateFromRgb() {
  const rgb = rgbColor.value
  hexColor.value = rgbToHex(rgb.r, rgb.g, rgb.b)
  hslColor.value = rgbToHsl(rgb.r, rgb.g, rgb.b)
}

function updateFromHsl() {
  const hsl = hslColor.value
  hexColor.value = hslToHex(hsl.h, hsl.s, hsl.l)
  rgbColor.value = hexToRgb(hexColor.value)
}

function updateFromNativePicker(event) {
  hexColor.value = event.target.value
  updateFromHex()
}

function selectPresetColor(hex) {
  hexColor.value = hex
  updateFromHex()
}

function randomColor() {
  const r = Math.floor(Math.random() * 256)
  const g = Math.floor(Math.random() * 256)
  const b = Math.floor(Math.random() * 256)
  rgbColor.value = { r, g, b }
  updateFromRgb()
}

function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    showSuccess('已复制到剪贴板')
  })
}

function copyHex() {
  copyToClipboard(hexColor.value)
}

function copyRgb() {
  const rgb = rgbColor.value
  copyToClipboard(`rgb(${rgb.r}, ${rgb.g}, ${rgb.b})`)
}

function copyHsl() {
  const hsl = hslColor.value
  copyToClipboard(`hsl(${hsl.h}, ${hsl.s}%, ${hsl.l}%)`)
}

function showSuccess(msg) {
  successMessage.value = msg
  setTimeout(() => successMessage.value = '', 2000)
}
</script>

<style scoped>
.color-picker {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.page-icon {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-lg);
  background: rgba(139, 92, 246, 0.1);
  color: #8b5cf6;
  display: flex;
  align-items: center;
  justify-content: center;
}

.page-title h1 {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.page-title p {
  font-size: 0.95rem;
  color: var(--text-secondary);
  margin: 0;
}

.card {
  background: var(--glass-bg);
  backdrop-filter: var(--glass-backdrop);
  -webkit-backdrop-filter: var(--glass-backdrop);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-glass);
  padding: 1.5rem;
  margin-bottom: 1.25rem;
  transition: all var(--transition-normal);
  border: 1px solid var(--glass-border);
  position: relative;
  overflow: hidden;
}

.card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #8b5cf6, #06b6d4, #8b5cf6);
  background-size: 200% 100%;
  animation: shimmerBorder 3s linear infinite;
  opacity: 0;
  transition: opacity var(--transition-normal);
}

.card:hover::before {
  opacity: 1;
}

.card:hover {
  box-shadow: 0 12px 40px rgba(139, 92, 246, 0.2);
  transform: translateY(-4px);
  border-color: #8b5cf6;
}

.card-header {
  margin-bottom: 1rem;
}

.card-header h2 {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.color-selection {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.color-preview {
  width: 120px;
  height: 120px;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  flex-shrink: 0;
  border: 3px solid var(--border-light);
  transition: transform var(--transition-normal);
}

.color-preview:hover {
  transform: scale(1.05);
}

.color-inputs {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.input-group label {
  font-weight: 600;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.input-field {
  padding: 0.75rem 1rem;
  border: 2px solid var(--border-light);
  border-radius: var(--radius-md);
  font-size: 1rem;
  transition: all var(--transition-normal);
  background: var(--bg-secondary);
  color: var(--text-primary);
  font-family: inherit;
}

.input-field:focus {
  outline: none;
  border-color: #8b5cf6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

.small-input {
  width: 80px;
}

.rgb-inputs,
.hsl-inputs {
  display: flex;
  gap: 0.75rem;
}

.color-sliders {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.slider-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.slider-group label {
  font-weight: 600;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.color-slider {
  -webkit-appearance: none;
  appearance: none;
  height: 12px;
  border-radius: 6px;
  outline: none;
  cursor: pointer;
}

.slider-red {
  background: linear-gradient(to right, #000000, #ff0000);
}

.slider-green {
  background: linear-gradient(to right, #000000, #00ff00);
}

.slider-blue {
  background: linear-gradient(to right, #000000, #0000ff);
}

.color-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: white;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  border: 2px solid var(--border-medium);
  transition: transform var(--transition-fast);
}

.color-slider::-webkit-slider-thumb:hover {
  transform: scale(1.1);
}

.native-picker {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.native-color-input {
  width: 60px;
  height: 40px;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  padding: 0;
  background: none;
}

.native-color-input::-webkit-color-swatch-wrapper {
  padding: 0;
}

.native-color-input::-webkit-color-swatch {
  border: 2px solid var(--border-light);
  border-radius: var(--radius-md);
}

.preset-colors {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(50px, 1fr));
  gap: 0.75rem;
}

.color-btn {
  width: 50px;
  height: 50px;
  border-radius: var(--radius-md);
  border: 2px solid var(--border-light);
  cursor: pointer;
  transition: all var(--transition-fast);
  padding: 0;
}

.color-btn:hover {
  transform: scale(1.15);
  border-color: #8b5cf6;
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
}

.color-schemes {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.scheme {
  text-align: center;
}

.scheme h3 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 0.75rem;
}

.scheme-colors {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.scheme-color {
  width: 50px;
  height: 50px;
  border-radius: var(--radius-md);
  border: 2px solid var(--border-light);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.scheme-color:hover {
  transform: scale(1.15);
  border-color: #8b5cf6;
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
}

.contrast-check {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.contrast-preview {
  width: 200px;
  height: 80px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.125rem;
  border: 2px solid var(--border-light);
  flex-shrink: 0;
}

.contrast-info p {
  margin: 0.25rem 0;
  color: var(--text-secondary);
}

.contrast-level {
  font-weight: 600;
  padding: 0.25rem 0.75rem;
  border-radius: var(--radius-sm);
  display: inline-block;
  margin-top: 0.5rem !important;
}

.contrast-excellent {
  background: rgba(16, 185, 129, 0.1);
  color: var(--accent-success);
}

.contrast-good {
  background: rgba(59, 130, 246, 0.1);
  color: var(--accent-primary);
}

.contrast-moderate {
  background: rgba(245, 158, 11, 0.1);
  color: var(--accent-warning);
}

.contrast-poor {
  background: rgba(239, 68, 68, 0.1);
  color: var(--accent-error);
}

.action-buttons {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin-top: 1.5rem;
}

.btn-primary {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 100%);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #7c3aed 0%, #0891b2 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
}

.btn-secondary {
  padding: 0.75rem 1.5rem;
  background: var(--glass-bg);
  color: var(--text-primary);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-secondary:hover {
  background: rgba(139, 92, 246, 0.1);
  border-color: #8b5cf6;
  transform: translateY(-2px);
}

.btn-warning {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, var(--accent-warning) 0%, #d97706 100%);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-warning:hover {
  background: linear-gradient(135deg, var(--accent-warning-hover) 0%, var(--accent-warning) 100%);
  transform: translateY(-2px);
}

.alert {
  padding: 1rem;
  border-radius: var(--radius-md);
  margin-top: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 500;
  backdrop-filter: var(--glass-backdrop);
  -webkit-backdrop-filter: var(--glass-backdrop);
}

.alert-success {
  background: rgba(16, 185, 129, 0.1);
  color: var(--accent-success);
  border: 1px solid rgba(16, 185, 129, 0.25);
}

@keyframes shimmerBorder {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

@media (max-width: 768px) {
  .color-selection {
    flex-direction: column;
  }

  .color-preview {
    width: 100%;
    height: 100px;
  }

  .rgb-inputs,
  .hsl-inputs {
    flex-wrap: wrap;
  }

  .contrast-check {
    flex-direction: column;
  }

  .contrast-preview {
    width: 100%;
  }

  .action-buttons {
    flex-direction: column;
  }

  .action-buttons button {
    width: 100%;
  }
}
</style>
