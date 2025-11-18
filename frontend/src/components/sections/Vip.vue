<template>
  <!-- <section class="vip">
    <div class="container">
      <div class="vip-content">
        <h2 class="section-title neon-text">VIP EXPERIENCE</h2>
        <div class="vip-features">
          <div class="vip-item" v-for="item in vipFeatures" :key="item">
            <span class="vip-icon">✨</span>
            <span>{{ item }}</span>
          </div>
        </div>
      </div>
    </div>
  </section> -->
</template>

<script setup lang="ts">
import { ref } from 'vue'

const vipFeatures = ref([
  'ОТДЕЛЬНЫЙ ВХОД',
  'PERSONAL HOST',
  'PREMIUM ALCOHOL',
  'BOTTLE SERVICE',
  'SECURITY',
  'PHOTO ZONE'
])
</script>

<style scoped>
.vip {
  padding: 6rem 0;
  background: linear-gradient(45deg, #000, #0a0020, #000);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.section-title {
  font-size: 3rem;
  text-align: center;
  margin-bottom: 4rem;
  text-transform: uppercase;
  letter-spacing: 0.3rem;
}

.neon-text {
  text-shadow: 
    0 0 10px currentColor,
    0 0 20px currentColor,
    0 0 40px currentColor;
}

.vip-features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  text-align: center;
}

.vip-item {
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.vip-item:hover {
  border-color: #ff00ff;
  box-shadow: 0 0 20px rgba(255, 0, 255, 0.3);
  transform: translateY(-5px);
}

.vip-icon {
  font-size: 2rem;
  display: block;
  margin-bottom: 1rem;
  filter: drop-shadow(0 0 5px #ffff00);
}

@media (max-width: 768px) {
  .section-title {
    font-size: 2rem;
  }
  
  .container {
    padding: 0 1rem;
  }
  
  .vip-features {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
  }
}
</style>