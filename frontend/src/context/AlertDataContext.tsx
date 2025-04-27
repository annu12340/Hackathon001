import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useParams } from 'react-router-dom';
import { DashboardData } from '@/utils/dashboardTypes';

interface AlertDataContextType {
  alertData: DashboardData | null;
  isLoading: boolean;
  error: Error | null;
  alertId: string | null;
}

const AlertDataContext = createContext<AlertDataContextType>({
  alertData: null,
  isLoading: true,
  error: null,
  alertId: null,
});

export const AlertDataProvider = ({ children }: { children: ReactNode }) => {
  const [alertData, setAlertData] = useState<DashboardData | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<Error | null>(null);
  
  const { alertId } = useParams<{ alertId?: string }>();

  useEffect(() => {
    const fetchAlertData = async () => {
      try {
        setIsLoading(true);
        setError(null);
        
        let response;
        
        if (!alertId) {
          // Default data if no alertId is provided
          response = await fetch('/data/data.json');
        } else {
          // Fetch data based on alertId
          response = await fetch(`/data/${alertId}/data.json`);
        }
        
        if (!response.ok) {
          throw new Error(`Failed to fetch alert data: ${response.status} ${response.statusText}`);
        }
        
        const data = await response.json();
        setAlertData(data as DashboardData);
        setIsLoading(false);
      } catch (err) {
        console.error("Error fetching alert data:", err);
        setError(err instanceof Error ? err : new Error('Failed to fetch alert data'));
        setIsLoading(false);
      }
    };

    fetchAlertData();
  }, [alertId]);

  return (
    <AlertDataContext.Provider value={{ alertData, isLoading, error, alertId: alertId || null }}>
      {children}
    </AlertDataContext.Provider>
  );
};

export const useAlertData = () => useContext(AlertDataContext); 