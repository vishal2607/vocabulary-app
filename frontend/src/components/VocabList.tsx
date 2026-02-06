// Vocabulary list component displaying entries in a table
import React from 'react';
import type { VocabEntry, Category } from '../types';

interface VocabListProps {
  entries: VocabEntry[];
  categories: Category[];
  onEdit: (entry: VocabEntry) => void;
  onDelete: (id: number) => void;
}

const VocabList: React.FC<VocabListProps> = ({ entries, categories, onEdit, onDelete }) => {
  const getCategoryName = (categoryId?: number) => {
    if (!categoryId) return '-';
    const category = categories.find((c) => c.id === categoryId);
    return category?.name || '-';
  };

  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead className="bg-gray-50 border-b">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Word
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Meaning
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Synonym
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Pronunciation
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Category
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {entries.map((entry) => (
            <tr key={entry.id} className="hover:bg-gray-50">
              <td className="px-4 py-3 text-sm font-medium text-gray-900">
                {entry.word}
              </td>
              <td className="px-4 py-3 text-sm text-gray-700">
                <div className="max-w-xs truncate" title={entry.meaning}>
                  {entry.meaning}
                </div>
              </td>
              <td className="px-4 py-3 text-sm text-gray-700">
                {entry.synonym || '-'}
              </td>
              <td className="px-4 py-3 text-sm text-gray-700">
                {entry.pronunciation || '-'}
              </td>
              <td className="px-4 py-3 text-sm text-gray-700">
                <span className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded">
                  {getCategoryName(entry.category_id)}
                </span>
              </td>
              <td className="px-4 py-3 text-sm">
                <div className="flex gap-2">
                  <button
                    onClick={() => onEdit(entry)}
                    className="text-blue-600 hover:text-blue-800"
                    title="Edit"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => entry.id && onDelete(entry.id)}
                    className="text-red-600 hover:text-red-800"
                    title="Delete"
                  >
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default VocabList;
