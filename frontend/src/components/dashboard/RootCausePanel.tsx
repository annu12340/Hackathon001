import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import RootCauseSteps from './RootCauseTree';
import { Search } from 'lucide-react';
import { RootCauseStep } from '@/utils/dashboardTypes';

interface RootCausePanelProps {
  data: RootCauseStep[];
}

const RootCausePanel: React.FC<RootCausePanelProps> = ({ data }) => {
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
            <RootCauseSteps steps={data} />
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default RootCausePanel;