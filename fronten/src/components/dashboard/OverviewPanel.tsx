
import React from 'react';
import MetricCard from './MetricCard';
import { Cpu, Database, Activity, Clock } from 'lucide-react';

const OverviewPanel = () => {
  return (
    <div className="animate-in fade-in duration-500">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-semibold text-gray-900">System Overview</h1>
        <div className="text-sm text-gray-500 flex items-center gap-2 bg-white px-3 py-1.5 rounded-full border border-gray-100">
          <Clock size={14} />
          Last updated: 2 mins ago
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        <MetricCard 
          title="CPU Usage" 
          value={42} 
          icon={<Cpu />}
          trend="down"
          description="4 cores @ 2.3GHz"
        />
        <MetricCard 
          title="Memory Usage" 
          value={68} 
          icon={<Database />}
          color="cyan"
          trend="up"
          description="10.9GB / 16GB Used"
        />
        <MetricCard 
          title="Node Health" 
          value={95} 
          icon={<Activity />}
          color="green"
          suffix="%"
          description="All services operational"
        />
      </div>

      <div className="mt-8 bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
        <h2 className="text-lg font-medium mb-4 text-gray-800">Recent Activity</h2>
        <div className="space-y-3">
          {[
            { time: '09:45 AM', event: 'Memory usage spike detected', severity: 'warning' },
            { time: '09:30 AM', event: 'Application restart', severity: 'info' },
            { time: '09:15 AM', event: 'CPU throttling resolved', severity: 'success' },
            { time: '08:45 AM', event: 'Garbage collection completed', severity: 'info' },
          ].map((activity, idx) => (
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
