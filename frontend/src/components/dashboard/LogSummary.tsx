import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { logsData } from '@/utils/dashboardData';

interface LogStat {
  label: string;
  value: number;
  delta: number;
}

const LogSummary = () => {
  return (
    <div className="grid">
      <Card className="col-span-full">
        <CardHeader>
          <CardTitle className="text-lg font-semibold text-gray-900">Summarized Logs</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex justify-between mb-4">
            {logsData.logSummaryStats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-2xl font-semibold text-gray-900">{stat.value}</div>
                <div className="text-sm text-gray-500">{stat.label}</div>
                <div className={cn(
                  "text-xs mt-1",
                  stat.delta > 0 ? "text-green-600" : "text-red-600"
                )}>
                  {stat.delta > 0 ? "+" : ""}{stat.delta}
                </div>
              </div>
            ))}
          </div>
          <p className="text-muted-foreground">
            This dashboard provides a comprehensive view of your system logs, highlighting key metrics and trends.
            Monitor your application's performance and quickly identify any anomalies or patterns in the logging data.
          </p>
        </CardContent>
      </Card>
    </div>
  );
};

export default LogSummary;
