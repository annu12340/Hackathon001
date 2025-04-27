import React from 'react';
import { ArrowUp, ArrowDown } from 'lucide-react';
import { LogSummaryStat } from '@/utils/dashboardTypes';

interface LogSummaryProps {
  data: LogSummaryStat[];
}

const LogSummary: React.FC<LogSummaryProps> = ({ data }) => {
  return (
    <div className="grid grid-cols-3 gap-6">
      {data.map((stat, idx) => (
        <div key={idx} className="bg-white p-4 rounded-xl border border-gray-100 shadow-sm">
          <div className="text-sm text-gray-500 mb-1">{stat.label}</div>
          <div className="flex items-end">
            <div className="text-2xl font-semibold mr-2">{stat.value}</div>
            <div className={`flex items-center text-xs font-medium ${stat.delta > 0 ? 'text-red-500' : 'text-green-500'}`}>
              {stat.delta > 0 ? (
                <>
                  <ArrowUp size={12} className="mr-0.5" />
                  +{stat.delta}
                </>
              ) : (
                <>
                  <ArrowDown size={12} className="mr-0.5" />
                  {stat.delta}
                </>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default LogSummary;
