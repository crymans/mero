// stores/admin.ts
import { defineStore } from 'pinia'
import { apiClient } from '@/utils/api'
import { API_CONFIG } from '@/config/api'
import { useUserStore } from '@/stores/user'

interface User {
  id: number
  telegram_id: string
  username: string | null
  first_name: string | null
  last_name: string | null
  phone: string | null
  role: string
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
  is_used: boolean
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

interface AnalyticsData {
  daily_orders: { date: string; count: number; revenue: number }[]
  popular_products: { product_id: number; name: string; count: number }[]
  user_registrations: { date: string; count: number }[]
  revenue_by_hour: { hour: number; revenue: number }[]
}

export const useAdminStore = defineStore('admin', {
  state: () => ({
    users: [] as User[],
    products: [] as Product[],
    orders: [] as Order[],
    tickets: [] as Ticket[],
    stats: null as AdminStats | null,
    analytics: null as AnalyticsData | null,
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
        // Временные mock данные до реализации бэкенда
        this.users = [
          {
            id: 1,
            telegram_id: "admin",
            username: "admin_user",
            first_name: "Администратор",
            last_name: "Системный",
            phone: "+79181112233",
            role: "admin",
            created_at: "2024-01-15T10:00:00Z"
          },
          {
            id: 2,
            telegram_id: "officiant_1",
            username: "officiant_user",
            first_name: "Анна",
            last_name: "Официантова",
            phone: "+79182223344",
            role: "officiant",
            created_at: "2024-01-16T11:00:00Z"
          },
          {
            id: 3,
            telegram_id: "chef_1",
            username: "chef_user",
            first_name: "Иван",
            last_name: "Поваров",
            phone: "+79183334455",
            role: "chef",
            created_at: "2024-01-16T12:00:00Z"
          },
          {
            id: 4,
            telegram_id: "qr_1",
            username: "qr_user",
            first_name: "Петр",
            last_name: "Сканеров",
            phone: "+79184445566",
            role: "qr",
            created_at: "2024-01-17T09:00:00Z"
          },
          {
            id: 5,
            telegram_id: "vip_user",
            username: "vip_client",
            first_name: "Мария",
            last_name: "VIP",
            phone: "+79185556677",
            role: "vip",
            created_at: "2024-01-18T14:00:00Z"
          }
        ]
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Failed to fetch users'
        console.error('Error fetching users:', error)
      } finally {
        this.isLoading = false
      }
    },

    async fetchAllProducts() {
      this.isLoading = true
      try {
        // Временные mock данные
        this.products = [
          {
            id: 1,
            name: "Jack Daniels",
            description: "Классический виски с карамельными нотами",
            price: 350.0,
            category: "drink",
            count: 50,
            is_for_table: false,
            image_url: null
          },
          {
            id: 2,
            name: "Jameson",
            description: "Ирландский виски с мягким вкусом",
            price: 320.0,
            category: "drink",
            count: 40,
            is_for_table: false,
            image_url: null
          },
          {
            id: 3,
            name: "Бургер",
            description: "Сочный бургер с говядиной и овощами",
            price: 450.0,
            category: "food",
            count: 30,
            is_for_table: false,
            image_url: null
          }
        ]
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
        // Временные mock данные
        this.orders = [
          {
            id: 1,
            user_id: 5,
            products_ids: "1,2,1",
            quantity: 3,
            total_price: 1020,
            is_fulfilled: false,
            table_id: 5,
            created_at: "2024-01-24T18:30:00Z"
          },
          {
            id: 2,
            user_id: 4,
            products_ids: "3,2",
            quantity: 2,
            total_price: 770,
            is_fulfilled: true,
            table_id: 3,
            created_at: "2024-01-24T17:45:00Z"
          }
        ]
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
        // Временные mock данные
        this.tickets = [
          {
            id: 1,
            user_id: 5,
            qr_code: "VIP_TICKET_001",
            is_used: false,
            price: 1300,
            created_at: "2024-01-20T12:00:00Z"
          },
          {
            id: 2,
            user_id: 1,
            qr_code: "ADMIN_TICKET_001",
            is_used: true,
            price: 0,
            created_at: "2024-01-15T10:00:00Z"
          }
        ]
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Failed to fetch tickets'
        console.error('Error fetching tickets:', error)
      } finally {
        this.isLoading = false
      }
    },

    async fetchStats() {
      try {
        // Mock статистика
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

    async fetchAnalytics() {
      try {
        // Mock аналитика
        this.analytics = {
          daily_orders: [
            { date: '2024-01-20', count: 15, revenue: 12500 },
            { date: '2024-01-21', count: 23, revenue: 18700 },
            { date: '2024-01-22', count: 18, revenue: 15200 },
            { date: '2024-01-23', count: 27, revenue: 21400 },
            { date: '2024-01-24', count: 19, revenue: 16800 }
          ],
          popular_products: [
            { product_id: 1, name: 'Jack Daniels', count: 45 },
            { product_id: 3, name: 'Бургер', count: 32 },
            { product_id: 2, name: 'Jameson', count: 28 }
          ],
          user_registrations: [
            { date: '2024-01-20', count: 8 },
            { date: '2024-01-21', count: 12 },
            { date: '2024-01-22', count: 5 },
            { date: '2024-01-23', count: 15 },
            { date: '2024-01-24', count: 9 }
          ],
          revenue_by_hour: [
            { hour: 18, revenue: 3500 },
            { hour: 19, revenue: 5200 },
            { hour: 20, revenue: 7800 },
            { hour: 21, revenue: 9500 },
            { hour: 22, revenue: 8200 }
          ]
        }
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Failed to fetch analytics'
        console.error('Error fetching analytics:', error)
      }
    },

    async updateUserRole(telegramId: string, role: string) {
      try {
        // Временная реализация до бэкенда
        const userIndex = this.users.findIndex(u => u.telegram_id === telegramId)
        if (userIndex !== -1) {
          this.users[userIndex].role = role
          return this.users[userIndex]
        }
        throw new Error('User not found')
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Failed to update user role'
        throw error
      }
    },

    async createProduct(productData: Omit<Product, 'id'>) {
      try {
        // Временная реализация до бэкенда
        const newProduct: Product = {
          id: Math.max(...this.products.map(p => p.id)) + 1,
          ...productData
        }
        this.products.push(newProduct)
        return newProduct
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Failed to create product'
        throw error
      }
    },

    async updateProduct(productId: number, productData: Partial<Product>) {
      try {
        // Временная реализация до бэкенда
        const productIndex = this.products.findIndex(p => p.id === productId)
        if (productIndex !== -1) {
          this.products[productIndex] = { ...this.products[productIndex], ...productData }
          return this.products[productIndex]
        }
        throw new Error('Product not found')
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Failed to update product'
        throw error
      }
    },

    async deleteProduct(productId: number) {
      try {
        // Временная реализация до бэкенда
        this.products = this.products.filter(p => p.id !== productId)
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Failed to delete product'
        throw error
      }
    },

    async updateOrderStatus(orderId: number, isFulfilled: boolean) {
      try {
        // Временная реализация до бэкенда
        const orderIndex = this.orders.findIndex(o => o.id === orderId)
        if (orderIndex !== -1) {
          this.orders[orderIndex].is_fulfilled = isFulfilled
          return this.orders[orderIndex]
        }
        throw new Error('Order not found')
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Failed to update order'
        throw error
      }
    },

    async markTicketAsUsed(ticketId: number) {
      try {
        // Временная реализация до бэкенда
        const ticketIndex = this.tickets.findIndex(t => t.id === ticketId)
        if (ticketIndex !== -1) {
          this.tickets[ticketIndex].is_used = true
          return this.tickets[ticketIndex]
        }
        throw new Error('Ticket not found')
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
      return userStore.user?.telegram_id || 'admin' // fallback для разработки
    },

    clearError() {
      this.error = null
    }
  }
})