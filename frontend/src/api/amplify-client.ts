import { Amplify } from 'aws-amplify';
import { signIn, signUp, signOut, getCurrentUser, fetchAuthSession } from 'aws-amplify/auth';
import { get, post, put, del } from 'aws-amplify/api';
import { awsConfig } from '../aws-config';
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

// Configure Amplify
Amplify.configure(awsConfig);

class AmplifyApiClient {
  private apiName = 'VocabularyAPI';

  // Authentication methods
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    try {
      const { isSignedIn } = await signIn({
        username: credentials.email,
        password: credentials.password,
      });

      if (isSignedIn) {
        const user = await getCurrentUser();
        return {
          token: 'cognito-managed', // Cognito manages tokens automatically
          user: {
            id: user.userId,
            email: credentials.email,
            username: user.username,
          },
        };
      }

      throw new Error('Login failed');
    } catch (error: any) {
      throw new Error(error.message || 'Login failed');
    }
  }

  async register(credentials: RegisterRequest): Promise<RegisterResponse> {
    try {
      const { isSignUpComplete, userId } = await signUp({
        username: credentials.email,
        password: credentials.password,
        options: {
          userAttributes: {
            email: credentials.email,
          },
        },
      });

      return {
        message: isSignUpComplete
          ? 'Registration successful'
          : 'Please check your email to verify your account',
        user: {
          id: userId || '',
          email: credentials.email,
          username: credentials.username,
        },
      };
    } catch (error: any) {
      throw new Error(error.message || 'Registration failed');
    }
  }

  async logout(): Promise<void> {
    await signOut();
  }

  async validateSession(): Promise<{ user: User }> {
    try {
      const user = await getCurrentUser();
      const session = await fetchAuthSession();

      if (!session.tokens) {
        throw new Error('No valid session');
      }

      return {
        user: {
          id: user.userId,
          email: user.signInDetails?.loginId || '',
          username: user.username,
        },
      };
    } catch (error) {
      throw new Error('Session validation failed');
    }
  }

  // Vocabulary methods
  async getEntries(filters?: FilterCriteria, search?: string): Promise<VocabEntry[]> {
    try {
      const queryParams: any = {};
      if (search) queryParams.search = search;
      if (filters?.word) queryParams.word = filters.word;
      if (filters?.meaning) queryParams.meaning = filters.meaning;
      if (filters?.synonym) queryParams.synonym = filters.synonym;
      if (filters?.category) queryParams.category = filters.category;

      const response = await get({
        apiName: this.apiName,
        path: '/vocab',
        options: {
          queryParams,
        },
      }).response;

      const data: any = await response.body.json();
      return data.entries || [];
    } catch (error: any) {
      console.error('Get entries error:', error);
      throw new Error(error.message || 'Failed to fetch entries');
    }
  }

  async createEntry(
    entry: Omit<VocabEntry, 'id' | 'user_id' | 'created_at' | 'updated_at'>
  ): Promise<VocabEntry> {
    try {
      const response = await post({
        apiName: this.apiName,
        path: '/vocab',
        options: {
          body: entry,
        },
      }).response;

      const data: any = await response.body.json();
      return data.entry;
    } catch (error: any) {
      throw new Error(error.message || 'Failed to create entry');
    }
  }

  async updateEntry(id: number, updates: Partial<VocabEntry>): Promise<VocabEntry> {
    try {
      const response = await put({
        apiName: this.apiName,
        path: `/vocab/${id}`,
        options: {
          body: updates,
        },
      }).response;

      const data: any = await response.body.json();
      return data.entry;
    } catch (error: any) {
      throw new Error(error.message || 'Failed to update entry');
    }
  }

  async deleteEntry(id: number): Promise<void> {
    try {
      await del({
        apiName: this.apiName,
        path: `/vocab/${id}`,
      }).response;
    } catch (error: any) {
      throw new Error(error.message || 'Failed to delete entry');
    }
  }

  // Category methods
  async getCategories(): Promise<Category[]> {
    try {
      const response = await get({
        apiName: this.apiName,
        path: '/categories',
      }).response;

      const data: any = await response.body.json();
      return data.categories || [];
    } catch (error: any) {
      throw new Error(error.message || 'Failed to fetch categories');
    }
  }

  async createCategory(name: string): Promise<Category> {
    try {
      const response = await post({
        apiName: this.apiName,
        path: '/categories',
        options: {
          body: { name },
        },
      }).response;

      const data: any = await response.body.json();
      return data.category;
    } catch (error: any) {
      throw new Error(error.message || 'Failed to create category');
    }
  }

  async updateCategory(id: number, name: string): Promise<Category> {
    try {
      const response = await put({
        apiName: this.apiName,
        path: `/categories/${id}`,
        options: {
          body: { name },
        },
      }).response;

      const data: any = await response.body.json();
      return data.category;
    } catch (error: any) {
      throw new Error(error.message || 'Failed to update category');
    }
  }

  async deleteCategory(id: number): Promise<void> {
    try {
      await del({
        apiName: this.apiName,
        path: `/categories/${id}`,
      }).response;
    } catch (error: any) {
      throw new Error(error.message || 'Failed to delete category');
    }
  }

  // CSV methods (placeholder - will implement later)
  async uploadCSV(file: File, encoding?: string): Promise<ImportResult> {
    throw new Error('CSV upload not yet implemented in serverless version');
  }

  async exportCSV(entryIds?: number[]): Promise<Blob> {
    throw new Error('CSV export not yet implemented in serverless version');
  }
}

export const apiClient = new AmplifyApiClient();
