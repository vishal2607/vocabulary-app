// API client for backend communication
import axios, { AxiosInstance, AxiosError } from 'axios';
import type {
  VocabEntry,
  User,
  Category,
  LoginRequest,
  LoginResponse,
  RegisterRequest,
  RegisterResponse,
  ImportResult,
  FilterCriteria,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001/api';

class ApiClient {
  private client: AxiosInstance;
  private token: string | null = null;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Load token from localStorage
    this.token = localStorage.getItem('auth_token');
    if (this.token) {
      this.setAuthToken(this.token);
    }

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          // Unauthorized - clear token and redirect to login
          this.clearAuthToken();
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  setAuthToken(token: string) {
    this.token = token;
    this.client.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    localStorage.setItem('auth_token', token);
  }

  clearAuthToken() {
    this.token = null;
    delete this.client.defaults.headers.common['Authorization'];
    localStorage.removeItem('auth_token');
  }

  getToken(): string | null {
    return this.token;
  }

  // Authentication endpoints
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    const response = await this.client.post<LoginResponse>('/auth/login', credentials);
    this.setAuthToken(response.data.token);
    return response.data;
  }

  async register(credentials: RegisterRequest): Promise<RegisterResponse> {
    const response = await this.client.post<RegisterResponse>('/auth/register', credentials);
    return response.data;
  }

  async logout(): Promise<void> {
    try {
      await this.client.post('/auth/logout');
    } finally {
      this.clearAuthToken();
    }
  }

  async validateSession(): Promise<{ user: User }> {
    const response = await this.client.get<{ user: User }>('/auth/validate');
    return response.data;
  }

  // Vocabulary endpoints
  async getEntries(filters?: FilterCriteria, search?: string): Promise<VocabEntry[]> {
    const params: any = {};
    if (search) {
      params.search = search;
    }
    if (filters) {
      if (filters.word) params.word = filters.word;
      if (filters.meaning) params.meaning = filters.meaning;
      if (filters.synonym) params.synonym = filters.synonym;
      if (filters.category) params.category = filters.category;
    }
    const response = await this.client.get<{ entries: VocabEntry[] }>('/vocab', { params });
    return response.data.entries;
  }

  async createEntry(entry: Omit<VocabEntry, 'id' | 'user_id' | 'created_at' | 'updated_at'>): Promise<VocabEntry> {
    const response = await this.client.post<{ entry: VocabEntry }>('/vocab', entry);
    return response.data.entry;
  }

  async updateEntry(id: number, updates: Partial<VocabEntry>): Promise<VocabEntry> {
    const response = await this.client.put<{ entry: VocabEntry }>(`/vocab/${id}`, updates);
    return response.data.entry;
  }

  async deleteEntry(id: number): Promise<void> {
    await this.client.delete(`/vocab/${id}`);
  }

  // Category endpoints
  async getCategories(): Promise<Category[]> {
    const response = await this.client.get<{ categories: Category[] }>('/categories');
    return response.data.categories;
  }

  async createCategory(name: string): Promise<Category> {
    const response = await this.client.post<{ category: Category }>('/categories', { name });
    return response.data.category;
  }

  async updateCategory(id: number, name: string): Promise<Category> {
    const response = await this.client.put<{ category: Category }>(`/categories/${id}`, { name });
    return response.data.category;
  }

  async deleteCategory(id: number): Promise<void> {
    await this.client.delete(`/categories/${id}`);
  }

  // CSV endpoints
  async uploadCSV(file: File, encoding?: string): Promise<ImportResult> {
    const formData = new FormData();
    formData.append('file', file);
    if (encoding) {
      formData.append('encoding', encoding);
    }
    const response = await this.client.post<{ result: ImportResult }>('/csv/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data.result;
  }

  async exportCSV(entryIds?: number[]): Promise<Blob> {
    const params = entryIds ? { ids: entryIds.join(',') } : {};
    const response = await this.client.get('/csv/export', {
      params,
      responseType: 'blob',
    });
    return response.data;
  }
}

// Export the Amplify-based API client
export { apiClient } from './amplify-client';
