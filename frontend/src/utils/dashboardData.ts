import dashboardData from '../components/data/data.json';
import { 
  DashboardData, 
  Task, 
  Overview, 
  RootCauseStep, 
  Logs 
} from './dashboardTypes';

// Type assertion for the imported JSON data
const typedData = dashboardData as unknown as DashboardData;

export const followUpTasks: Task[] = typedData.followUpTasks;
export const overviewData: Overview = typedData.overview;
export const rootCauseSteps: RootCauseStep[] = typedData.rootCauseSteps;
export const logsData: Logs = typedData.logs;

export default typedData; 