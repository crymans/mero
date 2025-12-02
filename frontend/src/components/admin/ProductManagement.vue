<!-- components/admin/ProductManagement.vue -->
<template>
  <div class="product-management">
    <div class="section-header">
      <h2>🍔 Управление продуктами</h2>
      <button class="add-product-btn" @click="showAddModal = true">
        + Добавить продукт
      </button>
    </div>

    <div class="products-grid">
      <div 
        v-for="product in products" 
        :key="product.id"
        class="product-card"
      >
        <div class="product-image">
          <img 

            :src="product.image_url" 
            :alt="product.name"
          >
          <!-- <div v-else class="product-image-placeholder">
            {{ getProductEmoji(product.category) }}
          </div> -->
        </div>
        
        <div class="product-info">
          <h3 class="product-name">{{ product.name }}</h3>
          <p class="product-description" v-if="product.description">
            {{ product.description }}
          </p>
          <div class="product-meta">
            <span class="product-category">{{ product.category }}</span>
            <span class="product-price">stars{{ product.price }}</span>
          </div>
          <div class="product-stock">
            В наличии: 
            <span :class="{ low: product.count < 10 }">{{ product.count }}</span>
          </div>
          <div class="product-flags">
            <span v-if="product.is_for_table" class="table-flag">🏆 Для стола</span>
          </div>
        </div>

        <div class="product-actions">
          <button class="edit-btn" @click="editProduct(product)">
            ✏️
          </button>
          <button class="delete-btn" @click="deleteProduct(product.id)">
            🗑️
          </button>
        </div>
      </div>
    </div>

    <!-- Модальное окно добавления/редактирования -->
    <div v-if="showAddModal || editingProduct" class="modal-overlay" @click.self="closeModal">
      <div class="product-modal">
        <h3>{{ editingProduct ? 'Редактировать' : 'Добавить' }} продукт</h3>
        <form @submit.prevent="saveProduct">
          <div class="form-group">
            <label>Название:</label>
            <input v-model="formData.name" type="text" required>
          </div>
          <div class="form-group">
            <label>Описание:</label>
            <textarea v-model="formData.description"></textarea>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Цена:</label>
              <input v-model.number="formData.price" type="number" step="0.01" required>
            </div>
            <div class="form-group">
              <label>Количество:</label>
              <input v-model.number="formData.count" type="number" required>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Категория:</label>
              <select v-model="formData.category" required>
                <option value="food">Еда</option>
                <option value="drink">Напитки</option>
                <option value="dessert">Десерты</option>
                <option value="alcohol">Алкоголь</option>
              </select>
            </div>
            <div class="form-group checkbox-group">
              <label>
                <input v-model="formData.is_for_table" type="checkbox">
                Только для стола
              </label>
            </div>
          </div>
          <div class="form-group">
            <label>URL изображения:</label>
            <input v-model="formData.image_url" type="url">
          </div>
          <div class="modal-actions">
            <button type="button" @click="closeModal" class="cancel-btn">
              Отмена
            </button>
            <button type="submit" class="save-btn">
              {{ editingProduct ? 'Обновить' : 'Создать' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Состояния загрузки и ошибки -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>Загружаем продукты...</p>
    </div>

    <div v-if="error" class="error-state">
      <p>❌ Ошибка: {{ error }}</p>
      <button @click="loadProducts" class="retry-btn">Попробовать снова</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { createApiService } from '@/services/api'
import type { Product, ProductCreate, ProductUpdate } from '@/types'

const authStore = useAuthStore()
const apiService = createApiService(authStore.telegramId)

const products = ref<Product[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const showAddModal = ref(false)
const editingProduct = ref<Product | null>(null)

const formData = reactive({
  name: '',
  description: '',
  price: 0,
  category: 'food',
  count: 0,
  is_for_table: false,
  image_url: ''
})

const getProductEmoji = (category: string) => {
  const emojis: Record<string, string> = {
    'food': '🍔',
    'drink': '🥤',
    'dessert': '🍰',
    'alcohol': '🍷'
  }
  return emojis[category] || '📦'
}

const loadProducts = async () => {
  loading.value = true
  error.value = null
  try {
    products.value = await apiService.getProducts()
    console.log(products.value)
  } catch (err: any) {
    error.value = err.message || 'Не удалось загрузить продукты'
  } finally {
    loading.value = false
  }
}

const editProduct = (product: Product) => {
  editingProduct.value = product
  Object.assign(formData, {
    name: product.name,
    description: product.description || '',
    price: product.price,
    category: product.category,
    count: product.count,
    is_for_table: product.is_for_table,
    image_url: product.image_url || ''
  })
}

const saveProduct = async () => {
  try {
    if (editingProduct.value) {
      // Обновление продукта
      const updateData: ProductUpdate = { ...formData }
      await apiService.updateProduct(editingProduct.value.id, updateData)
    } else {
      // Создание продукта
      const createData: ProductCreate = { ...formData }
      await apiService.createProduct(createData)
    }
    
    await loadProducts()
    closeModal()
  } catch (err: any) {
    alert('❌ Ошибка при сохранении: ' + (err.message || 'Неизвестная ошибка'))
  }
}

const deleteProduct = async (productId: number) => {
  if (!confirm('Вы уверены, что хотите удалить этот продукт?')) return
  
  try {
    await apiService.deleteProduct(productId)
    await loadProducts()
  } catch (err: any) {
    alert('❌ Ошибка при удалении: ' + (err.message || 'Неизвестная ошибка'))
  }
}

const closeModal = () => {
  showAddModal.value = false
  editingProduct.value = null
  Object.assign(formData, {
    name: '',
    description: '',
    price: 0,
    category: 'food',
    count: 0,
    is_for_table: false,
    image_url: ''
  })
}

onMounted(() => {
  loadProducts()
})
</script>

<style scoped>
.product-management {
  min-height: 400px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid rgba(0, 255, 255, 0.3);
}

.section-header h2 {
  color: #00ffff;
  margin: 0;
  font-size: 1.8rem;
}

.add-product-btn {
  background: linear-gradient(45deg, #00ff00, #00cc00);
  border: none;
  border-radius: 10px;
  color: #000;
  padding: 0.8rem 1.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-product-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 5px 15px rgba(0, 255, 0, 0.4);
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.product-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 1.5rem;
  display: flex;
  gap: 1rem;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.product-card:hover {
  border-color: #00ffff;
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(0, 255, 255, 0.2);
}

.product-image {
  width: 80px;
  height: 80px;
  border-radius: 10px;
  overflow: hidden;
  flex-shrink: 0;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-image-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #333, #555);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
}

.product-info {
  flex: 1;
}

.product-name {
  color: #fff;
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.product-description {
  color: #ccc;
  font-size: 0.9rem;
  margin: 0 0 0.8rem 0;
  line-height: 1.4;
}

.product-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.product-category {
  background: rgba(0, 255, 255, 0.2);
  color: #00ffff;
  padding: 0.2rem 0.6rem;
  border-radius: 10px;
  font-size: 0.8rem;
}

.product-price {
  color: #00ffff;
  font-weight: 700;
  font-size: 1.1rem;
}

.product-stock {
  color: #ccc;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.product-stock .low {
  color: #ff4444;
}

.product-flags {
  margin-bottom: 1rem;
}

.table-flag {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
  padding: 0.2rem 0.6rem;
  border-radius: 10px;
  font-size: 0.8rem;
}

.product-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.edit-btn, .delete-btn {
  background: none;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 5px;
  padding: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
}

.edit-btn:hover {
  background: rgba(0, 255, 255, 0.2);
  border-color: #00ffff;
}

.delete-btn:hover {
  background: rgba(255, 0, 0, 0.2);
  border-color: #ff4444;
}

/* Модальное окно */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3000;
  padding: 1rem;
}

.product-modal {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  border: 2px solid #00ffff;
  border-radius: 20px;
  padding: 2rem;
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.product-modal h3 {
  color: #00ffff;
  margin: 0 0 1.5rem 0;
  text-align: center;
  font-size: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group label {
  display: block;
  color: #fff;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.8rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  color: #fff;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #00ffff;
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox-group input[type="checkbox"] {
  width: auto;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.cancel-btn, .save-btn {
  flex: 1;
  padding: 1rem;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.cancel-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.save-btn {
  background: linear-gradient(45deg, #00ffff, #0080ff);
  color: #000;
}

.save-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 5px 15px rgba(0, 255, 255, 0.4);
}

/* Адаптивность */
@media (max-width: 768px) {
  .products-grid {
    grid-template-columns: 1fr;
  }
  
  .product-card {
    flex-direction: column;
    text-align: center;
  }
  
  .product-image {
    align-self: center;
  }
  
  .product-actions {
    flex-direction: row;
    justify-content: center;
  }
  
  .section-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .modal-actions {
    flex-direction: column;
  }
}
</style>