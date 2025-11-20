<template>
  <section class="contact">
    <div class="container">
      <h2 class="section-title neon-text">КОНТАКТЫ</h2>
      <div class="contact-links">
        <a href="https://t.me/leomaxslavanikitos" class="contact-link neon-hover">TELEGRAM</a>
        <a href="https://vk.com/slavatoxisss" class="contact-link neon-hover">VK</a>
      </div>
    </div>
  </section>
</template>

<style scoped>
.contact {
  padding: 4rem 0;
  background: #000;
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

.contact-links {
  display: flex;
  justify-content: center;
  gap: 3rem;
}

.contact-link {
  color: #fff;
  text-decoration: none;
  font-size: 1.2rem;
  text-transform: uppercase;
  letter-spacing: 0.1rem;
  padding: 1rem 2rem;
  border: 2px solid transparent;
  border-radius: 25px;
  transition: all 0.3s ease;
}

.neon-hover:hover {
  border-color: #00ffff;
  box-shadow: 
    0 0 10px #00ffff,
    inset 0 0 10px #00ffff;
  text-shadow: 0 0 10px #00ffff;
}

@media (max-width: 768px) {
  .section-title {
    font-size: 2rem;
  }
  
  .container {
    padding: 0 1rem;
  }
  
  .contact-links {
    flex-direction: column;
    align-items: center;
    gap: 0rem;
  }
}
</style>