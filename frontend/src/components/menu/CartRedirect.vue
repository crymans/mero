<template>
  <div class="cart-redirect" @click="$emit('openCart')">
    <div class="redirect-content">
      <div class="redirect-icon">
        <span class="icon">🛒</span>
        <div class="item-badge" v-if="itemCount > 0">{{ itemCount }}</div>
      </div>
      <div class="redirect-text">
        <div class="redirect-title">Корзина</div>
        <div class="redirect-subtitle">{{ formattedTotal }} stars</div>
      </div>
      <div class="redirect-arrow">
        <span class="arrow">›</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  cartTotal: number
  itemCount: number
}

const props = defineProps<Props>()
defineEmits<{
  openCart: []
}>()

const formattedTotal = computed(() => {
  return props.cartTotal.toLocaleString('ru-RU')
})
</script>

<style scoped>
.cart-redirect {
  position: sticky;
  top: 1rem;
  margin: 1rem 0 2rem 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 15px;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  z-index: 100;
}

.cart-redirect:hover {
  border-color: #00ffff;
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 255, 255, 0.2);
}

.redirect-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.redirect-icon {
  position: relative;
  font-size: 1.8rem;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #ff00ff, #00ffff);
  border-radius: 12px;
}

.item-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background: #ff4444;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: bold;
  border: 2px solid #1a1a1a;
  animation: pulse 2s infinite;
}

.redirect-text {
  flex: 1;
}

.redirect-title {
  font-size: 1.1rem;
  font-weight: bold;
  color: #fff;
  margin-bottom: 0.2rem;
}

.redirect-subtitle {
  font-size: 1.3rem;
  font-weight: bold;
  color: #00ffff;
}

.redirect-arrow {
  font-size: 1.5rem;
  color: #00ffff;
  transition: transform 0.3s ease;
}

.cart-redirect:hover .redirect-arrow {
  transform: translateX(5px);
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

@media (max-width: 768px) {
  .cart-redirect {
    margin: 0.5rem 0 1.5rem 0;
    padding: 0.8rem;
  }
  
  .redirect-icon {
    font-size: 1.5rem;
    width: 45px;
    height: 45px;
  }
  
  .redirect-title {
    font-size: 1rem;
  }
  
  .redirect-subtitle {
    font-size: 1.1rem;
  }
}
</style>