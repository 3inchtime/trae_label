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

export default api
