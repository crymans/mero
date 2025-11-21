// stores/user.ts
import { defineStore } from 'pinia'
import { apiClient } from '@/utils/api'
import { API_CONFIG } from '@/config/api'

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

interface Ticket {
  id: number
  user_id: number
  qr_code: string
  is_used: boolean
  price: number
  created_at: string
}

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null as User | null,
    ticket: null as Ticket | null,
    isLoading: false,
    purchase_link:'',
    error: null as string | null
  }),

  getters: {
    isAuthenticated: (state) => !!state.user,
    hasTicket: (state) => !!state.ticket,
    isVip: (state) => state.user?.role === 'vip' || state.user?.role === 'admin',
    
    // Геттер для получения URL QR-кода на основе qr_code из бэкенда
    qrCodeUrl: (state) => {
      if (!state.ticket?.qr_code) return null
      
      const qrData = encodeURIComponent(state.ticket.qr_code)
      return `https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=${qrData}&format=png&margin=10`
    },
    
    // Геттер для полноэкранного QR-кода
    fullscreenQrCodeUrl: (state) => {
      if (!state.ticket?.qr_code) return null
      
      const qrData = encodeURIComponent(state.ticket.qr_code)
      return `https://api.qrserver.com/v1/create-qr-code/?size=500x500&data=${qrData}&format=png&margin=20`
    }
  },

  actions: {
    async initializeUser(telegramId: string) {
      this.isLoading = true
      this.error = null
      
      try {
        const userData = await apiClient.post(`${API_CONFIG.ENDPOINTS.USERS}/`, {
          'user-data': telegramId
        })
        
        this.user = userData
        await this.fetchUserTicket(telegramId)
        
      } catch (error: any) {
        if (error.message.includes('404') || error.message.includes('not found')) {
          await this.registerUser(telegramId)
        }
        //  else {
        //   this.error = error.message
        //   console.error('User initialization error:', error)
        // }
      } 
      finally {
        this.isLoading = false
      }
    },

    async registerUser(telegramId: string, userData?: Partial<User>) {
      this.isLoading = true
      
      try {
        const newUser = await apiClient.post(
          API_CONFIG.ENDPOINTS.USERS,
          {
            telegram_id: telegramId,
            username: userData?.username || null,
            first_name: userData?.first_name || null,
            last_name: userData?.last_name || null,
            phone: userData?.phone || null,
          },
          {
            'user-data': telegramId
          }
        )

        this.user = newUser
      } catch (error: any) {
        this.error = error.message
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async fetchUserTicket(telegramId: string) {
      try {
        const ticketData = await apiClient.get(`${API_CONFIG.ENDPOINTS.TICKETS}/my`, {
          'user-data': telegramId
        })
        
        this.ticket = ticketData
      } catch (error: any) {
        if (!error.message.includes('404')) {
          console.error('Failed to fetch ticket:', error)
        }
      }
    },
    async createPurchase(telegramId: string, stars:number) {
      try {
        const purchaseData = await apiClient.get(`${API_CONFIG.ENDPOINTS.USERS}/purchase?stars_amount=${stars}`, {
          'user-data': telegramId
        })
        
        this.purchase_link = purchaseData
        console.log(this.purchase_link)
        // window.Telegram.WebApp.
      } catch (error: any) {
        if (!error.message.includes('404')) {
          console.error('Failed to fetch purchase:', error)
        }
      }
    },
    

    async buyTicket(telegramId: string, ticketType: string) {
      this.isLoading = true
      this.error = null
      let ticketsdata = {'vip':1300, 'standard':500, 'fast':900}
      
      try {
        const price = ticketsdata[ticketType]
        
        // Генерируем базовый qr_code, но бэкенд может его перезаписать
        
        const ticketData = await apiClient.post(
          API_CONFIG.ENDPOINTS.TICKETS,
          {
            price: price,
            qr_code: '12345'
          },
          {
            'user-data': telegramId
          }
        )

        // Используем qr_code, который вернул бэкенд
        this.ticket = ticketData
        return ticketData
        
      } catch (error: any) {
        this.error = 'Для приобритения билета, необходимо пополнить баланс stars в профиле!'
        const element = document.getElementById('howbuy')
        if (element) {
          element.scrollIntoView({ behavior: 'smooth' })
        }
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async updateProfile(telegramId: string, updateData: {
      username?: string
      first_name?: string
      last_name?: string
      phone?: string
    }) {
      this.isLoading = true
      this.error = null
      
      try {
        const updatedUser = await apiClient.patch(
          `${API_CONFIG.ENDPOINTS.USERS}/me`,
          updateData,
          {
            'user-data': telegramId
          }
        )

        this.user = updatedUser
        return updatedUser
        
      } catch (error: any) {
        this.error = error.message
        throw error
      } finally {
        this.isLoading = false
      }
    },

    clearError() {
      this.error = null
    }
  }
})