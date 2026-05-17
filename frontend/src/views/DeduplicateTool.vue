<template>
  <div class="deduplicate-tool">
    <div class="page-header">
      <div class="page-icon">
        <Icon name="trash" :size="28" />
      </div>
      <div class="page-title">
        <h1>文本去重工具</h1>
        <p>去除文本中的重复行，支持多种去重选项</p>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h2>输入文本</h2>
      </div>
      <textarea
        v-model="inputText"
        placeholder="在此粘贴需要去重的文本..."
        class="input-field textarea"
        rows="10"
      ></textarea>
      <div class="options">
        <label class="checkbox-label">
          <input type="checkbox" v-model="ignoreCase" />
          <span>忽略大小写</span>
        </label>
        <label class="checkbox-label">
          <input type="checkbox" v-model="removeEmptyLines" />
          <span>移除空行</span>
        </label>
        <label class="checkbox-label">
          <input type="checkbox" v-model="keepOrder" />
          <span>保留原始顺序</span>
        </label>
      </div>
      <div class="button-group">
        <button @click="processDeduplicate" class="btn-primary">开始去重</button>
        <button @click="clearAll" class="btn-secondary">清空</button>
      </div>
    </div>

    <div v-if="result" class="card">
      <div class="card-header">
        <h2>去重结果</h2>
      </div>
      <div class="stats">
        <div class="stat-item">
          <span class="stat-label">原行数</span>
          <span class="stat-value">{{ result.original_line_count }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">去重后</span>
          <span class="stat-value success">{{ result.deduplicated_line_count }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">已移除</span>
          <span class="stat-value removed">{{ result.removed_count }}</span>
        </div>
      </div>
      <textarea
        v-model="result.deduplicated_text"
        class="input-field textarea"
        rows="10"
        readonly
      ></textarea>
      <button @click="copyResult" class="btn-primary w-full">
        <Icon name="copy" :size="18" />
        复制结果
      </button>
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
import { deduplicateText } from '../api'
import Icon from '../components/Icon.vue'

const inputText = ref('')
const ignoreCase = ref(false)
const removeEmptyLines = ref(true)
const keepOrder = ref(true)
const result = ref(null)
const error = ref('')
const successMessage = ref('')

const processDeduplicate = async () => {
  if (!inputText.value.trim()) {
    showError('请输入需要去重的文本')
    return
  }
  try {
    const response = await deduplicateText({
      text: inputText.value,
      ignore_case: ignoreCase.value,
      remove_empty_lines: removeEmptyLines.value,
      keep_order: keepOrder.value
    })
    result.value = response.data
    showSuccess('去重完成！')
  } catch (err) {
    showError(err.response?.data?.detail || '去重失败')
  }
}

const clearAll = () => {
  inputText.value = ''
  result.value = null
  error.value = ''
  successMessage.value = ''
}

const copyResult = () => {
  if (result.value?.deduplicated_text) {
    navigator.clipboard.writeText(result.value.deduplicated_text).then(() => {
      showSuccess('已复制到剪贴板')
    })
  }
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
.deduplicate-tool {
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
  min-height: 150px;
}

.options {
  margin: 1rem 0;
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
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

.button-group {
  display: flex;
  gap: 1rem;
}

.btn-primary {
  padding: 0.75rem 1.5rem;
  background: var(--accent-success);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-normal);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-primary:hover {
  background: #059669;
  transform: translateY(-1px);
}

.btn-secondary {
  padding: 0.75rem 1.5rem;
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border: 1px solid var(--border-medium);
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-normal);
}

.btn-secondary:hover {
  background: var(--border-light);
}

.w-full {
  width: 100%;
}

.stats {
  display: flex;
  gap: 2rem;
  margin-bottom: 1rem;
  padding: 1rem;
  background: var(--bg-tertiary);
  border-radius: var(--radius-md);
}

.stat-item {
  text-align: center;
  flex: 1;
}

.stat-label {
  display: block;
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-bottom: 0.25rem;
}

.stat-value {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
}

.stat-value.success {
  color: var(--accent-success);
}

.stat-value.removed {
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
