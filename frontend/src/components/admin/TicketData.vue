<template>
  <section class="hero">
    <div class="hero-overlay"></div>
    
    <!-- Animated Neon Background -->
    <div class="neon-grid">
      <div class="grid-line"></div>
      <div class="grid-line"></div>
      <div class="grid-line"></div>
      <div class="grid-line"></div>
    </div>

    <div class="hero-content">
      <!-- Main Title with Glitch Effect -->
      <h1 class="main-title">
        <span class="glitch" data-text="СТАТУС">СТАТУС</span>
      </h1>
      
      <p class="hero-subtitle">ULTIMATE TREPP TUSOVKA</p>

      <!-- Loading State -->
      <div v-if="loading" class="loading-container">
        <div class="loading-spinner"></div>
        <p class="loading-text">Загрузка данных...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-container">
        <div class="error-icon">⚠️</div>
        <p class="error-text">{{ error }}</p>
        <button class="neon-btn blue" @click="fetchData">
          <span class="btn-text">ПОВТОРИТЬ</span>
          <div class="neon-glow"></div>
        </button>
      </div>

      <!-- Success State -->
      <div v-else-if="entryData" class="data-container">
                <!-- Ticket Information -->
        <div class="info-section">
          <h2 class="section-title">
            <span class="neon-icon">🎫</span>
            ИНФОРМАЦИЯ О БИЛЕТЕ
          </h2>
          <div class="info-grid">
            <div class="info-card">
              <span class="info-label">Type билета</span>
              <span class="info-value">{{ ticketType(entryData.ticket.price) }}</span>
            </div>
            <div class="info-card">
              <span class="info-label">Цена</span>
              <span class="info-value">{{ entryData.ticket.price }} ₽</span>
            </div>
            <div class="info-card highlight">
              <span class="info-label">Последний вход</span>
              <span class="info-value">{{ formattedLastEntry }}</span>
            </div>
            <div class="info-card">
              <span class="info-label">Создан</span>
              <span class="info-value">{{ formattedCreatedAt }}</span>
            </div>
          </div>
        </div>
        <!-- User Information -->
        <div class="info-section">
          <h2 class="section-title">
            <span class="neon-icon">👤</span>
            ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ
          </h2>
          <div class="info-grid">
            <div class="info-card">
              <span class="info-label">Telegram ID</span>
              <span class="info-value">{{ entryData.user.telegram_id || 'Не указан' }}</span>
            </div>
            <div class="info-card">
              <span class="info-label">Имя пользователя</span>
              <span class="info-value">{{ entryData.user.username || 'Не указан' }}</span>
            </div>
            <div class="info-card">
              <span class="info-label">Имя</span>
              <span class="info-value">{{ entryData.user.first_name || 'Не указано' }}</span>
            </div>
            <div class="info-card">
              <span class="info-label">Фамилия</span>
              <span class="info-value">{{ entryData.user.last_name || 'Не указана' }}</span>
            </div>
            <div class="info-card">
              <span class="info-label">Телефон</span>
              <span class="info-value">{{ entryData.user.phone || 'Не указан' }}</span>
            </div>
            <div class="info-card">
              <span class="info-label">Баланс</span>
              <span class="info-value">{{ entryData.user.balance }} ₽</span>
            </div>
          </div>
        </div>



        <!-- Status Indicator -->
        <div class="status-section">
          <div class="status-indicator" :class="statusClass">
            <div class="status-glow"></div>
            <span class="status-text">{{ statusText }}</span>
          </div>
        </div>
      </div>

      <!-- Event Info -->
      <div class="event-info">
        <div class="info-item">
          <span class="neon-icon">🔥</span>
          <span>13 декабря | 16:00-05:00</span>
        </div>
        <div class="info-item">
          <span class="neon-icon">📍</span>
          <span>московская 64 | ROSTOV</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { API_CONFIG } from '@/config/api'

interface UserBase {
  telegram_id?: string
  username?: string
  first_name?: string
  last_name?: string
  phone?: string
  balance: number
}

interface User extends UserBase {
  id: number
  role: string
  created_at: string
}

