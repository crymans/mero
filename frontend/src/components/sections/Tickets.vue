<template>
  <section class="tickets" id="tickets">
    <div class="container">
      <h2 class="section-title neon-text">БИЛЕТЫ НА ТУСОВКУ</h2>
      <p class="section-subtitle">Выбери свой вариант и присоединяйся к легенде!</p>
      
      <!-- Анимированный фон -->
      <div class="background-effects">
        <div class="floating-particle particle-1"></div>
        <div class="floating-particle particle-2"></div>
        <div class="floating-particle particle-3"></div>
        <div class="energy-wave"></div>
      </div>

      <!-- Основные билеты -->
      <div class="tickets-main">
        <div class="ticket-cards">
          <!-- Базовый билет -->
          <div class="ticket-card basic" @mouseenter="activateCard('basic')">
            <div class="card-glow"></div>
            <div class="ticket-content">
              <div class="ticket-header">
                <div class="ticket-title-wrapper">
                  <h3>STANDARD</h3>
                  <div class="title-underline"></div>
                </div>
                <div class="price">
                  <span class="old-price">800 stars</span>
                  <span class="current-price">400 stars</span>
                </div>
                <div class="ticket-tag">со скидкой</div>
              </div>
              <div class="ticket-features">
                <div class="feature">
                  <div class="feature-icon">🎫</div>
                  <span>Вход на вечеринку</span>
                </div>
                <div class="feature">
                  <div class="feature-icon">💃</div>
                  <span>Танцпол</span>
                </div>
                <div class="feature">
                  <div class="feature-icon">🍻</div>
                  <span>Базовый бар</span>
                </div>
                <div class="feature disabled">
                  <div class="feature-icon">🛋️</div>
                  <span>Сидячие места</span>
                </div>
              </div>
              <div class="ticket-conditions">
                <p>✓ Сделай репост мероприятия </p>
                <p>✓ Покажи на входе</p>
              </div>
              <button class="ticket-btn basic-btn" @click="buyTicket('standard')">
                <span class="btn-text">ВЗЯТЬ ПО СКИДКЕ</span>
                <span class="btn-glow"></span>
              </button>
            </div>
          </div>

          <!-- Быстрый вход -->
          <div class="ticket-card standard featured" @mouseenter="activateCard('standard')">
            <div class="card-glow"></div>
            <div class="ticket-content">
              <div class="ticket-header">
                <div class="ticket-title-wrapper">
                  <h3>FAST ENTRY</h3>
                  <div class="title-underline"></div>
                </div>
                <div class="price">
                  <span class="current-price">450 stars</span>
                </div>
                <div class="ticket-tag popular">популярный</div>
              </div>
              <div class="ticket-features">
                <div class="feature">
                  <div class="feature-icon">🚀</div>
                  <span>Быстрый вход</span>
                </div>
                <div class="feature">
                  <div class="feature-icon">🎫</div>
                  <span>Вход на вечеринку</span>
                </div>
                <div class="feature">
                  <div class="feature-icon">💃</div>
                  <span>Танцпол</span>
                </div>
                <div class="feature">
                  <div class="feature-icon">🍻</div>
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
          <div class="ticket-card vip" @mouseenter="activateCard('vip')" id="ticketsvip">
            <div class="card-glow"></div>
            <div class="ticket-content">
              <div class="ticket-header">
                <div class="ticket-title-wrapper">
                  <h3>VIP TICKET</h3>
                  <div class="title-underline"></div>
                </div>
                <div class="price">
                  <span class="current-price">650 stars</span>
                </div>
                <div class="ticket-tag">премиум</div>
              </div>
              <div class="ticket-features">
                <div class="feature">
                  <div class="feature-icon">⭐</div>
                  <span>VIP вход</span>
                </div>
                <div class="feature">
                  <div class="feature-icon">🛋️</div>
                  <span>Место за столом</span>
                </div>
                <div class="feature">
                  <div class="feature-icon">🍾</div>
                  <span>Премиум бар</span>
                </div>
                <div class="feature">
                  <div class="feature-icon">🎯</div>
                  <span>Персональный сервис</span>
                </div>
              </div>
              <div class="ticket-conditions">
                <p>✓ Без проверки репоста</p>
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
          <div class="service-card hookah" @mouseenter="activateService(0)">
            <div class="service-glow"></div>
            <div class="service-icon">💨</div>
            <div class="service-content">
              <div class="service-header">
                <h4>КАЛЬЯН</h4>
                <div class="service-price">1600 ₽</div>
              </div>
              <p class="service-desc">На компанию до 4 человек • 1 час</p>
              <div class="service-features">
                <div class="service-feature">
                  <span class="feature-check">✓</span>
                  <span>Премиальный табак</span>
                </div>
                <div class="service-feature">
                  <span class="feature-check">✓</span>
                  <span>Любые вкусы</span>
                </div>
                <div class="service-feature">
                  <span class="feature-check">✓</span>
                  <span>Профессиональный кальянщик</span>
                </div>
              </div>
              <div class="service-tag">расслабление</div>
            </div>
          </div>

          <div class="service-card room" @mouseenter="activateService(1)">
            <div class="service-glow"></div>
            <div class="service-icon">🛏️</div>
            <div class="service-content">
              <div class="service-header">
                <h4>КОМНАТА ОТДЫХА</h4>
                <div class="service-price">2000 ₽ </div>
              </div>
              <p class="service-desc">2-спальная кровать • 1 час</p>
              <div class="service-features">
                <div class="service-feature">
                  <span class="feature-check">✓</span>
                  <span>Полная приватность</span>
                </div>
                <div class="service-feature">
                  <span class="feature-check">✓</span>
                  <span>Комфортный отдых</span>
                </div>
                <div class="service-feature">
                  <span class="feature-check">✓</span>
                  <span>Отдельный вход</span>
                </div>
              </div>
              <div class="service-tag">уединение</div>
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

