<template>
  <!-- <section class="lineup">
    <div class="container">
      <h2 class="section-title neon-text">LINE UP</h2>
      
      <div class="dj-grid">
        <div class="dj-card" v-for="dj in djs" :key="dj.name">
          <div class="dj-image" :style="{ background: dj.color }"></div>
          <div class="dj-info">
            <h3>{{ dj.name }}</h3>
            <p>{{ dj.genre }}</p>
            <span class="dj-time">{{ dj.time }}</span>
          </div>
        </div>
      </div>
    </div>
  </section> -->
</template>

<script setup lang="ts">
import { ref } from 'vue'

const djs = ref([]
//   [
//   { name: 'RAZOGREV', genre: '13+', time: '16:00-22:00', color: 'linear-gradient(45deg, #ff00ff, #00ffff)' },
//   { name: 'OSNOVNAYA', genre: '18+', time: '00:00-02:00', color: 'linear-gradient(45deg, #00ff00, #ffff00)' },
//   { name: 'BASS KILLER', genre: 'DUBSTEP', time: '02:00-04:00', color: 'linear-gradient(45deg, #ff0000, #ff00ff)' },
//   { name: 'TREPP GOD', genre: 'MAIN STAGE', time: '04:00-06:00', color: 'linear-gradient(45deg, #0000ff, #00ffff)' }
// ]
)
</script>

<style scoped>
.lineup {
  padding: 6rem 0;
  background: linear-gradient(to bottom, #000, #0a0a0a, #000);
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

.dj-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.dj-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.dj-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
  transition: left 0.5s ease;
}

.dj-card:hover::before {
  left: 100%;
}

.dj-card:hover {
  transform: translateY(-5px);
  border-color: #ff00ff;
  box-shadow: 0 0 20px rgba(255, 0, 255, 0.3);
}

.dj-image {
  height: 120px;
  border-radius: 10px;
  margin-bottom: 1rem;
  position: relative;
}

.dj-image::after {
  content: '🎧';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 2rem;
  filter: drop-shadow(0 0 10px rgba(255,255,255,0.5));
}

.dj-info h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: #00ffff;
}

.dj-info p {
  color: #ccc;
  margin-bottom: 0.5rem;
}

.dj-time {
  color: #ff00ff;
  font-weight: bold;
}

@media (max-width: 768px) {
  .section-title {
    font-size: 2rem;
  }
  
  .container {
    padding: 0 1rem;
  }
}
</style>