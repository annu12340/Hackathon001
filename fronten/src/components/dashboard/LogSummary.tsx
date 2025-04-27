import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { cn } from '@/lib/utils';

interface LogStat {
  label: string;
  value: number;
  delta: number;
}

const LogSummary = () => {
  return (
    <div className="grid ">
      <Card className="col-span-full">

        <CardHeader>
            <CardTitle className="text-lg font-semibold text-gray-900">Summarized Logs </CardTitle>
          </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            This dashboard provides a comprehensive view of your system logs, hi1ghlighting key metrics and trends.
            Monitor your application's performance and quickly identify any anomalies or patterns in the logging data.
          </p>
        </CardContent>
      </Card>
    </div>
  );
};

export default LogSummary;
