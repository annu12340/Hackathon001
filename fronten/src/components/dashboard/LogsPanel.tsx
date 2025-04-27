import React, { useState } from 'react';
import { Search } from 'lucide-react';
import LogSourceSelector from './LogSourceSelector';
import { cn } from '@/lib/utils';
import LogSummary from './LogSummary';
const logData = {
  'kubectl': [
    { level: 'ERROR', timestamp: '2025-04-23 10:45:23', message: 'Failed to connect to database' },
    { level: 'WARN', timestamp: '2025-04-23 10:44:57', message: 'High memory usage detected' },
    { level: 'INFO', timestamp: '2025-04-23 10:44:30', message: 'Pod scaling completed' },
  ],
  'var-logs': [
    { level: 'ERROR', timestamp: '2025-04-23 10:43:12', message: 'System service crash detected' },
    { level: 'INFO', timestamp: '2025-04-23 10:42:45', message: 'System backup completed' },
    { level: 'WARN', timestamp: '2025-04-23 10:42:30', message: 'Disk usage above 80%' },
  ],
  'db-logs': [
    { level: 'ERROR', timestamp: '2025-04-23 10:41:15', message: 'Query timeout after 30s' },
    { level: 'WARN', timestamp: '2025-04-23 10:40:30', message: 'Slow query detected' },
    { level: 'INFO', timestamp: '2025-04-23 10:40:00', message: 'Database backup completed' },
  ],
};

const LogsPanel = () => {
  const [activeSource, setActiveSource] = useState('kubectl');

  return (
    <div className="animate-in fade-in duration-500">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold text-gray-900">System Logs</h1>
        <div className="relative">
          <input
            type="text"
            placeholder="Search logs..."
            className="pl-9 pr-4 py-2 bg-white border border-gray-300 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent w-64"
          />
          <Search size={18} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
        </div>
      </div>

      <div className="grid mt-6 mb-6">
        <LogSummary/>
      </div>
      
      <LogSourceSelector activeSource={activeSource} onSourceChange={setActiveSource} />

      <div className="bg-white rounded-xl shadow-sm border border-gray-100">
        <div className="overflow-x-auto">
          <div className="font-mono text-sm">
            {logData[activeSource as keyof typeof logData].map((log, idx) => (
              <div 
                key={idx}
                className={cn(
                  "flex px-6 py-3 border-b border-gray-100 hover:bg-gray-50",
                  log.level === 'ERROR' ? 'bg-red-50' :
                  log.level === 'WARN' ? 'bg-yellow-50' :
                  log.level === 'DEBUG' ? 'bg-purple-50' : ''
                )}
              >
                <div className="w-28 text-gray-500">{log.timestamp.split(' ')[1]}</div>
                <div className={cn(
                  "w-16 font-semibold",
                  log.level === 'ERROR' ? 'text-red-600' :
                  log.level === 'WARN' ? 'text-yellow-600' :
                  log.level === 'INFO' ? 'text-blue-600' :
                  'text-gray-600'
                )}>
                  {log.level}
                </div>
                <div className="flex-1 text-gray-800">{log.message}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LogsPanel;
