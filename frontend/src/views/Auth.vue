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
        
        <div v-if="!isLogin" class="form-group">
          <label for="email">邮箱</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="请输入邮箱地址"
            required
          />
        </div>
        
        <div v-if="!isLogin" class="form-group">
          <label for="phone">手机号</label>
          <input
            id="phone"
            v-model="form.phone"
            type="tel"
            placeholder="请输入手机号"
            required
          />
        </div>
        
        <div class="form-group">
          <label for="password">密码</label>
          <div class="password-input-wrapper">
            <input
              id="password"
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="请输入密码"
              required
            />
            <button type="button" class="toggle-password-btn" @click="showPassword = !showPassword">
              <Icon :name="showPassword ? 'eye-off' : 'eye'" :size="20" />
            </button>
          </div>
          <div v-if="!isLogin && form.password" class="password-strength">
            <div class="strength-bars">
              <div 
                v-for="i in 4" 
                :key="i" 
                class="strength-bar"
                :style="{ backgroundColor: i <= passwordStrength ? getStrengthColor() : 'var(--bg-tertiary)' }"
              ></div>
            </div>
            <span class="strength-text" :style="{ color: getStrengthColor() }">
              {{ getStrengthText() }}
            </span>
          </div>
        </div>
        
        <div v-if="!isLogin" class="form-group">
          <label for="confirmPassword">确认密码</label>
          <div class="password-input-wrapper">
            <input
              id="confirmPassword"
              v-model="form.confirmPassword"
              :type="showConfirmPassword ? 'text' : 'password'"
              placeholder="请再次输入密码"
              required
            />
            <button type="button" class="toggle-password-btn" @click="showConfirmPassword = !showConfirmPassword">
              <Icon :name="showConfirmPassword ? 'eye-off' : 'eye'" :size="20" />
            </button>
          </div>
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
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import Icon from '../components/Icon.vue'
import { login, register } from '../api/index.js'

const router = useRouter()
const isLogin = ref(true)
const loading = ref(false)
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const form = ref({
  username: '',
  email: '',
  phone: '',
  password: '',
  confirmPassword: ''
})

const passwordStrength = ref(0)

const calculatePasswordStrength = (password) => {
  if (!password) return 0
  let score = 0
  
  if (password.length >= 6) score += 1
  if (password.length >= 10) score += 1
  if (password.length >= 14) score += 1
  
  if (/[a-z]/.test(password)) score += 1
  if (/[A-Z]/.test(password)) score += 1
  if (/[0-9]/.test(password)) score += 1
  if (/[^a-zA-Z0-9]/.test(password)) score += 1
  
  return Math.min(score, 4)
}

const getStrengthText = () => {
  const texts = ['', '弱', '中等', '强', '非常强']
  return texts[passwordStrength.value] || ''
}

const getStrengthColor = () => {
  const colors = ['', '#ef4444', '#f59e0b', '#10b981', '#059669']
  return colors[passwordStrength.value] || ''
}

watch(() => form.value.password, (newPassword) => {
  passwordStrength.value = calculatePasswordStrength(newPassword)
})

const toggleMode = () => {
  isLogin.value = !isLogin.value
  form.value.email = ''
  form.value.phone = ''
  form.value.password = ''
  form.value.confirmPassword = ''
}

const handleSubmit = async () => {
  if (!form.value.username || !form.value.password) {
    alert('请填写用户名和密码')
    return
  }
  
  if (!isLogin.value) {
    if (!form.value.email) {
      alert('请填写邮箱地址')
      return
    }
    if (!form.value.phone) {
      alert('请填写手机号')
      return
    }
    if (form.value.password !== form.value.confirmPassword) {
      alert('两次输入的密码不一致，请检查')
      return
    }
    if (passwordStrength.value < 2) {
      alert('密码强度太弱，请设置更复杂的密码（建议包含大小写字母、数字和特殊字符）')
      return
    }
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

.password-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.password-input-wrapper input {
  width: 100%;
  padding-right: 3rem;
}

.toggle-password-btn {
  position: absolute;
  right: 0.875rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--text-tertiary);
  cursor: pointer;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color var(--transition-normal);
}

.toggle-password-btn:hover {
  color: var(--accent-primary);
}

.password-strength {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.strength-bars {
  display: flex;
  gap: 0.25rem;
  flex: 1;
}

.strength-bar {
  height: 4px;
  flex: 1;
  border-radius: 2px;
  transition: background-color var(--transition-normal);
}

.strength-text {
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
}

.submit-btn {
  margin-top: 0.5rem;
  padding: 1rem;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.7) 0%, rgba(37, 99, 235, 0.8) 30%, rgba(14, 165, 233, 0.7) 70%, rgba(59, 130, 246, 0.8) 100%);
  background-size: 300% 300%;
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all var(--transition-normal);
  box-shadow: 0 4px 20px rgba(59, 130, 246, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.3);
  animation: gradientShift 6s ease infinite;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  position: relative;
  overflow: hidden;
}

.submit-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.5), transparent);
  transition: left var(--transition-slow);
}

.submit-btn:hover:not(:disabled)::before {
  left: 100%;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 8px 35px rgba(59, 130, 246, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.4);
  border-color: rgba(255, 255, 255, 0.5);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(-1px);
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
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(59, 130, 246, 0.1) 50%, rgba(139, 92, 246, 0.1) 100%);
  background-size: 300% 300%;
  border: 1px solid rgba(99, 102, 241, 0.3);
  border-radius: var(--radius-md);
  color: var(--accent-primary);
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-normal);
  box-shadow: 0 2px 10px rgba(99, 102, 241, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.2);
  animation: gradientShift 15s ease infinite;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

.guest-btn:hover {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(59, 130, 246, 0.2) 50%, rgba(139, 92, 246, 0.2) 100%);
  border-color: rgba(99, 102, 241, 0.5);
  color: var(--accent-secondary);
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(99, 102, 241, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.3);
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
