<!-- components/OfficiantOrders.vue -->
<template>
  <div class="officiant-orders">
    <h2>Выполненные заказы</h2>
    
    <div class="orders-list">
      <div 
        v-for="order in recentOrders" 
        :key="order.id"
        class="order-item fulfilled"
      >
        <div class="order-header">
          <h3>Заказ #{{ order.id }}</h3>
          <span class="table">Стол: {{ order.table_id }}</span>
        </div>
        
        <div class="order-details">
          <p>Продукты: {{ order.products_ids }}</p>
          <p>Количество: {{ order.quantity }}</p>
          <p>Сумма: {{ order.total_price }}</p>
          <p>Время выполнения: {{ new Date(order.created_at).toLocaleString() }}</p>
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

const recentOrders = ref<Order[]>([])

const loadRecentOrders = async () => {
  try {
    recentOrders.value = await apiService.getRecentFulfilledOrders()
  } catch (error) {
    console.error('Ошибка загрузки заказов:', error)
  }
}

onMounted(() => {
  loadRecentOrders()
})
</script>