const activateCard = (type: string) => {
  // Можно добавить дополнительные эффекты при наведении
};

const activateService = (index: number) => {
  // Эффекты для сервисных карточек
};
</script>

<style scoped>
.tickets {
  padding: 3rem 1rem;
  background: linear-gradient(135deg, #0a0a0a 0%, #000 50%, #1a0a2a 100%);
  position: relative;
  overflow: hidden;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  position: relative;
  z-index: 2;
}

/* Анимированный фон */
.background-effects {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  pointer-events: none;
}

.floating-particle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
  animation: float 8s ease-in-out infinite;
}

.particle-1 {
  width: 6px;
  height: 6px;
  top: 20%;
  left: 10%;
  animation-delay: 0s;
  background: rgba(0, 255, 255, 0.3);
}

.particle-2 {
  width: 4px;
  height: 4px;
  top: 60%;
  left: 85%;
  animation-delay: 2s;
  background: rgba(255, 0, 255, 0.3);
}

.particle-3 {
  width: 5px;
  height: 5px;
  top: 80%;
  left: 20%;
  animation-delay: 4s;
  background: rgba(255, 255, 0, 0.3);
}

.energy-wave {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, transparent, #00ffff, #ff00ff, transparent);
  animation: wave 4s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-15px) rotate(180deg); }
}

@keyframes wave {
  0%, 100% { opacity: 0; transform: scaleX(0); }
  50% { opacity: 0.5; transform: scaleX(1); }
}

.section-title {
  font-size: 2.5rem;
  text-align: center;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.3rem;
  background: linear-gradient(45deg, #00ffff, #ff00ff, #ffff00);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: titleGlow 3s ease-in-out infinite alternate;
}

@keyframes titleGlow {
  from {
    text-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
  }
  to {
    text-shadow: 0 0 30px rgba(255, 0, 255, 0.5),
                 0 0 40px rgba(255, 255, 0, 0.3);
  }
}

.section-subtitle {
  text-align: center;
  color: #aaa;
  margin-bottom: 2rem;
  font-size: 1rem;
}

.ticket-cards {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  max-width: 400px;
  margin: 0 auto 3rem;
}

.ticket-card {
  position: relative;
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.08) 0%, 
    rgba(255, 255, 255, 0.03) 100%);
  border-radius: 20px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  overflow: hidden;
  min-height: 480px;
  display: flex;
  flex-direction: column;
}

.ticket-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, 
    transparent, 
    rgba(255, 255, 255, 0.05), 
    transparent);
  transition: left 0.6s ease;
}

.ticket-card:hover::before {
  left: 100%;
}

.ticket-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
}

.ticket-card.featured {
  border: 2px solid rgba(255, 255, 0, 0.4);
  transform: scale(1.02);
}

.ticket-card.featured:hover {
  transform: translateY(-5px) scale(1.02);
}

.ticket-card.basic {
  border-color: rgba(0, 255, 255, 0.3);
}

.ticket-card.standard {
  border-color: rgba(255, 255, 0, 0.3);
}

.ticket-card.vip {
  border-color: rgba(255, 0, 255, 0.3);
}

.card-glow {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  border-radius: 22px;
  background: linear-gradient(45deg, 
    rgba(0, 255, 255, 0.1), 
    rgba(255, 0, 255, 0.1), 
    rgba(255, 255, 0, 0.1));
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
}

.ticket-card:hover .card-glow {
  opacity: 1;
}

