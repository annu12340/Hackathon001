
import React from 'react';
import { Database, FileText, Server } from 'lucide-react';
import { cn } from '@/lib/utils';

const sources = [
  { id: 'kubectl', label: 'Kubernetes Logs', icon: Server },
  { id: 'var-logs', label: 'System Logs', icon: FileText },
  { id: 'db-logs', label: 'Database Logs', icon: Database },
];

interface LogSourceSelectorProps {
  activeSource: string;
  onSourceChange: (source: string) => void;
}

const LogSourceSelector = ({ activeSource, onSourceChange }: LogSourceSelectorProps) => {
  return (
    <div className="flex gap-2 mb-4">
      {sources.map((source) => (
        <button
          key={source.id}
          onClick={() => onSourceChange(source.id)}
          className={cn(
            "flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors",
            activeSource === source.id
              ? "bg-gray-900 text-white"
              : "bg-gray-100 text-gray-600 hover:bg-gray-200"
          )}
        >
          <source.icon className="w-4 h-4" />
          {source.label}
        </button>
      ))}
    </div>
  );
};

export default LogSourceSelector;
