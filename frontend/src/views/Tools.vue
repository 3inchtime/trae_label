<template>
  <div class="tools">
    <h2>工具列表</h2>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="tools-grid">
      <div v-for="tool in tools" :key="tool.id" class="tool-card">
        <h3>{{ tool.name }}</h3>
        <p v-if="tool.description">{{ tool.description }}</p>
        <span v-if="tool.category" class="category">{{ tool.category }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getTools } from '../api'

const tools = ref([])
const loading = ref(false)
const error = ref('')

const fetchTools = async () => {
  loading.value = true
  error.value = ''
  try {
    const response = await getTools()
    tools.value = response.data
  } catch (err) {
    error.value = '加载工具列表失败'
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchTools)
</script>

<style scoped>
.tools {
  max-width: 1000px;
  margin: 0 auto;
}

h2 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
}

.error {
  color: #e74c3c;
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.tool-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.tool-card:hover {
  transform: translateY(-2px);
}

.tool-card h3 {
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.tool-card p {
  color: #666;
  margin-bottom: 1rem;
  font-size: 0.95rem;
}

.category {
  display: inline-block;
  background: #42b983;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
}
</style>
