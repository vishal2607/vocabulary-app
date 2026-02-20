// Main dashboard for vocabulary management
import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { apiClient } from '../api/amplify-client';
import type { VocabEntry, Category } from '../types';
import VocabList from '../components/VocabList';
import EntryForm from '../components/EntryForm';
import SearchBar from '../components/SearchBar';

const Dashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const [entries, setEntries] = useState<VocabEntry[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingEntry, setEditingEntry] = useState<VocabEntry | null>(null);

  // Load entries and categories
  const loadData = async () => {
    try {
      setLoading(true);
      const [entriesData, categoriesData] = await Promise.all([
        apiClient.getEntries(undefined, searchQuery || undefined),
        apiClient.getCategories(),
      ]);
      setEntries(entriesData);
      setCategories(categoriesData);
      setError('');
    } catch (err: any) {
      setError('Failed to load data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [searchQuery]);

  const handleLogout = async () => {
    try {
      await logout();
    } catch (err) {
      console.error('Logout error:', err);
    }
  };

  const handleAddEntry = async (entry: Omit<VocabEntry, 'id' | 'user_id' | 'created_at' | 'updated_at'>) => {
    try {
      await apiClient.createEntry(entry);
      setShowAddForm(false);
      await loadData();
    } catch (err: any) {
      alert(err.message || 'Failed to create entry');
    }
  };

  const handleUpdateEntry = async (entry: Omit<VocabEntry, 'id' | 'user_id' | 'created_at' | 'updated_at'>) => {
    if (!editingEntry?.id) return;
    try {
      await apiClient.updateEntry(editingEntry.id, entry);
      setEditingEntry(null);
      await loadData();
    } catch (err: any) {
      alert(err.message || 'Failed to update entry');
    }
  };

  const handleDeleteEntry = async (id: number) => {
    if (!confirm('Are you sure you want to delete this entry?')) return;
    try {
      await apiClient.deleteEntry(id);
      await loadData();
    } catch (err: any) {
      alert(err.message || 'Failed to delete entry');
    }
  };

  const handleEditEntry = (entry: VocabEntry) => {
    setEditingEntry(entry);
    setShowAddForm(false);
  };

  const handleCSVUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    try {
      await apiClient.uploadCSV();
      alert('CSV import not yet implemented in serverless version');
    } catch (err: any) {
      alert(err.message || 'Failed to upload CSV');
    }
    // Reset file input
    event.target.value = '';
  };

  const handleCSVExport = async () => {
    try {
      await apiClient.exportCSV();
      alert('CSV export not yet implemented in serverless version');
    } catch (err: any) {
      alert(err.message || 'Failed to export CSV');
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold text-gray-800">Vocabulary App</h1>
          <div className="flex items-center gap-4">
            <span className="text-gray-600">Welcome, {user?.username}</span>
            <button
              onClick={handleLogout}
              className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Actions Bar */}
        <div className="bg-white rounded-lg shadow p-4 mb-6">
          <div className="flex flex-wrap gap-4 items-center justify-between">
            <div className="flex gap-2">
              <button
                onClick={() => {
                  setShowAddForm(true);
                  setEditingEntry(null);
                }}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                + Add Entry
              </button>
              <label className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 cursor-pointer">
                Import CSV
                <input
                  type="file"
                  accept=".csv"
                  onChange={handleCSVUpload}
                  className="hidden"
                />
              </label>
              <button
                onClick={handleCSVExport}
                className="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700"
              >
                Export CSV
              </button>
            </div>
            <div className="flex-1 max-w-md">
              <SearchBar value={searchQuery} onChange={setSearchQuery} />
            </div>
          </div>
        </div>

        {/* Add/Edit Form */}
        {(showAddForm || editingEntry) && (
          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <h2 className="text-xl font-bold mb-4">
              {editingEntry ? 'Edit Entry' : 'Add New Entry'}
            </h2>
            <EntryForm
              entry={editingEntry || undefined}
              categories={categories}
              onSubmit={editingEntry ? handleUpdateEntry : handleAddEntry}
              onCancel={() => {
                setShowAddForm(false);
                setEditingEntry(null);
              }}
            />
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {/* Vocabulary List */}
        <div className="bg-white rounded-lg shadow">
          {loading ? (
            <div className="p-8 text-center text-gray-500">Loading...</div>
          ) : entries.length === 0 ? (
            <div className="p-8 text-center text-gray-500">
              {searchQuery ? 'No entries found matching your search.' : 'No vocabulary entries yet. Add your first entry!'}
            </div>
          ) : (
            <VocabList
              entries={entries}
              categories={categories}
              onEdit={handleEditEntry}
              onDelete={handleDeleteEntry}
            />
          )}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
