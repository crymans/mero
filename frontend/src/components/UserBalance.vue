<template>
  <!-- Блок баланса пользователя -->
  <div class="user-balance-section" style="width: 98%;">
    <div class="balance-card">
      <div class="balance-glow"></div>
      <div class="balance-header">
        <div class="balance-icon">⭐</div>
        <div class="balance-info">
          <h3 class="balance-title">ВАШ БАЛАНС</h3>
          <div class="balance-amount">{{ userStore.user.balance}}</div>
        </div>
      </div>
      
      <div class="top-up-section">
        <div class="input-group">
          <label for="starsAmount" class="input-label">Количество звезд:</label>
          <div class="input-wrapper">
            <input 
              id="starsAmount"
              v-model.number="starsAmount"
              type="number"
              min="1"
              max="10000"
              class="stars-input"
              placeholder="Введите количество"
              @keypress.enter="handleTopUp"
            />
            <div class="input-border"></div>
          </div>
        </div>
        
        <button 
          class="top-up-btn"
          :disabled="!isValidAmount"
          @click="handleTopUp"
        >
          <span class="btn-text">ПОПОЛНИТЬ</span>
          <span class="btn-glow"></span>
          <div class="btn-sparkle"></div>
        </button>
      </div>
      
      <div v-if="loading" class="loading-overlay">
        <div class="loading-spinner"></div>
        <span>Обработка...</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import {useUserStore} from '@/stores/user' 
import router from '../router';

const userStore = useUserStore()
// Props и emits
const props = defineProps<{
  balance: number
}>()

const emit = defineEmits<{
  topUp: [amount: number]
}>()

// Реактивные данные
const starsAmount = ref<number>(0)
const loading = ref<boolean>(false)

// Вычисляемые свойства
const isValidAmount = computed(() => {
  return starsAmount.value > 0 && starsAmount.value <= 100000
})

const purchasecallback = (param) =>{
  console.log(param)
  if(param == 'paid'){
    window.Telegram.WebApp.HapticFeedback.notificationOccurred('success')
  }
  else{
    window.Telegram.WebApp.HapticFeedback.notificationOccurred('error')
  }
  location.reload()
}

// Методы
const handleTopUp = async () => {
  window.Telegram.WebApp.HapticFeedback.impactOccurred('soft')
  if (!isValidAmount.value) return
  
  loading.value = true
  try {
    // Эмитируем событие с количеством звезд
    await userStore.createPurchase('122345', starsAmount.value)
    
    window.Telegram.WebApp.openInvoice(userStore.purchase_link, purchasecallback)
    // Сброс поля ввода после успешного запроса
    starsAmount.value = 0
  } catch (error) {
    console.error('Ошибка при пополнении:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.user-balance-section {
  max-width: 400px;
  margin: 0 auto 3rem;
}

.balance-card {
  position: relative;
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.08) 0%, 
    rgba(255, 255, 255, 0.03) 100%);
  border-radius: 20px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 215, 0, 0.3);
  transition: all 0.3s ease;
  overflow: hidden;
  min-height: 200px;
  display: flex;
  flex-direction: column;
}

.balance-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, 
    transparent, 
    rgba(255, 255, 255, 0.05), 
    transparent);
  transition: left 0.6s ease;
}

.balance-card:hover::before {
  left: 100%;
}

.balance-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  border-color: rgba(255, 215, 0, 0.5);
}

.balance-glow {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  border-radius: 22px;
  background: linear-gradient(45deg, 
    rgba(255, 215, 0, 0.1), 
    rgba(255, 255, 0, 0.05));
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
}

.balance-card:hover .balance-glow {
  opacity: 1;
}

.balance-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.balance-icon {
  font-size: 2.5rem;
  filter: drop-shadow(0 0 10px rgba(255, 215, 0, 0.5));
}

.balance-info {
  flex-grow: 1;
}

.balance-title {
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #aaa;
  margin-bottom: 0.3rem;
}

.balance-amount {
  font-size: 1.8rem;
  font-weight: bold;
  background: linear-gradient(45deg, #ffff00, #ffaa00);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 10px rgba(255, 255, 0, 0.3);
}

.top-up-section {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.input-label {
  font-size: 0.8rem;
  color: #ccc;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.input-wrapper {
  position: relative;
}

.stars-input {
  width: 100%;
  padding: 0.8rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  color: #fff;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.stars-input:focus {
  outline: none;
  border-color: rgba(255, 215, 0, 0.5);
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 0 10px rgba(255, 215, 0, 0.2);
}

.stars-input::placeholder {
  color: #666;
}

.input-border {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  border-radius: 12px;
  background: linear-gradient(45deg, #ffff00, #ffaa00);
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
}

.stars-input:focus + .input-border {
  opacity: 0.3;
}

.top-up-btn {
  position: relative;
  width: 100%;
  padding: 0.8rem;
  border: none;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
  background: linear-gradient(45deg, #cccc00, #ffff00);
  color: #000;
}

.top-up-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.top-up-btn:not(:disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 215, 0, 0.3);
}

.btn-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, 
    transparent, 
    rgba(255, 255, 255, 0.4), 
    transparent);
  transition: left 0.5s ease;
}

.top-up-btn:hover:not(:disabled) .btn-glow {
  left: 100%;
}

.btn-sparkle {
  position: absolute;
  width: 15px;
  height: 15px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  opacity: 0;
  transition: all 0.3s ease;
}

.top-up-btn:hover:not(:disabled) .btn-sparkle {
  animation: sparkle 0.6s ease-out;
}

@keyframes sparkle {
  0% {
    opacity: 0;
    transform: scale(0) rotate(0deg);
  }
  50% {
    opacity: 1;
    transform: scale(1) rotate(180deg);
  }
  100% {
    opacity: 0;
    transform: scale(0) rotate(360deg);
  }
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(5px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  border-radius: 20px;
  z-index: 10;
}

.loading-spinner {
  width: 30px;
  height: 30px;
  border: 3px solid rgba(255, 215, 0, 0.3);
  border-top: 3px solid #ffff00;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-overlay span {
  color: #ffff00;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* Адаптивность */
@media (max-width: 768px) {
  .user-balance-section {
    max-width: 100%;
    margin: 0 auto 2rem;
  }
  
  .balance-card {
    padding: 1.2rem;
    min-height: 180px;
  }
  
  .balance-header {
    gap: 0.8rem;
  }
  
  .balance-icon {
    font-size: 2rem;
  }
  
  .balance-amount {
    font-size: 1.5rem;
  }
  
  .top-up-section {
    gap: 1rem;
  }
}

@media (min-width: 1024px) {
  .user-balance-section {
    max-width: 350px;
  }
}
</style>