const mockProducts: Product[] = [
  // Алкогольные напитки
  {
    id: 1,
    name: "Jack Daniels",
    description: "Классический виски с карамельными нотами",
    price: 350,
    category: "drink",
    is_available: true,
    image_url: "/images/jack-daniels.jpg"
  },
  {
    id: 2,
    name: "Jameson",
    description: "Ирландский виски с мягким вкусом",
    price: 320,
    category: "drink",
    is_available: true,
    image_url: "/images/jameson.jpg"
  },
  {
    id: 3,
    name: "Absolut Vodka",
    description: "Шведская водка премиум класса",
    price: 280,
    category: "drink",
    is_available: true,
    image_url: "/images/absolut.jpg"
  },
  {
    id: 4,
    name: "Beluga",
    description: "Российская водка высшего качества",
    price: 450,
    category: "drink",
    is_available: true,
    image_url: "/images/beluga.jpg"
  },
  {
    id: 5,
    name: "Gin Tonic",
    description: "Классический коктейль с джином и тоником",
    price: 300,
    category: "drink",
    is_available: true,
    image_url: "/images/gin-tonic.jpg"
  },
  {
    id: 6,
    name: "Mojito",
    description: "Освежающий коктейль с мятой и лаймом",
    price: 350,
    category: "drink",
    is_available: true,
    image_url: "/images/mojito.jpg"
  },
  {
    id: 7,
    name: "Cuba Libre",
    description: "Ром с колой и лаймом",
    price: 320,
    category: "drink",
    is_available: true,
    image_url: "/images/cuba-libre.jpg"
  },
  {
    id: 8,
    name: "Tequila Sunrise",
    description: "Яркий коктейль с текилой и апельсиновым соком",
    price: 380,
    category: "drink",
    is_available: true,
    image_url: "/images/tequila-sunrise.jpg"
  },
  {
    id: 9,
    name: "Bacardi",
    description: "Белый ром для коктейлей",
    price: 290,
    category: "drink",
    is_available: true,
    image_url: "/images/bacardi.jpg"
  },
  {
    id: 10,
    name: "Jägermeister",
    description: "Немецкий биттер с травами",
    price: 310,
    category: "drink",
    is_available: true,
    image_url: "/images/jagermeister.jpg"
  },

  // Безалкогольные напитки
  {
    id: 11,
    name: "Red Bull",
    description: "Энергетический напиток",
    price: 200,
    category: "drink",
    is_available: true,
    image_url: "/images/red-bull.jpg"
  },
  {
    id: 12,
    name: "Coca-Cola",
    description: "Классический газированный напиток",
    price: 150,
    category: "drink",
    is_available: true,
    image_url: "/images/coca-cola.jpg"
  },
  {
    id: 13,
    name: "Sprite",
    description: "Освежающий лимонно-лаймовый напиток",
    price: 150,
    category: "drink",
    is_available: true,
    image_url: "/images/sprite.jpg"
  },
  {
    id: 14,
    name: "Fanta",
    description: "Апельсиновая газировка",
    price: 150,
    category: "drink",
    is_available: true,
    image_url: "/images/fanta.jpg"
  },
  {
    id: 15,
    name: "Вода газированная",
    description: "Свежая газированная вода",
    price: 100,
    category: "drink",
    is_available: true,
    image_url: "/images/soda-water.jpg"
  },
  {
    id: 16,
    name: "Сок апельсиновый",
    description: "Свежевыжатый апельсиновый сок",
    price: 180,
    category: "drink",
    is_available: true,
    image_url: "/images/orange-juice.jpg"
  },

  // Закуски
  {
    id: 17,
    name: "Чипсы",
    description: "Хрустящие картофельные чипсы",
    price: 180,
    category: "food",
    is_available: true,
    image_url: "/images/chips.jpg"
  },
  {
    id: 18,
    name: "Орешки",
    description: "Ассорти из соленых орешков",
    price: 120,
    category: "food",
    is_available: true,
    image_url: "/images/nuts.jpg"
  },
  {
    id: 19,
    name: "Бургер",
    description: "Сочный бургер с говядиной",
    price: 450,
    category: "food",
    is_available: true,
    image_url: "/images/burger.jpg"
  },
  {
    id: 20,
    name: "Картофель фри",
    description: "Золотистая хрустящая картошка",
    price: 220,
    category: "food",
    is_available: true,
    image_url: "/images/fries.jpg"
  },
  {
    id: 21,
    name: "Крылья",
    description: "Куриные крылышки в соусе",
    price: 380,
    category: "food",
    is_available: true,
    image_url: "/images/wings.jpg"
  },
  {
    id: 22,
    name: "Сырные палочки",
    description: "Хрустящие палочки с сыром",
    price: 280,
    category: "food",
    is_available: true,
    image_url: "/images/cheese-sticks.jpg"
  },
  {
    id: 23,
    name: "Начос",
    description: "Хрустящие кукурузные чипсы с соусом",
    price: 320,
    category: "food",
    is_available: true,
    image_url: "/images/nachos.jpg"
  },
  {
    id: 24,
    name: "Пицца Маргарита",
    description: "Классическая пицца с томатами и моцареллой",
    price: 520,
    category: "food",
    is_available: true,
    image_url: "/images/pizza-margarita.jpg"
  },
  {
    id: 25,
    name: "Салат Цезарь",
    description: "Свежий салат с курицей и соусом цезарь",
    price: 380,
    category: "food",
    is_available: true,
    image_url: "/images/caesar-salad.jpg"
  },
  {
    id: 26,
    name: "Суши сет",
    description: "Ассорти из свежих суши и роллов",
    price: 680,
    category: "food",
    is_available: true,
    image_url: "/images/sushi-set.jpg"
  }
]