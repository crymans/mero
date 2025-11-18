<template>
  <div class="menu-categories">
    <div class="categories-scroll">
      <button 
        v-for="category in categories" 
        :key="category"
        @click="$emit('categoryChange', category)"
        class="category-btn"
        :class="{ active: activeCategory === category }"
      >
        <span class="category-emoji">{{ getCategoryEmoji(category) }}</span>
        <span class="category-name">{{ getCategoryName(category) }}</span>
        <div class="btn-glow"></div>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  categories: string[]
  activeCategory: string
}>()

defineEmits<{
  categoryChange: [category: string]
}>()

const getCategoryEmoji = (category: string) => {
  const emojis: {[key: string]: string} = {
    drink: '🍹',
    food: '🍔',
    all: '🌟'
  }
  return emojis[category] || '📦'
}

const getCategoryName = (category: string) => {
  const names: {[key: string]: string} = {
    drink: 'НАПИТКИ',
    food: 'ЗАКУСКИ',
    all: 'ВСЁ'
  }
  return names[category] || category
}
</script>

<style scoped>
.menu-categories {
  margin-bottom: 3rem;
}

.categories-scroll {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.category-btn {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 1rem 1.5rem;
  border: 2px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.05);
  color: #ccc;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  overflow: hidden;
}

.category-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transition: left 0.5s ease;
}

.category-btn:hover::before {
  left: 100%;
}

.category-btn.active {
  background: linear-gradient(135deg, #ff00ff, #00ffff);
  color: #000;
  border-color: black;
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(255, 0, 255, 0.3);
}

.category-btn:hover:not(.active) {
  border-color: #00ffff;
  color: #fff;
  transform: translateY(-2px);
}

.category-emoji {
  font-size: 1.5rem;
  filter: drop-shadow(0 0 5px rgba(255, 255, 255, 0.5));
}

.category-name {
  font-size: 0.9rem;
  white-space: nowrap;
}

.btn-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  transition: left 0.5s ease;
}

.category-btn:hover .btn-glow {
  left: 100%;
}

@media (max-width: 768px) {
  .categories-scroll {
    gap: 0.5rem;
  }
  
  .category-btn {
    padding: 0.8rem 1.2rem;
    gap: 0.5rem;
  }
  
  .category-emoji {
    font-size: 1.2rem;
  }
  
  .category-name {
    font-size: 0.8rem;
  }
}
</style>