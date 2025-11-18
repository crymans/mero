// stores/orders.ts
import { defineStore } from 'pinia'
import { apiClient } from '@/utils/api'
import { API_CONFIG } from '@/config/api'

interface Order {
  id: number
  user_id: number
  products_ids: string
  quantity: number
  total_price: number
  is_fulfilled: boolean
  table_id: number
  created_at: string
}

interface Product {
  id: number
  name: string
  description: string | null
  price: number
  category: string
  count: number
  is_for_table: boolean
  image_url: string | null
}

export const useOrdersStore = defineStore('orders', {
  state: () => ({
    orders: [] as Order[],
    products: [] as Product[],
    isLoading: false,
    error: null as string | null
  }),

  actions: {
    async fetchUserOrders(telegramId: string) {
      this.isLoading = true
      try {
        this.orders = await apiClient.get(API_CONFIG.ENDPOINTS.ORDERS, {
          'X-User-Telegram-ID': telegramId
        })
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Failed to fetch orders'
        console.error('Error fetching orders:', error)
      } finally {
        this.isLoading = false
      }
    },

    async fetchProducts() {
      try {
        this.products = await apiClient.get(API_CONFIG.ENDPOINTS.PRODUCTS)
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Failed to fetch products'
        console.error('Error fetching products:', error)
      }
    },

    getProductById(productId: number): Product | null {
      return this.products.find(p => p.id === productId) || null
    },

    parseProductsIds(productsIds: string): number[] {
      return productsIds.split(',').map(id => parseInt(id.trim())).filter(id => !isNaN(id))
    },

    getOrderProducts(order: Order): { product: Product | null, quantity: number }[] {
      const productIds = this.parseProductsIds(order.products_ids)
      
      // Группируем продукты по ID и считаем количество
      const productCounts: { [key: number]: number } = {}
      productIds.forEach(id => {
        productCounts[id] = (productCounts[id] || 0) + 1
      })

      return Object.entries(productCounts).map(([id, quantity]) => ({
        product: this.getProductById(parseInt(id)),
        quantity
      }))
    },

    clearError() {
      this.error = null
    }
  }
})