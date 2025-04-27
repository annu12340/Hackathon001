export interface Task {
  id: number;
  title: string;
  dueDate: string;
  priority: string;
  completed: boolean;
  assignee: string;
}

export interface Metric {
  title: string;
  value: number;
  icon: string;
  trend: string;
  color: string;
  suffix?: string;
  description: string;
}

export interface Activity {
  time: string;
  event: string;
  severity: string;
}

export interface Overview {
  title: string;
  metrics: Metric[];
  recentActivity: Activity[];
}

export interface RootCauseStep {
  id: string;
  title: string;
  description: string;
  status: 'completed' | 'in_progress' | 'pending';
}

export interface LogEntry {
  level: string;
  timestamp: string;
  message: string;
}

export interface LogSummaryStat {
  label: string;
  value: number;
  delta: number;
}

export interface LogData {
  [key: string]: LogEntry[];
}

export interface Logs {
  logSummaryStats: LogSummaryStat[];
  logData: LogData;
}

export interface DashboardData {
  followUpTasks: Task[];
  overview: Overview;
  rootCauseSteps: RootCauseStep[];
  logs: Logs;
} 