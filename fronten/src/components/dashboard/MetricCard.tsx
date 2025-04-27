
import React from 'react';
import { cn } from '@/lib/utils';
import { Progress } from '@/components/ui/progress';

interface MetricCardProps {
  title: string;
  value: number;
  icon: React.ReactNode;
  className?: string;
  color?: string;
  trend?: 'up' | 'down' | 'neutral';
  suffix?: string;
  description?: string;
}

const MetricCard = ({ 
  title, 
  value, 
  icon, 
  className, 
  color = 'blue',
  trend,
  suffix = '%',
  description
}: MetricCardProps) => {
  
  const getStatusColor = () => {
    if (value < 60) return 'bg-green-500';
    if (value < 80) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const getGradient = () => {
    switch (color) {
      case 'blue':
        return 'from-blue-50 to-white';
      case 'cyan':
        return 'from-cyan-50 to-white';
      case 'green':
        return 'from-green-50 to-white';
      default:
        return 'from-blue-50 to-white';
    }
  };

  return (
    <div className={cn(
      'metric-card bg-gradient-to-br', 
      getGradient(),
      className
    )}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-gray-700 font-medium">{title}</h3>
        <div className="text-gray-500">{icon}</div>
      </div>
      
      <div className="flex items-end gap-2 mb-3">
        <div className="text-3xl font-semibold">
          {value}{suffix}
        </div>
        
        {trend && (
          <div className={cn(
            "text-xs px-2 py-1 rounded-full flex items-center",
            trend === 'up' ? 'text-red-700 bg-red-50' : 'text-green-700 bg-green-50'
          )}>
            {trend === 'up' ? '↑' : '↓'} 
            {trend === 'up' ? '+' : '-'}2.5%
          </div>
        )}
      </div>

      <Progress value={value} className={cn("h-2 bg-gray-100", value >= 80 ? "animate-pulse-gentle" : "")} />
      
      {description && (
        <p className="text-xs text-gray-500 mt-3">{description}</p>
      )}
    </div>
  );
};

export default MetricCard;
