<template>
  <div class="url-tool">
    <div class="page-header">
      <div class="page-icon">
        <Icon name="link" :size="28" />
      </div>
      <div class="page-title">
        <h1>URL 编码解码</h1>
        <p>对URL或文本进行编码和解码，支持自定义安全字符</p>
      </div>
    </div>
    
    <div class="card">
      <div class="card-header">
        <h2>URL 编码</h2>
      </div>
      <textarea
        v-model="encodeInput"
        placeholder="输入要编码的URL或文本"
        class="input-field textarea"
        rows="4"
      ></textarea>
      <div class="options">
        <label class="input-label">
          <span>安全字符（不编码）</span>
          <input
            v-model="safeChars"
            type="text"
            placeholder="默认: /?=&"
            class="input-field"
          />
        </label>
      </div>
      <button @click="encodeUrl" class="btn-primary w-full">编码</button>
      <div v-if="encodeResult" class="result-box">
        <span class="result-label">编码结果</span>
        <div class="result-display">
          <span class="result-text">{{ encodeResult }}</span>
          <button @click="copyToClipboard(encodeResult)" class="copy-btn" title="复制">
            <Icon name="copy" :size="18" />
          </button>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h2>URL 解码</h2>
      </div>
      <textarea
        v-model="decodeInput"
        placeholder="输入要解码的URL或文本"
        class="input-field textarea"
        rows="4"
      ></textarea>
      <button @click="decodeUrl" class="btn-primary w-full">解码</button>
      <div v-if="decodeResult" class="result-box">
        <span class="result-label">解码结果</span>
        <div class="result-display">
          <span class="result-text">{{ decodeResult }}</span>
          <button @click="copyToClipboard(decodeResult)" class="copy-btn" title="复制">
            <Icon name="copy" :size="18" />
          </button>
        </div>
      </div>
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
import { urlEncode, urlDecode } from '../api'
import Icon from '../components/Icon.vue'

const encodeInput = ref('')
const safeChars = ref('/?=&')
const encodeResult = ref('')
const decodeInput = ref('')
const decodeResult = ref('')
const error = ref('')
const successMessage = ref('')

const encodeUrl = async () => {
  if (!encodeInput.value.trim()) {
    showError('请输入要编码的URL或文本')
    return
  }
  try {
    const response = await urlEncode({
      url: encodeInput.value,
      safe: safeChars.value
    })
    encodeResult.value = response.data.encoded
    decodeResult.value = ''
  } catch (err) {
    showError(err.response?.data?.detail || '编码失败')
  }
}

const decodeUrl = async () => {
  if (!decodeInput.value.trim()) {
    showError('请输入要解码的URL或文本')
    return
  }
  try {
    const response = await urlDecode({
      url: decodeInput.value
    })
    decodeResult.value = response.data.decoded
    encodeResult.value = ''
  } catch (err) {
    showError(err.response?.data?.detail || '解码失败')
  }
}

const copyToClipboard = (text) => {
  navigator.clipboard.writeText(String(text)).then(() => {
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
.url-tool {
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
  background: rgba(16, 185, 129, 0.1);
  color: var(--accent-success);
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

.input-field {
  width: 100%;
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
  border-color: var(--accent-success);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.textarea {
  resize: vertical;
  min-height: 100px;
}

.options {
  margin: 1rem 0;
}

.input-label {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.input-label input {
  margin-top: 0.25rem;
}

.w-full {
  width: 100%;
}

.result-box {
  margin-top: 1rem;
  padding: 1rem;
  border-radius: var(--radius-md);
  background: var(--bg-tertiary);
}

.result-label {
  display: block;
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
}

.result-display {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}

.result-text {
  flex: 1;
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 1rem;
  font-weight: 500;
  color: var(--accent-success);
  word-break: break-all;
  white-space: pre-wrap;
}

.copy-btn {
  padding: 0.5rem;
  background: var(--bg-tertiary);
  border: none;
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.copy-btn:hover {
  background: var(--border-medium);
  color: var(--text-primary);
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


</style>
