<template>
  <div class="weight-converter">
    <div class="page-header">
      <div class="page-icon">
        <Icon name="box" :size="28" />
      </div>
      <div class="page-title">
        <h1>重量单位换算</h1>
        <p>支持多种常用重量单位之间的相互转换</p>
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
            @keyup.enter="convertWeight"
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
        <button @click="convertWeight" class="btn-primary">转换</button>
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
        <li><strong>mg</strong> - 毫克，1克 = 1000毫克</li>
        <li><strong>g</strong> - 克，国际标准单位</li>
        <li><strong>kg</strong> - 千克，1千克 = 1000克</li>
        <li><strong>t</strong> - 吨，1吨 = 1000千克</li>
        <li><strong>oz</strong> - 盎司，1盎司 ≈ 28.35克</li>
        <li><strong>lb</strong> - 磅，1磅 ≈ 453.59克</li>
        <li><strong>斤</strong> - 市斤，1斤 = 500克</li>
        <li><strong>两</strong> - 市两，1两 = 50克</li>
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
import { convertWeight as apiConvertWeight } from '../api'
import Icon from '../components/Icon.vue'

const inputValue = ref(1)
const fromUnit = ref('kg')
const toUnit = ref('jin')
const result = ref('')
const error = ref('')
const successMessage = ref('')

const unitOptions = [
  { value: 'mg', label: '毫克 (mg)' },
  { value: 'g', label: '克 (g)' },
  { value: 'kg', label: '千克 (kg)' },
  { value: 't', label: '吨 (t)' },
  { value: 'oz', label: '盎司 (oz)' },
  { value: 'lb', label: '磅 (lb)' },
  { value: 'jin', label: '斤 (jin)' },
  { value: 'liang', label: '两 (liang)' }
]

const quickConversions = [
  { label: '1 千克 = 2 斤', value: 1, from: 'kg', to: 'jin' },
  { label: '1 斤 = 500 克', value: 1, from: 'jin', to: 'g' },
  { label: '1 磅 = 453.59 克', value: 1, from: 'lb', to: 'g' },
  { label: '1 盎司 = 28.35 克', value: 1, from: 'oz', to: 'g' },
  { label: '1 吨 = 1000 千克', value: 1, from: 't', to: 'kg' },
  { label: '1 斤 = 10 两', value: 1, from: 'jin', to: 'liang' }
]

const convertWeight = async () => {
  if (inputValue.value === null || inputValue.value === '' || isNaN(inputValue.value)) {
    showError('请输入有效的数值')
    return
  }
  try {
    const response = await apiConvertWeight({
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
  convertWeight()
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
.weight-converter {
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
  background: rgba(245, 158, 11, 0.1);
  color: var(--accent-warning);
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
  border-color: var(--accent-warning);
  box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.1);
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
  border-color: var(--accent-warning);
  box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.1);
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
  background: rgba(245, 158, 11, 0.1);
  border-color: var(--accent-warning);
  color: var(--accent-warning);
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