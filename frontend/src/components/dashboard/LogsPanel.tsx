import React, { useState } from 'react';
import { Search, ChevronDown, ChevronUp } from 'lucide-react';
import LogSourceSelector from './LogSourceSelector';
import { cn } from '@/lib/utils';
import LogSummary from './LogSummary';
import { Logs } from '@/utils/dashboardTypes';

interface LogsPanelProps {
  data: Logs;
}

const LogsPanel: React.FC<LogsPanelProps> = ({ data }) => {
  const [activeSource, setActiveSource] = useState('kubectl');
  const [showSummary, setShowSummary] = useState(true);

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
        <LogSummary data={data.logSummaryStats} />
      </div>
      
  
      
      {/* Summary Logs Section */}
      <div className="mt-6 bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
        <button
          onClick={() => setShowSummary(!showSummary)}
          className="w-full p-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
        >
          <h2 className="text-lg font-medium text-gray-900">Log Summary</h2>
          {showSummary ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
        </button>
        {showSummary && (
          <div className="p-4 max-h-[200px] overflow-y-auto text-sm border-t border-gray-100">
            {data.logSummary}
          </div>
        )}
      </div>
      <br />
      <LogSourceSelector activeSource={activeSource} onSourceChange={setActiveSource} />
      {/* Detailed Logs Section */}
      <div className="mt-6 bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
        <div className="p-4 max-h-[400px] overflow-y-auto font-mono text-sm">
          {data.logData[activeSource]?.map((log, idx) => (
            <div key={idx} className={cn(
              "py-1.5 px-3 my-1 rounded flex items-start",
              log.level === 'ERROR' ? "bg-red-50 text-red-700" : 
              log.level === 'WARN' ? "bg-yellow-50 text-yellow-700" : 
              "bg-gray-50 text-gray-700"
            )}>
              <span className="mr-3 opacity-60">{log.timestamp}</span>
              <span className={cn(
                "inline-block px-1.5 py-0.5 text-xs rounded font-medium mr-3",
                log.level === 'ERROR' ? "bg-red-100" : 
                log.level === 'WARN' ? "bg-yellow-100" : 
                "bg-gray-100"
              )}>
                {log.level}
              </span>
              <span>{log.message}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default LogsPanel;
