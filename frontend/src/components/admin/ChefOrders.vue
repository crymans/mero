<!-- components/ChefOrders.vue -->
<template>
  <div class="chef-orders">
    <h2>Все заказы</h2>
    
    <div class="orders-list">
      <div 
        v-for="order in orders" 
        :key="order.id"
        :class="['order-item', { fulfilled: order.is_fulfilled }]"
      >
        <div class="order-header">
          <h3>Заказ #{{ order.id }}</h3>
          <span class="table">Стол: {{ order.table_id }}</span>
        </div>
        
        <div class="order-details">
          <p>Продукты: {{getProductName(order.products_ids)}}</p>
          <p>Количество: {{ order.quantity }}</p>
          <p>Сумма: {{ order.total_price }}</p>
          <p>Столик: {{ order.table_id }}</p>
          <p>Время: {{ new Date(order.created_at).toLocaleString() }}</p>
        </div>
        
        <div class="order-actions">
          <button 
            @click="toggleFulfillment(order)"
            :disabled="loading"
            :class="{ fulfilled: order.is_fulfilled }"
          >
            {{ order.is_fulfilled ? 'Выполнен' : 'Отметить выполненным' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { createApiService } from '@/services/api'
import type { Order, Product } from '@/types'

const authStore = useAuthStore()
const apiService = createApiService(authStore.telegramId)

const orders = ref<Order[]>([])
const products = ref<Product[]>([])
const loading = ref(false)

const loadOrders = async () => {
  try {
    orders.value = await apiService.getAllOrders()
    products.value = await apiService.getProducts()
  } catch (error) {
    console.error('Ошибка загрузки заказов:', error)
  }
}

const toggleFulfillment = async (order: Order) => {
  loading.value = true
  try {
    await apiService.updateOrderFulfillment(order.id, !order.is_fulfilled)
    await loadOrders() // Reload to get updated data
  } catch (error) {
    alert('Ошибка при обновлении заказа')
  } finally {
    loading.value = false
  }
}

const getProductName = (ids)=> {
  let answer = {}
  ids = ids.split(',')
  
  ids.forEach(id => {
    let flag = true
    products.value.forEach(prod => {
    if(prod.id == parseInt(id)){
      if(answer[parseInt(id)] != undefined){
        answer[parseInt(id)] = [answer[parseInt(id)][0] + 1, answer[parseInt(id)][1]]  
      }
      else{
        answer[parseInt(id)] = [1, (prod.name + '   ' + prod.description)]
      }
      flag = false
    }
  });
  if(flag){
    answer[id] = id
  }

  });
  return Object.values(answer)

}

onMounted(() => {
  loadOrders()
})
</script>

<style scoped>


.chef-orders h2 {
  font-size: 2.5rem;
  text-align: center;
  margin-bottom: 2rem;
  text-transform: uppercase;
  letter-spacing: 0.3rem;
  background: linear-gradient(45deg, #00ffff, #ff00ff, #ffff00);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: titleGlow 3s ease-in-out infinite alternate;
  position: relative;
  z-index: 2;
}

@keyframes titleGlow {
  from {
    text-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
  }
  to {
    text-shadow: 0 0 30px rgba(255, 0, 255, 0.5),
                 0 0 40px rgba(255, 255, 0, 0.3);
  }
}

.orders-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 2;
}

.order-item {
  position: relative;
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.08) 0%, 
    rgba(255, 255, 255, 0.03) 100%);
  border-radius: 20px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  overflow: hidden;
}

.order-item::before {
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

.order-item:hover::before {
  left: 100%;
}

.order-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
}

/* Стили для выполненных заказов */
.order-item.fulfilled {
  border-color: rgba(0, 255, 0, 0.3);
  background: linear-gradient(135deg, 
    rgba(0, 255, 0, 0.05) 0%, 
    rgba(0, 255, 0, 0.02) 100%);
}

.order-item.fulfilled::after {
  content: '✓ ВЫПОЛНЕНО';
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(0, 255, 0, 0.2);
  color: #00ff00;
  padding: 0.3rem 0.8rem;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border: 1px solid rgba(0, 255, 0, 0.4);
  animation: pulseGreen 2s infinite;
}

@keyframes pulseGreen {
  0%, 100% { 
    box-shadow: 0 0 5px rgba(0, 255, 0, 0.3);
  }
  50% { 
    box-shadow: 0 0 15px rgba(0, 255, 0, 0.6);
  }
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.order-header h3 {
  font-size: 1.5rem;
  margin: 0;
  background: linear-gradient(45deg, #fff, #ccc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
}

.table {
  background: rgba(0, 255, 255, 0.1);
  color: #00ffff;
  padding: 0.3rem 0.8rem;
  border-radius: 12px;
  font-weight: bold;
  border: 1px solid rgba(0, 255, 255, 0.3);
  text-shadow: 0 0 8px rgba(0, 255, 255, 0.5);
}

.order-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.order-details p {
  margin: 0;
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  font-size: 0.9rem;
  border-left: 3px solid rgba(0, 255, 255, 0.3);
}

.order-actions {
  text-align: right;
}

.order-actions button {
  position: relative;
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
  background: linear-gradient(45deg, #00cccc, #00ffff);
  color: #000;
}

.order-actions button::before {
  content: '';
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

.order-actions button:hover::before {
  left: 100%;
}

.order-actions button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 255, 255, 0.3);
}

.order-actions button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.order-actions button:disabled:hover::before {
  left: -100%;
}

.order-actions button.fulfilled {
  background: linear-gradient(45deg, #00cc00, #00ff00);
  color: #000;
}

.order-actions button.fulfilled:hover {
  box-shadow: 0 5px 15px rgba(0, 255, 0, 0.3);
}

/* Анимированные частицы фона */
.background-particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  pointer-events: none;
}

.particle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
  animation: float 6s ease-in-out infinite;
}

.particle:nth-child(1) {
  width: 6px;
  height: 6px;
  top: 20%;
  left: 10%;
  animation-delay: 0s;
  background: rgba(0, 255, 255, 0.3);
}

.particle:nth-child(2) {
  width: 4px;
  height: 4px;
  top: 60%;
  left: 85%;
  animation-delay: 2s;
  background: rgba(255, 0, 255, 0.3);
}

.particle:nth-child(3) {
  width: 5px;
  height: 5px;
  top: 80%;
  left: 20%;
  animation-delay: 4s;
  background: rgba(255, 255, 0, 0.3);
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-15px) rotate(180deg); }
}

@media (max-width: 768px) {
  .chef-orders {
    padding: 1rem 0.5rem;
  }
  
  .chef-orders h2 {
    font-size: 2rem;
    letter-spacing: 0.2rem;
  }
  
  .order-item {
    padding: 1rem;
  }
  
  .order-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .order-details {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  
  .order-actions {
    text-align: center;
  }
  
  .order-actions button {
    width: 100%;
  }
}

@media (min-width: 1024px) {
  .orders-list {
    grid-template-columns: repeat(2, 1fr);
    gap: 2rem;
  }
  
  .order-item {
    padding: 2rem;
  }
}
</style>