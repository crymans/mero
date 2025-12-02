<template>
  <div class="product-card" :class="[product.category, { unavailable: !product.is_for_table }]">
    <!-- Бейдж категории -->
    <div class="category-badge" :class="product.category">
      {{ getCategoryEmoji(product.category) }}
    </div>
    
    <!-- Контент карточки -->
    <div class="card-content">
      <!-- Изображение -->
      <div class="product-image">
                  <img 

            :src="product.image_url" 
            :alt="product.name"
          >

        <div class="image-placeholder" :class="product.category">
          {{ getCategoryEmoji(product.category) }}
        </div>
        <div class="image-overlay"></div>
        <div class="price-tag">
          {{ product.price }} stars
        </div>
      </div>
      
      <!-- Информация -->
      <div class="product-info">
        <h3 class="product-name">{{ product.name }}</h3>
        <p class="product-desc">{{ product.description }}</p>
        
        <!-- Рейтинг (заглушка) -->
        <!-- <div class="product-rating">
          <span class="stars">★★★★★</span>
          <span class="rating-text">5.0</span>
        </div> -->
      </div>
      
      <!-- Кнопка добавления -->
      <button 
        class="add-to-cart-btn"
        @click="handleAddToCart"
        :disabled="!user || !(product.count > 0)"
        :class="{ unavailable: !(product.count > 0), added: isAdded }"
      >
        <span class="btn-icon">{{ isAdded ? '✅' : '🛒' }}</span>
        <span class="btn-text">
          {{ !(product.count > 0) ? 'НЕТ В НАЛИЧИИ' : !user ? 'ВОЙТИ ДЛЯ ЗАКАЗА' : isAdded ? 'ДОБАВЛЕНО' : 'ДОБАВИТЬ' }}
        </span>
        <div class="btn-glow"></div>
      </button>
    </div>
    
    <!-- Неоновое свечение -->
    <div class="card-glow" :class="product.category"></div>
  </div>
</template>

<script setup lang="ts">
import type { Product, User } from '../../types'
import { ref } from 'vue'

interface Props {
  product: Product
  user: User | null
}

const props = defineProps<Props>()
const emit = defineEmits<{
  addToCart: [product: Product]
}>()

const isAdded = ref(false)

const getCategoryEmoji = (category: string) => {
  const emojis: {[key: string]: string} = {
    drink: '🍹',
    food: '🍔'
  }
  return emojis[category] || '📦'
}

const handleAddToCart = () => {
  if (!props.user || !(props.product.count > 0)) return
  
  emit('addToCart', props.product)
  
  // Анимация подтверждения добавления
  isAdded.value = true
  setTimeout(() => {
    isAdded.value = false
  }, 1500)
}
</script>

<style scoped>
/* Существующие стили остаются без изменений */

.add-to-cart-btn.added {
  background: linear-gradient(135deg, #00ff00, #00cc00) !important;
  animation: buttonPulse 0.5s ease;
}

@keyframes buttonPulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
}

.product-card {
  position: relative;
  background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
  border-radius: 20px;
  padding: 0;
  border: 1px solid rgba(255,255,255,0.15);
  backdrop-filter: blur(10px);
  transition: all 0.4s ease;
  overflow: hidden;
  height: 100%;
}

.product-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
  transition: left 0.6s ease;
}

.product-card:hover::before {
  left: 100%;
}

.product-card:hover {
  transform: translateY(-8px);
  border-color: rgba(255, 255, 255, 0.3);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
}

/* Стили для разных категорий */
.product-card.drink:hover {
  border-color: #00ffff;
  box-shadow: 0 15px 40px rgba(0, 255, 255, 0.3);
}

.product-card.food:hover {
  border-color: #ffff00;
  box-shadow: 0 15px 40px rgba(255, 255, 0, 0.3);
}

.category-badge {
  position: absolute;
  top: 1rem;
  left: 1rem;
  background: rgba(0, 0, 0, 0.7);
  padding: 0.5rem 0.8rem;
  border-radius: 50px;
  font-size: 1.2rem;
  z-index: 2;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.card-content {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.product-image {
  position: relative;
  height: 160px;
  overflow: hidden;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 4rem;
  transition: transform 0.3s ease;
}

.product-card:hover .image-placeholder {
  transform: scale(1.1);
}

.image-placeholder.drink {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.image-placeholder.food {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, transparent 0%, rgba(0,0,0,0.7) 100%);
}

.price-tag {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  background: linear-gradient(135deg, #ff00ff, #00ffff);
  color: #000;
  padding: 0.5rem 1rem;
  border-radius: 25px;
  font-weight: bold;
  font-size: 1.1rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.product-info {
  padding: 1.5rem;
  flex-grow: 1;
}

.product-name {
  font-size: 1.3rem;
  margin-bottom: 0.8rem;
  color: #fff;
  font-weight: 700;
  line-height: 1.3;
}

.product-desc {
  color: #ccc;
  font-size: 0.9rem;
  margin-bottom: 1rem;
  line-height: 1.4;
}

.product-rating {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: auto;
}

.stars {
  color: #ffff00;
  font-size: 0.9rem;
}

.rating-text {
  color: #888;
  font-size: 0.8rem;
}

.add-to-cart-btn {
  position: relative;
  margin: 0 1.5rem 1.5rem;
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, #00ffff, #0080ff);
  color: #000;
  border: none;
  border-radius: 15px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
  overflow: hidden;
}

.add-to-cart-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 255, 255, 0.4);
}

.add-to-cart-btn:disabled {
  background: #666;
  cursor: not-allowed;
  transform: none;
}

.add-to-cart-btn.unavailable {
  background: #ff4444;
}

.btn-icon {
  font-size: 1.2rem;
}

.btn-text {
  font-size: 0.9rem;
}

.btn-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
  transition: left 0.5s ease;
}

.add-to-cart-btn:hover:not(:disabled) .btn-glow {
  left: 100%;
}

.card-glow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 20px;
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
}

.product-card:hover .card-glow {
  opacity: 0.3;
}

.card-glow.drink {
  background: radial-gradient(circle at center, rgba(0,255,255,0.4) 0%, transparent 70%);
  filter: blur(20px);
}

.card-glow.food {
  background: radial-gradient(circle at center, rgba(255,255,0,0.4) 0%, transparent 70%);
  filter: blur(20px);
}

/* Адаптивность */
@media (max-width: 768px) {
  .product-card {
    margin: 0 0.5rem;
  }
  
  .product-image {
    height: 140px;
  }
  
  .image-placeholder {
    font-size: 3rem;
  }
  
  .product-info {
    padding: 1rem;
  }
  
  .product-name {
    font-size: 1.1rem;
  }
  
  .add-to-cart-btn {
    margin: 0 1rem 1rem;
    padding: 0.8rem 1.2rem;
  }
}
</style>