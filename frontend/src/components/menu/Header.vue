<template>
  <div class="menu-header">
    <h1>🍹 МЕНЮ БАРА</h1>
    <p>Выбери свои любимые напитки и закуски</p>
    <div class="header-glow"></div>
  </div>
</template>

<style scoped>
.menu-header {
  text-align: center;
  margin-bottom: 3rem;
  position: relative;
  padding: 2rem 0;
}

.menu-header h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  background: linear-gradient(45deg, #ff00ff, #00ffff, #ffff00);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 0 30px rgba(255, 0, 255, 0.5);
  animation: titleGlow 3s ease-in-out infinite alternate;
}

.menu-header p {
  color: #ccc;
  font-size: 1.2rem;
  margin-bottom: 0;
}

.header-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 300px;
  height: 100px;
  background: radial-gradient(circle, rgba(255, 0, 255, 0.3) 0%, transparent 70%);
  filter: blur(40px);
  z-index: -1;
}

@keyframes titleGlow {
  0% {
    text-shadow: 0 0 20px rgba(255, 0, 255, 0.5),
                 0 0 40px rgba(255, 0, 255, 0.3);
  }
  100% {
    text-shadow: 0 0 30px rgba(0, 255, 255, 0.5),
                 0 0 60px rgba(0, 255, 255, 0.3);
  }
}

@media (max-width: 768px) {
  .menu-header h1 {
    font-size: 2rem;
  }
  
  .menu-header p {
    font-size: 1rem;
  }
}
</style>