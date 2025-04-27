
import React from 'react';
import RemediationNode from './RemediationNode';

import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import RootCauseSteps from './RootCauseTree';
import { Search } from 'lucide-react';


const RemediationPanel = () => {

  return (
    <div className="animate-in fade-in duration-500">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold text-gray-900">Root Cause Analysis</h1>
        <div className="relative">
          <input
            type="text"
            placeholder="Search steps..."
            className="pl-9 pr-4 py-2 bg-white border border-gray-300 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent w-64"
          />
          <Search size={18} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
        </div>
      </div>
      
      <div className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg font-semibold text-gray-900">Investigation Progress</CardTitle>
          </CardHeader>
          <CardContent>
            <RootCauseSteps steps={[
              {
                id: '1',
                title: 'Initial System Analysis',
                description: 'Review of system logs and error patterns',
                status: 'completed'
              },
              {
                id: '2',
                title: 'Memory Leak Investigation',
                description: 'Analyzing memory usage patterns and potential leaks',
                status: 'in_progress'
              },
              {
                id: '3',
                title: 'Database Connection Analysis',
                description: 'Review of connection pool settings and configurations',
                status: 'pending'
              },
              {
                id: '4',
                title: 'Performance Testing',
                description: 'Load testing and performance metrics analysis',
                status: 'pending'
              }
            ]} />
          </CardContent>
        </Card>

      </div>
    </div>
  );
};

export default RemediationPanel;
