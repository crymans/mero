// stores/auth.ts
import { defineStore } from 'pinia'
import { computed } from 'vue'
import { useUserStore } from './user'
import type { UserRole } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const userStore = useUserStore()
  
  // Используем данные из userStore
  const user = computed(() => userStore.user)
  const telegramId = computed(() => userStore.user?.telegram_id || '')
  
  const isAuthenticated = computed(() => !!userStore.user)
  
  // Получаем роль из userStore
  const userRole = computed(() => {
    if (userStore.user && userStore.user.role) {
      return userStore.user.role as UserRole
    }
    return 'user' as UserRole
  })
  
  // Иерархия ролей
  const roleHierarchy: Record<UserRole, number> = {
    'user': 0,
    'qr': 1,
    'chef': 2,
    'officiant': 3,
    'admin': 4
  }
  
  // Проверка прав
  const hasPermission = (requiredRole: UserRole) => {
    const currentRole = userRole.value
    
    // Админ имеет все права
    if (currentRole === 'admin') return true
    
    // Для остальных ролей проверяем иерархию
    return roleHierarchy[currentRole] >= roleHierarchy[requiredRole]
  }
  
  const setUser = (userData: any) => {
    // Теперь устанавливаем пользователя через userStore
    userStore.user = userData
  }
  
  const setTelegramId = (id: string) => {
    // Telegram ID теперь берется из userStore.user
  }
  
  return {
    user,
    telegramId,
    isAuthenticated,
    userRole,
    hasPermission,
    setUser,
    setTelegramId
  }
})