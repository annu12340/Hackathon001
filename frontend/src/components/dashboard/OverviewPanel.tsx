import React from 'react';
import { Cpu, Database, Activity, Clock, AlertCircle, Bell, Flame, Calendar, User, RefreshCw, Server, Globe, Box, Layers, AlertTriangle, Bot, Code, Sparkles, ExternalLink, FileText, PhoneCall } from 'lucide-react';
import { Overview } from '@/utils/dashboardTypes';

interface OverviewPanelProps {
  data: Overview;
}

const OverviewPanel: React.FC<OverviewPanelProps> = ({ data }) => {
  // Default AI data for demo purposes
  const aiData = data.aiGeneratedData 

  return (
    <div className="animate-in fade-in duration-500">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold text-gray-900">{data.title}</h1>
        <div className="text-sm text-gray-500 flex items-center gap-2 bg-white px-3 py-1.5 rounded-full border border-gray-100">
          <Clock size={14} />
          Last updated: 2 mins ago
        </div>
      </div>

      {/* Alert Details Card */}
      {data.alertDetails && (
        <div className="bg-gradient-to-r from-gray-50 to-white p-6 rounded-xl border border-gray-100 shadow-sm mb-8">
          <div className="flex items-start gap-6">
            {/* Left column - Status & Title */}
            <div className="flex-grow">
              <div className="flex gap-3 items-center mb-3">
                <div className="flex-shrink-0 w-3 h-3 rounded-full bg-red-500 animate-pulse"></div>
                <span className="text-red-600 font-semibold text-sm tracking-wide uppercase">
                  {data.alertDetails.status}
                </span>
                <div className="h-4 w-px bg-gray-200"></div>
                <div className="flex items-center text-orange-600 font-semibold text-sm">
                  <Flame size={14} className="mr-1" />
                  <span className="tracking-wide uppercase">{data.alertDetails.urgency}</span>
                </div>
              </div>
              
              <h2 className="text-xl font-bold text-gray-900 mb-2">{data.alertDetails.title}</h2>
              <div className="flex items-center text-gray-600 mb-4">
                <div className="flex items-center bg-blue-50 px-3 py-1 rounded-full text-blue-700 text-sm">
                  <Database size={12} className="mr-1.5" />
                  <span>{data.alertDetails.service}</span>
                </div>
              </div>
            </div>
            
            {/* Right column - Incident number and actions */}
            <div className="flex-shrink-0 flex flex-col items-end">
              <div className="text-xs text-gray-500 mb-2">Incident #Q3TAMBYDY6HQI4</div>
              <div className="flex gap-2">
              <button className="bg-green-600 hover:bg-green-700 text-white px-3 py-1.5 rounded-full text-xs font-medium transition-colors flex items-center">
              <PhoneCall size={12} className="mr-1.5" />
              PagerDuty Alert
            </button>
                <button className="bg-gray-50 hover:bg-gray-100 text-gray-600 px-3 py-1.5 rounded text-xs font-medium transition-colors flex items-center">
                  <RefreshCw size={12} className="mr-1.5" />
                  Refresh
                </button>
              </div>
            </div>
          </div>
          
          <div className="h-px w-full bg-gray-100 my-4"></div>
          
           {/* Info grid */}
           <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
              <div className="flex items-start bg-white/80 p-3 rounded-lg border border-gray-100 shadow-sm hover:shadow transition-all duration-200">
                <Calendar size={16} className="mr-3 text-indigo-500 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-gray-500 font-medium mb-1">Created</p>
                  <p className="font-semibold text-gray-900">{data.alertDetails.created}</p>
                </div>
              </div>
              <div className="flex items-start bg-white/80 p-3 rounded-lg border border-gray-100 shadow-sm hover:shadow transition-all duration-200">
                <Clock size={16} className="mr-3 text-indigo-500 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-gray-500 font-medium mb-1">Last Updated</p>
                  <p className="font-semibold text-gray-900">{data.alertDetails.lastUpdated}</p>
                </div>
              </div>
              <div className="flex items-start bg-white/80 p-3 rounded-lg border border-gray-100 shadow-sm hover:shadow transition-all duration-200">
                <User size={16} className="mr-3 text-indigo-500 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-gray-500 font-medium mb-1">Assigned To</p>
                  <div className="flex items-center">
                    <div className="w-6 h-6 rounded-full bg-purple-100 flex items-center justify-center text-xs font-medium text-purple-600 mr-2 border border-purple-200 shadow-sm">
                      {data.alertDetails.assignedTo.split(' ').map(word => word[0]).join('')}
                    </div>
                    <p className="font-semibold text-gray-900">{data.alertDetails.assignedTo}</p>
                  </div>
                </div>
              </div>
            </div>
        </div>
      )}

      {/* Generated by AI Section */}
      <div className="bg-gradient-to-br from-indigo-50 via-white to-purple-50 p-6 rounded-xl border border-indigo-100 shadow-sm mb-8 overflow-hidden relative">
        {/* Decorative elements */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-indigo-100/30 to-purple-100/20 rounded-full -mr-32 -mt-32 blur-3xl"></div>
        <div className="absolute bottom-0 left-0 w-64 h-64 bg-gradient-to-tr from-blue-100/20 to-indigo-100/10 rounded-full -ml-32 -mb-32 blur-3xl"></div>
        
        {/* Header */}
        <div className="flex items-center justify-between mb-6 relative">
          <div className="flex items-center">
            <div className="bg-indigo-100 p-2 rounded-lg mr-3">
              <Bot size={20} className="text-indigo-600" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-gray-900 flex items-center">
                Auto generated by AI
                <Sparkles size={16} className="ml-2 text-amber-400" />
              </h2>
              <p className="text-xs text-gray-500 mt-0.5">Using azure openai agents</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <div className="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full text-xs font-medium flex items-center">
              <span className="mr-1">Confidence:</span>
              <span className="font-bold">{aiData.confidence}</span>
            </div>
      
          </div>
        </div>

        {/* Alert Summary Section */}
        <div className="bg-white/90 backdrop-blur-sm p-4 rounded-lg border border-gray-100 shadow-sm mb-5">
          <div className="flex items-start gap-3">
            <div className="bg-orange-50 p-2 rounded text-orange-500 flex-shrink-0 mt-1">
              <FileText size={16} />
            </div>
            <div>
              <h3 className="text-sm font-semibold text-gray-700 mb-2">Alert Summary</h3>
              <p className="text-gray-700 text-sm leading-relaxed">{aiData.alertSummary}</p>
            </div>
          </div>
        </div>
        
        {/* Content grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="bg-white/80 backdrop-blur-sm p-4 rounded-lg border border-gray-100 shadow-sm hover:shadow transition-all duration-200 hover:border-indigo-200">
            <div className="flex items-center gap-2 mb-3">
              <div className="bg-blue-50 p-1.5 rounded text-blue-500">
                <Globe size={16} />
              </div>
              <h3 className="text-sm font-semibold text-gray-700">Environment</h3>
            </div>
            <p className="text-gray-900 font-medium ml-1">{aiData.environment}</p>
          </div>
          
          <div className="bg-white/80 backdrop-blur-sm p-4 rounded-lg border border-gray-100 shadow-sm hover:shadow transition-all duration-200 hover:border-indigo-200">
            <div className="flex items-center gap-2 mb-3">
              <div className="bg-blue-50 p-1.5 rounded text-blue-500">
                <Server size={16} />
              </div>
              <h3 className="text-sm font-semibold text-gray-700">Cluster</h3>
            </div>
            <p className="text-gray-900 font-medium ml-1">{aiData.cluster}</p>
          </div>
          
          <div className="bg-white/80 backdrop-blur-sm p-4 rounded-lg border border-gray-100 shadow-sm hover:shadow transition-all duration-200 hover:border-indigo-200">
            <div className="flex items-center gap-2 mb-3">
              <div className="bg-blue-50 p-1.5 rounded text-blue-500">
                <Box size={16} />
              </div>
              <h3 className="text-sm font-semibold text-gray-700">Node Name</h3>
            </div>
            <p className="text-gray-900 font-medium ml-1">{aiData.nodeName}</p>
          </div>
          
          <div className="bg-white/80 backdrop-blur-sm p-4 rounded-lg border border-gray-100 shadow-sm hover:shadow transition-all duration-200 hover:border-indigo-200">
            <div className="flex items-center gap-2 mb-3">
              <div className="bg-red-50 p-1.5 rounded text-red-500">
                <AlertTriangle size={16} />
              </div>
              <h3 className="text-sm font-semibold text-gray-700">Error Type</h3>
            </div>
            <div className="flex items-center ml-1">
              <span className="text-gray-900 font-medium">{aiData.errorType}</span>
              <span className="ml-2 bg-red-50 text-red-600 px-2 py-0.5 rounded-full text-xs font-semibold">
                {aiData.errorSeverity}
              </span>
            </div>
          </div>
          
          <div className="bg-white/80 backdrop-blur-sm p-4 rounded-lg border border-gray-100 shadow-sm hover:shadow transition-all duration-200 hover:border-indigo-200">
            <div className="flex items-center gap-2 mb-3">
              <div className="bg-blue-50 p-1.5 rounded text-blue-500">
                <Layers size={16} />
              </div>
              <h3 className="text-sm font-semibold text-gray-700">Impacted Component</h3>
            </div>
            <div className="flex items-center ml-1">
              <span className="text-gray-900 font-medium">{aiData.impactedComponent}</span>
              <span className="flex items-center ml-2 bg-blue-50 text-blue-600 px-2 py-0.5 rounded-full text-xs font-semibold">
                <Code size={10} className="mr-1" />
                {aiData.componentVersion}
              </span>
            </div>
          </div>
          
          <div className="bg-white/80 backdrop-blur-sm p-4 rounded-lg border border-gray-100 shadow-sm hover:shadow transition-all duration-200 hover:border-indigo-200">
            <div className="flex items-center gap-2 mb-3">
              <div className="bg-blue-50 p-1.5 rounded text-blue-500">
                <Clock size={16} />
              </div>
              <h3 className="text-sm font-semibold text-gray-700">First Detected</h3>
            </div>
            <p className="text-gray-900 font-medium ml-1">{aiData.firstDetected}</p>
          </div>
        </div>

      </div>
    </div>
  );
};

export default OverviewPanel;
