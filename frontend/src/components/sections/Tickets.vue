<template>
  <section class="tickets" id="tickets">
    <div class="container">
      <h2 class="section-title neon-text">БИЛЕТЫ НА ТУСОВКУ</h2>
      <p class="section-subtitle">Выбери свой вариант и присоединяйся к легенде!</p>
      
      <!-- Основные билеты -->
      <div class="tickets-main">
        <div class="ticket-cards">
          <!-- Базовый билет -->
          <div class="ticket-card basic">
            <div class="ticket-badge">🔥 ВЫГОДА</div>
            <div class="ticket-ribbon">РЕПОСТ = СКИДКА</div>
            <div class="ticket-content">
              <div class="ticket-header">
                <h3>STANDARD</h3>
                <div class="price">
                  <span class="old-price">900 ₽</span>
                  <span class="current-price">750 ₽</span>
                </div>
              </div>
              <div class="ticket-features">
                <div class="feature">
                  <span class="feature-icon">🎫</span>
                  <span>Вход на вечеринку</span>
                </div>
                <div class="feature">
                  <span class="feature-icon">💃</span>
                  <span>Танцпол</span>
                </div>
                <div class="feature">
                  <span class="feature-icon">🍻</span>
                  <span>Базовый бар</span>
                </div>
                <div class="feature disabled">
                  <span class="feature-icon">🛋️</span>
                  <span>Сидячие места</span>
                </div>
              </div>
              <div class="ticket-conditions">
                <p>✓ Сделай репост мероприятия</p>
                <p>✓ Покажи на входе</p>
              </div>
              <button class="ticket-btn basic-btn" @click="buyTicket('standard')">
                <span class="btn-text">ВЗЯТЬ ПО СКИДКЕ</span>
                <span class="btn-glow"></span>
              </button>
            </div>
          </div>

          <!-- Быстрый вход -->
          <div class="ticket-card standard">
            <div class="ticket-badge">⚡ ПОПУЛЯРНО</div>
            <div class="ticket-content">
              <div class="ticket-header">
                <h3>FAST ENTRY</h3>
                <div class="price">
                  <span class="current-price">900 ₽</span>
                </div>
              </div>
              <div class="ticket-features">
                <div class="feature">
                  <span class="feature-icon">🚀</span>
                  <span>Быстрый вход</span>
                </div>
                <div class="feature">
                  <span class="feature-icon">🎫</span>
                  <span>Вход на вечеринку</span>
                </div>
                <div class="feature">
                  <span class="feature-icon">💃</span>
                  <span>Танцпол</span>
                </div>
                <div class="feature">
                  <span class="feature-icon">🍻</span>
                  <span>Базовый бар</span>
                </div>
              </div>
              <div class="ticket-conditions">
                <p>✓ Без проверки репоста</p>
                <p>✓ Приоритетный вход</p>
              </div>
              <button class="ticket-btn standard-btn" @click="buyTicket('fast')">
                <span class="btn-text">БЫСТРЫЙ ВХОД</span>
                <span class="btn-glow"></span>
              </button>
            </div>
          </div>

          <!-- VIP билет -->
          <div class="ticket-card vip">
            <div class="ticket-badge">👑 ПРЕМИУМ</div>
            <div class="ticket-content">
              <div class="ticket-header">
                <h3>VIP EXPERIENCE</h3>
                <div class="price">
                  <span class="current-price">1300 ₽</span>
                </div>
              </div>
              <div class="ticket-features">
                <div class="feature">
                  <span class="feature-icon">⭐</span>
                  <span>VIP вход</span>
                </div>
                <div class="feature">
                  <span class="feature-icon">🛋️</span>
                  <span>Место за столом</span>
                </div>
                <div class="feature">
                  <span class="feature-icon">🍾</span>
                  <span>Премиум бар</span>
                </div>
                <div class="feature">
                  <span class="feature-icon">🎯</span>
                  <span>Персональный сервис</span>
                </div>
              </div>
              <div class="ticket-conditions">
                <p>✓ Гарантированное место</p>
                <p>✓ Лучший сервис</p>
              </div>
              <button class="ticket-btn vip-btn" @click="buyTicket('vip')">
                <span class="btn-text">VIP ДОСТУП</span>
                <span class="btn-glow"></span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Дополнительные услуги -->
      <div class="services">
        <h3 class="subsection-title">ДОПОЛНИТЕЛЬНО НА МЕСТЕ</h3>
        <p class="services-subtitle">Эти услуги можно заказать непосредственно на вечеринке</p>
        
        <div class="service-cards">
          <div class="service-card">
            <div class="service-icon">💨</div>
            <div class="service-content">
              <h4>КАЛЬЯН</h4>
              <div class="service-price">1600 ₽</div>
              <p class="service-desc">На компанию до 4 человек • 1 час</p>
              <ul class="service-features">
                <li>✓ Премиальный табак</li>
                <li>✓ Любые вкусы</li>
                <li>✓ Профессиональный кальянщик</li>
              </ul>
            </div>
          </div>

          <div class="service-card">
            <div class="service-icon">🛏️</div>
            <div class="service-content">
              <h4>КОМНАТА УЕДИНЕНИЯ</h4>
              <div class="service-price">2000 ₽</div>
              <p class="service-desc">2-спальная кровать • 1 час</p>
              <ul class="service-features">
                <li>✓ Полная приватность</li>
                <li>✓ Комфортный отдых</li>
                <li>✓ Отдельный вход</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const emit = defineEmits<{
  buyTicket: [type: string]
}>();

