import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

export const getTools = () => api.get('/tools')
export const createTool = (data) => api.post('/tools', data)
export const getTool = (id) => api.get(`/tools/${id}`)
export const healthCheck = () => api.get('/health')

export const convertTimestamp = (data) => api.post('/tools/timestamp/convert', data)
export const getCurrentTimestamp = () => api.get('/tools/timestamp/now')

export const formatJson = (data) => api.post('/tools/json/format', data)
export const validateJson = (data) => api.post('/tools/json/validate', data)
export const md5Encrypt = (data) => api.post('/tools/md5/encrypt', data)
export const md5Compare = (data) => api.post('/tools/md5/compare', data)
export const convertNumberToChinese = (data) => api.post('/tools/number-to-chinese', data)

export const generateRsaKeys = (data) => api.post('/tools/rsa/generate-keys', data)
export const rsaEncrypt = (data) => api.post('/tools/rsa/encrypt', data)
export const rsaDecrypt = (data) => api.post('/tools/rsa/decrypt', data)

export const createTimer = (data) => api.post('/tools/timer/create', data)
export const startTimer = (timerId) => api.post(`/tools/timer/${timerId}/start`)
export const pauseTimer = (timerId) => api.post(`/tools/timer/${timerId}/pause`)
export const resetTimer = (timerId) => api.post(`/tools/timer/${timerId}/reset`)
export const getTimerStatus = (timerId) => api.get(`/tools/timer/${timerId}/status`)
export const deleteTimer = (timerId) => api.delete(`/tools/timer/${timerId}`)
export const getActiveTimers = () => api.get('/tools/timer/active')
export const getTimerHistory = () => api.get('/tools/timer/history')

export const convertWeight = (data) => api.post('/tools/weight/convert', data)
export const calculateTimeDifference = (data) => api.post('/tools/time-difference/calculate', data)

export const getCalendarMonth = (data) => api.post('/tools/calendar/month', data)
export const getTodayInfo = () => api.get('/tools/calendar/today')

export const convertLength = (data) => api.post('/tools/length/convert', data)
export const urlEncode = (data) => api.post('/tools/url/encode', data)
export const urlDecode = (data) => api.post('/tools/url/decode', data)

export const validateYaml = (data) => api.post('/tools/yaml/validate', data)
export const formatYaml = (data) => api.post('/tools/yaml/format', data)

export default api
