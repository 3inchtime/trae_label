<template>
  <div class="number-to-chinese">
    <div class="page-header">
      <div class="page-icon">
        <Icon name="money" :size="28" />
      </div>
      <div class="page-title">
        <h1>数字转中文大写</h1>
        <p>将数字金额转换为标准中文大写金额，支持小数和负数</p>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h2>输入金额</h2>
      </div>
      <div class="input-row">
        <input
          v-model.number="numberInput"
          type="number"
          step="0.01"
          placeholder="请输入数字金额"
          class="input-field"
          @keyup.enter="convertNumber"
        />
        <button @click="convertNumber" class="btn-primary">转换</button>
      </div>
    </div>

    <div v-if="result" class="card">
      <div class="card-header">
        <h2>转换结果</h2>
      </div>
      <div class="result-item">
        <span class="result-label">输入金额</span>
        <span class="result-value">¥ {{ result.number.toFixed(2) }}</span>
      </div>
      <div class="result-item main-result">
        <span class="result-label">中文大写</span>
        <span class="chinese-text">{{ result.chinese }}</span>
        <button @click="copyToClipboard(result.chinese)" class="copy-btn" title="复制">
          <Icon name="copy" :size="18" />
        </button>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h2>快捷示例</h2>
      </div>
      <div class="example-buttons">
        <button @click="setExample(1234.56)" class="btn-secondary">1234.56</button>
        <button @click="setExample(10000)" class="btn-secondary">10000</button>
        <button @click="setExample(98765432.1)" class="btn-secondary">98765432.1</button>
        <button @click="setExample(0)" class="btn-secondary">0</button>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h2>转换规则</h2>
      </div>
      <ul class="rules-list">
        <li>支持整数和小数（最多两位小数）</li>
        <li>使用标准中文大写金额格式</li>
        <li>支持负数转换</li>
        <li>单位包括：元、角、分、拾、佰、仟、万、亿</li>
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
import { convertNumberToChinese } from '../api'
import Icon from '../components/Icon.vue'

const numberInput = ref(null)
const result = ref(null)
const error = ref('')
const successMessage = ref('')

const convertNumber = async () => {
  if (numberInput.value === null || numberInput.value === '') {
    showError('请输入数字金额')
    return
  }
  try {
    const response = await convertNumberToChinese({
      number: numberInput.value
    })
    result.value = response.data
  } catch (err) {
    showError('转换失败')
  }
}

const setExample = (num) => {
  numberInput.value = num
  convertNumber()
}

const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text).then(() => {
    showSuccess('已复制到剪贴板')
  })
}

const showError = (msg) => {
  error.value = msg
  setTimeout(() => error.value = '', 3000)
}

const showSuccess = (msg) => {
  successMessage.value = msg
  setTimeout(() => successMessage.value = '', 2000)
}
</script>

<style scoped>
.number-to-chinese {
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

.input-row {
  display: flex;
  gap: 0.75rem;
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

.result-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--border-light);
}

.result-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.result-item.main-result {
  padding: 1rem;
  background: var(--bg-tertiary);
  border-radius: var(--radius-md);
  margin-top: 0.5rem;
  border-bottom: none;
}

.result-label {
  font-weight: 500;
  min-width: 80px;
  color: var(--text-secondary);
}

.result-value {
  flex: 1;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  font-family: 'Monaco', 'Menlo', monospace;
}

.chinese-text {
  flex: 1;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--accent-warning);
  word-break: break-all;
}

.copy-btn {
  padding: 0.5rem;
  background: var(--bg-secondary);
  border: none;
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  justify-content: center;
}

.copy-btn:hover {
  background: var(--border-medium);
  color: var(--text-primary);
}

.example-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 0.75rem;
}

.rules-list {
  margin: 0;
  padding-left: 1.5rem;
  color: var(--text-secondary);
}

.rules-list li {
  margin-bottom: 0.5rem;
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
  
  .example-buttons {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
