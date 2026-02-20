// TypeScript type definitions for the Vocabulary Visualization App

export interface VocabEntry {
  id?: number;
  user_id?: number;
  word: string;
  meaning: string;
  synonym?: string;
  pronunciation?: string;
  example?: string;
  category_id?: number;
  created_at?: string;
  updated_at?: string;
}

export interface User {
  id: string;
  username: string;
  email?: string;
  created_at?: string;
}

export interface Category {
  id: number;
  user_id: number;
  name: string;
  created_at: string;
}

export interface FilterCriteria {
  word?: string;
  meaning?: string;
  synonym?: string;
  category?: number;
}

export interface ImportResult {
  imported_count: number;
  skipped_count: number;
  error_count: number;
  errors: string[];
}

export interface ApiError {
  code: string;
  message: string;
  details: string[];
}

export interface ApiResponse<T> {
  data?: T;
  error?: ApiError;
}

export interface LoginRequest {
  email: string;
  password: string;
  remember?: boolean;
}

export interface LoginResponse {
  user: User;
  token: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
}

export interface RegisterResponse {
  user: User;
  message: string;
}
