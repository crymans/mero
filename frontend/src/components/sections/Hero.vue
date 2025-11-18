<template>
  <section class="hero">
    <div class="hero-overlay"></div>
    
    <!-- Animated Neon Background -->
    <div class="neon-grid">
      <div class="grid-line"></div>
      <div class="grid-line"></div>
      <div class="grid-line"></div>
      <div class="grid-line"></div>
    </div>

    <div class="hero-content">
      <!-- Main Title with Glitch Effect -->
      <h1 class="main-title">
        <span class="glitch" data-text="ЗАГРУЗКА">ЗАГРУЗКА</span>
      </h1>
      
      <p class="hero-subtitle">ULTIMATE TREPP TUSOVKA</p>
      
      <!-- Event Info -->
      <div class="event-info">
        <div class="info-item">
          <span class="neon-icon">🔥</span>
          <span>13 декабря | 16:00-05:00</span>
        </div>
        <div class="info-item">
          <span class="neon-icon">📍</span>
          <span>московская 64 | ROSTOV</span>
        </div>
      </div>

      <!-- CTA Buttons -->
      <div class="cta-buttons">
        <button class="neon-btn pink" @click="scrollToTickets">
          <span class="btn-text">БРОНЬ СТОЛА</span>
          <div class="neon-glow"></div>
        </button>
        <button class="neon-btn blue" @click="scrollToTickets">
          <span class="btn-text">КУПИТЬ БИЛЕТ</span>
          <div class="neon-glow"></div>
        </button>
      </div>

      <!-- Scroll Indicator -->
      <!-- <div class="scroll-indicator">
        <div class="scroll-line"></div>
      </div> -->
    </div>
  </section>
</template>

<script setup lang="ts">
const emit = defineEmits<{
  scrollToTickets: []
}>();

const scrollToTickets = () => {
  emit('scrollToTickets');
};
</script>

<style scoped>
.hero {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  /* background: radial-gradient(circle at center, #0a0a0a 0%, #000 100%); */
  background-image: url('./bg.png');
  background-position: center center;
  background-attachment: fixed;
  background-size: contain;
  
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.762);
  /* background: 
    radial-gradient(circle at 20% 80%, rgba(255, 0, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(0, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(255, 255, 0, 0.05) 0%, transparent 50%); */
    /* filter: brightness(1); */
}

.neon-grid {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  opacity: 0.3;
}

.grid-line {
  position: absolute;
  background: linear-gradient(90deg, transparent, #00ffff, transparent);
  height: 1px;
  width: 100%;
  animation: gridMove 20s linear infinite;
}

.grid-line:nth-child(1) { top: 25%; animation-delay: 0s; }
.grid-line:nth-child(2) { top: 50%; animation-delay: -5s; }
.grid-line:nth-child(3) { top: 75%; animation-delay: -10s; }
.grid-line:nth-child(4) { top: 100%; animation-delay: -15s; }

.hero-content {
  text-align: center;
  z-index: 10;
  position: relative;
}

.main-title {
  font-size: 9rem;
  font-weight: 900;
  margin-bottom: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.5rem;
}

.glitch {
  position: relative;
  color: #fff;
  text-shadow: 
    0 0 10px #ff00ff,
    0 0 20px #ff00ff,
    0 0 40px #ff00ff,
    0 0 80px #ff00ff;
  animation: glitch 5s infinite;
}

.glitch::before,
.glitch::after {
  content: attr(data-text);
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.glitch::before {
  animation: glitch-top 1s infinite;
  clip-path: polygon(0 0, 100% 0, 100% 33%, 0 33%);
  color: #00ffff;
}

.glitch::after {
  animation: glitch-bottom 1.5s infinite;
  clip-path: polygon(0 67%, 100% 67%, 100% 100%, 0 100%);
  color: #ffff00;
}

.hero-subtitle {
  font-size: 1.5rem;
  margin-bottom: 3rem;
  text-transform: uppercase;
  letter-spacing: 0.3rem;
  color: #00ffff;
  text-shadow: 0 0 10px #00ffff;
}

.event-info {
  display: flex;
  justify-content: center;
  gap: 3rem;
  margin-bottom: 3rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 1.2rem;
  text-transform: uppercase;
  letter-spacing: 0.1rem;
}

.neon-icon {
  font-size: 1.5rem;
  filter: drop-shadow(0 0 5px currentColor);
}

.cta-buttons {
  display: flex;
  gap: 2rem;
  justify-content: center;
  margin-bottom: 4rem;
}

.neon-btn {
  position: relative;
  padding: 1.2rem 2.5rem;
  border: none;
  background: transparent;
  color: white;
  font-size: 1.1rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.1rem;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
}

.neon-btn.pink {
  border: 2px solid #ff00ff;
  box-shadow: 
    0 0 10px #ff00ff,
    inset 0 0 10px #ff00ff;
}

.neon-btn.blue {
  border: 2px solid #00ffff;
  box-shadow: 
    0 0 10px #00ffff,
    inset 0 0 10px #00ffff;
}

.neon-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
  transition: left 0.5s ease;
}

.neon-btn:hover .neon-glow {
  left: 100%;
}

.neon-btn:hover {
  transform: translateY(-2px);
}

.neon-btn.pink:hover {
  box-shadow: 
    0 0 20px #ff00ff,
    0 0 40px #ff00ff,
    inset 0 0 20px #ff00ff;
}

.neon-btn.blue:hover {
  box-shadow: 
    0 0 20px #00ffff,
    0 0 40px #00ffff,
    inset 0 0 20px #00ffff;
}

.scroll-indicator {
  position: absolute;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
}

.scroll-line {
  width: 2px;
  height: 50px;
  background: linear-gradient(to bottom, #ff00ff, transparent);
  animation: scrollBounce 2s infinite;
}

@keyframes glitch {
  0%, 100% { transform: translate(0); }
  20% { transform: translate(-2px, 2px); }
  40% { transform: translate(-2px, -2px); }
  60% { transform: translate(2px, 2px); }
  80% { transform: translate(2px, -2px); }
}

@keyframes glitch-top {
  0%, 100% { transform: translate(0); }
  33% { transform: translate(-2px, -2px); }
  66% { transform: translate(2px, 2px); }
}

@keyframes glitch-bottom {
  0%, 100% { transform: translate(0); }
  33% { transform: translate(2px, 2px); }
  66% { transform: translate(-2px, -2px); }
}

@keyframes gridMove {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

@keyframes scrollBounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}

@media (max-width: 768px) {
  .main-title {
    font-size: 4rem;
  }
  
  .hero-subtitle {
    font-size: 1rem;
  }
  
  .event-info {
    flex-direction: column;
    gap: 1rem;
  }
  
  .cta-buttons {
    flex-direction: column;
    align-items: center;
  }
}
</style>