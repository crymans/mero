<template>
  <nav class="bottom-nav">
    <router-link 
      v-for="item in navItems" 
      :key="item.path"
      :to="item.path"
      class="nav-item"
      :class="{ active: $route.path === item.path }"
    >
      <div class="nav-icon">
        <component :is="item.icon" />
      </div>
      <span class="nav-label">{{ item.name }}</span>
    </router-link>

    <!-- Кнопка админа для соответствующих ролей -->
    <router-link 
      v-if="showAdminButton"
      to="/admin"
      class="nav-item admin-item"
      :class="{ active: $route.path.startsWith('/admin') || isStaffRoute }"
    >
      <div class="nav-icon">
        <AdminIcon />
      </div>
      <span class="nav-label">Admin</span>
    </router-link>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const userStore = useUserStore()

// Проверяем, нужно ли показывать кнопку админа
const showAdminButton = computed(() => {
  const userRole = userStore.user?.role
  return userRole && ['admin', 'qr', 'chef', 'officiant'].includes(userRole)
})

// Проверяем, находимся ли на staff странице
const isStaffRoute = computed(() => {
  return ['/officiant', '/chef', '/qr-scanner'].includes(route.path)
})

// Иконки для навигации
const HomeIcon = {
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
            d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
    </svg>
  `
}

const MenuIcon = {
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
            d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"/>
    </svg>
  `
}

const ProfileIcon = {
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
            d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
    </svg>
  `
}

const AdminIcon = {
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
            d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
    </svg>
  `
}

const navItems = [
  { path: '/', name: 'Главная', icon: HomeIcon },
  { path: '/menu', name: 'Меню', icon: MenuIcon },
  { path: '/profile', name: 'Профиль', icon: ProfileIcon }
]
</script>

<style scoped>
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.95);
  backdrop-filter: blur(20px);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  padding: 0.5rem 0;
  z-index: 1000;
}

.nav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.5rem;
  text-decoration: none;
  color: #666;
  transition: all 0.3s ease;
  position: relative;
}

.nav-item.active {
  color: #ff00ff;
}

.nav-item.active::before {
  content: '';
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 30px;
  height: 2px;
  background: #ff00ff;
  border-radius: 1px;
}

/* Специальные стили для админ кнопки */
.admin-item.active {
  color: #00ffff;
}

.admin-item.active::before {
  background: #00ffff;
}

.nav-icon {
  width: 24px;
  height: 24px;
  margin-bottom: 0.25rem;
}

.nav-label {
  font-size: 0.7rem;
  font-weight: 500;
}

/* Анимация для активного состояния */
.nav-item.active .nav-icon {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

/* Адаптивность */
@media (max-width: 768px) {
  .bottom-nav {
    padding: 0.5rem 0;
  }
  
  .nav-label {
    font-size: 0.65rem;
  }
  
  /* Если показывается админ кнопка, уменьшаем отступы */
  .bottom-nav:has(.admin-item) .nav-item {
    padding: 0.5rem 0.3rem;
  }
}

@media (max-width: 480px) {
  .nav-label {
    font-size: 0.6rem;
  }
  
  .nav-icon {
    width: 20px;
    height: 20px;
    margin-bottom: 0.2rem;
  }
}
</style>