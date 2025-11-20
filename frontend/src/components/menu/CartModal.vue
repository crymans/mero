<template>
  <div class="cart-modal-overlay" @click.self="$emit('close')">
    <div class="cart-modal">
      <!-- Заголовок -->
      <div class="modal-header">
        <h2>🛒 Ваш заказ</h2>
        <button class="close-btn" @click="$emit('close')">
          <span class="close-icon">×</span>
        </button>
      </div>

      <!-- Содержимое корзины -->
      <div class="modal-content">
        <div v-if="props.cart.length === 0" class="empty-cart">
          <div class="empty-icon">🛒</div>
          <h3>Корзина пуста</h3>
          <p>Добавьте товары из меню</p>
        </div>

        <div v-else class="cart-content">
          <!-- Поле ввода номера стола -->
          <div class="table-input-section">
            <label class="table-label">
              <span class="label-icon">🪑</span>
              <span class="label-text">Номер вашего стола, барная стойка - 4 номер</span>
            </label>
            <div class="table-input-container">
              <input 
                v-model="tableNumber"
                type="number"
                min="1"
                max="4"
                placeholder="Введите 1-4"
                class="table-input"
                :class="{ error: tableError }"
                @input="validateTableNumber"
              />
              <!-- <div class="table-hint">Столы от 1 до 4</div> -->
              <div v-if="tableError" class="error-message">{{ tableError }}</div>
            </div>
          </div>

          <!-- Список товаров -->
          <div class="cart-items">
            <div 
              v-for="item in props.cart" 
              :key="item.product.id"
              class="cart-item"
            >
              <div class="item-image">
                <div class="image-mini" :class="item.product.category">
                  {{ getCategoryEmoji(item.product.category) }}
                </div>
              </div>
              
              <div class="item-details">
                <h4 class="item-name">{{ item.product.name }}</h4>
                <p class="item-desc">{{ item.product.description }}</p>
                
                <!-- Общая стоимость товара внутри плашки -->
                <div class="item-price-section">
                  <div class="price-per-item">{{ item.product.price }} ₽ × {{ item.quantity }}</div>
                  <div class="item-total-mini">{{ (item.product.price * item.quantity).toLocaleString('ru-RU') }} ₽</div>
                </div>
              </div>
              
              <div class="item-controls">
                <button class="control-btn" @click="$emit('decreaseQuantity', item.product.id)">
                  <span class="control-icon">−</span>
                </button>
                <span class="quantity">{{ item.quantity }}</span>
                <button class="control-btn" @click="$emit('increaseQuantity', item.product.id)">
                  <span class="control-icon">+</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Футер с итогами -->
      <div v-if="props.cart.length > 0" class="modal-footer">
        <div class="total-section">
          <div class="total-line">
            <span>Товары:</span>
            <span>{{ props.cart.reduce((sum, item) => sum + item.quantity, 0) }} шт</span>
          </div>
          <div class="total-line main">
            <span class="total-label">Общая сумма:</span>
            <span class="total-amount">{{ props.cartTotal.toLocaleString('ru-RU') }} ₽</span>
          </div>
        </div>
        
        <button 
          class="order-btn" 
          @click="handlePlaceOrder"
          :disabled="!isTableValid"
          :class="{ disabled: !isTableValid }"
        >
          <span class="order-icon">🚀</span>
          <span class="order-text">
            {{ isTableValid ? 'ОФОРМИТЬ ЗАКАЗ' : 'УКАЖИТЕ НОМЕР СТОЛА' }}
          </span>
          <div class="btn-glow"></div>
        </button>
        
        <!-- <div class="delivery-info">
          <span class="info-icon">⏱️</span>
          <span>Доставка к столику за 10-15 минут</span>
        </div> -->
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Product } from '../../types'
import { ref, computed } from 'vue'

interface Props {
  cart: {product: Product, quantity: number}[]
  cartTotal: number
}

const props = defineProps<Props>()
const emit = defineEmits<{
  increaseQuantity: [productId: number]
  decreaseQuantity: [productId: number]
  placeOrder: [tableNumber: number]
  close: []
}>()

const tableNumber = ref<number | null>(null)
const tableError = ref<string>('')

const isTableValid = computed(() => {
  return tableNumber.value !== null && tableNumber.value >= 1 && tableNumber.value <= 4
})

const validateTableNumber = () => {
  if (tableNumber.value === null || tableNumber.value === 0) {
    tableError.value = 'Введите номер стола'
    return
  }

  if (tableNumber.value < 1 || tableNumber.value > 4) {
    tableError.value = 'Номер стола должен быть от 1 до 4'
    return
  }

  tableError.value = ''
}

const handlePlaceOrder = () => {
  window.Telegram.WebApp.HapticFeedback.impactOccurred('soft')
  if (!isTableValid.value) {
    tableError.value = 'Пожалуйста, укажите номер стола'
    return
  }

  emit('placeOrder', tableNumber.value!)
}

const getCategoryEmoji = (category: string) => {
  const emojis: {[key: string]: string} = {
    drink: '🍹',
    food: '🍔'
  }
  return emojis[category] || '📦'
}
</script>

<style scoped>
.cart-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 1rem;
  animation: fadeIn 0.3s ease;
}

