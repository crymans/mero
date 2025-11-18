import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import './style.css'

// Создаем реактивное состояние для пользователя
const app = createApp(App)
const pinia = createPinia()
// Простое хранилище пользователя
app.provide('user', null)
app.use(pinia)
app.use(router).mount('#app')