<template>
  <div class="neon-party">
    <!-- Компонент загрузки -->
    <div v-if="userStore.isLoading" class="loading-overlay">
      <div class="loading-spinner"></div>
    </div>

    <!-- Компонент ошибки -->
    <div v-if="userStore.error" class="error-banner">
      {{ userStore.error }}
      <button @click="userStore.clearError()" class="close-btn">×</button>
    </div>

    <HeroSection style="margin-top: 10%;" 
      :user="userStore.user"
      :has-ticket="userStore.hasTicket"
      @scroll-to-tickets="scrollToTickets" 
      @scroll-to-tickets-vip="scrollToTicketsVip" 
    />
    <LineupSection />
    <TicketsSection 
      id="tickets" 
      :user="userStore.user"
      :ticket="userStore.ticket"
      :is-loading="userStore.isLoading"
      @buy-ticket="handleBuyTicket" 
    />
    <VipSection :is-vip="userStore.isVip" />
    <ContactSection />
    <FooterSection />
  </div>
</template>

<script setup lang="ts">
import HeroSection from '@/components/sections/Hero.vue'
import LineupSection from '@/components/sections/Lineup.vue'
import TicketsSection from '@/components/sections/Tickets.vue'
import VipSection from '@/components/sections/Vip.vue'
import ContactSection from '@/components/sections/Contact.vue'
import FooterSection from '@/components/sections/Footer.vue'
import { useUserStore } from '@/stores/user'
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const userStore = useUserStore()
const authStore = useAuthStore()

// Функция для получения telegram_id
const getTelegramId = (): string => {
  let telegramId = localStorage.getItem('telegram_id')
  
  if (!telegramId) {
    telegramId = prompt('Введите ваш Telegram ID (для демо):') || 'demo_user_' + Date.now()
    localStorage.setItem('telegram_id', telegramId)
  }
  
  return telegramId
}

onMounted(async () => {
  const telegramId = getTelegramId()
  await userStore.initializeUser(telegramId)
})

const scrollToTickets = () => {
  const element = document.getElementById('tickets')
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}
const scrollToTicketsVip = () => {
  const element = document.getElementById('ticketsvip')
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}

const handleBuyTicket = async (type: string) => {
  const telegramId = getTelegramId()
  
  try {
    await userStore.buyTicket(telegramId, type)
    console.log(`Successfully bought ${type} ticket`)
    
    // Можно показать уведомление об успехе
    alert(`Билет "${type}" успешно приобретен!`)
    
  } catch (error) {
    console.error('Failed to buy ticket:', error)
  }
}
</script>

<style>
/* Стили остаются без изменений */
.neon-party {
  background: #000;
  color: #fff;
  font-family: 'Arial', sans-serif;
  overflow-x: hidden;
  position: relative;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #333;
  border-top: 5px solid #00ffff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-banner {
  position: fixed;
  top: 15%;
  left: 50%;
  transform: translateX(-50%);
  background: #ff4444;
  color: white;
  padding: 12px 20px;
  border-radius: 8px;
  z-index: 1001;
  display: flex;
  align-items: center;
  gap: 10px;
  max-width: 400px;
  width: 90%;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
  padding: 0;
  margin-left: auto;
}
</style>