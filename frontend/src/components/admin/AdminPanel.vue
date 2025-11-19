<!-- components/admin/AdminPanel.vue -->
<template>
  <div class="admin-panel">
    <div class="admin-header">
      <h1>⚙️ Панель администратора</h1>
      <p>Управление системой и пользователями</p>
      <div class="current-role">
        Текущая роль: <span :class="authStore.userRole">{{ getRoleName(authStore.userRole) }}</span>
      </div>
      <!-- Добавим отладочную информацию -->
      <!-- <div v-if="debugInfo" class="debug-info">
        <p>User data: {{ JSON.stringify(authStore.user) }}</p>
        <p>Computed role: {{ authStore.userRole }}</p>
      </div> -->
    </div>

    <!-- Остальной код без изменений -->
    <div class="admin-tabs">
      <button
        v-for="tab in filteredTabs"
        :key="tab.id"
        :class="['tab-btn', { active: activeTab === tab.id }]"
        @click="activeTab = tab.id"
      >
        <span class="tab-icon">{{ tab.icon }}</span>
        <span class="tab-text">{{ tab.name }}</span>
      </button>
    </div>

    <div class="tab-content">
      <!-- Управление пользователями (только admin) -->
      <div v-if="activeTab === 'users'" class="tab-pane">
        <UserManagement v-if="authStore.hasPermission('admin')" />
        <NoAccess v-else :required-role="'Администратор'" />
      </div>

      <!-- Управление продуктами (только admin) -->
      <div v-if="activeTab === 'products'" class="tab-pane">
        <ProductManagement v-if="authStore.hasPermission('admin')" />
        <NoAccess v-else :required-role="'Администратор'" />
      </div>

      <!-- Все заказы (chef и admin) -->
      <div v-if="activeTab === 'orders'" class="tab-pane">
        <ChefOrders v-if="authStore.hasPermission('chef')" />
        <NoAccess v-else :required-role="'Повар'" />
      </div>

      <!-- Выполненные заказы (officiant и admin) -->
      <div v-if="activeTab === 'fulfilled'" class="tab-pane">
        <OfficiantOrders v-if="authStore.hasPermission('officiant')" />
        <NoAccess v-else :required-role="'Официант'" />
      </div>

      <!-- Сканирование QR (qr и admin) -->
      <div v-if="activeTab === 'qr'" class="tab-pane">
        <QrScanner v-if="authStore.hasPermission('qr')" />
        <NoAccess v-else :required-role="'QR Scanner'" />
      </div>

      <!-- Статистика (только admin)
      <div v-if="activeTab === 'stats'" class="tab-pane">
        <AdminStats v-if="authStore.hasPermission('admin')" />
        <NoAccess v-else :required-role="'Администратор'" />
      </div> -->
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import UserManagement from '@/components/admin/UserManagement.vue'
import ProductManagement from '@/components/admin/ProductManagement.vue'
import ChefOrders from '@/components/admin/ChefOrders.vue'
import OfficiantOrders from '@/components/admin/OfficiantOrders.vue'
import QrScanner from '@/components/admin/QrScanner.vue'
// import AdminStats from '@/components/admin/AdminStats.vue'
// import NoAccess from '@/components/admin/NoAccess.vue'

const authStore = useAuthStore()
const activeTab = ref('')
const debugInfo = ref(true) // Включите для отладки, затем отключите

// Все возможные вкладки с требованиями к ролям
const allTabs = [
  { id: 'users', name: 'Пользователи', icon: '👥', roles: ['admin'] },
  { id: 'products', name: 'Продукты', icon: '🍔', roles: ['admin'] },
  { id: 'orders', name: 'Все заказы', icon: '📦', roles: ['chef', 'admin'] },
  { id: 'fulfilled', name: 'Выполненные', icon: '✅', roles: ['officiant', 'admin'] },
  { id: 'qr', name: 'QR Сканер', icon: '📱', roles: ['qr', 'admin'] },
  { id: 'stats', name: 'Статистика', icon: '📊', roles: ['admin'] }
]

