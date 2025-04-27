import React from 'react';
import MetricCard from './MetricCard';
import { Cpu, Database, Activity, Clock, AlertCircle, Bell, Flame, Calendar, User, RefreshCw } from 'lucide-react';
import { Overview } from '@/utils/dashboardTypes';

interface OverviewPanelProps {
  data: Overview;
}

const OverviewPanel: React.FC<OverviewPanelProps> = ({ data }) => {
  return (
    <div className="animate-in fade-in duration-500">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold text-gray-900">{data.title}</h1>
        <div className="text-sm text-gray-500 flex items-center gap-2 bg-white px-3 py-1.5 rounded-full border border-gray-100">
          <Clock size={14} />
          Last updated: 2 mins ago
        </div>
      </div>

      {/* Alert Details Card */}
      {data.alertDetails && (
        <div className="bg-gradient-to-r from-gray-50 to-white p-6 rounded-xl border border-gray-100 shadow-sm mb-8">
          <div className="flex items-start gap-6">
            {/* Left column - Status & Title */}
            <div className="flex-grow">
              <div className="flex gap-3 items-center mb-3">
                <div className="flex-shrink-0 w-3 h-3 rounded-full bg-red-500 animate-pulse"></div>
                <span className="text-red-600 font-semibold text-sm tracking-wide uppercase">
                  {data.alertDetails.status}
                </span>
                <div className="h-4 w-px bg-gray-200"></div>
                <div className="flex items-center text-orange-600 font-semibold text-sm">
                  <Flame size={14} className="mr-1" />
                  <span className="tracking-wide uppercase">{data.alertDetails.urgency}</span>
                </div>
              </div>
              
              <h2 className="text-xl font-bold text-gray-900 mb-2">{data.alertDetails.title}</h2>
              <div className="flex items-center text-gray-600 mb-4">
                <div className="flex items-center bg-blue-50 px-3 py-1 rounded-full text-blue-700 text-sm">
                  <Database size={12} className="mr-1.5" />
                  <span>{data.alertDetails.service}</span>
                </div>
              </div>
            </div>
            
            {/* Right column - Incident number and actions */}
            <div className="flex-shrink-0 flex flex-col items-end">
              <div className="text-sm text-gray-500 mb-2">Incident #ABC-123</div>
              <div className="flex gap-2">
                <button className="bg-blue-50 hover:bg-blue-100 text-blue-600 px-3 py-1.5 rounded text-xs font-medium transition-colors flex items-center">
                  <Bell size={12} className="mr-1.5" />
                  Subscribe
                </button>
                <button className="bg-gray-50 hover:bg-gray-100 text-gray-600 px-3 py-1.5 rounded text-xs font-medium transition-colors flex items-center">
                  <RefreshCw size={12} className="mr-1.5" />
                  Refresh
                </button>
              </div>
            </div>
          </div>
          
          <div className="h-px w-full bg-gray-100 my-4"></div>
          
          {/* Info grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
            <div className="flex items-start">
              <Calendar size={16} className="mr-3 text-gray-400 mt-0.5 flex-shrink-0" />
              <div>
                <p className="text-gray-500 font-medium mb-1">Created</p>
                <p className="font-semibold text-gray-900">{data.alertDetails.created}</p>
              </div>
            </div>
            <div className="flex items-start">
              <Clock size={16} className="mr-3 text-gray-400 mt-0.5 flex-shrink-0" />
              <div>
                <p className="text-gray-500 font-medium mb-1">Last Updated</p>
                <p className="font-semibold text-gray-900">{data.alertDetails.lastUpdated}</p>
              </div>
            </div>
            <div className="flex items-start">
              <User size={16} className="mr-3 text-gray-400 mt-0.5 flex-shrink-0" />
              <div>
                <p className="text-gray-500 font-medium mb-1">Assigned To</p>
                <div className="flex items-center">
                  <div className="w-6 h-6 rounded-full bg-purple-100 flex items-center justify-center text-xs font-medium text-purple-600 mr-2">
                    {data.alertDetails.assignedTo.split(' ').map(word => word[0]).join('')}
                  </div>
                  <p className="font-semibold text-gray-900">{data.alertDetails.assignedTo}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}



      <div className="mt-8 bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
        <h2 className="text-lg font-medium mb-4 text-gray-800">Recent Activity</h2>
        <div className="space-y-3">
          {data.recentActivity.map((activity, idx) => (
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
