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
          <p>Продукты: {{ order.products_ids }}</p>
          <p>Количество: {{ order.quantity }}</p>
          <p>Сумма: {{ order.total_price }}</p>
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
import type { Order } from '@/types'

const authStore = useAuthStore()
const apiService = createApiService(authStore.telegramId)

const orders = ref<Order[]>([])
const loading = ref(false)

const loadOrders = async () => {
  try {
    orders.value = await apiService.getAllOrders()
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

onMounted(() => {
  loadOrders()
})
</script>