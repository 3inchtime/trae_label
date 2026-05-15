<template>
  <div class="md5-tool">
    <div class="page-header">
      <div class="page-icon">
        <Icon name="lock" :size="28" />
      </div>
      <div class="page-title">
        <h1>MD5 加密工具</h1>
        <p>文本MD5哈希加密与对比验证，支持大小写输出</p>
      </div>
    </div>
    
    <div class="card">
      <div class="card-header">
        <h2>文本加密</h2>
      </div>
      <textarea
        v-model="encryptInput"
        placeholder="输入要加密的文本"
        class="input-field textarea"
        rows="4"
      ></textarea>
      <div class="options">
        <label class="checkbox-label">
          <input type="checkbox" v-model="uppercase" />
          <span>大写输出</span>
        </label>
      </div>
      <button @click="encryptText" class="btn-primary w-full">生成 MD5</button>
      <div v-if="encryptResult" class="result-box">
        <span class="result-label">MD5 哈希值</span>
        <div class="hash-display">
          <span class="hash-text">{{ encryptResult }}</span>
          <button @click="copyToClipboard(encryptResult)" class="copy-btn" title="复制">
            <Icon name="copy" :size="18" />
          </button>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h2>哈希对比</h2>
      </div>
      <div class="input-group">
        <input
          v-model="compareText"
          type="text"
          placeholder="输入原始文本"
          class="input-field"
        />
      </div>
      <div class="input-group">
        <input
          v-model="compareHash"
          type="text"
          placeholder="输入 MD5 哈希值"
          class="input-field"
        />
      </div>
      <button @click="compareHashFunc" class="btn-primary w-full">对比验证</button>
      <div v-if="compareResult !== null" class="result-box" :class="compareResult ? 'success' : 'error'">
        <Icon :name="compareResult ? 'check' : 'error'" :size="20" />
        <span>{{ compareResult ? '匹配成功！文本与哈希值一致' : '匹配失败！文本与哈希值不一致' }}</span>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h2>快速示例</h2>
      </div>
      <div class="example-buttons">
        <button @click="setExample('hello world')" class="btn-secondary">hello world</button>
        <button @click="setExample('123456')" class="btn-secondary">123456</button>
        <button @click="setExample('admin')" class="btn-secondary">admin</button>
        <button @click="setExample('password')" class="btn-secondary">password</button>
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
import { md5Encrypt, md5Compare } from '../api'
import Icon from '../components/Icon.vue'

const encryptInput = ref('')
const uppercase = ref(false)
const encryptResult = ref('')
const compareText = ref('')
const compareHash = ref('')
const compareResult = ref(null)
const error = ref('')
const successMessage = ref('')

const encryptText = async () => {
  if (!encryptInput.value.trim()) {
    showError('请输入要加密的文本')
    return
  }
  try {
    const response = await md5Encrypt({
      text: encryptInput.value,
      uppercase: uppercase.value
    })
    encryptResult.value = response.data.md5_hash
    compareResult.value = null
  } catch (err) {
    showError(err.response?.data?.detail || '加密失败')
  }
}

const compareHashFunc = async () => {
  if (!compareText.value.trim() || !compareHash.value.trim()) {
    showError('请输入文本和MD5哈希值')
    return
  }
  try {
    const response = await md5Compare({
      text: compareText.value,
      md5_hash: compareHash.value
    })
    compareResult.value = response.data.match
    encryptResult.value = ''
  } catch (err) {
    showError(err.response?.data?.detail || '对比失败')
  }
}

const setExample = (text) => {
  encryptInput.value = text
  compareText.value = text
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
.md5-tool {
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

.input-group {
  margin-bottom: 1rem;
}

.options {
  margin: 1rem 0;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  color: var(--text-secondary);
  font-weight: 500;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: var(--accent-success);
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

.result-box.success {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.2);
  color: var(--accent-success);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 500;
}

.result-box.error {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: var(--accent-error);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 500;
}

.result-label {
  display: block;
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
}

.hash-display {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.hash-text {
  flex: 1;
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--accent-success);
  word-break: break-all;
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
  .example-buttons {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
