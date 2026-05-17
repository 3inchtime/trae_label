<template>
  <div class="length-converter">
    <div class="page-header">
      <div class="page-icon">
        <Icon name="ruler" :size="28" />
      </div>
      <div class="page-title">
        <h1>长度单位换算</h1>
        <p>支持多种常用长度单位之间的相互转换</p>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h2>输入数值</h2>
      </div>
      <div class="input-group">
        <div class="input-row">
          <input
            v-model.number="inputValue"
            type="number"
            step="0.001"
            placeholder="请输入数值"
            class="input-field"
            @keyup.enter="convertLength"
          />
          <select v-model="fromUnit" class="select-field">
            <option v-for="unit in unitOptions" :key="unit.value" :value="unit.value">
              {{ unit.label }}
            </option>
          </select>
        </div>
        <div class="swap-row">
          <button @click="swapUnits" class="swap-btn" title="交换单位">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="7 17 2 12 7 7"></polyline>
              <polyline points="17 7 22 12 17 17"></polyline>
            </svg>
          </button>
        </div>
        <div class="input-row">
          <input
            :value="result"
            type="text"
            placeholder="转换结果"
            class="input-field result-field"
            readonly
          />
          <select v-model="toUnit" class="select-field">
            <option v-for="unit in unitOptions" :key="unit.value" :value="unit.value">
              {{ unit.label }}
            </option>
          </select>
        </div>
      </div>
      <div class="action-buttons">
        <button @click="convertLength" class="btn-primary">转换</button>
        <button @click="copyResult" class="btn-secondary" :disabled="!result">
          <Icon name="copy" :size="18" />
          复制结果
        </button>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h2>常用转换</h2>
      </div>
      <div class="quick-conversions">
        <button
          v-for="conv in quickConversions"
          :key="conv.label"
          @click="setQuickConversion(conv)"
          class="conv-btn"
        >
          {{ conv.label }}
        </button>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h2>单位说明</h2>
      </div>
      <ul class="unit-list">
        <li><strong>mm</strong> - 毫米，1米 = 1000毫米</li>
        <li><strong>cm</strong> - 厘米，1米 = 100厘米</li>
        <li><strong>dm</strong> - 分米，1米 = 10分米</li>
        <li><strong>m</strong> - 米，国际标准单位</li>
        <li><strong>km</strong> - 千米，1千米 = 1000米</li>
        <li><strong>in</strong> - 英寸，1英寸 = 2.54厘米</li>
        <li><strong>ft</strong> - 英尺，1英尺 = 12英寸</li>
        <li><strong>yd</strong> - 码，1码 = 3英尺</li>
        <li><strong>mi</strong> - 英里，1英里 ≈ 1.609千米</li>
        <li><strong>里</strong> - 市里，1里 = 500米</li>
        <li><strong>丈</strong> - 市丈，1丈 ≈ 3.33米</li>
        <li><strong>尺</strong> - 市尺，1尺 ≈ 0.333米</li>
        <li><strong>寸</strong> - 市寸，1寸 ≈ 3.33厘米</li>
      </ul>
    </div>

    <div v-if="error" class="alert alert-error">
      <Icon name="error" :size="20" />
      <span>{{ error }}</span>
    </div>
    <div v-if="successMessage" class="alert alert-success">
      <Icon name="check" :size="20" />
      <span>{{ successMessage }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { convertLength as apiConvertLength } from '../api'
import Icon from '../components/Icon.vue'

const inputValue = ref(1)
const fromUnit = ref('m')
const toUnit = ref('cm')
const result = ref('')
const error = ref('')
const successMessage = ref('')

const unitOptions = [
  { value: 'mm', label: '毫米 (mm)' },
  { value: 'cm', label: '厘米 (cm)' },
  { value: 'dm', label: '分米 (dm)' },
  { value: 'm', label: '米 (m)' },
  { value: 'km', label: '千米 (km)' },
  { value: 'in', label: '英寸 (in)' },
  { value: 'ft', label: '英尺 (ft)' },
  { value: 'yd', label: '码 (yd)' },
  { value: 'mi', label: '英里 (mi)' },
  { value: 'li', label: '里 (li)' },
  { value: 'zhang', label: '丈 (zhang)' },
  { value: 'chi', label: '尺 (chi)' },
  { value: 'cun', label: '寸 (cun)' }
]

const quickConversions = [
  { label: '1 米 = 100 厘米', value: 1, from: 'm', to: 'cm' },
  { label: '1 千米 = 1000 米', value: 1, from: 'km', to: 'm' },
  { label: '1 英寸 = 2.54 厘米', value: 1, from: 'in', to: 'cm' },
  { label: '1 英尺 = 30.48 厘米', value: 1, from: 'ft', to: 'cm' },
  { label: '1 英里 ≈ 1.609 千米', value: 1, from: 'mi', to: 'km' },
  { label: '1 里 = 500 米', value: 1, from: 'li', to: 'm' },
  { label: '3 尺 = 1 米', value: 3, from: 'chi', to: 'm' }
]

const convertLength = async () => {
  if (inputValue.value === null || inputValue.value === '' || isNaN(inputValue.value)) {
    showError('请输入有效的数值')
    return
  }
  try {
    const response = await apiConvertLength({
      value: inputValue.value,
      from_unit: fromUnit.value,
      to_unit: toUnit.value
    })
    result.value = response.data.result
    clearError()
  } catch (err) {
    showError('转换失败，请重试')
  }
}

const swapUnits = () => {
  const temp = fromUnit.value
  fromUnit.value = toUnit.value
  toUnit.value = temp
  if (result.value) {
    inputValue.value = parseFloat(result.value)
    result.value = ''
  }
}

const setQuickConversion = (conv) => {
  inputValue.value = conv.value
  fromUnit.value = conv.from
  toUnit.value = conv.to
  convertLength()
}

const copyResult = () => {
  if (result.value) {
    navigator.clipboard.writeText(result.value.toString()).then(() => {
      showSuccess('已复制到剪贴板')
    })
  }
}

const showError = (msg) => {
  error.value = msg
  setTimeout(() => error.value = '', 3000)
}

const clearError = () => {
  error.value = ''
}

const showSuccess = (msg) => {
  successMessage.value = msg
  setTimeout(() => successMessage.value = '', 2000)
}
</script>

<style scoped>
.length-converter {
  width: 100%;
  max-width: 800px;
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
  background: rgba(251, 146, 60, 0.1);
  color: #fb923c;
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
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  margin-bottom: 1.25rem;
  transition: all var(--transition-normal);
}

.card:hover {
  border-color: var(--border-medium);
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

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
}

.input-row {
  display: flex;
  gap: 0.75rem;
}

.swap-row {
  display: flex;
  justify-content: center;
}

.swap-btn {
  padding: 0.5rem;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  justify-content: center;
}

.swap-btn:hover {
  background: var(--accent-primary);
  color: white;
  border-color: var(--accent-primary);
}

.input-field {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 2px solid var(--border-light);
  border-radius: var(--radius-md);
  font-size: 1rem;
  transition: all var(--transition-normal);
  background: var(--bg-secondary);
  color: var(--text-primary);
  font-family: inherit;
}

.input-field::placeholder {
  color: var(--text-tertiary);
}

.input-field:focus {
  outline: none;
  border-color: #fb923c;
  box-shadow: 0 0 0 3px rgba(251, 146, 60, 0.1);
}

.input-field.result-field {
  background: var(--bg-tertiary);
  font-weight: 600;
  color: var(--accent-primary);
}

.select-field {
  padding: 0.75rem 1rem;
  border: 2px solid var(--border-light);
  border-radius: var(--radius-md);
  font-size: 1rem;
  transition: all var(--transition-normal);
  background: var(--bg-secondary);
  color: var(--text-primary);
  font-family: inherit;
  cursor: pointer;
  min-width: 140px;
}

.select-field:focus {
  outline: none;
  border-color: #fb923c;
  box-shadow: 0 0 0 3px rgba(251, 146, 60, 0.1);
}

.action-buttons {
  display: flex;
  gap: 0.75rem;
}

.btn-primary {
  flex: 1;
  padding: 0.75rem 1.5rem;
  background: var(--accent-primary);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-primary:hover {
  background: var(--accent-primary-dark);
  transform: translateY(-1px);
}

.btn-secondary {
  padding: 0.75rem 1.5rem;
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-secondary:hover:not(:disabled) {
  background: var(--border-light);
  border-color: var(--border-medium);
}

.btn-secondary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quick-conversions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 0.75rem;
}

.conv-btn {
  padding: 0.75rem 1rem;
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  font-size: 0.9rem;
  cursor: pointer;
  transition: all var(--transition-fast);
  text-align: left;
}

.conv-btn:hover {
  background: rgba(251, 146, 60, 0.1);
  border-color: #fb923c;
  color: #fb923c;
}

.unit-list {
  margin: 0;
  padding-left: 1.5rem;
  color: var(--text-secondary);
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
}

.unit-list li {
  line-height: 1.6;
}

.alert {
  padding: 1rem;
  border-radius: var(--radius-md);
  margin-top: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 500;
}

.alert-error {
  background: rgba(239, 68, 68, 0.1);
  color: var(--accent-error);
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.alert-success {
  background: rgba(16, 185, 129, 0.1);
  color: var(--accent-success);
  border: 1px solid rgba(16, 185, 129, 0.2);
}

@media (max-width: 640px) {
  .input-row {
    flex-direction: column;
  }
  
  .select-field {
    min-width: auto;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .unit-list {
    grid-template-columns: 1fr;
  }
}
</style>
