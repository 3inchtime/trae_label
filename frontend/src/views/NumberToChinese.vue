<template>
  <div class="number-to-chinese">
    <h2>💰 数字转中文大写</h2>

    <div class="converter-section">
      <h3>输入金额</h3>
      <div class="input-group">
        <input
          v-model.number="numberInput"
          type="number"
          step="0.01"
          placeholder="请输入数字金额"
          class="input-field"
          @keyup.enter="convertNumber"
        />
        <button @click="convertNumber" class="convert-btn">转换</button>
      </div>
    </div>

    <div v-if="result" class="result-section">
      <h3>转换结果</h3>
      <div class="result-display">
        <div class="result-item">
          <label>输入金额:</label>
          <span>¥ {{ result.number.toFixed(2) }}</span>
        </div>
        <div class="result-item main-result">
          <label>中文大写:</label>
          <span>{{ result.chinese }}</span>
          <button @click="copyToClipboard(result.chinese)" class="copy-btn">复制</button>
        </div>
      </div>
    </div>

    <div class="quick-examples">
      <h3>快捷示例</h3>
      <div class="example-buttons">
        <button @click="setExample(1234.56)">1234.56</button>
        <button @click="setExample(10000)">10000</button>
        <button @click="setExample(98765432.1)">98765432.1</button>
        <button @click="setExample(0)">0</button>
      </div>
    </div>

    <div class="rules-section">
      <h3>转换规则</h3>
      <ul>
        <li>支持整数和小数（最多两位小数）</li>
        <li>使用标准中文大写金额格式</li>
        <li>支持负数转换</li>
        <li>单位包括：元、角、分、拾、佰、仟、万、亿</li>
      </ul>
    </div>

    <div v-if="error" class="error-message">{{ error }}</div>
    <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { convertNumberToChinese } from '../api'

const numberInput = ref(null)
const result = ref(null)
const error = ref('')
const successMessage = ref('')

const convertNumber = async () => {
  if (numberInput.value === null || numberInput.value === '') {
    error.value = '请输入数字金额'
    setTimeout(() => error.value = '', 3000)
    return
  }
  try {
    const response = await convertNumberToChinese({
      number: numberInput.value
    })
    result.value = response.data
  } catch (err) {
    error.value = '转换失败'
    setTimeout(() => error.value = '', 3000)
  }
}

const setExample = (num) => {
  numberInput.value = num
  convertNumber()
}

const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text).then(() => {
    successMessage.value = '已复制到剪贴板'
    setTimeout(() => successMessage.value = '', 2000)
  })
}
</script>

<style scoped>
.number-to-chinese {
  max-width: 800px;
  margin: 0 auto;
}

h2 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.converter-section {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.converter-section h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.input-group {
  display: flex;
  gap: 0.5rem;
}

.input-field {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.input-field:focus {
  outline: none;
  border-color: #42b983;
}

.convert-btn {
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

.convert-btn:hover {
  background: #3aa876;
}

.result-section {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.result-section h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.result-display {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.result-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.result-item label {
  font-weight: 500;
  min-width: 100px;
  color: #666;
}

.result-item span {
  font-size: 1.1rem;
  color: #2c3e50;
}

.result-item.main-result {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.result-item.main-result span {
  font-size: 1.3rem;
  font-weight: 600;
  color: #42b983;
  flex: 1;
}

.copy-btn {
  padding: 0.25rem 0.75rem;
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

.quick-examples {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.quick-examples h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
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
  font-family: monospace;
  transition: all 0.2s;
}

.example-buttons button:hover {
  background: #42b983;
  color: white;
}

.rules-section {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.rules-section h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.rules-section ul {
  margin: 0;
  padding-left: 1.5rem;
}

.rules-section li {
  margin-bottom: 0.5rem;
  color: #666;
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
