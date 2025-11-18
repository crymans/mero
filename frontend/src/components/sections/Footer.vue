<template>
  <footer class="footer">
    <div class="container">
      <p>NEON DROP | ROSTOV-ON-DON | 18+</p>
      <p class="warning">🚫 НАРКОТИКИ ЗАПРЕЩЕНЫ</p>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  padding: 2rem 0;
  background: #000;
  text-align: center;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.warning {
  color: #ff0000;
  text-shadow: 0 0 10px #ff0000;
  margin-top: 1rem;
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }
}
</style>