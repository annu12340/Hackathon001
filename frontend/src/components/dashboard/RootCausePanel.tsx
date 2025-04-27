import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Search, Filter, Clock, CheckCircle2, CircleDashed, Lightbulb, ArrowRight, Users } from 'lucide-react';
import { RootCauseStep } from '@/utils/dashboardTypes';

interface RootCausePanelProps {
  data: RootCauseStep[];
}

const RootCausePanel: React.FC<RootCausePanelProps> = ({ data }) => {
  const [searchQuery, setSearchQuery] = useState('');
  
  // Calculate progress
  const completedSteps = data.filter(step => step.status === 'completed').length;
  const inProgressSteps = data.filter(step => step.status === 'in_progress').length;
  const totalSteps = data.length;
  const progressPercentage = Math.round((completedSteps / totalSteps) * 100);
  
  // Get current in-progress step(s)
  const currentStep = data.find(step => step.status === 'in_progress');

  return (
    <div className="animate-in fade-in duration-500">
      <div className="flex flex-col md:flex-row md:justify-between md:items-center gap-4 mb-6">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">Root Cause Analysis</h1>
          <p className="text-gray-500 text-sm mt-1">Identifying and resolving the underlying issue</p>
        </div>
        <div className="flex gap-3">
          <div className="relative">
            <input
              type="text"
              placeholder="Search steps..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-9 pr-4 py-2 bg-white border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent w-64 shadow-sm"
            />
            <Search size={18} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
          </div>
          <button className="bg-white px-3 py-2 rounded-lg border border-gray-300 shadow-sm hover:bg-gray-50 transition-colors text-gray-600 flex items-center">
            <Filter size={16} className="mr-2" />
            <span className="text-sm">Filter</span>
          </button>
        </div>
      </div>
      
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <Card className="bg-gradient-to-r from-indigo-50 to-white border-indigo-100">
          <CardContent className="p-4 flex items-center">
            <div className="bg-indigo-100 p-2 rounded-lg mr-3">
              <Clock size={20} className="text-indigo-600" />
            </div>
            <div>
              <p className="text-gray-500 text-xs mb-1">Time Elapsed</p>
              <p className="font-semibold">2 hours 45 minutes</p>
            </div>
          </CardContent>
        </Card>
        
        <Card className="bg-gradient-to-r from-amber-50 to-white border-amber-100">
          <CardContent className="p-4 flex items-center">
            <div className="bg-amber-100 p-2 rounded-lg mr-3">
              <Users size={20} className="text-amber-600" />
            </div>
            <div>
              <p className="text-gray-500 text-xs mb-1">Team Assigned</p>
              <p className="font-semibold">Platform Engineering</p>
            </div>
          </CardContent>
        </Card>
        
        <Card className="bg-gradient-to-r from-green-50 to-white border-green-100">
          <CardContent className="p-4 flex items-center">
            <div className="bg-green-100 p-2 rounded-lg mr-3">
              <CheckCircle2 size={20} className="text-green-600" />
            </div>
            <div>
              <p className="text-gray-500 text-xs mb-1">Progress</p>
              <div className="flex items-center gap-2">
                <div className="w-20 h-1.5 bg-gray-200 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-green-500 rounded-full" 
                    style={{ width: `${progressPercentage}%` }}
                  />
                </div>
                <span className="text-sm font-medium">{progressPercentage}%</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
      
      {/* Current Step Info */}
      {currentStep && (
        <Card className="bg-white border-indigo-100 shadow-sm mb-6 overflow-hidden">
          <div className="h-1.5 bg-indigo-500 w-full"></div>
          <CardContent className="p-5">
            <div className="flex items-center text-indigo-600 text-sm font-medium mb-2">
              <CircleDashed size={16} className="mr-2 animate-pulse" />
              <span>IN PROGRESS</span>
            </div>
            <h3 className="text-lg font-semibold mb-2">{currentStep.title}</h3>
            <p className="text-gray-600 mb-4">{currentStep.description}</p>
            
            {/* Recommended action */}
            <div className="bg-indigo-50 rounded-lg p-4 flex items-start">
              <div className="bg-indigo-100 p-1.5 rounded text-indigo-600 mr-3 mt-0.5">
                <Lightbulb size={16} />
              </div>
              <div>
                <p className="font-medium text-sm text-gray-800 mb-1">Recommended Next Action</p>
                <p className="text-sm text-gray-600">Analyze memory consumption patterns and check for potential memory leaks in the API Gateway component.</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
      

    </div>
  );
};

export default RootCausePanel;