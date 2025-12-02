<template>
  <div class="profile-page">
    <div class="container">
      <!-- Заголовок -->
      <div class="profile-header">
        <h1>👤 МОЙ ПРОФИЛЬ</h1>
        <p>Управление вашими данными и билетами</p>
      </div>

      <!-- Состояние загрузки -->
      <div v-if="userStore.isLoading || ordersStore.isLoading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>Загружаем данные...</p>
      </div>

      <!-- Ошибка -->
      <div v-if="userStore.error" class="error-state">
        <p>Ошибка: {{ userStore.error }}</p>
        <button @click="loadUserData" class="retry-btn">Попробовать снова</button>
      </div>

      <div v-if="!userStore.isLoading && userStore.user" class="profile-content">
        <!-- Левая колонка - QR код и статус -->
        <div class="profile-left">
          <!-- QR код -->
          <div class="qr-section">
            <h3>🎫 ВАШ БИЛЕТ</h3>
            <div class="qr-container">
              <div v-if="userStore.ticket && userStore.qrCodeUrl" class="qr-code" @click="openFullscreenQR">
                <img 
                  :src="userStore.qrCodeUrl" 
                  :alt="`QR Code: ${userStore.ticket.qr_code}`"
                  class="qr-image"
                  @load="handleImageLoad"
                  @error="handleImageError"
                />
                <div class="qr-overlay">
                  <span class="zoom-icon">🔍</span>
                  <span class="zoom-text">Нажмите для увеличения</span>
                </div>
                <div v-if="imageLoading" class="qr-loading">
                  <div class="loading-spinner-small"></div>
                  <p>Загружаем QR-код...</p>
                </div>
              </div>
              <div v-else-if="userStore.ticket && !userStore.qrCodeUrl" class="qr-code-fallback">
                <div class="qr-fallback-content">
                  <div class="qr-fallback-text">{{ userStore.ticket.qr_code }}</div>
                  <div class="qr-fallback-hint">QR-код для сканирования</div>
                </div>
                <div class="qr-overlay">
                  <span class="zoom-icon">🔍</span>
                  <span class="zoom-text">Нажмите для просмотра</span>
                </div>
              </div>
              <div v-else class="no-ticket">
                <div class="no-ticket-icon">🎫</div>
                <h4>Билет не приобретен</h4>
                <p>Купите билет чтобы получить QR-код</p>
                <button class="buy-ticket-btn" @click="goToTickets">
                  КУПИТЬ БИЛЕТ
                </button>
              </div>
            </div>
            
            <!-- Информация о билете -->
            <div v-if="userStore.ticket" class="ticket-info">
              <div class="ticket-info-item">
                <span class="info-label">Код билета:</span>
                <span class="info-value ticket-code">{{ userStore.ticket.qr_code }}</span>
              </div>
              <div class="ticket-info-item">
                <span class="info-label">Статус:</span>
                <span class="info-value" :class="userStore.ticket.is_used ? 'used' : 'active'">
                  {{ userStore.ticket.is_used ? 'Использован' : 'Активен' }}
                </span>
              </div>
              <div class="ticket-info-item">
                <span class="info-label">Тип:</span>
                <span class="info-value">{{ ticketType }}</span>
              </div>
              <div class="ticket-info-item">
                <span class="info-label">Стоимость:</span>
                <span class="info-value">{{ userStore.ticket.price }} stars</span>
              </div>
              <div class="ticket-info-item">
                <span class="info-label">Приобретен:</span>
                <span class="info-value">{{ formatDate(userStore.ticket.created_at) }}</span>
              </div>
            </div>
          </div>

          <!-- Статус гостя -->
          <div class="status-section">
            <h3>⭐ СТАТУС ГОСТЯ</h3>
            <div class="status-card" :class="userStatus">
              <div class="status-icon">
                <span v-if="userStatus === 'vip'">👑</span>
                <span v-else-if="userStatus === 'standard'">🎫</span>
                <span v-else>🚫</span>
              </div>
              <div class="status-info">
                <div class="status-title">{{ statusTitle }}</div>
                <div class="status-desc">{{ statusDescription }}</div>
                <div v-if="userStore.ticket" class="status-benefits">
                  <div v-for="benefit in statusBenefits" :key="benefit" class="benefit-item">
                    <span class="benefit-icon">✓</span>
                    <span class="benefit-text">{{ benefit }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Правая колонка - контактные данные -->
        <div class="profile-right">
          <!-- Контактные данные -->
          <div class="contact-section">
            <h3>📝 КОНТАКТНЫЕ ДАННЫЕ</h3>
            <div class="contact-notice">
              <div class="notice-icon">⚠️</div>
              <div class="notice-text">
                При входе будут проверяться указанные данные и паспорт. 
                Убедитесь, что данные совпадают с документом.
              </div>
            </div>

            <form class="contact-form" @submit.prevent="saveContactInfo">
              <div class="form-row">
                <div class="form-group">
                  <label for="firstName">Имя *</label>
                  <input
                    id="firstName"
                    v-model="contactForm.first_name"
                    type="text"
                    required
                    placeholder="Введите ваше имя"
                  />
                </div>

                <div class="form-group">
                  <label for="lastName">Фамилия *</label>
                  <input
                    id="lastName"
                    v-model="contactForm.last_name"
                    type="text"
                    required
                    placeholder="Введите вашу фамилию"
                  />
                </div>
              </div>

              <div class="form-group">
                <label for="phone">Телефон *</label>
                <input
                  id="phone"
                  v-model="contactForm.phone"
                  type="tel"
                  required
                  placeholder="+7 (999) 999-99-99"
                  @input="formatPhone"
                />
              </div>

              <div class="form-actions">
                <button 
                  type="submit" 
                  class="save-btn" 
                  :disabled="!isFormValid || !isFormChanged || userStore.isLoading"
                >
                  <span class="btn-icon">💾</span>
                  <span class="btn-text">
                    {{ userStore.isLoading ? 'СОХРАНЕНИЕ...' : (isFormChanged ? 'СОХРАНИТЬ ИЗМЕНЕНИЯ' : 'ДАННЫЕ СОХРАНЕНЫ') }}
                  </span>
                </button>
              </div>
            </form>
          </div>

          <!-- История заказов -->
          <div class="orders-section">
            <h3>📦 ПОСЛЕДНИЕ ЗАКАЗЫ</h3>
            <div v-if="ordersStore.orders.length === 0" class="no-orders">
              <div class="no-orders-icon">📦</div>
              <p>У вас еще нет заказов</p>
              <button class="go-to-menu-btn" @click="goToMenu">
                ПЕРЕЙТИ В МЕНЮ
              </button>
            </div>
            <div v-else class="orders-list">
              <div 
                v-for="order in ordersStore.orders" 
                :key="order.id"
                class="order-item"
              >
                <div class="order-info">
                  <div class="order-header">
                    <span class="order-id">Заказ #{{ order.id }}</span>
                    <span class="order-table">Стол {{ order.table_id }}</span>
                  </div>
                  <div class="order-products">
                    <div 
                      v-for="item in getOrderProducts(order)" 
                      :key="item.product?.id"
                      class="product-item"
                    >
                      <span class="product-name">{{ item.product?.name || 'Неизвестный товар' }}</span>
                      <span class="product-quantity">×{{ item.quantity }}</span>
                    </div>
                  </div>
                  <div class="order-meta">
                    <span class="order-total">{{ order.total_price }} stars</span>
                    <span class="order-date">{{ formatDate(order.created_at) }}</span>
                  </div>
                </div>
                <div class="order-status" :class="getOrderStatusClass(order)">
                  {{ getOrderStatusText(order) }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно полноэкранного QR-кода -->
    <div v-if="showFullscreenQR && userStore.ticket" class="qr-fullscreen-overlay" @click="closeFullscreenQR">
      <div class="qr-fullscreen-content" @click.stop>
        <button class="close-fullscreen-btn" @click="closeFullscreenQR">
          <span class="close-icon">×</span>
        </button>
        
        <div class="fullscreen-qr-container">
          <div class="fullscreen-qr-code">
            <div v-if="userStore.fullscreenQrCodeUrl" class="qr-image-container">
              <img 
                :src="userStore.fullscreenQrCodeUrl" 
                :alt="`QR Code: ${userStore.ticket.qr_code}`"
                class="fullscreen-qr-image"
                @load="handleFullscreenImageLoad"
                @error="handleFullscreenImageError"
              />
              <div v-if="fullscreenImageLoading" class="fullscreen-qr-loading">
                <div class="loading-spinner"></div>
                <p>Загружаем QR-код...</p>
              </div>
            </div>
            <div v-else class="fullscreen-qr-fallback">
              <div class="fullscreen-qr-fallback-content">
                <div class="fullscreen-qr-fallback-text">{{ userStore.ticket.qr_code }}</div>
                <div class="fullscreen-qr-fallback-hint">Код билета для проверки</div>
              </div>
            </div>
          </div>
          
          <div class="qr-instructions">
            <h3>Информация о билете:</h3>
            <div class="ticket-details">
              <div class="ticket-detail-item">
                <span class="detail-label">Код:</span>
                <span class="detail-value">{{ userStore.ticket.qr_code }}</span>
              </div>
              <div class="ticket-detail-item">
                <span class="detail-label">Тип:</span>
                <span class="detail-value">{{ ticketType }}</span>
              </div>
              <div class="ticket-detail-item">
                <span class="detail-label">Статус:</span>
                <span class="detail-value" :class="userStore.ticket.is_used ? 'used' : 'active'">
                  {{ userStore.ticket.is_used ? 'Использован' : 'Активен' }}
                </span>
              </div>
            </div>
            
            <h3>Как использовать:</h3>
            <div class="instruction-steps">
              <div class="instruction-step">
                <span class="step-number">1</span>
                <span class="step-text">Покажите QR-код на входе для сканирования</span>
              </div>
              <div class="instruction-step">
                <span class="step-number">2</span>
                <span class="step-text">Убедитесь, что экран достаточно яркий</span>
              </div>
              <div class="instruction-step">
                <span class="step-number">3</span>
                <span class="step-text">QR-код должен быть полностью виден в кадре</span>
              </div>
            </div>
          </div>
          
          <button v-if="userStore.fullscreenQrCodeUrl" class="download-qr-btn" @click="downloadQRCode" :disabled="fullscreenImageLoading">
            <span class="download-icon">📥</span>
            <span class="download-text">СОХРАНИТЬ QR-КОД</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useOrdersStore } from '@/stores/orders'
import type { Order } from '@/types'

const router = useRouter()
const userStore = useUserStore()
const ordersStore = useOrdersStore()

// Состояния для загрузки изображений
const imageLoading = ref(true)
const fullscreenImageLoading = ref(true)
const showFullscreenQR = ref(false)

// Форма контактных данных
const contactForm = ref({
  first_name: '',
  last_name: '',
  phone: ''
})

const originalContactForm = ref({ ...contactForm.value })

// Получаем пользователя из хранилища
const user = computed(() => userStore.user)

// Вычисляемые свойства для статуса
const userStatus = computed(() => {
  if (!userStore.ticket) return 'none'
  if (userStore.ticket.price >= 650) return 'vip'
  if (userStore.ticket.price >= 450) return 'standard'
  return 'basic'
})

const ticketType = computed(() => {
  if (!userStore.ticket) return 'Нет билета'
  if (userStore.ticket.price >= 650) return 'VIP'
  if (userStore.ticket.price >= 450) return 'Стандарт'
  return 'Базовый'
})

const statusTitle = computed(() => {
  switch (userStatus.value) {
    case 'vip': return 'VIP ГОСТЬ'
    case 'standard': return 'СТАНДАРТ'
    case 'basic': return 'БАЗОВЫЙ'
    default: return 'НЕТ БИЛЕТА'
  }
})

const statusDescription = computed(() => {
  switch (userStatus.value) {
    case 'vip': return 'Премиум доступ ко всем зонам'
    case 'standard': return 'Стандартный вход на вечеринку'
    case 'basic': return 'Базовый доступ со скидкой'
    default: return 'Приобретите билет для получения статуса'
  }
})

const statusBenefits = computed(() => {
  switch (userStatus.value) {
    case 'vip':
      return [
        'Приоритетный вход',
        'VIP место с дополнительным меню',
        'Танцпол',
      ]
    case 'standard':
      return [
        'Быстрый вход',
        'Доступ к основному бару',
        'Танцпол',
        'Место стоя'
      ]
    case 'basic':
      return [
        'Экономичный вход',
        'Доступ к основному бару',
        'Танцпол',
        'Место стоя'
      ]
    default:
      return []
  }
})

const isFormValid = computed(() => {
  return contactForm.value.first_name.trim() !== '' && 
         contactForm.value.last_name.trim() !== '' && 
         contactForm.value.phone.trim() !== ''
})

const isFormChanged = computed(() => {
  return contactForm.value.first_name !== originalContactForm.value.first_name ||
         contactForm.value.last_name !== originalContactForm.value.last_name ||
         contactForm.value.phone !== originalContactForm.value.phone
})

// Методы
const loadUserData = async () => {
  const telegramId = getTelegramId()
  await userStore.initializeUser(telegramId)
  await ordersStore.fetchUserOrders(telegramId)
  await ordersStore.fetchProducts()
  
  if (userStore.user) {
    contactForm.value = {
      first_name: userStore.user.first_name || '',
      last_name: userStore.user.last_name || '',
      phone: userStore.user.phone || ''
    }
    originalContactForm.value = { ...contactForm.value }
  }
}

const saveContactInfo = async () => {
  try {
    const telegramId = getTelegramId()
    await userStore.updateProfile(telegramId, contactForm.value)
    originalContactForm.value = { ...contactForm.value }
    alert('✅ Данные успешно сохранены!')
  } catch (error) {
    console.error('Error saving contact info:', error)
    alert('❌ Ошибка при сохранении данных')
  }
}

const formatPhone = (event: Event) => {
  const input = event.target as HTMLInputElement
  let value = input.value.replace(/\D/g, '')
  
  if (value === '') {
    contactForm.value.phone = ''
    return
  }
  
  let countryCode = '7'
  if (value.startsWith('7') || value.startsWith('8')) {
    countryCode = '7'
    value = value.substring(1)
  }
  
  value = value.substring(0, 10)
  
  let formattedValue = '+7'
  
  if (value.length > 0) {
    formattedValue += ' (' + value.substring(0, 3)
  }
  if (value.length > 3) {
    formattedValue += ') ' + value.substring(3, 6)
  }
  if (value.length > 6) {
    formattedValue += '-' + value.substring(6, 8)
  }
  if (value.length > 8) {
    formattedValue += '-' + value.substring(8, 10)
  }
  
  contactForm.value.phone = formattedValue
}

// Обработчики загрузки изображений
const handleImageLoad = () => {
  imageLoading.value = false
}

const handleImageError = () => {
  imageLoading.value = false
  console.error('Failed to load QR code image')
}

const handleFullscreenImageLoad = () => {
  fullscreenImageLoading.value = false
}

const handleFullscreenImageError = () => {
  fullscreenImageLoading.value = false
  console.error('Failed to load fullscreen QR code image')
}

const openFullscreenQR = () => {
  if (userStore.ticket) {
    showFullscreenQR.value = true
    fullscreenImageLoading.value = true
    document.body.style.overflow = 'hidden'
  }
}

const closeFullscreenQR = () => {
  showFullscreenQR.value = false
  document.body.style.overflow = 'auto'
}

const downloadQRCode = async () => {
  if (!userStore.fullscreenQrCodeUrl) return
  
  try {
    const response = await fetch(userStore.fullscreenQrCodeUrl)
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `qr-code-${userStore.ticket?.qr_code || 'neon-party'}.png`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
    alert('✅ QR-код успешно сохранен!')
  } catch (error) {
    console.error('Error downloading QR code:', error)
    alert('❌ Ошибка при сохранении QR-кода')
  }
}

const goToTickets = () => {
  router.push('/')
  setTimeout(() => {
    const ticketsSection = document.getElementById('tickets')
    if (ticketsSection) {
      ticketsSection.scrollIntoView({ behavior: 'smooth' })
    }
  }, 100)
}

const goToMenu = () => {
  router.push('/menu')
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getOrderStatusClass = (order: Order) => {
  if (order.is_fulfilled) return 'completed'
  return 'preparing'
}

const getOrderStatusText = (order: Order) => {
  if (order.is_fulfilled) return 'ВЫПОЛНЕН'
  return 'ГОТОВИТСЯ'
}

const getOrderProducts = (order: Order) => {
  return ordersStore.getOrderProducts(order)
}

// Функция для получения telegram_id
const getTelegramId = (): string => {
  return window.Telegram.WebApp.initData
}

// Обработка клавиши Escape для закрытия полноэкранного режима
const handleKeydown = (event: KeyboardEvent) => {
  if (event.key === 'Escape' && showFullscreenQR.value) {
    closeFullscreenQR()
  }
}

onMounted(async () => {
  await loadUserData()
  document.addEventListener('keydown', handleKeydown)
})

// Убираем обработчик при размонтировании
import { onUnmounted } from 'vue'
onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
  document.body.style.overflow = 'auto'
})
</script>

