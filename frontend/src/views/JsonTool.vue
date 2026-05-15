<template>
  <div class="json-tool">
    <h2>📄 JSON格式化工具</h2>
    
    <div class="input-section">
      <h3>输入JSON</h3>
      <textarea
        v-model="jsonInput"
        placeholder="在此粘贴或输入JSON字符串..."
        class="json-textarea"
        rows="12"
      ></textarea>
      <div class="button-group">
        <button @click="validateJson" class="btn validate-btn">🔍 验证</button>
        <button @click="formatJson" class="btn format-btn">✨ 格式化</button>
        <button @click="minifyJson" class="btn minify-btn">📦 压缩</button>
        <button @click="clearAll" class="btn clear-btn">🗑️ 清空</button>
      </div>
    </div>

    <div v-if="validationResult !== null" class="result-section">
      <h3>验证结果</h3>
      <div :class="validationResult.valid ? 'valid-result' : 'error-result'">
        <span v-if="validationResult.valid">✅ JSON格式正确</span>
        <span v-else>❌ {{ validationResult.error }}</span>
      </div>
    </div>

    <div v-if="formattedJson" class="result-section">
      <div class="result-header">
        <h3>格式化结果</h3>
        <button @click="copyToClipboard(formattedJson)" class="copy-btn">复制</button>
      </div>
      <pre class="json-output">{{ formattedJson }}</pre>
    </div>

    <div v-if="minifiedJson" class="result-section">
      <div class="result-header">
        <h3>压缩结果</h3>
        <button @click="copyToClipboard(minifiedJson)" class="copy-btn">复制</button>
      </div>
      <pre class="json-output minified">{{ minifiedJson }}</pre>
    </div>

    <div class="sample-section">
      <h3>示例JSON</h3>
      <div class="sample-buttons">
        <button @click="loadSample(1)" class="sample-btn">示例1: 简单对象</button>
        <button @click="loadSample(2)" class="sample-btn">示例2: 数组</button>
        <button @click="loadSample(3)" class="sample-btn">示例3: 复杂嵌套</button>
      </div>
    </div>

    <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { formatJson as formatJsonApi, validateJson as validateJsonApi } from '../api'

const jsonInput = ref('')
const formattedJson = ref('')
const minifiedJson = ref('')
const validationResult = ref(null)
const successMessage = ref('')

const validateJson = async () => {
  if (!jsonInput.value.trim()) {
    validationResult.value = { valid: false, error: '请输入JSON字符串' }
    return
  }
  try {
    const response = await validateJsonApi({ json_str: jsonInput.value })
    validationResult.value = response.data
    if (!response.data.valid) {
      formattedJson.value = ''
      minifiedJson.value = ''
    }
  } catch (err) {
    validationResult.value = { valid: false, error: '验证失败' }
  }
}

const formatJson = async () => {
  if (!jsonInput.value.trim()) {
    validationResult.value = { valid: false, error: '请输入JSON字符串' }
    return
  }
  try {
    const response = await formatJsonApi({ json_str: jsonInput.value, indent: 2 })
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

const minifyJson = async () => {
  if (!jsonInput.value.trim()) {
    validationResult.value = { valid: false, error: '请输入JSON字符串' }
    return
  }
  try {
    const response = await formatJsonApi({ json_str: jsonInput.value, indent: 0 })
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

const loadSample = (type) => {
  const samples = {
    1: '{"name": "张三", "age": 25, "city": "北京"}',
    2: '[{"id": 1, "name": "苹果"}, {"id": 2, "name": "香蕉"}, {"id": 3, "name": "橙子"}]',
    3: '{"user": {"name": "李四", "age": 30}, "hobbies": ["读书", "游泳", "编程"], "address": {"city": "上海", "district": "浦东新区"}}'
  }
  jsonInput.value = samples[type]
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
  max-width: 900px;
  margin: 0 auto;
}

h2 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.input-section,
.result-section,
.sample-section {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
  font-size: 1.2rem;
}

.json-textarea {
  width: 100%;
  padding: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 4px;
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 0.9rem;
  resize: vertical;
  transition: border-color 0.2s;
}

.json-textarea:focus {
  outline: none;
  border-color: #42b983;
}

.button-group {
  display: flex;
  gap: 0.75rem;
  margin-top: 1rem;
  flex-wrap: wrap;
}

.btn {
  padding: 0.75rem 1.25rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 500;
  transition: all 0.2s;
}

.validate-btn {
  background: #3498db;
  color: white;
}

.validate-btn:hover {
  background: #2980b9;
}

.format-btn {
  background: #42b983;
  color: white;
}

.format-btn:hover {
  background: #3aa876;
}

.minify-btn {
  background: #f39c12;
  color: white;
}

.minify-btn:hover {
  background: #e67e22;
}

.clear-btn {
  background: #e74c3c;
  color: white;
}

.clear-btn:hover {
  background: #c0392b;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.result-header h3 {
  margin: 0;
}

.copy-btn {
  padding: 0.5rem 1rem;
  background: #ecf0f1;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: background 0.2s;
}

.copy-btn:hover {
  background: #d5dbdb;
}

.json-output {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 0.9rem;
  white-space: pre-wrap;
  word-break: break-all;
  max-height: 400px;
  overflow-y: auto;
  margin: 0;
}

.json-output.minified {
  color: #e74c3c;
}

.valid-result,
.error-result {
  padding: 1rem;
  border-radius: 4px;
  font-weight: 500;
}

.valid-result {
  background: #efe;
  color: #3c3;
}

.error-result {
  background: #fee;
  color: #c33;
}

.sample-buttons {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.sample-btn {
  padding: 0.5rem 1rem;
  background: #ecf0f1;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.sample-btn:hover {
  background: #42b983;
  color: white;
}

.success-message {
  background: #efe;
  color: #3c3;
  padding: 1rem;
  border-radius: 4px;
  text-align: center;
  font-weight: 500;
}
</style>