/* Улучшенные стили для заголовков билетов */
.ticket-header {
  text-align: center;
  margin-bottom: 1.5rem;
  flex-shrink: 0;
  position: relative;
}

.ticket-title-wrapper {
  margin-bottom: 1rem;
}

.ticket-header h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 2px;
  font-weight: 800;
  background: linear-gradient(45deg, #fff, #ccc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
}

/* Подчеркивание для заголовков */
.title-underline {
  height: 2px;
  width: 60px;
  margin: 0.5rem auto;
  border-radius: 2px;
  transition: all 0.3s ease;
}

.ticket-card.basic .title-underline {
  background: linear-gradient(90deg, #00ffff, #0088ff);
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
}

.ticket-card.standard .title-underline {
  background: linear-gradient(90deg, #ffff00, #ffaa00);
  box-shadow: 0 0 10px rgba(255, 255, 0, 0.3);
}

.ticket-card.vip .title-underline {
  background: linear-gradient(90deg, #ff00ff, #ff0088);
  box-shadow: 0 0 10px rgba(255, 0, 255, 0.3);
}

.ticket-card:hover .title-underline {
  width: 80px;
  box-shadow: 0 0 15px currentColor;
}

/* Стили для тегов под названиями */
.ticket-tag {
  display: inline-block;
  padding: 0.3rem 0.8rem;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-top: 0.5rem;
}

.ticket-card.basic .ticket-tag {
  background: rgba(0, 255, 255, 0.1);
  color: #00ffff;
  border: 1px solid rgba(0, 255, 255, 0.3);
}

.ticket-card.standard .ticket-tag {
  background: rgba(255, 255, 0, 0.1);
  color: #ffff00;
  border: 1px solid rgba(255, 255, 0, 0.3);
}

.ticket-card.standard .ticket-tag.popular {
  background: rgba(255, 255, 0, 0.2);
  color: #ffff00;
  border: 1px solid rgba(255, 255, 0, 0.5);
  animation: pulse-gold 2s infinite;
}

.ticket-card.vip .ticket-tag {
  background: rgba(255, 0, 255, 0.1);
  color: #ff00ff;
  border: 1px solid rgba(255, 0, 255, 0.3);
}

@keyframes pulse-gold {
  0%, 100% { 
    box-shadow: 0 0 5px rgba(255, 255, 0, 0.3);
  }
  50% { 
    box-shadow: 0 0 15px rgba(255, 255, 0, 0.6);
  }
}

.price {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
}

.old-price {
  color: #666;
  text-decoration: line-through;
  font-size: 0.9rem;
}

.current-price {
  font-size: 1.8rem;
  font-weight: bold;
  background: linear-gradient(45deg, #00ffff, #ffff00);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.ticket-features {
  margin-bottom: 1.5rem;
  flex-grow: 1;
}

.feature {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.6rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.2s ease;
}

.feature:hover {
  transform: translateX(3px);
}

.feature.disabled {
  color: #666;
}

.feature-icon {
  font-size: 1.1rem;
  width: 24px;
  text-align: center;
  flex-shrink: 0;
}

/* Цвета галочек в зависимости от типа билета */
.ticket-card.basic .ticket-conditions p {
  color: #00ffff;
  text-shadow: 0 0 8px rgba(0, 255, 255, 0.3);
}

.ticket-card.standard .ticket-conditions p {
  color: #ffff00;
  text-shadow: 0 0 8px rgba(255, 255, 0, 0.3);
}

.ticket-card.vip .ticket-conditions p {
  color: #ff00ff;
  text-shadow: 0 0 8px rgba(255, 0, 255, 0.3);
}

.ticket-conditions {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 1.5rem;
  flex-shrink: 0;
}

.ticket-conditions p {
  font-size: 0.8rem;
  margin-bottom: 0.3rem;
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
  flex-shrink: 0;
}

.btn-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, 
    transparent, 
    rgba(255, 255, 255, 0.4), 
    transparent);
  transition: left 0.5s ease;
}

.ticket-btn:hover .btn-glow {
  left: 100%;
}

.ticket-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.basic-btn {
  background: linear-gradient(45deg, #00cccc, #00ffff);
  color: #000;
}

.standard-btn {
  background: linear-gradient(45deg, #cccc00, #ffff00);
  color: #000;
}

.vip-btn {
  background: linear-gradient(45deg, #cc00cc, #ff00ff);
  color: #000;
}

/* УЛУЧШЕННЫЕ СТИЛИ ДЛЯ ДОПОЛНИТЕЛЬНЫХ УСЛУГ */
.services {
  margin-top: 4rem;
}

.subsection-title {
  text-align: center;
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  background: linear-gradient(45deg, #00ffff, #ff00ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-transform: uppercase;
  letter-spacing: 2px;
  animation: titleGlow 3s ease-in-out infinite alternate;
}

.services-subtitle {
  text-align: center;
  color: #aaa;
  font-size: 0.9rem;
  margin-bottom: 2rem;
}

.service-cards {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
  max-width: 450px;
  margin: 0 auto;
}

.service-card {
  position: relative;
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.1) 0%, 
    rgba(255, 255, 255, 0.05) 100%);
  border-radius: 20px;
  padding: 2rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-height: 320px;
}

.service-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, 
    transparent, 
    rgba(255, 255, 255, 0.08), 
    transparent);
  transition: left 0.6s ease;
}

.service-card:hover::before {
  left: 100%;
}

.service-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
}

/* Индивидуальные цвета для услуг */
.service-card.hookah {
  border-color: rgba(0, 255, 255, 0.4);
}

.service-card.room {
  border-color: rgba(255, 0, 255, 0.4);
}

.service-glow {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  border-radius: 22px;
  opacity: 0;
  transition: opacity 0.4s ease;
  z-index: -1;
}

.service-card.hookah .service-glow {
  background: linear-gradient(45deg, 
    rgba(0, 255, 255, 0.2), 
    rgba(0, 200, 255, 0.1));
}

.service-card.room .service-glow {
  background: linear-gradient(45deg, 
    rgba(255, 0, 255, 0.2), 
    rgba(255, 100, 255, 0.1));
}

.service-card:hover .service-glow {
  opacity: 1;
  animation: serviceGlow 2s ease-in-out infinite alternate;
}

@keyframes serviceGlow {
  0% { opacity: 0.3; }
  100% { opacity: 0.6; }
}

.service-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  text-align: center;
  filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.3));
}

