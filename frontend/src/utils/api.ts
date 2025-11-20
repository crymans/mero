// utils/api.ts
import { API_CONFIG } from '@/config/api'

interface ApiOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'
  headers?: Record<string, string>
  body?: any
}

export class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string = API_CONFIG.BASE_URL) {
    this.baseUrl = baseUrl
  }

  async request(endpoint: string, options: ApiOptions = {}) {
    const url = `${this.baseUrl}${endpoint}`
    
    const config: RequestInit = {
      method: options.method || 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Access-Control-Allow-Origin' : 'http://localost:3000',
        'user-data': window.Telegram.WebApp.initData,
        ...options.headers
      },
      // credentials: 'include' // Для работы с куками, если понадобится
    }

    if (options.body) {
      config.body = JSON.stringify(options.body)
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        // Если статус 405 (Method Not Allowed), это может быть CORS проблема
        if (response.status === 405) {
          throw new Error('CORS error: Method not allowed. Check server CORS configuration.')
        }
        
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }))
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  async get(endpoint: string, headers?: Record<string, string>) {
    return this.request(endpoint, { method: 'GET', headers })
  }

  async post(endpoint: string, data?: any, headers?: Record<string, string>) {
    return this.request(endpoint, { method: 'POST', body: data, headers })
  }

  async patch(endpoint: string, data?: any, headers?: Record<string, string>) {
    return this.request(endpoint, { method: 'PATCH', body: data, headers })
  }

  async put(endpoint: string, data?: any, headers?: Record<string, string>) {
    return this.request(endpoint, { method: 'PUT', body: data, headers })
  }

  async delete(endpoint: string, headers?: Record<string, string>) {
    return this.request(endpoint, { method: 'DELETE', headers })
  }
}

export const apiClient = new ApiClient()