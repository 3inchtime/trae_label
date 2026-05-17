<template>
  <div class="json-tool">
    <div class="page-header">
      <div class="page-icon">
        <Icon name="json" :size="28" />
      </div>
      <div class="page-title">
        <h1>JSON 格式化工具</h1>
        <p>验证JSON格式正确性，支持格式化、压缩和示例加载</p>
      </div>
    </div>
    
    <div class="card">
      <div class="card-header">
        <h2>输入JSON</h2>
      </div>
      <textarea
        v-model="jsonInput"
        placeholder="在此粘贴或输入JSON字符串..."
        class="json-textarea"
        rows="12"
      ></textarea>
      <div class="button-group">
        <button @click="handleValidate" class="btn-secondary">
          <Icon name="search" :size="18" />
          <span>验证</span>
        </button>
        <button @click="handleFormat" class="btn-primary">
          <Icon name="star" :size="18" />
          <span>格式化</span>
        </button>
        <button @click="handleMinify" class="btn-warning">
          <Icon name="box" :size="18" />
          <span>压缩</span>
        </button>
        <button @click="clearAll" class="btn-error">
          <Icon name="trash" :size="18" />
          <span>清空</span>
        </button>
      </div>
    </div>

    <div v-if="validationResult !== null" class="card">
      <div class="card-header">
        <h2>验证结果</h2>
      </div>
      <div :class="validationResult.valid ? 'result-valid' : 'result-error'">
        <Icon :name="validationResult.valid ? 'check' : 'error'" :size="20" />
        <span>{{ validationResult.valid ? 'JSON 格式正确' : validationResult.error }}</span>
      </div>
    </div>

    <div v-if="formattedJson" class="card">
      <div class="card-header">
        <h2>格式化结果</h2>
        <button @click="copyToClipboard(formattedJson)" class="btn-secondary btn-sm">
          <Icon name="copy" :size="16" />
          <span>复制</span>
        </button>
      </div>
      <pre class="json-output">{{ formattedJson }}</pre>
    </div>

    <div v-if="minifiedJson" class="card">
      <div class="card-header">
        <h2>压缩结果</h2>
        <button @click="copyToClipboard(minifiedJson)" class="btn-secondary btn-sm">
          <Icon name="copy" :size="16" />
          <span>复制</span>
        </button>
      </div>
      <pre class="json-output minified">{{ minifiedJson }}</pre>
    </div>

    <div v-if="successMessage" class="alert alert-success">
      <Icon name="check" :size="20" />
      <span>{{ successMessage }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { formatJson, validateJson } from '../api'
import Icon from '../components/Icon.vue'

const jsonInput = ref('')
const formattedJson = ref('')
const minifiedJson = ref('')
const validationResult = ref(null)
const successMessage = ref('')

const handleValidate = async () => {
  if (!jsonInput.value.trim()) {
    validationResult.value = { valid: false, error: '请输入JSON字符串' }
    return
  }
  try {
    const response = await validateJson({ json_str: jsonInput.value })
    validationResult.value = response.data
    if (!response.data.valid) {
      formattedJson.value = ''
      minifiedJson.value = ''
    }
  } catch (err) {
    validationResult.value = { valid: false, error: '验证失败' }
  }
}

const handleFormat = async () => {
  if (!jsonInput.value.trim()) {
    validationResult.value = { valid: false, error: '请输入JSON字符串' }
    return
  }
  try {
    const response = await formatJson({ json_str: jsonInput.value, indent: 2 })
    validationResult.value = response.data
    if (response.data.valid) {
      formattedJson.value = response.data.formatted
      minifiedJson.value = response.data.minified
    } else {
      formattedJson.value = ''
      minifiedJson.value = ''
    }
  } catch (err) {
    validationResult.value = { valid: false, error: '格式化失败' }
  }
}

const handleMinify = async () => {
  if (!jsonInput.value.trim()) {
    validationResult.value = { valid: false, error: '请输入JSON字符串' }
    return
  }
  try {
    const response = await formatJson({ json_str: jsonInput.value, indent: 0 })
    validationResult.value = response.data
    if (response.data.valid) {
      minifiedJson.value = response.data.minified
      formattedJson.value = response.data.formatted
    } else {
      formattedJson.value = ''
      minifiedJson.value = ''
    }
  } catch (err) {
    validationResult.value = { valid: false, error: '压缩失败' }
  }
}

const clearAll = () => {
  jsonInput.value = ''
  formattedJson.value = ''
  minifiedJson.value = ''
  validationResult.value = null
}

const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text).then(() => {
    successMessage.value = '已复制到剪贴板'
    setTimeout(() => successMessage.value = '', 2000)
  })
}
</script>

<style scoped>
.json-tool {
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
  background: rgba(99, 102, 241, 0.1);
  color: var(--accent-secondary);
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
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.card-header h2 {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.btn-sm {
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  gap: 0.375rem;
}

.json-textarea {
  width: 100%;
  padding: 1rem;
  border: 2px solid var(--border-light);
  border-radius: var(--radius-md);
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 0.9rem;
  resize: vertical;
  transition: all var(--transition-normal);
  background: var(--bg-secondary);
  color: var(--text-primary);
  min-height: 200px;
}

.json-textarea::placeholder {
  color: var(--text-tertiary);
}

.json-textarea:focus {
  outline: none;
  border-color: var(--accent-secondary);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.button-group {
  display: flex;
  gap: 0.75rem;
  margin-top: 1rem;
  flex-wrap: wrap;
}

.result-valid,
.result-error {
  padding: 1rem;
  border-radius: var(--radius-md);
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.result-valid {
  background: rgba(16, 185, 129, 0.1);
  color: var(--accent-success);
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.result-error {
  background: rgba(239, 68, 68, 0.1);
  color: var(--accent-error);
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.json-output {
  background: var(--bg-tertiary);
  padding: 1rem;
  border-radius: var(--radius-md);
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 0.9rem;
  white-space: pre-wrap;
  word-break: break-all;
  max-height: 400px;
  overflow-y: auto;
  margin: 0;
  color: var(--text-primary);
}

.json-output.minified {
  color: var(--accent-error);
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

.alert-success {
  background: rgba(16, 185, 129, 0.1);
  color: var(--accent-success);
  border: 1px solid rgba(16, 185, 129, 0.2);
}

@media (max-width: 640px) {
  .button-group {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }
}
</style>
