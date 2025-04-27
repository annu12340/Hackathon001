
import React from 'react';
import { Gauge, ScrollText, Search, Wrench, CheckSquare } from 'lucide-react';
import { cn } from '@/lib/utils';

type NavItem = {
  icon: React.ElementType;
  label: string;
  id: string;
};

type SectionHeader = {
  section: string;
  id: string;
};

type SidebarItem = NavItem | SectionHeader;

const isSectionHeader = (item: SidebarItem): item is SectionHeader => {
  return 'section' in item;
};

const navItems: NavItem[] = [
  { icon: Gauge, label: 'Overview', id: 'overview' },
  { icon: ScrollText, label: 'Logs', id: 'logs' },
  { icon: Search, label: 'Root Cause', id: 'rootCause' },
  { icon: Wrench, label: 'Remediation', id: 'remediation' },
  { icon: CheckSquare, label: 'Follow-up', id: 'followUp' },
];

const itemsWithSections: SidebarItem[] = [
  { section: 'Platform', id: 'section-1' },
  ...navItems
];

interface SidebarProps {
  activePage: string;
  setActivePage: (page: string) => void;
}

const Sidebar = ({ activePage, setActivePage }: SidebarProps) => {
  return (
    <div className="h-screen w-64 bg-white border-r border-gray-100 p-4 flex flex-col">
      <div className="flex items-center gap-3 mb-8 pl-4">
        <div className="h-8 w-8 bg-black rounded-lg flex items-center justify-center">
          <span className="text-white font-semibold">N</span>
        </div>
        <h1 className="text-lg font-medium text-gray-800">Node Triage</h1>
      </div>

      <nav className="flex-1 space-y-1">
        {itemsWithSections.map((item) => {
          if (isSectionHeader(item)) {
            return (
              <div key={item.id} className="text-xs text-gray-500 font-medium px-4 pt-6 pb-2">
                {item.section}
              </div>
            );
          }
          
          return (
            <button
              key={item.id}
              onClick={() => setActivePage(item.id)}
              className={cn(
                'w-full flex items-center gap-3 px-4 py-2 rounded-lg text-sm transition-colors',
                'hover:bg-gray-50',
                activePage === item.id 
                  ? 'bg-blue-50 text-blue-600 font-medium' 
                  : 'text-gray-600'
              )}
            >
              <item.icon className="w-4 h-4" />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      <div className="mt-auto pb-4">
        <div className="p-4 bg-gray-50 rounded-xl">
          <p className="text-sm text-gray-600">
            some random text
          </p>
          <button className="text-sm text-blue-600 font-medium mt-1 hover:text-blue-700">
            View docs →
          </button>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
