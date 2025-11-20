// services/api.ts
import type { Product, Order, OrderCreate, User, Ticket } from '@/types'
import { API_CONFIG } from '@/config/api'
const API_BASE_URL = API_CONFIG.BASE_URL

class ApiService {
  constructor(private telegramId: string) {}

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`
    let u_id = window.Telegram.WebApp.initData
    if (typeof u_id !== 'string'){
        u_id = ''
    }
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        'user-data': window.Telegram.WebApp.initData,
        ...options.headers,
      },
      ...options,
    }

    const response = await fetch(url, config)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return response.json()
  }

  // Products
  async getProducts(): Promise<Product[]> {
    return this.request<Product[]>('/products/')
  }

  // Orders
  async createOrder(orderData: OrderCreate): Promise<Order> {
    return this.request<Order>('/orders/', {
      method: 'POST',
      body: JSON.stringify(orderData),
    })
  }

  async getAllOrders(): Promise<Order[]> {
    return this.request<Order[]>('/orders/')
  }

  async getMyOrders(): Promise<Order[]> {
    return this.request<Order[]>('/orders/my')
  }

  async getRecentFulfilledOrders(): Promise<Order[]> {
    return this.request<Order[]>('/orders/recent-fulfilled')
  }

  async updateOrderFulfillment(orderId: number, isFulfilled: boolean): Promise<Order> {
    return this.request<Order>(`/orders/${orderId}/fulfill`, {
      method: 'PATCH',
      body: JSON.stringify({ is_fulfilled: isFulfilled }),
    })
  }

  // Tickets
  async getTicketByQr(qrCode: string): Promise<Ticket> {
    return this.request<Ticket>(`/tickets/qr/${qrCode}`)
  }

  async markTicketUsed(ticketId: number): Promise<Ticket> {
    return this.request<Ticket>(`/tickets/${ticketId}/mark-used`, {
      method: 'PATCH',
    })
  }

  async getMyTicket(): Promise<Ticket> {
    return this.request<Ticket>('/tickets/my')
  }

  // Users
  async getCurrentUser(): Promise<User> {
    return this.request<User>('/users/me')
  }

  // Admin endpoints
  async getAllUsers(): Promise<User[]> {
    let el = this.request<User[]>('/admin/users')
    return el
  }

  async updateUserRole(telegramId: string, role: string): Promise<User> {
    return this.request<User>(`/admin/users/${telegramId}/role`, {
      method: 'PATCH',
      body: JSON.stringify({ role }),
    })
  }
  // В services/api.ts добавить следующие методы:

// Products
async createProduct(productData: ProductCreate): Promise<Product> {
  return this.request<Product>('/admin/products', {
    method: 'POST',
    body: JSON.stringify(productData),
  })
}

async updateProduct(productId: number, productData: ProductUpdate): Promise<Product> {
  return this.request<Product>(`/admin/products/${productId}`, {
    method: 'PUT',
    body: JSON.stringify(productData),
  })
}

async deleteProduct(productId: number): Promise<void> {
  return this.request<void>(`/admin/products/${productId}`, {
    method: 'DELETE',
  })
}
}


export const createApiService = (telegramId: string='') => new ApiService(telegramId)