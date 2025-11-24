<template>
  <div class="user-management">
    <div class="section-header">
      <h2>👥 Управление пользователями</h2>
      <div class="header-stats">
        <span class="stat">Всего: {{ users.length }}</span>
        <span class="stat">Админы: {{ adminCount }}</span>
        <span class="stat">Пользователи: {{ memberCount }}</span>
      </div>
    </div>

    <div class="controls">
      <button 
        @click="loadUsers" 
        :disabled="isLoading"
        class="refresh-btn"
      >
        🔄 Обновить
      </button>
    </div>

    <div class="users-grid" v-if="users.length > 0">
      <div 
        v-for="user in users" 
        :key="user.id"
        :class="['user-card', user.role]"
      >
        <div class="user-avatar">
          {{ getUserInitials(user) }}
        </div>
        
        <div class="user-info">
          <h3 class="user-name">
            {{ user.first_name || 'Без имени' }} {{ user.last_name || '' }}
          </h3>
          <p class="user-telegram">
            <span v-if="user.username">@{{ user.username }}</span>
            <span v-else>без username</span>
          </p>
          <p class="user-telegram-id">Telegram ID: {{ user.telegram_id }}</p>
          <p class="user-phone" v-if="user.phone">📱 {{ user.phone }}</p>
          <p class="user-balance" v-if="user.balance !== undefined">
            Баланс: {{ user.balance }} ₽
          </p>
          <p class="user-joined">
            Зарегистрирован: {{ formatDate(user.created_at) }}
          </p>
        </div>

        <div class="user-actions">
          <div class="role-selector">
            <label>Роль:</label>
            <select 
              :value="user.role" 
              @change="updateUserRole(user.telegram_id, $event.target.value)"
              :disabled="user.role === 'admin' || isLoading"
              :class="{ disabled: user.role === 'admin' }"
            >
              <option value="member">👤 Пользователь</option>
              <option value="qr">📱 QR Scanner</option>
              <option value="chef">👨‍🍳 Повар</option>
              <option value="officiant">💁 Официант</option>
             
              <option value="standard">⭐ STANDARD</option>
              <option value="fast">⭐ FAST</option>
               <option value="vip">⭐ VIP</option>
              
            </select>
          </div>
          
          <div class="user-badge" :class="user.role">
            {{ getRoleName(user.role) }}
          </div>
        </div>
      </div>
    </div>

    <!-- Состояние загрузки -->
    <div v-if="isLoading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>Загружаем пользователей...</p>
    </div>

    <!-- Состояние ошибки -->
    <div v-if="error" class="error-state">
      <p>❌ Ошибка: {{ error }}</p>
      <button @click="loadUsers" class="retry-btn">Попробовать снова</button>
    </div>

    <!-- Состояние пустого списка -->
    <div v-if="!isLoading && users.length === 0" class="empty-state">
      <p>Пользователи не найдены</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAdminStore } from '@/stores/admin'
import type { User } from '@/stores/admin'

// Создаем локальные реактивные переменные
const users = ref<User[]>([])
const isLoading = ref(false)
const error = ref<string | null>(null)

const adminCount = computed(() => {
  return users.value.filter(user => user.role === 'admin').length
})

const memberCount = computed(() => {
  return users.value.filter(user => user.role === 'member').length
})

const getUserInitials = (user: User) => {
  const first = user.first_name?.[0] || 'U'
  const last = user.last_name?.[0] || 'S'
  return (first + last).toUpperCase()
}

