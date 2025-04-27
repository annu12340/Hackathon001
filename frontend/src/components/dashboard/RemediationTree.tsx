import React from 'react';
import { Check, Circle } from 'lucide-react';
import { cn } from '@/lib/utils';

export interface Step {
  id: string;
  title: string;
  description?: string;
  status: 'completed' | 'in_progress' | 'pending';
}

interface StepItemProps {
  step: Step;
  isLast: boolean;
}

const StepItem: React.FC<StepItemProps> = ({ step, isLast }) => {
  const statusConfig = {
    completed: {
      icon: <Check className="w-5 h-5" />,
      color: 'text-green-600 border-green-600',
      bgColor: 'bg-green-50',
      textColor: 'text-green-600',
      lineColor: 'border-green-200'
    },
    in_progress: {
      icon: <div className="w-3 h-3 rounded-full bg-blue-500 animate-pulse" />,
      color: 'text-blue-600 border-blue-600',
      bgColor: 'bg-blue-50',
      textColor: 'text-blue-600',
      lineColor: 'border-blue-200'
    },
    pending: {
      icon: <Circle className="w-5 h-5" />,
      color: 'text-gray-300 border-gray-300',
      bgColor: 'bg-gray-50',
      textColor: 'text-gray-400',
      lineColor: 'border-gray-200'
    }
  };

  const config = statusConfig[step.status];

  return (
    <div className="relative">
      <div className={cn(
        'flex items-start gap-4 py-4',
        step.status === 'in_progress' && 'bg-blue-50/50 px-4 rounded-lg'
      )}>
        {/* Status indicator */}
        <div className="relative">
          <div className={cn(
            'w-8 h-8 rounded-full border-2 flex items-center justify-center',
            config.color,
            config.bgColor
          )}>
            {config.icon}
          </div>
          {!isLast && (
            <div className={cn(
              'absolute top-8 left-1/2 w-0.5 h-full -translate-x-1/2 border-l-2',
              config.lineColor
            )} />
          )}
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0 pt-1">
          <h3 className={cn(
            "font-medium",
            step.status === 'pending' ? 'text-gray-400' : 'text-gray-900'
          )}>
            {step.title}
          </h3>
          {step.description && (
            <p className={cn(
              "text-sm mt-1",
              step.status === 'pending' ? 'text-gray-400' : 'text-gray-600'
            )}>
              {step.description}
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

interface RemediationStepsProps {
  steps: Step[];
}

const RemediationSteps: React.FC<RemediationStepsProps> = ({ steps }) => {
  return (
    <div className="bg-white rounded-lg p-4">
      {steps.map((step, index) => (
        <StepItem
          key={step.id}
          step={step}
          isLast={index === steps.length - 1}
        />
      ))}
    </div>
  );
};

export default RemediationSteps;