.service-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.service-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.service-header h4 {
  font-size: 1.3rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin: 0;
}

.service-card.hookah .service-header h4 {
  background: linear-gradient(45deg, #00ffff, #00ccff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.service-card.room .service-header h4 {
  background: linear-gradient(45deg, #ff00ff, #ff66ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.service-price {
  font-size: 1.5rem;
  font-weight: bold;
  text-shadow: 0 0 10px rgba(255, 255, 0, 0.5);
}

.service-card.hookah .service-price {
  color: #ffff00;
}

.service-card.room .service-price {
  color: #ffaa00;
}

.service-desc {
  font-size: 0.9rem;
  color: #ccc;
  margin-bottom: 1.5rem;
  text-align: center;
  line-height: 1.4;
}

.service-features {
  margin-bottom: 1.5rem;
  flex-grow: 1;
}

.service-feature {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.2s ease;
}

.service-feature:hover {
  transform: translateX(5px);
}

.feature-check {
  font-size: 1rem;
  width: 20px;
  flex-shrink: 0;
}

.service-card.hookah .feature-check {
  color: #00ffff;
  text-shadow: 0 0 8px rgba(0, 255, 255, 0.5);
}

.service-card.room .feature-check {
  color: #ff00ff;
  text-shadow: 0 0 8px rgba(255, 0, 255, 0.5);
}

.service-tag {
  display: inline-block;
  padding: 0.4rem 1rem;
  border-radius: 15px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  text-align: center;
  margin-top: auto;
}

.service-card.hookah .service-tag {
  background: rgba(0, 255, 255, 0.15);
  color: #00ffff;
  border: 1px solid rgba(0, 255, 255, 0.4);
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.2);
}

.service-card.room .service-tag {
  background: rgba(255, 0, 255, 0.15);
  color: #ff00ff;
  border: 1px solid rgba(255, 0, 255, 0.4);
  box-shadow: 0 0 10px rgba(255, 0, 255, 0.2);
}

@media (max-width: 768px) {
  .tickets {
    padding: 2rem 1rem;
  }
  
  .section-title {
    font-size: 2rem;
    letter-spacing: 0.2rem;
  }
  
  .ticket-cards {
    gap: 1.2rem;
  }
  
  .ticket-card {
    padding: 1.2rem;
    min-height: 460px;
  }
  
  .current-price {
    font-size: 1.6rem;
  }
  
  .service-card {
    padding: 1.5rem;
    min-height: 300px;
  }
  
  .service-header {
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
  }
  
  .service-header h4 {
    text-align: center;
  }
}

@media (min-width: 1024px) {
  .ticket-cards {
    grid-template-columns: repeat(3, 1fr);
    max-width: 100%;
    gap: 2rem;
  }
  
  .ticket-card {
    min-height: 500px;
  }
  
  .service-cards {
    grid-template-columns: repeat(2, 1fr);
    max-width: 100%;
    gap: 2.5rem;
  }
  
  .container {
    padding: 0 2rem;
  }
  
  .service-card {
    min-height: 350px;
  }
}
</style>