const getRoleName = (role: string) => {
  const names: Record<string, string> = {
    'member': '👤 Пользователь',
    'user': '👤 Пользователь',
    'vip': '⭐ VIP',
    'qr': '📱 QR Scanner',
    'chef': '👨‍🍳 Повар',
    'officiant': '💁 Официант',
    'admin': '⚙️ Админ'
  }
  return names[role] || role
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const loadUsers = async () => {
  isLoading.value = true
  error.value = null
  try {
    const adminStore = useAdminStore()
    await adminStore.fetchAllUsers()
    users.value = adminStore.users
    console.log(users.value)
  } catch (err: any) {
    error.value = err.message || 'Ошибка при загрузке пользователей'
    console.error('Error loading users:', err)
  } finally {
    isLoading.value = false
  }
}

const updateUserRole = async (telegramId: string, newRole: string) => {
  if (newRole === 'admin') return
  
  try {
    const adminStore = useAdminStore()
    await adminStore.updateUserRole(telegramId, newRole)
    // После успешного обновления перезагружаем список
    await loadUsers()
  } catch (err: any) {
    error.value = err.message || 'Ошибка при обновлении роли'
    console.error('Error updating user role:', err)
  }
}

onMounted(() => {
  loadUsers()
})
</script>

<style scoped>
.user-management {
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

.header-stats {
  display: flex;
  gap: 1.5rem;
}

.stat {
  background: rgba(0, 255, 255, 0.2);
  color: #00ffff;
  padding: 0.5rem 1rem;
  border-radius: 10px;
  font-weight: 600;
}

.users-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 1.5rem;
}

.user-card {
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid transparent;
  border-radius: 15px;
  padding: 1.5rem;
  display: flex;
  gap: 1.5rem;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.user-card:hover {
  border-color: rgba(0, 255, 255, 0.3);
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(0, 255, 255, 0.2);
}

.user-card.admin {
  border-color: #00ffff;
  background: rgba(0, 255, 255, 0.1);
}

.user-card.chef {
  border-color: #ff4444;
  background: rgba(255, 68, 68, 0.1);
}

.user-card.officiant {
  border-color: #ffd700;
  background: rgba(255, 215, 0, 0.1);
}

.user-card.qr {
  border-color: #00ff00;
  background: rgba(0, 255, 0, 0.1);
}

.user-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #00ffff, #0080ff);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: #000;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.user-info {
  flex: 1;
}

.user-name {
  color: #fff;
  margin: 0 0 0.5rem 0;
  font-size: 1.2rem;
  font-weight: 600;
}

.user-telegram {
  color: #00ffff;
  margin: 0 0 0.3rem 0;
  font-size: 0.9rem;
}

.user-phone {
  color: #ccc;
  margin: 0 0 0.3rem 0;
  font-size: 0.9rem;
}

.user-joined {
  color: #666;
  margin: 0;
  font-size: 0.8rem;
}

.user-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  min-width: 150px;
}

.role-selector {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.role-selector label {
  color: #ccc;
  font-size: 0.8rem;
  font-weight: 600;
}

.role-selector select {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  color: #fff;
  padding: 0.5rem;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.role-selector select:focus {
  outline: none;
  border-color: #00ffff;
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
}

.role-selector select.disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.user-badge {
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-align: center;
  text-transform: uppercase;
}

.user-badge.admin {
  background: linear-gradient(45deg, #00ffff, #0080ff);
  color: #000;
}

.user-badge.chef {
  background: linear-gradient(45deg, #ff4444, #ff0080);
  color: #fff;
}

.user-badge.officiant {
  background: linear-gradient(45deg, #ffd700, #ff6b00);
  color: #000;
}

.user-badge.qr {
  background: linear-gradient(45deg, #00ff00, #00cc00);
  color: #000;
}

.user-badge.user {
  background: #333;
  color: #fff;
}

.loading-state {
  text-align: center;
  padding: 3rem;
  color: #fff;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #333;
  border-top: 4px solid #00ffff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

.error-state {
  text-align: center;
  padding: 2rem;
  background: rgba(255, 0, 0, 0.1);
  border: 1px solid rgba(255, 0, 0, 0.3);
  border-radius: 10px;
  color: #ff4444;
}

.retry-btn {
  background: linear-gradient(45deg, #00ffff, #0080ff);
  border: none;
  border-radius: 5px;
  color: white;
  padding: 10px 20px;
  margin-top: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .users-grid {
    grid-template-columns: 1fr;
  }
  
  .user-card {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
  
  .user-actions {
    min-width: auto;
  }
  
  .section-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .header-stats {
    justify-content: center;
  }
}
</style>