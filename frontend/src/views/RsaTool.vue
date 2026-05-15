<template>
  <div class="rsa-tool">
    <div class="page-header">
      <div class="page-icon">
        <Icon name="lock" :size="28" />
      </div>
      <div class="page-title">
        <h1>RSA 加密解密工具</h1>
        <p>生成RSA密钥对，使用公钥加密，私钥解密</p>
      </div>
    </div>
    
    <div class="card">
      <div class="card-header">
        <h2>生成密钥对</h2>
      </div>
      <div class="key-size-select">
        <label class="select-label">密钥长度</label>
        <select v-model="keySize" class="select-field">
          <option :value="1024">1024 位</option>
          <option :value="2048">2048 位 (推荐)</option>
          <option :value="3072">3072 位</option>
          <option :value="4096">4096 位</option>
        </select>
      </div>
      <button @click="generateKeys" class="btn-primary w-full" :disabled="generating">
        {{ generating ? '生成中...' : '生成密钥对' }}
      </button>
      
      <div v-if="publicKey" class="key-display">
        <div class="key-header">
          <span class="key-label">公钥 (Public Key)</span>
          <button @click="copyToClipboard(publicKey, '公钥')" class="copy-btn" title="复制">
            <Icon name="copy" :size="16" />
          </button>
        </div>
        <textarea v-model="publicKey" class="key-textarea" rows="8" readonly></textarea>
      </div>
      
      <div v-if="privateKey" class="key-display">
        <div class="key-header">
          <span class="key-label">私钥 (Private Key)</span>
          <button @click="copyToClipboard(privateKey, '私钥')" class="copy-btn" title="复制">
            <Icon name="copy" :size="16" />
          </button>
        </div>
        <textarea v-model="privateKey" class="key-textarea" rows="12" readonly></textarea>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h2>公钥加密</h2>
      </div>
      <textarea
        v-model="encryptInput"
        placeholder="输入要加密的明文"
        class="input-field textarea"
        rows="4"
      ></textarea>
      <div class="input-group">
        <label class="input-label">公钥</label>
        <textarea
          v-model="encryptPublicKey"
          placeholder="粘贴PEM格式的公钥"
          class="input-field textarea"
          rows="6"
        ></textarea>
      </div>
      <button @click="encryptText" class="btn-primary w-full" :disabled="encrypting">
        {{ encrypting ? '加密中...' : '加密' }}
      </button>
      <div v-if="encryptResult" class="result-box">
        <div class="result-header">
          <span class="result-label">密文 (Base64)</span>
          <button @click="copyToClipboard(encryptResult, '密文')" class="copy-btn" title="复制">
            <Icon name="copy" :size="16" />
          </button>
        </div>
        <div class="ciphertext-display">{{ encryptResult }}</div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h2>私钥解密</h2>
      </div>
      <textarea
        v-model="decryptInput"
        placeholder="输入要解密的Base64密文"
        class="input-field textarea"
        rows="4"
      ></textarea>
      <div class="input-group">
        <label class="input-label">私钥</label>
        <textarea
          v-model="decryptPrivateKey"
          placeholder="粘贴PEM格式的私钥"
          class="input-field textarea"
          rows="8"
        ></textarea>
      </div>
      <button @click="decryptText" class="btn-primary w-full" :disabled="decrypting">
        {{ decrypting ? '解密中...' : '解密' }}
      </button>
      <div v-if="decryptResult" class="result-box">
        <span class="result-label">解密结果</span>
        <div class="plaintext-display">{{ decryptResult }}</div>
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
import { generateRsaKeys, rsaEncrypt, rsaDecrypt } from '../api'
import Icon from '../components/Icon.vue'

const keySize = ref(2048)
const publicKey = ref('')
const privateKey = ref('')
const generating = ref(false)

const encryptInput = ref('')
const encryptPublicKey = ref('')
const encryptResult = ref('')
const encrypting = ref(false)

const decryptInput = ref('')
const decryptPrivateKey = ref('')
const decryptResult = ref('')
const decrypting = ref(false)

const error = ref('')
const successMessage = ref('')

const generateKeys = async () => {
  generating.value = true
  error.value = ''
  try {
    const response = await generateRsaKeys({ key_size: keySize.value })
    publicKey.value = response.data.public_key
    privateKey.value = response.data.private_key
    encryptPublicKey.value = response.data.public_key
    decryptPrivateKey.value = response.data.private_key
    showSuccess('密钥对生成成功！')
  } catch (err) {
    showError(err.response?.data?.detail || '生成密钥失败')
  } finally {
    generating.value = false
  }
}

const encryptText = async () => {
  if (!encryptInput.value.trim()) {
    showError('请输入要加密的明文')
    return
  }
  if (!encryptPublicKey.value.trim()) {
    showError('请输入公钥')
    return
  }
  
  encrypting.value = true
  error.value = ''
  try {
    const response = await rsaEncrypt({
      plaintext: encryptInput.value,
      public_key: encryptPublicKey.value
    })
    encryptResult.value = response.data.ciphertext
    decryptInput.value = response.data.ciphertext
    showSuccess('加密成功！')
  } catch (err) {
    showError(err.response?.data?.detail || '加密失败')
  } finally {
    encrypting.value = false
  }
}

const decryptText = async () => {
  if (!decryptInput.value.trim()) {
    showError('请输入要解密的密文')
    return
  }
  if (!decryptPrivateKey.value.trim()) {
    showError('请输入私钥')
    return
  }
  
  decrypting.value = true
  error.value = ''
  try {
    const response = await rsaDecrypt({
      ciphertext: decryptInput.value,
      private_key: decryptPrivateKey.value
    })
    decryptResult.value = response.data.plaintext
    showSuccess('解密成功！')
  } catch (err) {
    showError(err.response?.data?.detail || '解密失败')
  } finally {
    decrypting.value = false
  }
}

const copyToClipboard = (text, label) => {
  navigator.clipboard.writeText(String(text)).then(() => {
    showSuccess(`${label}已复制到剪贴板`)
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
.rsa-tool {
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
  background: rgba(59, 130, 246, 0.1);
  color: var(--accent-primary);
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

.key-size-select {
  margin-bottom: 1rem;
}

.select-label {
  display: block;
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.select-field {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid var(--border-light);
  border-radius: var(--radius-md);
  font-size: 1rem;
  background: var(--bg-secondary);
  color: var(--text-primary);
  cursor: pointer;
  transition: all var(--transition-normal);
}

.select-field:focus {
  outline: none;
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
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
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.textarea {
  resize: vertical;
  min-height: 80px;
}

.input-group {
  margin-bottom: 1rem;
}

.input-label {
  display: block;
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.w-full {
  width: 100%;
}

.key-display {
  margin-top: 1rem;
}

.key-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.key-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.key-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid var(--border-light);
  border-radius: var(--radius-md);
  font-size: 0.75rem;
  font-family: 'Monaco', 'Menlo', monospace;
  background: var(--bg-tertiary);
  color: var(--text-primary);
  resize: vertical;
}

.result-box {
  margin-top: 1rem;
  padding: 1rem;
  border-radius: var(--radius-md);
  background: var(--bg-tertiary);
}

.result-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.result-label {
  display: block;
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.ciphertext-display {
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 0.875rem;
  color: var(--accent-primary);
  word-break: break-all;
  line-height: 1.5;
}

.plaintext-display {
  font-size: 1rem;
  color: var(--text-primary);
  word-break: break-word;
  line-height: 1.5;
}

.copy-btn {
  padding: 0.375rem;
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

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>