interface TicketBase {
  price: number
  qr_code: string
}

interface Ticket extends TicketBase {
  id: number
  user_id: number
  last_entry: number
  created_at: string
}

interface EntryAnswer {
  ticket: Ticket
  user: User
}

const loading = ref(true)
const error = ref('')
const entryData = ref<EntryAnswer | null>(null)

const formattedLastEntry = computed(() => {
  if (!entryData.value) return ''
  const date = new Date(entryData.value.ticket.last_entry * 1000)
  return date.toLocaleString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
})

const formattedCreatedAt = computed(() => {
  if (!entryData.value) return ''
  const date = new Date(entryData.value.ticket.created_at)
  return date.toLocaleString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
})

function ticketType(price){
    let data = {700:'standard', 900:'fast', 1500:'vip'}
    return data[parseInt(price)]
}

const statusClass = computed(() => {
  if (!entryData.value) return 'unknown'
  const now = Math.floor(Date.now() / 1000)
  const lastEntry = entryData.value.ticket.last_entry
  const diff = now - lastEntry
  
  if (diff < 3600) return 'active' // Менее часа
  if (diff < 86400) return 'recent' // Менее суток
  return 'inactive'
})

const statusText = computed(() => {
  switch (statusClass.value) {
    case 'active': return 'АКТИВЕН'
    case 'recent': return 'НЕДАВНИЙ ВХОД'
    case 'inactive': return 'НЕАКТИВЕН'
    default: return 'НЕИЗВЕСТНО'
  }
})

const getTokenFromUrl = () => {
  const urlParams = new URLSearchParams(window.location.search)
  return urlParams.get('token')
}

