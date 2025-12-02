<template>
  <div id="app">
    <!-- Верхняя навигация для десктопа -->
    <DesktopNavigation v-if="!isMobile" />
    
    <!-- Основной контент с отступом для навигации -->
    <main class="main-content" :class="{ 'with-desktop-nav': !isMobile, 'with-mobile-nav': isMobile }">
      <router-view />
    </main>
    
    <!-- Нижняя навигация для мобильных устройств -->
    <BottomNavigation v-if="isMobile" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import BottomNavigation from '@/components/BottomNavigation.vue'
import DesktopNavigation from '@/components/layout/DesktopNavigation.vue'

<<<<<<< HEAD
try{window.Telegram.WebApp.disableVerticalSwipes()
window.Telegram.WebApp.requestFullscreen()
window.Telegram.WebApp.lockOrientation()
window.Telegram.WebApp.backgroundColor('#000000')
}
catch{
}

=======
>>>>>>> 7e9ba3fe22c549f8ccc0e6223dbc5677b26f11aa
// Определяем мобильное устройство
const isMobile = ref(false)

const checkMobile = () => {
  isMobile.value = window.innerWidth < 768
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', checkMobile)
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  background: #000;
  color: #fff;
  font-family: 'Arial', sans-serif;
  overflow-x: hidden;
}

#app {
  min-height: 100vh;
  background: #000;
}

/* Стили для основного контента */
.main-content {
  min-height: 100vh;
}

/* Отступы когда показывается десктопная навигация */
.main-content.with-desktop-nav {
  padding-top: 70px; /* Высота верхней навигации */
}

/* Отступы когда показывается мобильная навигация */
.main-content.with-mobile-nav {
  padding-bottom: 70px; /* Высота нижней навигации */
}

/* Кастомные стили для мобильной оптимизации */
@media (max-width: 768px) {
  .main-content.with-mobile-nav {
    padding-bottom: 60px;
  }
}

/* Улучшаем скроллбар */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #000;
}

::-webkit-scrollbar-thumb {
  background: #ff00ff;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #00ffff;
}

/* Убираем выделение при тапе на мобильных */
* {
  -webkit-tap-highlight-color: transparent;
}

/* Улучшаем рендеринг шрифтов */
body {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Оптимизация анимаций */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
</style>