<style scoped>
/* Добавляем новые стили для отображения кода билета */

.ticket-code {
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  background: rgba(255, 255, 255, 0.1);
  padding: 0.3rem 0.5rem;
  border-radius: 5px;
  word-break: break-all;
}

.qr-code-fallback {
  background: white;
  padding: 1rem;
  border-radius: 15px;
  display: inline-block;
  position: relative;
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
  min-height: 200px;
  min-width: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.qr-code-fallback:hover {
  transform: scale(1.02);
  box-shadow: 0 10px 30px rgba(0, 255, 255, 0.3);
}

.qr-code-fallback:hover .qr-overlay {
  opacity: 1;
}

.qr-fallback-content {
  text-align: center;
  color: #000;
}

.qr-fallback-text {
  font-family: 'Courier New', monospace;
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  word-break: break-all;
  max-width: 180px;
}

.qr-fallback-hint {
  font-size: 0.8rem;
  opacity: 0.8;
}

.fullscreen-qr-fallback {
  background: white;
  padding: 2rem;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  min-width: 400px;
}

.fullscreen-qr-fallback-content {
  text-align: center;
  color: #000;
}

.fullscreen-qr-fallback-text {
  font-family: 'Courier New', monospace;
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 1rem;
  word-break: break-all;
  max-width: 350px;
}

.fullscreen-qr-fallback-hint {
  font-size: 1rem;
  opacity: 0.8;
}

.ticket-details {
  margin: 1.5rem 0;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.ticket-detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.ticket-detail-item:last-child {
  border-bottom: none;
}

.detail-label {
  color: #ccc;
  font-weight: 600;
}

.detail-value {
  color: #fff;
  font-weight: 600;
}


.loading-state {
  text-align: center;
  padding: 3rem;
  color: #fff;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #333;
  border-top: 4px solid #00ffff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-state {
  text-align: center;
  padding: 2rem;
  background: rgba(255, 0, 0, 0.1);
  border: 1px solid rgba(255, 0, 0, 0.3);
  border-radius: 10px;
  margin: 2rem 0;
  color: #ff4444;
}

.retry-btn {
  background: linear-gradient(45deg, #00ffff, #0080ff);
  border: none;
  border-radius: 5px;
  color: white;
  padding: 10px 20px;
  margin-top: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
}

.no-orders {
  text-align: center;
  padding: 2rem;
}

.no-orders-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.no-orders p {
  color: #666;
  margin-bottom: 1.5rem;
}

.go-to-menu-btn {
  background: linear-gradient(135deg, #ff00ff, #ff0080);
  color: #000;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 10px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.go-to-menu-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 0, 255, 0.4);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.order-id {
  color: #fff;
  font-weight: bold;
  font-size: 0.9rem;
}

.order-table {
  color: #00ffff;
  font-size: 0.8rem;
  background: rgba(0, 255, 255, 0.1);
  padding: 0.2rem 0.5rem;
  border-radius: 10px;
}

.order-products {
  margin-bottom: 0.5rem;
}

.product-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.2rem 0;
  font-size: 0.8rem;
}

.product-name {
  color: #ccc;
}

.product-quantity {
  color: #888;
}

.order-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.7rem;
}

.order-total {
  color: #00ff00;
  font-weight: bold;
}

.order-date {
  color: #888;
}
.profile-page {
  padding: 2rem 1rem;
  min-height: calc(100vh - 70px);
  background: #000;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.profile-header {
  text-align: center;
  margin-bottom: 3rem;
}

.profile-header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  background: linear-gradient(45deg, #ff00ff, #00ffff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.profile-header p {
  color: #666;
  font-size: 1.1rem;
}

.profile-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

/* Левая колонка */
.profile-left {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.qr-section, .status-section, .contact-section, .orders-section {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  padding: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.qr-section h3, .status-section h3, .contact-section h3, .orders-section h3 {
  margin: 0 0 1.5rem 0;
  color: #00ffff;
  font-size: 1.3rem;
}

.qr-container {
  text-align: center;
}

.qr-code {
  background: white;
  padding: 1rem;
  border-radius: 15px;
  display: inline-block;
  position: relative;
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
}

.qr-code:hover {
  transform: scale(1.02);
  box-shadow: 0 10px 30px rgba(0, 255, 255, 0.3);
}

.qr-code:hover .qr-overlay {
  opacity: 1;
}

.qr-code img {
  width: 200px;
  height: 200px;
  border-radius: 10px;
  display: block;
}

.qr-placeholder {
  width: 200px;
  height: 200px;
  background: linear-gradient(45deg, #ff00ff, #00ffff);
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #000;
  font-weight: bold;
}

.qr-text {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  font-family: 'Courier New', monospace;
}

.qr-hint {
  font-size: 0.8rem;
  opacity: 0.8;
}

.qr-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 10px;
}

.zoom-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.zoom-text {
  font-size: 0.9rem;
  font-weight: bold;
}

.ticket-info {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.ticket-info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.ticket-info-item:last-child {
  border-bottom: none;
}

.info-label {
  color: #ccc;
  font-size: 0.9rem;
}

.info-value {
  font-weight: 600;
  color: #fff;
}

.info-value.active {
  color: #00ff00;
}

.info-value.used {
  color: #ff4444;
}

.info-value.paid {
  color: #00ff00;
}

.info-value.unpaid {
  color: #ff4444;
}

.no-ticket {
  padding: 2rem;
  text-align: center;
}

.no-ticket-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.no-ticket h4 {
  margin: 0 0 0.5rem 0;
  color: #fff;
}

.no-ticket p {
  margin: 0 0 1.5rem 0;
  color: #666;
}

.buy-ticket-btn {
  background: linear-gradient(135deg, #ff00ff, #ff0080);
  color: #000;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 10px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.buy-ticket-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 0, 255, 0.4);
}

/* Статус гостя */
.status-card {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1.5rem;
  border-radius: 15px;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.status-card.vip {
  border-color: #ff00ff;
  background: linear-gradient(135deg, rgba(255, 0, 255, 0.1), rgba(255, 0, 255, 0.05));
}

.status-card.standard {
  border-color: #00ffff;
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(0, 255, 255, 0.05));
}

.status-card.basic {
  border-color: #ffff00;
  background: linear-gradient(135deg, rgba(255, 255, 0, 0.1), rgba(255, 255, 0, 0.05));
}

.status-card.none {
  border-color: #666;
  background: rgba(255, 255, 255, 0.05);
}

.status-icon {
  font-size: 2.5rem;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  flex-shrink: 0;
}

.status-info {
  flex: 1;
}

.status-title {
  font-size: 1.3rem;
  font-weight: bold;
  color: #fff;
  margin-bottom: 0.3rem;
}

.status-desc {
  color: #ccc;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.status-benefits {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.benefit-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.benefit-icon {
  color: #00ff00;
  font-weight: bold;
  font-size: 0.9rem;
}

.benefit-text {
  color: #ccc;
  font-size: 0.8rem;
}

/* Правая колонка */
.profile-right {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.contact-notice {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  background: rgba(255, 255, 0, 0.1);
  border: 1px solid rgba(255, 255, 0, 0.3);
  border-radius: 10px;
  padding: 1rem;
  margin-bottom: 1.5rem;
}

.notice-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.notice-text {
  color: #ffff00;
  font-size: 0.9rem;
  line-height: 1.4;
}

.contact-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  color: #fff;
  font-weight: 600;
  font-size: 0.9rem;
}

.form-group input {
  padding: 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  color: #fff;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #00ffff;
  background: rgba(0, 255, 255, 0.1);
}

.form-group input::placeholder {
  color: #888;
}

.form-actions {
  margin-top: 1rem;
}

.save-btn {
  width: 100%;
  padding: 1.2rem;
  background: linear-gradient(135deg, #00ffff, #0080ff);
  color: #000;
  border: none;
  border-radius: 12px;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
}

.save-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 255, 255, 0.4);
}

.save-btn:disabled {
  background: #666;
  cursor: not-allowed;
  transform: none;
}

/* История заказов */
.orders-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.order-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.order-info {
  flex: 1;
}

.order-name {
  color: #fff;
  font-weight: 600;
  margin-bottom: 0.3rem;
}

.order-meta {
  color: #ccc;
  font-size: 0.8rem;
  margin-bottom: 0.3rem;
}

.order-date {
  color: #888;
  font-size: 0.7rem;
}

.order-status {
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: bold;
  text-transform: uppercase;
}

.order-status.pending {
  background: rgba(255, 255, 0, 0.2);
  color: #ffff00;
}

.order-status.preparing {
  background: rgba(0, 255, 255, 0.2);
  color: #00ffff;
}

.order-status.completed {
  background: rgba(0, 255, 0, 0.2);
  color: #00ff00;
}

/* Полноэкранный QR-код */
.qr-fullscreen-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.95);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  padding: 2rem;
  animation: fadeIn 0.3s ease;
}

.qr-fullscreen-content {
  background: linear-gradient(135deg, #1a1a1a, #0a0a0a);
  border-radius: 25px;
  border: 2px solid rgba(255, 255, 255, 0.2);
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  animation: scaleIn 0.3s ease;
}

.close-fullscreen-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: #fff;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  z-index: 1;
  transition: all 0.3s ease;
}

.close-fullscreen-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: rotate(90deg);
}

.fullscreen-qr-container {
  padding: 3rem 2rem 2rem;
  text-align: center;
}

.fullscreen-qr-code {
  background: white;
  padding: 2rem;
  border-radius: 20px;
  display: inline-block;
  margin-bottom: 2rem;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
}

.fullscreen-qr-code img {
  width: 300px;
  height: 300px;
  border-radius: 15px;
  display: block;
}

.fullscreen-qr-placeholder {
  width: 300px;
  height: 300px;
  background: linear-gradient(45deg, #ff00ff, #00ffff);
  border-radius: 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #000;
  font-weight: bold;
}

.fullscreen-qr-text {
  font-size: 2rem;
  margin-bottom: 1rem;
  font-family: 'Courier New', monospace;
}

.fullscreen-qr-hint {
  font-size: 1rem;
  opacity: 0.8;
}

.qr-instructions {
  margin-bottom: 2rem;
  text-align: left;
}

.qr-instructions h3 {
  color: #00ffff;
  margin-bottom: 1rem;
  text-align: center;
}

.instruction-steps {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.instruction-step {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.step-number {
  background: linear-gradient(135deg, #ff00ff, #00ffff);
  color: #000;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  flex-shrink: 0;
}

.step-text {
  color: #fff;
  font-size: 0.9rem;
}

.download-qr-btn {
  width: 100%;
  padding: 1.2rem 2rem;
  background: linear-gradient(135deg, #ff00ff, #ff0080);
  color: #000;
  border: none;
  border-radius: 15px;
  font-weight: bold;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
}

.download-qr-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(255, 0, 255, 0.4);
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* Адаптивность */
@media (max-width: 768px) {
  .profile-content {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .profile-header h1 {
    font-size: 2rem;
  }
  
  .qr-section, .status-section, .contact-section, .orders-section {
    padding: 1.2rem;
  }
  
  .status-card {
    padding: 1rem;
  }
  
  .status-icon {
    font-size: 2rem;
    width: 50px;
    height: 50px;
  }
  
  .contact-notice {
    padding: 0.8rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .form-group input {
    padding: 0.8rem;
  }
  
  .save-btn {
    padding: 1rem;
  }
  
  .qr-fullscreen-overlay {
    padding: 1rem;
  }
  
  .fullscreen-qr-container {
    padding: 2rem 1rem 1rem;
  }
  
  .fullscreen-qr-code {
    padding: 1rem;
  }
  
  .fullscreen-qr-code img {
    width: 250px;
    height: 250px;
  }
  
  .fullscreen-qr-placeholder {
    width: 250px;
    height: 250px;
  }
  
  .instruction-step {
    padding: 0.8rem;
  }
}

@media (max-width: 480px) {
  .profile-page {
    padding: 1rem 0.5rem;
  }
  
  .qr-code img {
    width: 150px;
    height: 150px;
  }
  
  .qr-placeholder {
    width: 150px;
    height: 150px;
  }
  
  .order-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.8rem;
  }
  
  .order-status {
    align-self: flex-end;
  }
  
  .fullscreen-qr-code img {
    width: 200px;
    height: 200px;
  }
  
  .fullscreen-qr-placeholder {
    width: 200px;
    height: 200px;
  }
}
</style>