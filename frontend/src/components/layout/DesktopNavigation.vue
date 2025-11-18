<template>
  <nav class="desktop-nav">
    <div class="nav-container">
      <!-- Логотип -->
      <router-link to="/" class="nav-brand">
        🎉 NEON PARTY
      </router-link>
      
      <!-- Основные ссылки -->
      <div class="nav-links">
        <router-link to="/" class="nav-link">Главная</router-link>
        <router-link to="/menu" class="nav-link">Меню</router-link>
        <router-link to="/profile" class="nav-link">Профиль</router-link>
      </div>
      
      <!-- Админские и staff ссылки -->
      <div class="staff-links" v-if="userStore.user?.role && ['admin', 'qr', 'chef', 'officiant'].includes(userStore.user.role)">
        <router-link 
          v-for="item in staffRoutes" 
          :key="item.path"
          :to="item.path"
          class="staff-link"
          :class="item.role"
        >
          <span class="staff-icon">{{ item.icon }}</span>
          <span class="staff-label">{{ item.name }}</span>
        </router-link>
      </div>
      
      <!-- Информация о пользователе -->
      <div class="user-info" v-if="userStore.user">
        <span class="user-name">
          {{ userStore.user.first_name || userStore.user.username }}
        </span>
        <span class="user-role" :class="userStore.user.role">
          {{ getUserRoleLabel(userStore.user.role) }}
        </span>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const staffRoutes = [
  { path: '/admin', name: 'Админ', icon: '👑', role: 'admin' },
  { path: '/officiant', name: 'Официант', icon: '🍽️', role: 'officiant' },
  { path: '/chef', name: 'Повар', icon: '👨‍🍳', role: 'chef' },
  { path: '/qr-scanner', name: 'QR Сканер', icon: '📱', role: 'qr' }
]

const getUserRoleLabel = (role: string) => {
  const roleLabels: { [key: string]: string } = {
    admin: 'Админ',
    officiant: 'Официант',
    chef: 'Повар',
    qr: 'QR',
    member: 'Гость',
    vip: 'VIP'
  }
  return roleLabels[role] || role
}
</script>

<style scoped>
.desktop-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  z-index: 1000;
  height: 70px;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
}

.nav-brand {
  font-size: 1.5rem;
  font-weight: bold;
  color: #00ffff;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-link {
  color: #fff;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #00ffff;
}

.nav-link.router-link-active {
  background: linear-gradient(45deg, #00ffff, #0080ff);
  color: #000;
  font-weight: bold;
}

.staff-links {
  display: flex;
  gap: 1rem;
}

.staff-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  text-decoration: none;
  color: #000;
  font-weight: bold;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.staff-link.admin {
  background: linear-gradient(45deg, #ff00ff, #ff0080);
}

.staff-link.officiant {
  background: linear-gradient(45deg, #ffff00, #ff8000);
}

.staff-link.chef {
  background: linear-gradient(45deg, #00ff00, #00cc00);
}

.staff-link.qr {
  background: linear-gradient(45deg, #00ffff, #0080ff);
}

.staff-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 255, 255, 0.2);
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.2rem;
}

.user-name {
  color: #fff;
  font-weight: 500;
}

.user-role {
  font-size: 0.7rem;
  padding: 0.2rem 0.5rem;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.user-role.admin {
  background: linear-gradient(45deg, #ff00ff, #ff0080);
  color: #000;
}

.user-role.officiant {
  background: linear-gradient(45deg, #ffff00, #ff8000);
  color: #000;
}

.user-role.chef {
  background: linear-gradient(45deg, #00ff00, #00cc00);
  color: #000;
}

.user-role.qr {
  background: linear-gradient(45deg, #00ffff, #0080ff);
  color: #000;
}

.user-role.vip {
  background: linear-gradient(45deg, #ffd700, #ff9900);
  color: #000;
}

/* Адаптивность для планшетов */
@media (max-width: 1024px) {
  .nav-container {
    padding: 0 1rem;
  }
  
  .nav-links {
    gap: 1rem;
  }
  
  .staff-links {
    gap: 0.5rem;
  }
  
  .staff-link {
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
  }
}
</style>