// Отфильтрованные вкладки для текущей роли
const filteredTabs = computed(() => {
  return allTabs.filter(tab => 
    tab.roles.some(role => hasRoleAccess(role))
  )
})

// Проверка доступа к роли
const hasRoleAccess = (role: string) => {
  // Для роли admin проверяем специально
  if (role === 'admin') {
    return authStore.userRole === 'admin'
  }
  // Для остальных ролей проверяем через hasPermission
  return authStore.hasPermission(role as any)
}

// Установка активной вкладки при изменении роли
watch(filteredTabs, (newTabs) => {
  if (newTabs.length > 0 && (!activeTab.value || !filteredTabs.value.some(tab => tab.id === activeTab.value))) {
    activeTab.value = newTabs[0].id
  }
}, { immediate: true })

const getRoleName = (role: string) => {
  const names: Record<string, string> = {
    'member': '👤 Пользователь',
    'qr': '📱 QR Scanner',
    'chef': '👨‍🍳 Повар',
    'officiant': '💁 Официант',
    'admin': '⚙️ Администратор'
  }
  return names[role] || role
}
</script>

<style scoped>
.debug-info {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(255, 0, 0, 0.1);
  border-radius: 10px;
  font-size: 0.8rem;
  color: #ff4444;
}

.debug-info p {
  margin: 0.2rem 0;
}

/* Остальные стили без изменений */
.admin-panel {
  padding: 2rem;
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
}

.admin-header {
  text-align: center;
  margin-bottom: 3rem;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  border: 1px solid rgba(0, 255, 255, 0.2);
  backdrop-filter: blur(10px);
}

.admin-header h1 {
  color: #00ffff;
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
  text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
}

.admin-header p {
  color: #ccc;
  font-size: 1.2rem;
  margin: 0 0 1rem 0;
}

.current-role {
  color: #fff;
  font-size: 1rem;
}

.current-role span {
  padding: 0.3rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  text-transform: uppercase;
}

.current-role span.admin {
  background: linear-gradient(45deg, #00ffff, #0080ff);
  color: #000;
}

.current-role span.chef {
  background: linear-gradient(45deg, #ff4444, #ff0080);
  color: #fff;
}

.current-role span.officiant {
  background: linear-gradient(45deg, #ffd700, #ff6b00);
  color: #000;
}

.current-role span.qr {
  background: linear-gradient(45deg, #00ff00, #00cc00);
  color: #000;
}

.admin-tabs {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 3rem;
  padding: 0 1rem;
}

.tab-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.8rem;
  padding: 1.5rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid transparent;
  border-radius: 15px;
  color: #fff;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.tab-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(0, 255, 255, 0.2);
}

.tab-btn.active {
  background: linear-gradient(135deg, #00ffff, #0080ff);
  color: #000;
  border-color: #00ffff;
  box-shadow: 0 10px 30px rgba(0, 255, 255, 0.4);
  transform: translateY(-3px);
}

.tab-icon {
  font-size: 2rem;
}

.tab-text {
  font-size: 1rem;
  font-weight: 600;
  text-align: center;
}

.tab-content {
  background: rgba(255, 255, 255, 0.02);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  min-height: 500px;
}

.tab-pane {
  padding: 2rem;
}

@media (max-width: 768px) {
  .admin-panel {
    padding: 1rem;
  }
  
  .admin-header {
    padding: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .admin-header h1 {
    font-size: 2rem;
  }
  
  .admin-tabs {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.8rem;
  }
  
  .tab-btn {
    padding: 1rem 0.5rem;
  }
  
  .tab-icon {
    font-size: 1.5rem;
  }
  
  .tab-text {
    font-size: 0.9rem;
  }
  
  .tab-pane {
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .admin-tabs {
    grid-template-columns: 1fr;
  }
}
</style>