const buyTicket = (type: string) => {
  emit('buyTicket', type);
};
</script>

<style scoped>
.tickets {
  padding: 3rem 1rem;
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

.section-subtitle {
  text-align: center;
  color: #ccc;
  margin-bottom: 2rem;
  font-size: 1rem;
}

.ticket-cards {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  max-width: 400px;
  margin: 0 auto 3rem;
}

.ticket-card {
  position: relative;
  background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
  border-radius: 20px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.1);
  transition: all 0.3s ease;
  overflow: hidden;
}

.ticket-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
  transition: left 0.5s ease;
}

.ticket-card:hover::before {
  left: 100%;
}

.ticket-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

.ticket-card.basic {
  border-color: #00ffff;
}

.ticket-card.standard {
  border-color: #ffff00;
  transform: scale(1.02);
}

.ticket-card.vip {
  border-color: #ff00ff;
}

.ticket-badge {
  position: absolute;
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  background: currentColor;
  color: #000;
  padding: 0.4rem 1.2rem;
  border-radius: 15px;
  font-size: 0.7rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  z-index: 2;
}

.ticket-ribbon {
  position: absolute;
  top: 10px;
  right: -30px;
  background: #ff0000;
  color: white;
  padding: 0.3rem 2rem;
  font-size: 0.7rem;
  font-weight: bold;
  transform: rotate(45deg);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.ticket-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.ticket-header h3 {
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.price {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.old-price {
  color: #666;
  text-decoration: line-through;
  font-size: 0.9rem;
}

.current-price {
  font-size: 1.8rem;
  font-weight: bold;
  color: currentColor;
}

.ticket-features {
  margin-bottom: 1.5rem;
}

.feature {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.6rem 0;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.feature.disabled {
  color: #666;
}

.feature-icon {
  font-size: 1.2rem;
  width: 24px;
  text-align: center;
}

.ticket-conditions {
  background: rgba(255,255,255,0.05);
  border-radius: 10px;
  padding: 1rem;
  margin-bottom: 1.5rem;
}

.ticket-conditions p {
  font-size: 0.8rem;
  margin-bottom: 0.3rem;
  color: #00ff00;
}

.ticket-btn {
  position: relative;
  width: 100%;
  padding: 1rem;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
}

.btn-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
  transition: left 0.5s ease;
}

.ticket-btn:hover .btn-glow {
  left: 100%;
}

.ticket-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}

.basic-btn {
  background: #00ffff;
  color: #000;
}

.standard-btn {
  background: #ffff00;
  color: #000;
}

.vip-btn {
  background: #ff00ff;
  color: #000;
}

.services {
  margin-top: 3rem;
}

.subsection-title {
  text-align: center;
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  color: #00ffff;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.services-subtitle {
  text-align: center;
  color: #666;
  font-size: 0.8rem;
  margin-bottom: 1.5rem;
}

.service-cards {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 400px;
  margin: 0 auto;
}

.service-card {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  background: rgba(255,255,255,0.05);
  border-radius: 15px;
  padding: 1.2rem;
  border: 1px solid rgba(255,255,255,0.1);
}

.service-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.service-content h4 {
  font-size: 1.1rem;
  margin-bottom: 0.3rem;
  color: #00ffff;
}

.service-price {
  font-size: 1.3rem;
  font-weight: bold;
  margin-bottom: 0.3rem;
  color: #ffff00;
}

.service-desc {
  font-size: 0.8rem;
  color: #ccc;
  margin-bottom: 0.5rem;
}

.service-features {
  list-style: none;
}

.service-features li {
  font-size: 0.75rem;
  padding: 0.2rem 0;
  color: #00ff00;
}

@media (max-width: 768px) {
  .tickets {
    padding: 2rem 1rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .container {
    padding: 0 1rem;
  }
  
  .ticket-cards {
    gap: 1rem;
  }
  
  .ticket-card {
    padding: 1.2rem;
  }
  
  .current-price {
    font-size: 1.5rem;
  }
  
  .service-card {
    padding: 1rem;
  }
}
</style>