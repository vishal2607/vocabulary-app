// Form for creating/editing vocabulary entries
import React, { useState, useEffect } from 'react';
import type { VocabEntry, Category } from '../types';

interface EntryFormProps {
  entry?: VocabEntry;
  categories: Category[];
  onSubmit: (entry: Omit<VocabEntry, 'id' | 'user_id' | 'created_at' | 'updated_at'>) => void;
  onCancel: () => void;
}

const EntryForm: React.FC<EntryFormProps> = ({ entry, categories, onSubmit, onCancel }) => {
  const [word, setWord] = useState(entry?.word || '');
  const [meaning, setMeaning] = useState(entry?.meaning || '');
  const [synonym, setSynonym] = useState(entry?.synonym || '');
  const [pronunciation, setPronunciation] = useState(entry?.pronunciation || '');
  const [example, setExample] = useState(entry?.example || '');
  const [categoryId, setCategoryId] = useState<number | undefined>(entry?.category_id);

  useEffect(() => {
    if (entry) {
      setWord(entry.word);
      setMeaning(entry.meaning);
      setSynonym(entry.synonym || '');
      setPronunciation(entry.pronunciation || '');
      setExample(entry.example || '');
      setCategoryId(entry.category_id);
    }
  }, [entry]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!word.trim() || !meaning.trim()) {
      alert('Word and meaning are required');
      return;
    }

    if (word.length > 100) {
      alert('Word must be 100 characters or less');
      return;
    }

    onSubmit({
      word: word.trim(),
      meaning: meaning.trim(),
      synonym: synonym.trim() || undefined,
      pronunciation: pronunciation.trim() || undefined,
      example: example.trim() || undefined,
      category_id: categoryId || undefined,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label htmlFor="word" className="block text-sm font-medium text-gray-700 mb-1">
            Word <span className="text-red-500">*</span>
          </label>
          <input
            id="word"
            type="text"
            value={word}
            onChange={(e) => setWord(e.target.value)}
            required
            maxLength={100}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter word"
          />
        </div>

        <div>
          <label htmlFor="pronunciation" className="block text-sm font-medium text-gray-700 mb-1">
            Pronunciation
          </label>
          <input
            id="pronunciation"
            type="text"
            value={pronunciation}
            onChange={(e) => setPronunciation(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="e.g., /wɜːrd/"
          />
        </div>
      </div>

      <div>
        <label htmlFor="meaning" className="block text-sm font-medium text-gray-700 mb-1">
          Meaning <span className="text-red-500">*</span>
        </label>
        <textarea
          id="meaning"
          value={meaning}
          onChange={(e) => setMeaning(e.target.value)}
          required
          rows={3}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Enter meaning"
        />
      </div>

      <div>
        <label htmlFor="synonym" className="block text-sm font-medium text-gray-700 mb-1">
          Synonym
        </label>
        <input
          id="synonym"
          type="text"
          value={synonym}
          onChange={(e) => setSynonym(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Enter synonym"
        />
      </div>

      <div>
        <label htmlFor="example" className="block text-sm font-medium text-gray-700 mb-1">
          Example
        </label>
        <textarea
          id="example"
          value={example}
          onChange={(e) => setExample(e.target.value)}
          rows={2}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Enter example sentence"
        />
      </div>

      <div>
        <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-1">
          Category
        </label>
        <select
          id="category"
          value={categoryId || ''}
          onChange={(e) => setCategoryId(e.target.value ? Number(e.target.value) : undefined)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">No category</option>
          {categories.map((cat) => (
            <option key={cat.id} value={cat.id}>
              {cat.name}
            </option>
          ))}
        </select>
      </div>

      <div className="flex gap-2 justify-end">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 border border-gray-300 text-gray-700 rounded hover:bg-gray-50"
        >
          Cancel
        </button>
        <button
          type="submit"
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          {entry ? 'Update' : 'Add'} Entry
        </button>
      </div>
    </form>
  );
};

export default EntryForm;
