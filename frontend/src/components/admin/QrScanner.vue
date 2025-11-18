<!-- components/admin/RealQrScanner.vue -->
<template>
  <div class="real-qr-scanner">
    <div class="scanner-header">
      <h2>📱 Сканирование QR-кодов</h2>
      <p>Наведите камеру на QR-код билета для проверки</p>
      
      <!-- Отладочная информация -->
      <div class="debug-info">
        <p><strong>Отладка:</strong></p>
        <p>Telegram ID: {{ authStore.telegramId }}</p>
        <p>User Role: {{ authStore.userRole }}</p>
        <p>Is Authenticated: {{ authStore.isAuthenticated }}</p>
        <p>API Service: {{ apiService ? 'Создан' : 'Не создан' }}</p>
      </div>
    </div>

    <!-- Остальной код без изменений -->
    <div v-if="cameraError" class="camera-error">
      <div class="error-icon">📵</div>
      <h3>Ошибка доступа к камере</h3>
      <p>{{ cameraError }}</p>
      <button @click="initCamera" class="retry-btn">Повторить</button>
    </div>

    <div v-else-if="!isCameraActive" class="camera-inactive">
      <div class="camera-placeholder">
        <div class="placeholder-icon">📷</div>
        <p>Камера не активирована</p>
        <button @click="initCamera" class="start-btn">Запустить сканер</button>
      </div>
    </div>

    <div v-else class="scanner-container">
      <div class="scanner-wrapper">
        <qrcode-stream 
          :camera="cameraState"
          @decode="onDecode"
          @error="onCameraError"
          :track="paintOutline"
        >
          <div class="scanner-overlay">
            <div class="scan-frame"></div>
            <div class="scan-line" :class="{ scanning: isScanning }"></div>
          </div>
        </qrcode-stream>
        
        <div class="scanner-controls">
          <button @click="toggleCamera" class="control-btn">
            {{ cameraState === 'on' ? '⏸️' : '▶️' }}
          </button>
          <button @click="switchCamera" class="control-btn" v-if="hasMultipleCameras">
            🔄
          </button>
          <button @click="stopCamera" class="control-btn stop-btn">
            ⏹️
          </button>
        </div>
      </div>

      <div v-if="scannedTicket" class="scan-results">
        <div class="ticket-card" :class="{ used: scannedTicket.is_used }">
          <div class="ticket-header">
            <h3>Билет #{{ scannedTicket.id }}</h3>
            <span class="ticket-status" :class="scannedTicket.is_used ? 'used' : 'active'">
              {{ scannedTicket.is_used ? 'Использован' : 'Активен' }}
            </span>
          </div>
          
          <div class="ticket-details">
            <div class="detail-row">
              <span class="label">QR код:</span>
              <span class="value">{{ scannedTicket.qr_code }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Цена:</span>
              <span class="value">₽{{ scannedTicket.price }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Владелец:</span>
              <span class="value">ID {{ scannedTicket.user_id }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Создан:</span>
              <span class="value">{{ formatDate(scannedTicket.created_at) }}</span>
            </div>
          </div>

          <div class="ticket-actions">
            <button 
              v-if="!scannedTicket.is_used"
              @click="markTicketAsUsed"
              :disabled="isLoading"
              class="mark-used-btn"
            >
              <span v-if="isLoading" class="loading-spinner-small"></span>
              {{ isLoading ? 'Обработка...' : 'Отметить использованным' }}
            </button>
            
            <button 
              v-else
              disabled
              class="already-used-btn"
            >
              ✅ Билет уже использован
            </button>
            
            <button @click="clearScan" class="scan-again-btn">
              Сканировать следующий
            </button>
          </div>
        </div>
      </div>

      <div v-if="scanHistory.length > 0" class="scan-history">
        <h4>История сканирований (последние 5):</h4>
        <div class="history-list">
          <div 
            v-for="item in scanHistory" 
            :key="item.ticket.id + item.timestamp"
            class="history-item"
          >
            <span class="history-time">{{ formatTime(item.timestamp) }}</span>
            <span class="history-ticket">Билет #{{ item.ticket.id }}</span>
            <span class="history-status" :class="item.ticket.is_used ? 'used' : 'active'">
              {{ item.ticket.is_used ? 'Использован' : 'Активен' }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showNotification" class="scan-notification" :class="notificationType">
      <span class="notification-icon">{{ notificationIcon }}</span>
      <span class="notification-text">{{ notificationMessage }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { QrcodeStream } from 'vue-qrcode-reader'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'
import { createApiService } from '@/services/api'
import type { Ticket } from '@/types'

const authStore = useAuthStore()
const userStore = useUserStore()

// Создаем API service с актуальным telegramId
const apiService = computed(() => {
  const telegramId = authStore.telegramId || userStore.user?.telegram_id
  console.log('Creating API service with Telegram ID:', telegramId)
  return createApiService(telegramId || '')
})

// Состояние камеры
const isCameraActive = ref(false)
const cameraState = ref<'on' | 'off'>('off')
const cameraError = ref<string>('')
const hasMultipleCameras = ref(false)

// Сканирование
const isScanning = ref(false)
const scannedTicket = ref<Ticket | null>(null)
const scanHistory = ref<Array<{ticket: Ticket, timestamp: number}>>([])

// UI состояния
const isLoading = ref(false)
const showNotification = ref(false)
const notificationMessage = ref('')
const notificationType = ref<'success' | 'error'>('success')
const notificationIcon = ref('')

// Функция для отрисовки рамки вокруг QR-кода
const paintOutline = (detectedCodes: any[], ctx: CanvasRenderingContext2D) => {
  for (const detectedCode of detectedCodes) {
    const [ firstPoint, ...otherPoints ] = detectedCode.cornerPoints
    
    ctx.strokeStyle = '#00ffff'
    ctx.lineWidth = 4
    ctx.beginPath()
    ctx.moveTo(firstPoint.x, firstPoint.y)
    
    for (const { x, y } of otherPoints) {
      ctx.lineTo(x, y)
    }
    
    ctx.lineTo(firstPoint.x, firstPoint.y)
    ctx.stroke()
  }
}

// Инициализация камеры
const initCamera = async () => {
  try {
    cameraError.value = ''
    
    // Проверяем доступность камеры
    const devices = await navigator.mediaDevices.enumerateDevices()
    const videoDevices = devices.filter(device => device.kind === 'videoinput')
    hasMultipleCameras.value = videoDevices.length > 1
    
    isCameraActive.value = true
    cameraState.value = 'on'
    isScanning.value = true
    
    console.log('Camera initialized successfully')
    
  } catch (error) {
    cameraError.value = 'Не удалось получить доступ к камере. Проверьте разрешения.'
    console.error('Camera error:', error)
  }
}

// Обработка сканирования QR-кода
const onDecode = async (decodedString: string) => {
  console.log('QR Code decoded:', decodedString)
  
  if (isLoading.value) return
  
  isScanning.value = false
  isLoading.value = true
  
  try {
    console.log('Making API request to get ticket by QR...')
    
    // Получаем информацию о билете
    const ticket = await apiService.value.getTicketByQr(decodedString)
    console.log('Ticket received:', ticket)
    
    scannedTicket.value = ticket
    
    // Добавляем в историю
    scanHistory.value.unshift({
      ticket,
      timestamp: Date.now()
    })
    
    // Ограничиваем историю 5 последними сканированиями
    if (scanHistory.value.length > 5) {
      scanHistory.value = scanHistory.value.slice(0, 5)
    }
    
    showNotificationMessage('success', '✅ Билет найден!', '🔍')
    
  } catch (error: any) {
    console.error('Scan error:', error)
    console.error('Error details:', error.message, error.response)
    showNotificationMessage('error', '❌ Билет не найден', '❌')
  } finally {
    isLoading.value = false
    // Возобновляем сканирование через секунду
    setTimeout(() => {
      isScanning.value = true
    }, 1000)
  }
}

// Отметка билета как использованного
const markTicketAsUsed = async () => {
  if (!scannedTicket.value) return
  
  isLoading.value = true
  
  try {
    console.log('Marking ticket as used:', scannedTicket.value.id)
    
    const updatedTicket = await apiService.value.markTicketUsed(scannedTicket.value.id)
    console.log('Ticket updated:', updatedTicket)
    
    scannedTicket.value = updatedTicket
    
    // Обновляем в истории
    const historyItem = scanHistory.value.find(item => 
      item.ticket.id === scannedTicket.value?.id
    )
    if (historyItem) {
      historyItem.ticket = updatedTicket
    }
    
    showNotificationMessage('success', '✅ Билет отмечен как использованный!', '✅')
    
  } catch (error: any) {
    console.error('Mark used error:', error)
    console.error('Error details:', error.message, error.response)
    showNotificationMessage('error', '❌ Ошибка при обновлении билета', '❌')
  } finally {
    isLoading.value = false
  }
}

// Обработка ошибок камеры
const onCameraError = (error: any) => {
  console.error('Camera error:', error)
  cameraError.value = 'Ошибка работы камеры. Проверьте подключение и разрешения.'
  isCameraActive.value = false
  cameraState.value = 'off'
}

// Управление камерой
const toggleCamera = () => {
  cameraState.value = cameraState.value === 'on' ? 'off' : 'on'
}

const switchCamera = async () => {
  showNotificationMessage('success', '🔄 Переключение камеры...', '🔄')
}

const stopCamera = () => {
  cameraState.value = 'off'
  isCameraActive.value = false
  scannedTicket.value = null
}

const clearScan = () => {
  scannedTicket.value = null
  isScanning.value = true
}

// Уведомления
const showNotificationMessage = (type: 'success' | 'error', message: string, icon: string) => {
  notificationType.value = type
  notificationMessage.value = message
  notificationIcon.value = icon
  showNotification.value = true
  
  setTimeout(() => {
    showNotification.value = false
  }, 3000)
}

// Форматирование дат
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('ru-RU')
}

const formatTime = (timestamp: number) => {
  return new Date(timestamp).toLocaleTimeString('ru-RU', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Жизненный цикл
onMounted(() => {
  console.log('QR Scanner mounted')
  console.log('Auth store:', authStore)
  console.log('User store:', userStore)
  
  // Автоматически запускаем камеру при монтировании
  initCamera()
})

onUnmounted(() => {
  // Выключаем камеру при размонтировании
  cameraState.value = 'off'
})
</script>

<style scoped>
.debug-info {
  margin: 1rem 0;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 0.8rem;
  color: #00ffff;
  text-align: left;
}

.debug-info p {
  margin: 0.2rem 0;
  font-family: monospace;
}

/* Остальные стили без изменений */
.real-qr-scanner {
  padding: 1rem;
  max-width: 100%;
}

.scanner-header {
  text-align: center;
  margin-bottom: 2rem;
}

.scanner-header h2 {
  color: #00ffff;
  margin: 0 0 0.5rem 0;
  font-size: 1.8rem;
}

.scanner-header p {
  color: #ccc;
  margin: 0;
}

.camera-error,
.camera-inactive {
  text-align: center;
  padding: 3rem 2rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.error-icon,
.placeholder-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.7;
}

.camera-error h3,
.camera-inactive p {
  color: #fff;
  margin: 0 0 1rem 0;
}

.camera-error p {
  color: #ccc;
  margin: 0 0 1.5rem 0;
}

.retry-btn,
.start-btn {
  background: linear-gradient(45deg, #00ffff, #0080ff);
  border: none;
  border-radius: 10px;
  color: #000;
  padding: 1rem 2rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-btn:hover,
.start-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 5px 15px rgba(0, 255, 255, 0.4);
}

.scanner-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.scanner-wrapper {
  position: relative;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  max-width: 500px;
  margin: 0 auto;
}

.scanner-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  display: flex;
  align-items: center;
  justify-content: center;
}

.scan-frame {
  width: 70%;
  height: 70%;
  border: 3px solid #00ffff;
  border-radius: 15px;
  box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.5);
  position: relative;
}

.scan-line {
  position: absolute;
  top: 10%;
  left: 10%;
  right: 10%;
  height: 3px;
  background: linear-gradient(90deg, transparent, #00ffff, transparent);
  opacity: 0;
}

.scan-line.scanning {
  opacity: 1;
  animation: scan 2s linear infinite;
}

@keyframes scan {
  0% {
    top: 10%;
  }
  50% {
    top: 90%;
  }
  100% {
    top: 10%;
  }
}

.scanner-controls {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 1rem;
}

.control-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 1.2rem;
  transition: all 0.3s ease;
}

.control-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

.stop-btn:hover {
  background: rgba(255, 0, 0, 0.2);
  border-color: #ff4444;
}

.scan-results {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.ticket-card {
  background: rgba(255, 255, 255, 0.02);
  border-radius: 10px;
  padding: 1.5rem;
  border-left: 4px solid #00ff00;
}

.ticket-card.used {
  border-left-color: #ff4444;
  opacity: 0.7;
}

.ticket-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.ticket-header h3 {
  color: #fff;
  margin: 0;
}

.ticket-status {
  padding: 0.3rem 0.8rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
}

.ticket-status.active {
  background: rgba(0, 255, 0, 0.2);
  color: #00ff00;
}

.ticket-status.used {
  background: rgba(255, 0, 0, 0.2);
  color: #ff4444;
}

.ticket-details {
  margin-bottom: 1.5rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.detail-row:last-child {
  border-bottom: none;
}

.label {
  color: #ccc;
  font-weight: 600;
}

.value {
  color: #fff;
}

.ticket-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.mark-used-btn,
.already-used-btn,
.scan-again-btn {
  flex: 1;
  padding: 1rem;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 200px;
}

.mark-used-btn {
  background: linear-gradient(45deg, #00ff00, #00cc00);
  color: #000;
}

.mark-used-btn:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 5px 15px rgba(0, 255, 0, 0.4);
}

.mark-used-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.already-used-btn {
  background: rgba(255, 255, 255, 0.1);
  color: #ccc;
  cursor: not-allowed;
}

.scan-again-btn {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.scan-again-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.loading-spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid #000;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  display: inline-block;
  margin-right: 0.5rem;
}

.scan-history {
  background: rgba(255, 255, 255, 0.02);
  border-radius: 15px;
  padding: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.scan-history h4 {
  color: #fff;
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.8rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  font-size: 0.9rem;
}

.history-time {
  color: #00ffff;
  font-weight: 600;
}

.history-ticket {
  color: #fff;
}

.history-status {
  padding: 0.2rem 0.6rem;
  border-radius: 10px;
  font-size: 0.8rem;
  font-weight: 600;
}

.history-status.active {
  background: rgba(0, 255, 0, 0.2);
  color: #00ff00;
}

.history-status.used {
  background: rgba(255, 0, 0, 0.2);
  color: #ff4444;
}

.scan-notification {
  position: fixed;
  top: 20px;
  right: 20px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 10px;
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.8rem;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  animation: slideIn 0.3s ease;
}

.scan-notification.success {
  border-left: 4px solid #00ff00;
}

.scan-notification.error {
  border-left: 4px solid #ff4444;
}

.notification-icon {
  font-size: 1.2rem;
}

.notification-text {
  color: #000;
  font-weight: 600;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .scanner-wrapper {
    max-width: 100%;
  }
  
  .ticket-actions {
    flex-direction: column;
  }
  
  .mark-used-btn,
  .already-used-btn,
  .scan-again-btn {
    min-width: auto;
  }
   
  .history-item {
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
  }
  
  .scan-notification {
    left: 20px;
    right: 20px;
    top: 10px;
  }
}
</style>