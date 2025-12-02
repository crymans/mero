<template>
  <div class="menu-page">
    <div class="container">
      <MenuHeader style="margin-top: 15%;" />
      
      <!-- Элемент перенаправления на корзину -->
      <CartRedirect 
        v-if="cart.length > 0"
        :cart-total="cartTotal"
        :item-count="itemCount"
        @open-cart="showCartModal = true"
      />
      
      <MenuCategories 
        :categories="categories"
        :active-category="activeCategory"
        @category-change="activeCategory = $event"
      />
      
      <!-- Состояние загрузки -->
      <div v-if="ordersStore.isLoading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>Загружаем меню...</p>
      </div>

      <!-- Ошибка загрузки -->
      <!-- <div v-if="ordersStore.error" class="error-state">
        <p>Ошибка: {{ ordersStore.error }}</p>
        <button @click="loadProducts" class="retry-btn">Попробовать снова</button>
      </div> -->

      <ProductsGrid 
        :products="filteredProducts"
        :user="user"
        @add-to-cart="addToCart"
      />
    </div>

    <!-- Плавающая корзина -->
    <FloatingCart 
      :cart="cart"
      :cart-total="cartTotal"
      :item-count="itemCount"
      @toggle-cart="showCartModal = !showCartModal"
    />

    <!-- Модальное окно корзины -->
    <CartModal 
      v-if="showCartModal"
      :cart="cart"
      :cart-total="cartTotal"
      :is-loading="isPlacingOrder"
      @increase-quantity="increaseQuantity"
      @decrease-quantity="decreaseQuantity"
      @place-order="placeOrder"
      @close="showCartModal = false"
    />

    <!-- Уведомление о добавлении в корзину -->
    <!-- <div v-if="showAddNotification" class="add-notification">
      <div class="notification-content">
        <span class="notification-icon">✅</span>
        <span class="notification-text">Товар добавлен в корзину!</span>
      </div>
    </div> -->
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import type { Product, OrderCreate, User } from '@/types'
import { useOrdersStore } from '@/stores/orders'
import { useUserStore } from '@/stores/user'
import MenuHeader from '@/components/menu/Header.vue'
import MenuCategories from '@/components/menu/Categories.vue'
import ProductsGrid from '@/components/menu/ProductsGrid.vue'
import FloatingCart from '@/components/menu/FloatingCart.vue'
import CartModal from '@/components/menu/CartModal.vue'
import CartRedirect from '@/components/menu/CartRedirect.vue'
import { createApiService } from '@/services/api'



const router = useRouter()
const ordersStore = useOrdersStore()
const userStore = useUserStore()
const apiService = createApiService(userStore.user.telegramId)

// Данные страницы
const products = ref<Product[]>([])
const activeCategory = ref('all')
const cart = ref<{product: Product, quantity: number}[]>([])
const showCartModal = ref(false)
const showAddNotification = ref(false)
const addNotificationTimeout = ref<number | null>(null)
const isPlacingOrder = ref(false)

const categories = ['all', 'drink', 'food']

// Получаем пользователя из хранилища
const user = computed(() => userStore.user)

const filteredProducts = computed(() => {
  if (activeCategory.value === 'all') {
    return products.value
  }
  return products.value.filter(product => product.category === activeCategory.value)
})

const cartTotal = computed(() => {
  return cart.value.reduce((total, item) => total + (item.product.price * item.quantity), 0)
})

const itemCount = computed(() => {
  return cart.value.reduce((count, item) => count + item.quantity, 0)
})

// Загрузка продуктов
const loadProducts = async () => {
  try {
    await ordersStore.fetchProducts()
    products.value = ordersStore.products
  } catch (error) {
    console.error('Failed to load products:', error)
  }
}

const showAddToCartNotification = () => {
  showAddNotification.value = true
  
  if (addNotificationTimeout.value) {
    clearTimeout(addNotificationTimeout.value)
  }
  
  addNotificationTimeout.value = setTimeout(() => {
    showAddNotification.value = false
  }, 2000)
}

