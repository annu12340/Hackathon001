
import React, { useState } from 'react';
import Sidebar from '@/components/dashboard/Sidebar';
import OverviewPanel from '@/components/dashboard/OverviewPanel';
import LogsPanel from '@/components/dashboard/LogsPanel';
import RootCausePanel from '@/components/dashboard/RootCausePanel';
import RemediationPanel from '@/components/dashboard/RemediationPanel';
import FollowUpPanel from '@/components/dashboard/FollowUpPanel';
import ChatDrawer from '@/components/dashboard/ChatDrawer';
import { MessageCircle } from 'lucide-react';

const Index = () => {
  const [activePage, setActivePage] = useState('overview');
  const [isChatOpen, setIsChatOpen] = useState(false);
  
  const renderContent = () => {
    switch (activePage) {
      case 'overview':
        return <OverviewPanel />;
      case 'logs':
        return <LogsPanel />;
      case 'rootCause':
        return <RootCausePanel />;
      case 'remediation':
        return <RemediationPanel />;
      case 'followUp':
        return <FollowUpPanel />;
      default:
        return <OverviewPanel />;
    }
  };
  
  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar activePage={activePage} setActivePage={setActivePage} />
      
      <div className="flex-1 p-8">
        <div className="max-w-6xl mx-auto">
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
