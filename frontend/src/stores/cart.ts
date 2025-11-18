import { defineStore } from 'pinia'
import type { Product } from '@/router'

interface CartItem {
  product: Product
  quantity: number
}

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [] as CartItem[],
    quantities: {} as { [key: number]: number }
  }),

  getters: {
    getCartItems: (state) => state.items,
    getCartTotal: (state) => 
      state.items.reduce((total, item) => total + (item.product.price * item.quantity), 0),
    getItemQuantity: (state) => (productId: number) => 
      state.quantities[productId] || 0,
    getCartCount: (state) => 
      state.items.reduce((count, item) => count + item.quantity, 0),
    isCartEmpty: (state) => state.items.length === 0
  },

  actions: {
    increaseQuantity(productId: number) {
      if (!this.quantities[productId]) {
        this.quantities[productId] = 0
      }
      this.quantities[productId]++
    },

    decreaseQuantity(productId: number) {
      if (this.quantities[productId] && this.quantities[productId] > 0) {
        this.quantities[productId]--
      }
    },

    addToCart(product: Product) {
      const quantity = this.quantities[product.id] || 0
      if (quantity === 0) return

      const existingItem = this.items.find(item => item.product.id === product.id)
      if (existingItem) {
        existingItem.quantity += quantity
      } else {
        this.items.push({ product, quantity })
      }
      
      this.quantities[product.id] = 0
    },

    removeFromCart(productId: number) {
      this.items = this.items.filter(item => item.product.id !== productId)
    },

    clearCart() {
      this.items = []
      this.quantities = {}
    },

    updateQuantity(productId: number, quantity: number) {
      this.quantities[productId] = quantity
    }
  }
})