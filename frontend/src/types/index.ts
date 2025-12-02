// types/index.ts
export interface Product {
  id: number
  name: string
  description: string | null
  price: number
  category: string
  count: number
  is_for_table: boolean
  image_url: string | null
}

export interface OrderCreate {
  products_ids: string
  quantity: number
  total_price: number
  table_id: number
}

export interface Order {
  id: number
  user_id: number
  products_ids: string
  quantity: number
  total_price: number
  is_fulfilled: boolean
  table_id: number
  created_at: string
}

export interface User {
  id: number
  telegram_id: string
  username: string | null
  first_name: string | null
  last_name: string | null
  phone: string | null
  role: string
  balance: number
  created_at: string
}

export interface Ticket {
  id: number
  user_id: number
  qr_code: string
  price: number
  last_entry: number
  created_at: string
}

export type UserRole = 'qr' | 'chef' | 'officiant' | 'admin' | 'member'