.cart-modal {
  background: linear-gradient(135deg, #1a1a1a, #0a0a0a);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  width: 100%;
  max-width: 500px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  animation: slideUp 0.3s ease;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header h2 {
  margin: 0;
  color: #00ffff;
  font-size: 1.5rem;
}

.close-btn {
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
  transition: all 0.3s ease;
  font-size: 1.5rem;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: rotate(90deg);
}

.modal-content {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}

.empty-cart {
  text-align: center;
  padding: 3rem 2rem;
  color: #666;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-cart h3 {
  margin: 0 0 0.5rem 0;
  color: #ccc;
}

.empty-cart p {
  margin: 0;
  font-size: 0.9rem;
}

.cart-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Стили для ввода номера стола */
.table-input-section {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.table-label {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin-bottom: 1rem;
  font-weight: 600;
  color: #fff;
  font-size: 1.1rem;
}

.label-icon {
  font-size: 1.3rem;
}

.table-input-container {
  position: relative;
}

.table-input {
  width: 100%;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  color: #fff;
  font-size: 1.1rem;
  font-weight: bold;
  text-align: center;
  transition: all 0.3s ease;
}

.table-input:focus {
  outline: none;
  border-color: #00ffff;
  background: rgba(0, 255, 255, 0.1);
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
}

.table-input::placeholder {
  color: #888;
  font-weight: normal;
}

.table-input.error {
  border-color: #ff4444;
  background: rgba(255, 68, 68, 0.1);
}

.table-hint {
  margin-top: 0.5rem;
  color: #888;
  font-size: 0.8rem;
  text-align: center;
}

.error-message {
  color: #ff4444;
  font-size: 0.8rem;
  margin-top: 0.5rem;
  text-align: center;
  font-weight: 600;
}

.cart-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.cart-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.2rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.cart-item:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.2);
}

.item-image {
  flex-shrink: 0;
}

.image-mini {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.image-mini.drink {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.image-mini.food {
  background: linear-gradient(135deg, #f093fb, #f5576c);
}

.item-details {
  flex: 1;
  min-width: 0;
}

.item-name {
  color: #fff;
  font-weight: 600;
  margin: 0 0 0.3rem 0;
  font-size: 1rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-desc {
  color: #888;
  font-size: 0.8rem;
  margin: 0 0 0.8rem 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-price-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.05);
  padding: 0.5rem 0.8rem;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.price-per-item {
  color: #ccc;
  font-size: 0.8rem;
}

.item-total-mini {
  color: #00ffff;
  font-weight: bold;
  font-size: 0.9rem;
}

.item-controls {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin: 0 0.5rem;
}

.control-btn {
  width: 32px;
  height: 32px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  background: transparent;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.control-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: #00ffff;
}

.control-icon {
  font-size: 1.2rem;
  font-weight: bold;
  line-height: 1;
}

.quantity {
  min-width: 30px;
  text-align: center;
  font-weight: bold;
  color: #fff;
  font-size: 1rem;
}

.modal-footer {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1.5rem;
  background: rgba(0, 0, 0, 0.3);
}

.total-section {
  margin-bottom: 1.5rem;
}

.total-line {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  color: #ccc;
  font-size: 0.9rem;
}

.total-line.main {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.total-label {
  color: #fff;
  font-size: 1.1rem;
  font-weight: 600;
}

.total-amount {
  color: #00ffff;
  font-size: 1.5rem;
  font-weight: bold;
}

.order-btn {
  position: relative;
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
  overflow: hidden;
  margin-bottom: 1rem;
}

.order-btn:hover:not(.disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(255, 0, 255, 0.4);
}

.order-btn.disabled {
  background: #666;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.order-btn.disabled:hover {
  transform: none;
  box-shadow: none;
}

.order-icon {
  font-size: 1.3rem;
}

.order-text {
  font-size: 1rem;
  font-weight: 700;
}

.btn-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  transition: left 0.5s ease;
}

.order-btn:hover:not(.disabled) .btn-glow {
  left: 100%;
}

.delivery-info {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: #00ff00;
  font-size: 0.8rem;
  text-align: center;
}

.info-icon {
  font-size: 1rem;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Адаптивность */
@media (max-width: 768px) {
  .cart-modal {
    max-height: 90vh;
    margin: 0;
    border-radius: 20px 20px 0 0;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    max-width: none;
    animation: slideUpMobile 0.3s ease;
  }
  
  .cart-modal-overlay {
    align-items: flex-end;
    padding: 0;
  }
  
  .modal-header {
    padding: 1.2rem;
  }
  
  .modal-content {
    padding: 0.8rem;
  }
  
  .table-input-section {
    padding: 1.2rem;
  }
  
  .cart-item {
    padding: 1rem;
    gap: 0.8rem;
  }
  
  .item-details {
    min-width: 120px;
  }
  
  .item-name {
    font-size: 0.9rem;
  }
  
  .item-desc {
    font-size: 0.75rem;
  }
  
  .item-price-section {
    padding: 0.4rem 0.6rem;
  }
  
  .modal-footer {
    padding: 1.2rem;
  }
  
  .total-amount {
    font-size: 1.3rem;
  }
  
  .order-btn {
    padding: 1rem 1.5rem;
  }
}

@keyframes slideUpMobile {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}

/* Скрытие скроллбара для WebKit браузеров */
.modal-content::-webkit-scrollbar {
  width: 6px;
}

.modal-content::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

.modal-content::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 3px;
}

.modal-content::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}
</style>