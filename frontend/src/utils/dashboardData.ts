import { DashboardData } from './dashboardTypes';

// This file now exports functions to get the data from the provided alert data
// rather than importing directly from a static file

export const getFollowUpTasks = (data: DashboardData) => data.followUpTasks;
export const getOverviewData = (data: DashboardData) => data.overview;
export const getRootCauseSteps = (data: DashboardData) => data.rootCauseSteps;
export const getLogsData = (data: DashboardData) => data.logs;

export default null; // No longer exporting the data directly 