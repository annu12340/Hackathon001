import React from 'react';
import MetricCard from './MetricCard';
import { Cpu, Database, Activity, Clock } from 'lucide-react';
import { overviewData } from '@/utils/dashboardData';

const OverviewPanel = () => {
  return (
    <div className="animate-in fade-in duration-500">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-semibold text-gray-900">{overviewData.title}</h1>
        <div className="text-sm text-gray-500 flex items-center gap-2 bg-white px-3 py-1.5 rounded-full border border-gray-100">
          <Clock size={14} />
          Last updated: 2 mins ago
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        {overviewData.metrics.map((metric, index) => (
          <MetricCard 
            key={index}
            title={metric.title} 
            value={metric.value} 
            icon={
              metric.icon === 'Cpu' ? <Cpu /> : 
              metric.icon === 'Database' ? <Database /> : 
              <Activity />
            }
            color={metric.color}
            trend={metric.trend}
            suffix={metric.suffix}
            description={metric.description}
          />
        ))}
      </div>

      <div className="mt-8 bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
        <h2 className="text-lg font-medium mb-4 text-gray-800">Recent Activity</h2>
        <div className="space-y-3">
          {overviewData.recentActivity.map((activity, idx) => (
            <div key={idx} className="flex items-center py-2 border-b border-gray-50 last:border-none">
              <div className={`w-2 h-2 rounded-full mr-3 ${
                activity.severity === 'warning' ? 'bg-yellow-400' : 
                activity.severity === 'error' ? 'bg-red-400' : 
                activity.severity === 'success' ? 'bg-green-400' : 'bg-blue-400'
              }`}></div>
              <span className="text-sm text-gray-500 w-20">{activity.time}</span>
              <span className="text-sm text-gray-700">{activity.event}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default OverviewPanel;
