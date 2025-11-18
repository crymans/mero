import { defineStore } from 'pinia'
import type { Product } from '@/router'
import { productsApi } from '@/services/api'

export const useProductsStore = defineStore('products', {
  state: () => ({
    products: [] as Product[],
    loading: false,
    error: null as string | null
  }),

  getters: {
    getProducts: (state) => state.products,
    getProductById: (state) => (id: number) => 
      state.products.find(product => product.id === id),
    getProductsByCategory: (state) => (category: string) => 
      category === 'all' 
        ? state.products 
        : state.products.filter(product => product.category === category)
  },

  actions: {
    async fetchProducts() {
      this.loading = true
      this.error = null
      try {
        const productsList = await productsApi.getProducts()
        this.products = productsList
      } catch (error) {
        this.error = 'Ошибка при загрузке меню'
        console.error('Error loading products:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateProductAvailability(productId: number, isAvailable: boolean) {
      const product = this.products.find(p => p.id === productId)
      if (product) {
        product.is_available = isAvailable
      }
    }
  }
})