const fetchData = async () => {
  try {
    loading.value = true
    error.value = ''
    
    const token = getTokenFromUrl()
    if (!token) {
      throw new Error('Token не найден в URL')
    }

    const response = await fetch(`${API_CONFIG.BASE_URL}/tickets/${token}/mark-used`)
    
    if (!response.ok) {
      throw new Error(`Ошибка: ${response.status} ${response.statusText}`)
    }

    const data: EntryAnswer = await response.json()
    entryData.value = data
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Неизвестная ошибка'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.hero {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  background-image: url('./bg.png');
  background-position: center center;
  background-attachment: fixed;
  background-size: contain;
  padding: 2rem 0;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
}

.neon-grid {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  opacity: 0.3;
}

.grid-line {
  position: absolute;
  background: linear-gradient(90deg, transparent, #00ffff, transparent);
  height: 1px;
  width: 100%;
  animation: gridMove 20s linear infinite;
}

.grid-line:nth-child(1) { top: 25%; animation-delay: 0s; }
.grid-line:nth-child(2) { top: 50%; animation-delay: -5s; }
.grid-line:nth-child(3) { top: 75%; animation-delay: -10s; }
.grid-line:nth-child(4) { top: 100%; animation-delay: -15s; }

.hero-content {
  text-align: center;
  z-index: 10;
  position: relative;
  width: 90%;
  max-width: 1200px;
}

.main-title {
  font-size: 6rem;
  font-weight: 900;
  margin-bottom: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.5rem;
}

.glitch {
  position: relative;
  color: #fff;
  text-shadow: 
    0 0 10px #ff00ff,
    0 0 20px #ff00ff,
    0 0 40px #ff00ff,
    0 0 80px #ff00ff;
  animation: glitch 5s infinite;
}

.hero-subtitle {
  font-size: 1.5rem;
  margin-bottom: 3rem;
  text-transform: uppercase;
  letter-spacing: 0.3rem;
  color: #00ffff;
  text-shadow: 0 0 10px #00ffff;
}

/* Loading Styles */
.loading-container {
  margin: 3rem 0;
}

.loading-spinner {
  width: 60px;
  height: 60px;
  border: 3px solid #00ffff;
  border-top: 3px solid transparent;
  border-radius: 50%;
  margin: 0 auto 1rem;
  animation: spin 1s linear infinite;
  box-shadow: 0 0 20px #00ffff;
}

.loading-text {
  font-size: 1.2rem;
  color: #00ffff;
  text-shadow: 0 0 10px #00ffff;
}

/* Error Styles */
.error-container {
  margin: 3rem 0;
  padding: 2rem;
  border: 2px solid #ff4444;
  border-radius: 10px;
  background: rgba(255, 68, 68, 0.1);
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.error-text {
  font-size: 1.2rem;
  color: #ff4444;
  margin-bottom: 1.5rem;
  text-shadow: 0 0 10px #ff4444;
}

/* Data Container Styles */
.data-container {
  margin: 3rem 0;
}

.info-section {
  margin-bottom: 3rem;
  text-align: left;
}

.section-title {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  text-transform: uppercase;
  letter-spacing: 0.1rem;
  color: #00ffff;
  text-shadow: 0 0 10px #00ffff;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.info-card {
  background: rgba(0, 255, 255, 0.1);
  border: 1px solid #00ffff;
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.info-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 20px #00ffff;
}

.info-card.highlight {
  background: rgba(255, 0, 255, 0.1);
  border-color: #ff00ff;
  animation: pulse 2s infinite;
}

.info-card.highlight:hover {
  box-shadow: 0 0 20px #ff00ff;
}

.info-label {
  font-size: 0.9rem;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.05rem;
}

.info-value {
  font-size: 1.1rem;
  color: #fff;
  font-weight: bold;
}

.info-value.code {
  font-family: monospace;
  word-break: break-all;
}

/* Status Indicator */
.status-section {
  margin: 2rem 0;
}

.status-indicator {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 2rem;
  border-radius: 50px;
  font-size: 1.2rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.1rem;
  overflow: hidden;
}

.status-indicator.active {
  border: 2px solid #00ff00;
  color: #00ff00;
  box-shadow: 0 0 20px #00ff00;
}

.status-indicator.recent {
  border: 2px solid #ffff00;
  color: #ffff00;
  box-shadow: 0 0 20px #ffff00;
}

.status-indicator.inactive {
  border: 2px solid #ff4444;
  color: #ff4444;
  box-shadow: 0 0 20px #ff4444;
}

.status-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
  animation: glowMove 2s infinite;
}

/* Event Info */
.event-info {
  display: flex;
  justify-content: center;
  gap: 3rem;
  margin-bottom: 2rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 1.2rem;
  text-transform: uppercase;
  letter-spacing: 0.1rem;
}

.neon-icon {
  font-size: 1.5rem;
  filter: drop-shadow(0 0 5px currentColor);
}

/* Buttons */
.neon-btn {
  position: relative;
  padding: 1.2rem 2.5rem;
  border: none;
  background: transparent;
  color: white;
  font-size: 1.1rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.1rem;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
}

.neon-btn.blue {
  border: 2px solid #00ffff;
  box-shadow: 
    0 0 10px #00ffff,
    inset 0 0 10px #00ffff;
}

.neon-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
  transition: left 0.5s ease;
}

.neon-btn:hover .neon-glow {
  left: 100%;
}

.neon-btn:hover {
  transform: translateY(-2px);
}

.neon-btn.blue:hover {
  box-shadow: 
    0 0 20px #00ffff,
    0 0 40px #00ffff,
    inset 0 0 20px #00ffff;
}

/* Animations */
@keyframes glitch {
  0%, 100% { transform: translate(0); }
  20% { transform: translate(-2px, 2px); }
  40% { transform: translate(-2px, -2px); }
  60% { transform: translate(2px, 2px); }
  80% { transform: translate(2px, -2px); }
}

@keyframes gridMove {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

@keyframes glowMove {
  0% { left: -100%; }
  100% { left: 100%; }
}

/* Responsive */
@media (max-width: 768px) {
  .main-title {
    font-size: 3rem;
  }
  
  .hero-subtitle {
    font-size: 1rem;
  }
  
  .event-info {
    flex-direction: column;
    gap: 1rem;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .section-title {
    font-size: 1.2rem;
  }
  
  .status-indicator {
    font-size: 1rem;
    padding: 0.8rem 1.5rem;
  }
}
</style>