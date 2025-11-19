import Home from '@/views/Home.vue'
import Menu from '@/views/MenuPage.vue'
import Profile from '@/views/Profile.vue'
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  { path: '/rostov_party', component: Home },
  { path: '/rostov_party/menu', component: Menu },
  { path: '/rostov_party/profile', component: Profile },
  // Админские маршруты
  {
    path: '/rostov_party/admin',
    name: 'Admin',
    component: () => import('@/components/admin/AdminPanel.vue'),
    meta: { requiresAuth: true, requiredRole: ['admin', 'chef', 'qr', 'officiant'] }
  },
  // {
  //   path: '/admin/users',
  //   name: 'AdminUsers',
  //   component: () => import('@/views/admin/UserManagement.vue'),
  //   meta: { requiresAuth: true, requiredRole: 'admin' }
  // },
  // {
  //   path: '/admin/products',
  //   name: 'AdminProducts',
  //   component: () => import('@/views/admin/ProductManagement.vue'),
  //   meta: { requiresAuth: true, requiredRole: 'admin' }
  // },
  // {
  //   path: '/admin/orders',
  //   name: 'AdminOrders',
  //   component: () => import('@/views/admin/OrderManagement.vue'),
  //   meta: { requiresAuth: true, requiredRole: 'admin' }
  // },
  // {
  //   path: '/admin/tickets',
  //   name: 'AdminTickets',
  //   component: () => import('@/views/admin/TicketManagement.vue'),
  //   meta: { requiresAuth: true, requiredRole: 'admin' }
  // },
  // {
  //   path: '/admin/analytics',
  //   name: 'AdminAnalytics',
  //   component: () => import('@/views/admin/AnalyticsView.vue'),
  //   meta: { requiresAuth: true, requiredRole: 'admin' }
  // },
  // {
  //   path: '/admin/settings',
  //   name: 'AdminSettings',
  //   component: () => import('@/views/admin/SettingsView.vue'),
  //   meta: { requiresAuth: true, requiredRole: 'admin' }
  // },
  // Страница официанта
  // {
  //   path: '/officiant',
  //   name: 'Officiant',
  //   component: () => import('@/views/staff/OfficiantView.vue'),
  //   meta: { requiresAuth: true, requiredRole: 'officiant' }
  // },
  // // Страница повара
  // {
  //   path: '/chef',
  //   name: 'Chef',
  //   component: () => import('@/views/staff/ChefView.vue'),
  //   meta: { requiresAuth: true, requiredRole: 'chef' }
  // },
  // // Страница QR сканера
  // {
  //   path: '/qr-scanner',
  //   name: 'QrScanner',
  //   component: () => import('@/views/staff/QrScannerView.vue'),
  //   meta: { requiresAuth: true, requiredRole: 'qr' }
  // }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Глобальный guard для проверки прав доступа
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  // Проверка аутентификации
  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    next('/')
    return
  }

  // Проверка ролей
  if (to.meta.requiredRole) {
    const userRole = userStore.user?.role
    
    if (!userRole) {
      next('/')
      return
    }

    // Админ имеет доступ ко всем страницам
    if (userRole !== 'admin' && !to.meta.requiredRole.includes(userRole)) {
      next('/')
      return
    }
  }

  next()
})

export default router