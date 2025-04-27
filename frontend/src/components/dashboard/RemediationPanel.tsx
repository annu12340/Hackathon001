import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import RootCauseSteps from './RootCauseTree';
import { Search, WrenchIcon, Lightbulb, CheckCircle, Filter, PlusCircle, ArrowRight, Terminal, GitBranch, RefreshCw, Shield } from 'lucide-react';
import { useAlertData } from '@/context/AlertDataContext';

const RemediationPanel = () => {
  const { alertData, isLoading, error } = useAlertData();
  const [filterActive, setFilterActive] = useState(false);

  // If we're loading or have an error, these states are handled in Index.tsx
  if (!alertData) return null;

  return (
    <div className="animate-in fade-in duration-700 space-y-8">
      <div className="flex justify-between items-center">
        <div className="flex items-center gap-2">
          <WrenchIcon size={24} className="text-indigo-500" />
          <h1 className="text-2xl font-bold text-gray-900 tracking-tight">Remediation Actions</h1>
        </div>
        
        <div className="flex items-center gap-3">
          <button 
            onClick={() => setFilterActive(!filterActive)}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium transition-colors border ${filterActive 
              ? 'bg-indigo-100 text-indigo-700 border-indigo-200' 
              : 'bg-white text-gray-600 border-gray-200'}`}
          >
            <Filter size={14} className={filterActive ? 'text-indigo-500' : 'text-gray-400'} />
            Filter
          </button>
          
          <div className="relative group">
            <input
              type="text"
              placeholder="Search actions..."
              className="pl-9 pr-4 py-2 bg-white/90 backdrop-blur-sm border border-gray-200 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent w-64 shadow-sm hover:shadow transition-all duration-200"
            />
            <Search size={16} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 group-hover:text-indigo-500 transition-colors duration-200" />
          </div>
        </div>
      </div>
      
      {/* Quick Actions Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {[
          {
            icon: <Lightbulb size={18} />,
            title: "AI Suggestions",
            description: "Get smart recommendations",
            color: "amber"
          },
          {
            icon: <Terminal size={18} />,
            title: "Run Diagnostics",
            description: "Execute automated tests",
            color: "indigo"
          },
          {
            icon: <Shield size={18} />,
            title: "Apply Safe Fixes",
            description: "Auto-fix non-critical issues",
            color: "green"
          }
        ].map((action, index) => (
          <button key={index} className={`flex items-center justify-between p-4 rounded-xl border border-${action.color}-100 bg-${action.color}-50/40 hover:bg-${action.color}-50 text-left group transition-all duration-200 shadow-sm hover:shadow`}>
            <div className="flex items-center gap-3">
              <div className={`p-2.5 rounded-lg bg-${action.color}-100 text-${action.color}-600`}>
                {action.icon}
              </div>
              <div>
                <h3 className="font-semibold text-gray-900">{action.title}</h3>
                <p className="text-sm text-gray-500">{action.description}</p>
              </div>
            </div>
            <ArrowRight size={16} className={`text-${action.color}-400 opacity-0 group-hover:opacity-100 transition-opacity duration-200`} />
          </button>
        ))}
      </div>
      
      <div className="space-y-6">
        {/* Recommended Actions Card */}
        <Card className="border-gray-100 shadow-sm overflow-hidden hover:shadow transition-all duration-200">
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-indigo-500 via-blue-500 to-indigo-400"></div>
          
          <CardHeader className="bg-gradient-to-r from-gray-50 to-white pb-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <CheckCircle size={18} className="text-green-500" />
                <CardTitle className="text-lg font-bold text-gray-900">Recommended Actions</CardTitle>
              </div>
              
              <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-white text-gray-600 border border-gray-200 shadow-sm hover:bg-gray-50 transition-colors">
                <RefreshCw size={14} className="text-gray-400" />
                Refresh
              </button>
            </div>
          </CardHeader>
          
          <CardContent className="pt-2">
            <RootCauseSteps steps={alertData.rootCauseSteps} />
            
            <div className="mt-6 pt-5 border-t border-gray-100 flex justify-between items-center">
              <button className="flex items-center gap-2 text-indigo-600 hover:text-indigo-700 font-medium text-sm transition-colors">
                <PlusCircle size={16} />
                Add Custom Action
              </button>
              
              <button className="flex items-center gap-2 text-gray-500 hover:text-gray-700 text-sm transition-colors">
                <GitBranch size={16} />
                View Action History
              </button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default RemediationPanel;
