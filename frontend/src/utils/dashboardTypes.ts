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
  trend: 'up' | 'down' | 'neutral';
  color: string;
  suffix?: string;
  description: string;
}

export interface Activity {
  time: string;
  event: string;
  severity: string;
}

export interface AlertDetails {
  status: string;
  urgency: string;
  title: string;
  service: string;
  created: string;
  lastUpdated: string;
  assignedTo: string;
}

export interface AiGeneratedData {
  confidence: string;
  environment: string;
  cluster: string;
  nodeName: string;
  errorType: string;
  errorSeverity: string;
  impactedComponent: string;
  componentVersion: string;
  firstDetected: string;
  alertSummary?: string;
}

export interface Overview {
  title: string;
  metrics: Metric[];
  recentActivity: Activity[];
  alertDetails: AlertDetails;
  aiGeneratedData?: AiGeneratedData;
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