const addToCart = (product: Product) => {
  if (!user.value) {
    router.push('/profile')
    return
  }

  const existingItem = cart.value.find(item => item.product.id === product.id)
  if (existingItem) {
    existingItem.quantity++
  } else {
    cart.value.push({ product, quantity: 1 })
  }
  
  showAddToCartNotification()
}

const increaseQuantity = (productId: number) => {
  const item = cart.value.find(item => item.product.id === productId)
  if (item) {
    item.quantity++
  }
}

const decreaseQuantity = (productId: number) => {
  const item = cart.value.find(item => item.product.id === productId)
  if (item) {
    if (item.quantity > 1) {
      item.quantity--
    } else {
      cart.value = cart.value.filter(item => item.product.id !== productId)
    }
  }
}

// Создание заказа
const placeOrder = async (tableNumber: number) => {
  if (!user.value || cart.value.length === 0) return

  isPlacingOrder.value = true

  try {
    // Формируем данные для заказа
    const productsIds = cart.value.map(item => 
      Array(item.quantity).fill(item.product.id).join(',')
    ).join(',')

    const orderData: OrderCreate = {
      products_ids: productsIds,
      quantity: itemCount.value,
      total_price: cartTotal.value,
      table_id: tableNumber
    }

    console.log('Creating order:', orderData)
    
    // Отправляем запрос на создание заказа
    await apiService.createOrder(orderData)
    
    // Успешное создание заказа
    alert(`🎉 Заказ успешно оформлен! Доставка к столу №${tableNumber} через 10-15 минут`)
    cart.value = []
    showCartModal.value = false
    
  } catch (error: any) {
    console.error('Error placing order:', error)
    
    // Проверяем специфические ошибки
    if (error.message.includes('Maximum active orders limit reached')) {
      alert('❌ Достигнут лимит активных заказов (2 заказа). Дождитесь выполнения текущих заказов.')
    } else if (error.message.includes('Non-VIP users cannot order table products')) {
      alert('❌ Обычные пользователи не могут заказывать продукты для стола. Станьте VIP!')
    } else {
      alert('❌ Ошибка при оформлении заказа. Попробуйте еще раз.')
    }
  } finally {
    isPlacingOrder.value = false
  }
}

onMounted(async () => {
  await loadProducts()
})

// Очищаем таймаут при размонтировании компонента
import { onUnmounted } from 'vue'
onUnmounted(() => {
  if (addNotificationTimeout.value) {
    clearTimeout(addNotificationTimeout.value)
  }
  ordersStore.clearError()
})
</script>

<style scoped>
.menu-page {
  padding: 1rem;
  min-height: calc(100vh - 70px);
  background: #000;
  padding-bottom: 100px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Состояние загрузки */
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

/* Состояние ошибки */
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

/* Стили для уведомления о добавлении в корзину */
.add-notification {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 3000;
  animation: notificationSlide 0.3s ease-out;
}

.notification-content {
  background: linear-gradient(135deg, #00ff00, #00cc00);
  color: #000;
  padding: 1rem 2rem;
  border-radius: 50px;
  display: flex;
  align-items: center;
  gap: 0.8rem;
  box-shadow: 0 10px 30px rgba(0, 255, 0, 0.3);
  border: 2px solid rgba(255, 255, 255, 0.3);
  font-weight: bold;
}

.notification-icon {
  font-size: 1.2rem;
}

.notification-text {
  font-size: 1rem;
}

@keyframes notificationSlide {
  0% {
    opacity: 0;
    transform: translate(-50%, -40%);
  }
  100% {
    opacity: 1;
    transform: translate(-50%, -50%);
  }
}

/* Адаптивность для уведомления */
@media (max-width: 768px) {
  .notification-content {
    padding: 0.8rem 1.5rem;
  }
  
  .notification-text {
    font-size: 0.9rem;
  }
}
</style>