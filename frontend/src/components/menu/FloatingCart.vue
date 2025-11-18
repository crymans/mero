<template>
  <div class="floating-cart" :class="{ 'has-items': props.itemCount > 0 }" @click="$emit('toggleCart')">
    <!-- Основная кнопка корзины -->
    <div class="cart-button">
      <div class="cart-icon">
        <span class="icon">🛒</span>
        <div class="pulse-effect" v-if="props.itemCount > 0"></div>
      </div>
      
      <div class="cart-info">
        <div class="total-price">{{ formattedTotal }} ₽</div>
        <div class="item-count">{{ props.itemCount }} {{ itemText }}</div>
      </div>
      
      <div class="cart-arrow">
        <span class="arrow">›</span>
      </div>
    </div>

    <!-- Индикатор новых товаров -->
    <div class="new-item-indicator" v-if="props.itemCount > 0">
      <div class="indicator-dot"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Product } from '../../types'
import { computed } from 'vue'

interface Props {
  cart: {product: Product, quantity: number}[]
  cartTotal: number
  itemCount: number
}

const props = defineProps<Props>()
defineEmits<{
  toggleCart: []
}>()

const formattedTotal = computed(() => {
  return props.cartTotal.toLocaleString('ru-RU')
})

const itemText = computed(() => {
  const count = props.itemCount
  if (count % 10 === 1 && count % 100 !== 11) return 'товар'
  if (count % 10 >= 2 && count % 10 <= 4 && (count % 100 < 10 || count % 100 >= 20)) return 'товара'
  return 'товаров'
})
</script>

<style scoped>
.floating-cart {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 1000;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.floating-cart.has-items {
  animation: cartBounce 0.6s ease;
}

.cart-button {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, #ff00ff, #00ffff);
  color: #000;
  border-radius: 50px;
  box-shadow: 
    0 8px 32px rgba(255, 0, 255, 0.3),
    0 2px 8px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.floating-cart:hover .cart-button {
  transform: translateY(-3px);
  box-shadow: 
    0 12px 40px rgba(255, 0, 255, 0.4),
    0 4px 12px rgba(0, 0, 0, 0.3);
}

.cart-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.6s ease;
}

.floating-cart:hover .cart-button::before {
  left: 100%;
}

.cart-icon {
  position: relative;
  font-size: 1.5rem;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pulse-effect {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.6);
  animation: pulse 2s infinite;
}

.cart-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.total-price {
  font-size: 1.3rem;
  font-weight: bold;
  line-height: 1;
  margin-bottom: 0.2rem;
}

.item-count {
  font-size: 0.8rem;
  opacity: 0.9;
  font-weight: 600;
}

.cart-arrow {
  font-size: 1.5rem;
  font-weight: bold;
  transition: transform 0.3s ease;
}

.floating-cart:hover .cart-arrow {
  transform: translateX(3px);
}

.new-item-indicator {
  position: absolute;
  top: -5px;
  right: -5px;
}

.indicator-dot {
  width: 12px;
  height: 12px;
  background: #ff4444;
  border-radius: 50%;
  border: 2px solid #000;
  animation: blink 1.5s infinite;
}

@keyframes cartBounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  70% {
    transform: scale(1.5);
    opacity: 0;
  }
  100% {
    transform: scale(1.5);
    opacity: 0;
  }
}

@keyframes blink {
  0%, 50% {
    opacity: 1;
  }
  51%, 100% {
    opacity: 0.3;
  }
}

/* Адаптивность */
@media (max-width: 768px) {
  .floating-cart {
    bottom: 1rem;
    right: 1rem;
    left: 1rem;
  }
  
  .cart-button {
    padding: 0.8rem 1.2rem;
    gap: 0.8rem;
  }
  
  .cart-icon {
    font-size: 1.3rem;
    width: 35px;
    height: 35px;
  }
  
  .total-price {
    font-size: 1.1rem;
  }
  
  .item-count {
    font-size: 0.7rem;
  }
}

@media (max-width: 480px) {
  .floating-cart {
    bottom: 0.5rem;
    right: 0.5rem;
    left: 0.5rem;
  }
  
  .cart-button {
    padding: 0.7rem 1rem;
    gap: 0.6rem;
  }
  
  .total-price {
    font-size: 1rem;
  }
}
</style>