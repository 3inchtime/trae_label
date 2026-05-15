<template>
  <div class="md5-tool">
    <h2>🔐 MD5 加密工具</h2>
    
    <div class="encrypt-section">
      <h3>文本加密</h3>
      <div class="input-group">
        <textarea
          v-model="encryptInput"
          placeholder="输入要加密的文本"
          class="input-field textarea"
          rows="4"
        ></textarea>
      </div>
      <div class="options">
        <label class="checkbox-label">
          <input type="checkbox" v-model="uppercase" />
          <span>大写输出</span>
        </label>
      </div>
      <button @click="encryptText" class="encrypt-btn">生成 MD5</button>
      <div v-if="encryptResult" class="result">
        <p>MD5 哈希值:</p>
        <div class="hash-display">
          <span class="hash-text">{{ encryptResult }}</span>
          <button @click="copyToClipboard(encryptResult)" class="copy-btn">复制</button>
        </div>
      </div>
    </div>

    <div class="compare-section">
      <h3>哈希对比</h3>
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
      <button @click="compareHashFunc" class="compare-btn">对比验证</button>
      <div v-if="compareResult !== null" class="result">
        <p v-if="compareResult" class="success">✅ 匹配成功！文本与哈希值一致</p>
        <p v-else class="fail">❌ 匹配失败！文本与哈希值不一致</p>
      </div>
    </div>

    <div class="quick-examples">
      <h3>快速示例</h3>
      <div class="example-buttons">
        <button @click="setExample('hello world')">hello world</button>
        <button @click="setExample('123456')">123456</button>
        <button @click="setExample('admin')">admin</button>
        <button @click="setExample('password')">password</button>
      </div>
    </div>

    <div v-if="error" class="error-message">{{ error }}</div>
    <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { md5Encrypt, md5Compare } from '../api'

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
    error.value = '请输入要加密的文本'
    setTimeout(() => error.value = '', 3000)
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
    error.value = err.response?.data?.detail || '加密失败'
    setTimeout(() => error.value = '', 3000)
  }
}

const compareHashFunc = async () => {
  if (!compareText.value.trim() || !compareHash.value.trim()) {
    error.value = '请输入文本和MD5哈希值'
    setTimeout(() => error.value = '', 3000)
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
    error.value = err.response?.data?.detail || '对比失败'
    setTimeout(() => error.value = '', 3000)
  }
}

const setExample = (text) => {
  encryptInput.value = text
  compareText.value = text
}

const copyToClipboard = (text) => {
  navigator.clipboard.writeText(String(text)).then(() => {
    successMessage.value = '已复制到剪贴板'
    setTimeout(() => successMessage.value = '', 2000)
  })
}
</script>

<style scoped>
.md5-tool {
  max-width: 800px;
  margin: 0 auto;
}

h2 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.encrypt-section,
.compare-section,
.quick-examples {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.encrypt-section h3,
.compare-section h3,
.quick-examples h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.input-group {
  margin-bottom: 1rem;
}

.input-field {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.input-field:focus {
  outline: none;
  border-color: #42b983;
}

.textarea {
  resize: vertical;
  min-height: 100px;
  font-family: inherit;
}

.options {
  margin-bottom: 1rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  color: #666;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.encrypt-btn,
.compare-btn {
  width: 100%;
  padding: 0.75rem 1.5rem;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: background 0.2s;
}

.encrypt-btn:hover,
.compare-btn:hover {
  background: #3aa876;
}

.result {
  margin-top: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.result p {
  margin: 0 0 0.5rem 0;
  color: #666;
}

.hash-display {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.hash-text {
  flex: 1;
  font-family: monospace;
  font-size: 1.1rem;
  color: #42b983;
  font-weight: 600;
  word-break: break-all;
}

.copy-btn {
  padding: 0.25rem 0.75rem;
  background: #ecf0f1;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: background 0.2s;
  white-space: nowrap;
}

.copy-btn:hover {
  background: #d5dbdb;
}

.success {
  color: #3c3;
  font-weight: 500;
}

.fail {
  color: #c33;
  font-weight: 500;
}

.example-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 0.75rem;
}

.example-buttons button {
  padding: 0.75rem;
  background: #ecf0f1;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.example-buttons button:hover {
  background: #42b983;
  color: white;
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
}

.success-message {
  background: #efe;
  color: #3c3;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
}
</style>
