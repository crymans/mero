<template>
  <div class="products-grid">
    <div 
      v-for="product in products" 
      :key="product.id"
      class="product-card-wrapper"
    >
      <ProductCard 
        :product="product"
        :user="user"
        @add-to-cart="$emit('addToCart', product)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Product, User } from '../../types'
import ProductCard from './ProductCard.vue'

defineProps<{
  products: Product[]
  user: User | null
}>()

defineEmits<{
  addToCart: [product: Product]
}>()
</script>

<style scoped>
.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.product-card-wrapper {
  transition: transform 0.3s ease;
}

.product-card-wrapper:hover {
  transform: translateY(-5px);
}

@media (max-width: 768px) {
  .products-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
    padding: 0 0.5rem;
  }
}

@media (min-width: 1200px) {
  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  }
}
</style>