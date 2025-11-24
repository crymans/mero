// stores/admin.ts
import { defineStore } from 'pinia'
import { createApiService } from '@/services/api'
import { API_CONFIG } from '@/config/api'
import { useUserStore } from '@/stores/user'

const apiClient = createApiService(window.Telegram.WebApp.initData)
interface User {
  id: number
  telegram_id: string
  username: string | null
  first_name: string | null
  last_name: string | null
  phone: string | null
  role: string
  created_at: string
  balance?: number
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

interface Ticket {
  id: number
  user_id: number
  qr_code: string
  last_entry: number
  price: number
  created_at: string
  user?: User
}

interface AdminStats {
  total_users: number
  total_orders: number
  total_tickets: number
  total_revenue: number
  active_orders: number
}

export const useAdminStore = defineStore('admin', {
  state: () => ({
    users: [] as User[],
    products: [] as Product[],
    orders: [] as Order[],
    tickets: [] as Ticket[],
    stats: null as AdminStats | null,
    isLoading: false,
    error: null as string | null,
    selectedUser: null as User | null,
    selectedProduct: null as Product | null
  }),

  getters: {
    totalRevenue: (state) => {
      return state.orders.reduce((sum, order) => sum + order.total_price, 0)
    },
    activeOrders: (state) => {
      return state.orders.filter(order => !order.is_fulfilled)
    },
    usedTickets: (state) => {
      return state.tickets.filter(ticket => ticket.is_used)
    },
    vipUsers: (state) => {
      return state.users.filter(user => user.role === 'vip')
    }
  },

  actions: {
    async fetchAllUsers() {
      this.isLoading = true
      try {
        const response = await apiClient.getAllUsers()
        console.log(response)
        this.users = response
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Failed to fetch users'
        console.error('Error fetching users:', error)
      } finally {
        this.isLoading = false
      }
      this.isLoading = false
    },

    async fetchAllProducts() {
      this.isLoading = true
      try {
        const response = await apiClient.get('/admin/products')
        this.products = response.data
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Failed to fetch products'
        console.error('Error fetching products:', error)
      } finally {
        this.isLoading = false
      }
    },

    async fetchAllOrders() {
      this.isLoading = true
      try {
        const response = await apiClient.get('/orders/', {
          params: { limit: 1000 }
        })
        this.orders = response.data
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Failed to fetch orders'
        console.error('Error fetching orders:', error)
      } finally {
        this.isLoading = false
      }
    },

    async fetchAllTickets() {
      this.isLoading = true
      try {
        const response = await apiClient.get('/admin/tickets')
        this.tickets = response.data
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Failed to fetch tickets'
        console.error('Error fetching tickets:', error)
      } finally {
        this.isLoading = false
      }
    },

    async fetchStats() {
      try {
        // Собираем статистику из загруженных данных
        await Promise.all([
          this.fetchAllUsers(),
          this.fetchAllOrders(),
          this.fetchAllTickets()
        ])

        this.stats = {
          total_users: this.users.length,
          total_orders: this.orders.length,
          total_tickets: this.tickets.length,
          total_revenue: this.totalRevenue,
          active_orders: this.activeOrders.length
        }
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Failed to fetch stats'
        console.error('Error fetching stats:', error)
      }
    },

    async updateUserRole(telegramId: string, role: string) {
      try {
        const response = await apiClient.updateUserRole(telegramId, role)
        
      
        // Обновляем пользователя в локальном состоянии
        const userIndex = this.users.findIndex(u => u.telegram_id === telegramId)
        if (userIndex !== -1) {
          this.users[userIndex] = response.data
        }
        
        return response.data
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Failed to update user role'
        throw error
      }
    },

    async createProduct(productData: Omit<Product, 'id'>) {
      try {
        const response = await apiClient.post(
          '/admin/products',
          productData
        )
        this.products.push(response.data)
        return response.data
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Failed to create product'
        throw error
      }
    },

    async updateProduct(productId: number, productData: Partial<Product>) {
      try {
        const response = await apiClient.put(
          `/admin/products/${productId}`,
          productData
        )
        
        // Обновляем продукт в локальном состоянии
        const productIndex = this.products.findIndex(p => p.id === productId)
        if (productIndex !== -1) {
          this.products[productIndex] = response.data
        }
        
        return response.data
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Failed to update product'
        throw error
      }
    },

    async deleteProduct(productId: number) {
      try {
        await apiClient.delete(`/admin/products/${productId}`)
        this.products = this.products.filter(p => p.id !== productId)
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Failed to delete product'
        throw error
      }
    },

    async updateOrderStatus(orderId: number, isFulfilled: boolean) {
      try {
        const response = await apiClient.patch(
          `/orders/${orderId}/fulfill`,
          { is_fulfilled: isFulfilled }
        )
        
        // Обновляем заказ в локальном состоянии
        const orderIndex = this.orders.findIndex(o => o.id === orderId)
        if (orderIndex !== -1) {
          this.orders[orderIndex] = response.data
        }
        
        return response.data
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Failed to update order'
        throw error
      }
    },

    async markTicketAsUsed(ticketId: number) {
      try {
        const response = await apiClient.patch(
          `/tickets/${ticketId}/mark-used`
        )
        
        // Обновляем билет в локальном состоянии
        const ticketIndex = this.tickets.findIndex(t => t.id === ticketId)
        if (ticketIndex !== -1) {
          this.tickets[ticketIndex] = response.data
        }
        
        return response.data
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Failed to mark ticket as used'
        throw error
      }
    },

    setSelectedUser(user: User | null) {
      this.selectedUser = user
    },

    setSelectedProduct(product: Product | null) {
      this.selectedProduct = product
    },

    getCurrentUserTelegramId(): string {
      const userStore = useUserStore()
      return userStore.user?.telegram_id || 'admin'
    },

    clearError() {
      this.error = null
    }
  }
})