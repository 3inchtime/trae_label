<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <Icon :name="isLogin ? 'lock' : 'user'" :size="32" />
        <h1>{{ isLogin ? '登录' : '注册' }}</h1>
        <p>{{ isLogin ? '欢迎回来！登录以继续使用' : '创建一个新账户' }}</p>
      </div>
      
      <form @submit.prevent="handleSubmit" class="auth-form">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            placeholder="请输入用户名"
            required
          />
        </div>
        
        <div class="form-group">
          <label for="password">密码</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            required
          />
        </div>
        
        <div v-if="!isLogin" class="form-group">
          <label for="confirmPassword">确认密码</label>
          <input
            id="confirmPassword"
            v-model="form.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            required
          />
        </div>
        
        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? '处理中...' : (isLogin ? '登录' : '注册') }}
        </button>
      </form>
      
      <div class="auth-switch">
        <span>{{ isLogin ? '还没有账户？' : '已有账户？' }}</span>
        <button @click="toggleMode" class="switch-btn">
          {{ isLogin ? '立即注册' : '立即登录' }}
        </button>
      </div>
      
      <div class="auth-divider">
        <span>或</span>
      </div>
      
      <div class="auth-guest">
        <button @click="continueAsGuest" class="guest-btn">
          <Icon name="home" :size="18" />
          <span>不登录，直接访问</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Icon from '../components/Icon.vue'
import { login, register } from '../api/index.js'

const router = useRouter()
const isLogin = ref(true)
const loading = ref(false)
const form = ref({
  username: '',
  password: '',
  confirmPassword: ''
})

const toggleMode = () => {
  isLogin.value = !isLogin.value
  form.value.confirmPassword = ''
}

const handleSubmit = async () => {
  if (!form.value.username || !form.value.password) {
    alert('请填写用户名和密码')
    return
  }
  
  if (!isLogin.value && form.value.password !== form.value.confirmPassword) {
    alert('两次输入的密码不一致，请检查')
    return
  }
  
  loading.value = true
  try {
    const apiCall = isLogin.value ? login : register
    const response = await apiCall(form.value)
    
    if (isLogin.value) {
      localStorage.setItem('token', response.data.access_token)
      localStorage.setItem('user', JSON.stringify(response.data.user))
    }
    
    alert(isLogin.value ? '登录成功！' : '注册成功！请登录')
    
    if (isLogin.value) {
      router.push('/')
    } else {
      isLogin.value = true
      form.value.password = ''
    }
  } catch (error) {
    alert(error.response?.data?.detail || '操作失败，请重试')
  } finally {
    loading.value = false
  }
}

const continueAsGuest = () => {
  router.push('/')
}
</script>

<style scoped>
.auth-container {
  min-height: calc(100vh - 70px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%);
}

.auth-card {
  width: 100%;
  max-width: 420px;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-backdrop);
  -webkit-backdrop-filter: var(--glass-backdrop);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-xl);
  padding: 2.5rem;
  box-shadow: 0 20px 60px rgba(59, 130, 246, 0.15);
  animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.auth-header {
  text-align: center;
  margin-bottom: 2rem;
}

.auth-header svg {
  color: var(--accent-primary);
  margin-bottom: 1rem;
}

.auth-header h1 {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.auth-header p {
  color: var(--text-secondary);
  font-size: 0.95rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  margin-bottom: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-primary);
}

.form-group input {
  padding: 0.875rem 1.125rem;
  border: 2px solid var(--glass-border);
  border-radius: var(--radius-md);
  background: var(--bg-secondary);
  color: var(--text-primary);
  font-size: 1rem;
  transition: all var(--transition-normal);
  outline: none;
}

.form-group input:focus {
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.form-group input::placeholder {
  color: var(--text-tertiary);
}

.submit-btn {
  margin-top: 0.5rem;
  padding: 1rem;
  background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all var(--transition-normal);
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.auth-switch {
  text-align: center;
  padding: 1rem;
  border-radius: var(--radius-md);
  background: rgba(59, 130, 246, 0.05);
}

.auth-switch span {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.switch-btn {
  background: none;
  border: none;
  color: var(--accent-primary);
  font-weight: 700;
  font-size: 0.9rem;
  cursor: pointer;
  margin-left: 0.25rem;
  transition: color var(--transition-normal);
}

.switch-btn:hover {
  color: var(--accent-secondary);
  text-decoration: underline;
}

.auth-divider {
  display: flex;
  align-items: center;
  margin: 1.5rem 0;
}

.auth-divider::before,
.auth-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--glass-border);
}

.auth-divider span {
  padding: 0 1rem;
  color: var(--text-tertiary);
  font-size: 0.875rem;
}

.auth-guest {
  text-align: center;
}

.guest-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  background: var(--glass-bg);
  border: 2px solid var(--glass-border);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-normal);
}

.guest-btn:hover {
  border-color: var(--accent-primary);
  color: var(--accent-primary);
  background: rgba(59, 130, 246, 0.08);
  transform: translateY(-2px);
}

@media (max-width: 480px) {
  .auth-container {
    padding: 1rem;
  }
  
  .auth-card {
    padding: 1.75rem 1.5rem;
  }
}
</style>
