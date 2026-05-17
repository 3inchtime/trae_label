<template>
  <svg 
    :class="['icon', `icon-${name}`]" 
    :width="size" 
    :height="size" 
    viewBox="0 0 24 24" 
    fill="none" 
    stroke="currentColor" 
    stroke-width="2" 
    stroke-linecap="round" 
    stroke-linejoin="round"
  >
    <circle cx="12" cy="12" r="10" v-if="name === 'clock'" />
    <polyline v-if="name === 'clock'" points="12 6 12 12 16 14" />
    
    <polyline v-if="name === 'json'" points="16 18 22 12 16 6" />
    <polyline v-if="name === 'json'" points="8 6 2 12 8 18" />
    
    <rect v-if="name === 'lock'" x="3" y="11" width="18" height="11" rx="2" ry="2" />
    <path v-if="name === 'lock'" d="M7 11V7a5 5 0 0 1 10 0v4" />
    
    <circle v-if="name === 'money'" cx="12" cy="12" r="10" />
    <line v-if="name === 'money'" x1="12" y1="16" x2="12" y2="12" />
    <path v-if="name === 'money'" d="M12 8h.01" />
    
    <polyline v-if="name === 'refresh'" points="23 4 23 10 17 10" />
    <polyline v-if="name === 'refresh'" points="1 20 1 14 7 14" />
    <path v-if="name === 'refresh'" d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" />
    
    <rect v-if="name === 'copy'" x="9" y="9" width="13" height="13" rx="2" ry="2" />
    <path v-if="name === 'copy'" d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
    
    <circle v-if="name === 'search'" cx="11" cy="11" r="8" />
    <line v-if="name === 'search'" x1="21" y1="21" x2="16.65" y2="16.65" />
    
    <polygon v-if="name === 'star'" points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
    
    <path v-if="name === 'box'" d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
    <polyline v-if="name === 'box'" points="3.27 6.96 12 12.01 20.73 6.96" />
    <line v-if="name === 'box'" x1="12" y1="22.08" x2="12" y2="12" />
    
    <polyline v-if="name === 'trash'" points="3 6 5 6 21 6" />
    <path v-if="name === 'trash'" d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
    <line v-if="name === 'trash'" x1="10" y1="11" x2="10" y2="17" />
    <line v-if="name === 'trash'" x1="14" y1="11" x2="14" y2="17" />
    
    <circle v-if="name === 'sun'" cx="12" cy="12" r="5" />
    <line v-if="name === 'sun'" x1="12" y1="1" x2="12" y2="3" />
    <line v-if="name === 'sun'" x1="12" y1="21" x2="12" y2="23" />
    <line v-if="name === 'sun'" x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
    <line v-if="name === 'sun'" x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
    <line v-if="name === 'sun'" x1="1" y1="12" x2="3" y2="12" />
    <line v-if="name === 'sun'" x1="21" y1="12" x2="23" y2="12" />
    <line v-if="name === 'sun'" x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
    <line v-if="name === 'sun'" x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
    
    <path v-if="name === 'moon'" d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
    
    <path v-if="name === 'home'" d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
    <polyline v-if="name === 'home'" points="9 22 9 12 15 12 15 22" />
    
    <path v-if="name === 'tools'" d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z" />
    
    <polyline v-if="name === 'check'" points="20 6 9 17 4 12" />
    
    <circle v-if="name === 'error'" cx="12" cy="12" r="10" />
    <line v-if="name === 'error'" x1="15" y1="9" x2="9" y2="15" />
    <line v-if="name === 'error'" x1="9" y1="9" x2="15" y2="15" />
    
    <path v-if="name === 'rocket'" d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z" />
    <path v-if="name === 'rocket'" d="M12 15l-3-3a22 22 0 0 1-9-1.5h2c0 2.5.5 5 1.5 7.5L12 15z" />
    <path v-if="name === 'rocket'" d="m12 15 3-3a22 22 0 0 0 9-1.5h-2c0 2.5-.5 5-1.5 7.5L12 15z" />
    <path v-if="name === 'rocket'" d="M15 11.9V6.1l-3-3.1-3 3.1v5.7l3 3.1 3-3.1z" />
    
    <ellipse v-if="name === 'database'" cx="12" cy="5" rx="9" ry="3" />
    <path v-if="name === 'database'" d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3" />
    <path v-if="name === 'database'" d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" />
    
    <path v-if="name === 'wrench'" d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z" />
    
    <polygon v-if="name === 'play'" points="5 3 19 12 5 21 5 3" />
    
    <rect v-if="name === 'pause'" x="6" y="4" width="4" height="16" />
    <rect v-if="name === 'pause'" x="14" y="4" width="4" height="16" />
    
    <line v-if="name === 'plus'" x1="12" y1="5" x2="12" y2="19" />
    <line v-if="name === 'plus'" x1="5" y1="12" x2="19" y2="12" />
    
    <line v-if="name === 'close'" x1="18" y1="6" x2="6" y2="18" />
    <line v-if="name === 'close'" x1="6" y1="6" x2="18" y2="18" />
    
    <path v-if="name === 'history'" d="M1 4v6h6" />
    <path v-if="name === 'history'" d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10" />
    
    <rect v-if="name === 'calendar'" x="3" y="4" width="18" height="18" rx="2" ry="2" />
    <line v-if="name === 'calendar'" x1="16" y1="2" x2="16" y2="6" />
    <line v-if="name === 'calendar'" x1="8" y1="2" x2="8" y2="6" />
    <line v-if="name === 'calendar'" x1="3" y1="10" x2="21" y2="10" />
    
    <path v-if="name === 'ruler'" d="M3 7h18M3 12h18M3 17h18M8 7v5M13 7v10M18 7v5" />
    <rect v-if="name === 'ruler'" x="2" y="3" width="20" height="18" rx="2" />
    
    <circle v-if="name === 'palette'" cx="12" cy="12" r="10" />
    <path v-if="name === 'palette'" d="M12 2a10 10 0 0 1 0 20c-1.5 0-2.7-1.2-2.7-2.7 0-.6.2-1.2.6-1.7.3-.4.5-1 .5-1.6 0-1.5-1.2-2.7-2.7-2.7-1.5 0-2.7 1.2-2.7 2.7 0 .6.2 1.2.5 1.6.4.5.6 1.1.6 1.7 0 1.5-1.2 2.7-2.7 2.7-1.5 0-2.7-1.2-2.7-2.7 0-.6.2-1.2.5-1.6.4-.5.6-1.1.6-1.7 0-1.5-1.2-2.7-2.7-2.7-1.5 0-2.7 1.2-2.7 2.7 0 .6.2 1.2.5 1.6.4.5.6 1.1.6 1.7C4.7 19.2 3.5 18 2 18A10 10 0 0 1 12 2z" />
    
    <polyline v-if="name === 'code'" points="16 18 22 12 16 6" />
    <polyline v-if="name === 'code'" points="8 6 2 12 8 18" />
    
    <path v-if="name === 'link'" d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" />
    <path v-if="name === 'link'" d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" />
  </svg>
</template>

<script setup>
defineProps({
  name: {
    type: String,
    required: true
  },
  size: {
    type: [Number, String],
    default: 20
  }
})
</script>

<style scoped>
.icon {
  display: inline-block;
  vertical-align: middle;
  flex-shrink: 0;
}
</style>
