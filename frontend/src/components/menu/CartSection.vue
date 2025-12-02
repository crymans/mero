<template>
  <div class="cart-section">
    <div class="cart-header">
      <h3>🛒 ВАША КОРЗИНА</h3>
      <div class="items-count">{{ cart.length }} позиций</div>
    </div>
    
    <div class="cart-items">
      <div 
        v-for="item in cart" 
        :key="item.product.id"
        class="cart-item"
      >
        <div class="item-image">
          <div class="image-mini" :class="item.product.category">
            {{ getCategoryEmoji(item.product.category) }}
          </div>
        </div>
        
        <div class="item-details">
          <span class="item-name">{{ item.product.name }}</span>
          <span class="item-price">{{ item.product.price }} stars/шт</span>
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
        
        <div class="item-total">
          {{ item.product.price * item.quantity }} stars
        </div>
      </div>
    </div>
    
    <div class="cart-footer">
      <div class="total-section">
        <div class="total-label">Общая сумма:</div>
        <div class="total-amount">{{ cartTotal }} stars</div>
      </div>
      
      <button class="order-btn" @click="$emit('placeOrder')">
        <span class="order-icon">🚀</span>
        <span class="order-text">ОФОРМИТЬ ЗАКАЗ</span>
        <div class="order-glow"></div>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Product } from '../../../types'

defineProps<{
  cart: {product: Product, quantity: number}[]
  cartTotal: number
}>()

defineEmits<{
  increaseQuantity: [productId: number]
  decreaseQuantity: [productId: number]
  placeOrder: []
}>()

const getCategoryEmoji = (category: string) => {
  const emojis: {[key: string]: string} = {
    drink: '🍹',
    food: '🍔'
  }
  return emojis[category] || '📦'
}
</script>

<style scoped>
.cart-section {
  background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
  border-radius: 20px;
  padding: 2rem;
  margin-top: 2rem;
  border: 1px solid rgba(255,255,255,0.15);
  backdrop-filter: blur(10px);
}

.cart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.cart-header h3 {
  color: #00ffff;
  margin: 0;
  font-size: 1.5rem;
}

.items-count {
  color: #ccc;
  font-size: 0.9rem;
}

.cart-items {
  margin-bottom: 2rem;
}

.cart-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255,255,255,0.05);
  border-radius: 15px;
  margin-bottom: 0.8rem;
  transition: all 0.3s ease;
}

.cart-item:hover {
  background: rgba(255,255,255,0.08);
  transform: translateX(5px);
}

.item-image {
  flex-shrink: 0;
}

.image-mini {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.image-mini.drink {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.image-mini.food {
  background: linear-gradient(135deg, #f093fb, #f5576c);
}

.item-details {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.item-name {
  color: #fff;
  font-weight: 600;
  margin-bottom: 0.2rem;
}

.item-price {
  color: #ccc;
  font-size: 0.8rem;
}

.item-controls {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin: 0 1rem;
}

.control-btn {
  width: 32px;
  height: 32px;
  border: 1px solid rgba(255,255,255,0.3);
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
  background: rgba(255,255,255,0.1);
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
}

.item-total {
  font-weight: bold;
  color: #00ffff;
  font-size: 1.1rem;
  min-width: 80px;
  text-align: right;
}

.cart-footer {
  border-top: 1px solid rgba(255,255,255,0.1);
  padding-top: 1.5rem;
}

.total-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.total-label {
  color: #ccc;
  font-size: 1.1rem;
}

.total-amount {
  color: #00ffff;
  font-size: 1.8rem;
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
}

.order-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(255, 0, 255, 0.4);
}

.order-icon {
  font-size: 1.3rem;
}

.order-text {
  font-size: 1rem;
}

.order-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
  transition: left 0.5s ease;
}

.order-btn:hover .order-glow {
  left: 100%;
}

@media (max-width: 768px) {
  .cart-section {
    padding: 1.5rem;
    margin: 1rem 0.5rem 0;
  }
  
  .cart-header {
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }
  
  .cart-item {
    gap: 0.8rem;
    padding: 0.8rem;
  }
  
  .item-controls {
    margin: 0 0.5rem;
  }
  
  .total-amount {
    font-size: 1.5rem;
  }
  
  .order-btn {
    padding: 1rem 1.5rem;
  }
}
</style>