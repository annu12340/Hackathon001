
import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { cn } from '@/lib/utils';

interface Cause {
  title: string;
  description: string;
}

const currentInvestigation = {
  title: "Database Connection Issues",
  description: "Intermittent connection failures observed in the primary database cluster. Investigating network latency and connection pool settings.",
};

const potentialCauses: Cause[] = [
  { title: "Network latency spikes during peak hours", description: "Observed increased latency during high traffic periods" },
  { title: "Connection pool exhaustion", description: "Max connections reached multiple times" },
  { title: "Database CPU utilization above threshold", description: "CPU usage consistently above 80%" },
];

const RootCausePanel = () => {
  return (
    <div className="animate-in fade-in duration-500">
      <h1 className="text-2xl font-semibold text-gray-900 mb-6">Root Cause Analysis</h1>
      
      <div className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg font-semibold text-gray-900">Current Investigation</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="bg-yellow-50 border border-yellow-100 rounded-lg p-4">
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                {currentInvestigation.title}
              </h3>
              <p className="text-gray-600 leading-relaxed">
                {currentInvestigation.description}
              </p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg font-semibold text-gray-900">Potential Causes</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-4">
              {potentialCauses.map((cause, index) => (
                <li key={index} className="flex gap-4">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-50 flex items-center justify-center">
                    <span className="text-sm font-semibold text-blue-600">{index + 1}</span>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900">{cause.title}</h4>
                    <p className="text-sm text-gray-600 mt-1 leading-relaxed">{cause.description}</p>
                  </div>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default RootCausePanel;