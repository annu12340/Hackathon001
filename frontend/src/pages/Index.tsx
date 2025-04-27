import React, { useState } from 'react';
import Sidebar from '@/components/dashboard/Sidebar';
import OverviewPanel from '@/components/dashboard/OverviewPanel';
import LogsPanel from '@/components/dashboard/LogsPanel';
import RootCausePanel from '@/components/dashboard/RootCausePanel';
import RemediationPanel from '@/components/dashboard/RemediationPanel';
import FollowUpPanel from '@/components/dashboard/FollowUpPanel';
import ChatDrawer from '@/components/dashboard/ChatDrawer';
import { MessageCircle } from 'lucide-react';
import { useAlertData } from '@/context/AlertDataContext';

const Index = () => {
  const [activePage, setActivePage] = useState('overview');
  const [isChatOpen, setIsChatOpen] = useState(false);
  const { alertData, isLoading, error, alertId } = useAlertData();
  
  const renderContent = () => {
    if (isLoading) {
      return (
        <div className="flex items-center justify-center h-screen">
          <div className="text-center">
            <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]" />
            <p className="mt-4 text-lg">Loading alert data...</p>
          </div>
        </div>
      );
    }

    if (error) {
      return (
        <div className="flex items-center justify-center h-screen">
          <div className="text-center text-red-500">
            <p className="text-xl font-semibold">Error loading data</p>
            <p className="mt-2">{error.message}</p>
          </div>
        </div>
      );
    }

    if (!alertData) {
      return (
        <div className="flex items-center justify-center h-screen">
          <div className="text-center">
            <p className="text-xl font-semibold">No alert data found</p>
            {alertId && (
              <p className="mt-2">Alert ID: {alertId} not found. Please check the URL.</p>
            )}
          </div>
        </div>
      );
    }

    switch (activePage) {
      case 'overview':
        return <OverviewPanel data={alertData.overview} />;
      case 'logs':
        return <LogsPanel data={alertData.logs} />;
      case 'rootCause':
        return <RootCausePanel data={alertData.rootCauseSteps} />;
      case 'remediation':
        return <RemediationPanel />;
      case 'followUp':
        return <FollowUpPanel data={alertData.followUpTasks} />;
      default:
        return <OverviewPanel data={alertData.overview} />;
    }
  };
  
  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar activePage={activePage} setActivePage={setActivePage} />
      
      <div className="flex-1 p-8">
        <div className="max-w-6xl mx-auto">
          {alertId && (
            <div className="mb-4 text-sm text-gray-500">
              Alert ID: {alertId}
            </div>
          )}
          {renderContent()}
        </div>
      </div>
      
      <button 
        className="fixed bottom-4 right-4 flex items-center gap-2 bg-black text-white px-4 py-2 rounded-full shadow-lg hover:bg-gray-800 transition-colors"
        onClick={() => setIsChatOpen(true)}
      >
        <MessageCircle className="h-5 w-5" />
        <span className="hidden md:inline">Chat</span>
      </button>
      
      <ChatDrawer isOpen={isChatOpen} onClose={() => setIsChatOpen(false)} />
    </div>
  );
};

export default Index;
