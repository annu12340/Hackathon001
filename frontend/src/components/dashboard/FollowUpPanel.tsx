import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { PlusCircle, Check, CalendarDays, AlertCircle, ClipboardList, Filter, Search, Users, MoreHorizontal, Clock, ArrowUpRight, BellRing } from 'lucide-react';
import { Task } from '@/utils/dashboardTypes';

interface FollowUpPanelProps {
  data: Task[];
}

const FollowUpPanel: React.FC<FollowUpPanelProps> = ({ data }) => {
  const [tasks, setTasks] = useState<Task[]>(data);
  const [filterActive, setFilterActive] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const toggleTaskCompletion = (taskId: number) => {
    setTasks(
      tasks.map((task) => {
        if (task.id === taskId) {
          return { ...task, completed: !task.completed };
        }
        return task;
      })
    );
  };

  // Calculate summary statistics
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(t => t.completed).length;
  const highPriorityTasks = tasks.filter(t => t.priority === 'high' && !t.completed).length;
  const progressPercentage = Math.round((completedTasks / totalTasks) * 100) || 0;

  return (
    <div className="animate-in fade-in duration-700 space-y-8">
      <div className="flex justify-between items-center">
        <div className="flex items-center gap-2">
          <ClipboardList size={24} className="text-indigo-500" />
          <h1 className="text-2xl font-bold text-gray-900 tracking-tight">Follow-up Tasks</h1>
        </div>
        
        <div className="flex items-center gap-3">
          <button 
            onClick={() => setFilterActive(!filterActive)}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium transition-colors border ${filterActive 
              ? 'bg-indigo-100 text-indigo-700 border-indigo-200' 
              : 'bg-white text-gray-600 border-gray-200'}`}
          >
            <Filter size={14} className={filterActive ? 'text-indigo-500' : 'text-gray-400'} />
            Filter
          </button>
          
          <div className="relative group">
            <input
              type="text"
              placeholder="Search tasks..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-9 pr-4 py-2 bg-white/90 backdrop-blur-sm border border-gray-200 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent w-64 shadow-sm hover:shadow transition-all duration-200"
            />
            <Search size={16} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 group-hover:text-indigo-500 transition-colors duration-200" />
          </div>
          

        </div>
      </div>
      
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {[
          {
            title: "Total Tasks",
            value: totalTasks,
            icon: <ClipboardList size={18} />,
            color: "gray"
          },
          {
            title: "High Priority",
            value: highPriorityTasks,
            icon: <BellRing size={18} />,
            color: "red" 
          },
          {
            title: "Completed",
            value: completedTasks,
            icon: <Check size={18} />,
            color: "green"
          },
  
        ].map((stat, index) => (
          <Card key={index} className={`border-${stat.color}-100 bg-gradient-to-r from-${stat.color}-50 to-white shadow-sm hover:shadow transition-all duration-200`}>
            <CardContent className="p-4 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className={`p-2.5 rounded-lg bg-${stat.color}-100 text-${stat.color}-600`}>
                  {stat.icon}
                </div>
                <div>
                  <p className="text-xs text-gray-500 mb-1">{stat.title}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                </div>
              </div>
              
              {stat.title === "Completed" && (
                <div className="flex flex-col items-end gap-1">
                  <span className="text-xs font-medium text-green-600">{progressPercentage}%</span>
                  <div className="w-16 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-green-500 rounded-full" 
                      style={{ width: `${progressPercentage}%` }}
                    />
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
      
      {/* Tasks List */}
      <Card className="border-gray-100 shadow-sm overflow-hidden hover:shadow transition-all duration-200">
        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-indigo-500 via-blue-500 to-indigo-400"></div>
        
        <CardHeader className="bg-gradient-to-r from-gray-50 to-white pb-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <ClipboardList size={18} className="text-indigo-500" />
              <CardTitle className="text-lg font-bold text-gray-900">Active Tasks</CardTitle>
            </div>
            
      
          </div>
        </CardHeader>
        
        <CardContent className="p-0">
          <div className="space-y-px">
            {tasks.map((task) => (
              <div
                key={task.id}
                className={`p-4 flex items-start gap-4 hover:bg-gray-50 transition-colors border-b border-gray-100 last:border-b-0 ${
                  task.completed ? 'bg-gray-50/50' : ''
                }`}
              >
                <button
                  onClick={() => toggleTaskCompletion(task.id)}
                  className={`flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                    task.completed
                      ? 'bg-green-500 border-green-500 text-white'
                      : 'border-gray-300 hover:border-indigo-400'
                  }`}
                >
                  {task.completed && <Check size={14} />}
                </button>
                
                <div className="flex-grow min-w-0">
                  <div className="flex justify-between items-center mb-1">
                    <h3
                      className={`font-medium ${
                        task.completed ? 'text-gray-400 line-through' : 'text-gray-900'
                      }`}
                    >
                      {task.title}
                    </h3>
                    <div className="flex items-center gap-2">
                      <div
                        className={`text-xs font-medium rounded-full px-2 py-0.5 ${
                          task.priority === 'high'
                            ? 'bg-red-50 text-red-700'
                            : task.priority === 'medium'
                            ? 'bg-amber-50 text-amber-700'
                            : 'bg-blue-50 text-blue-700'
                        }`}
                      >
                        {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
                      </div>
                      <button className="text-gray-400 hover:text-gray-600">
                        <MoreHorizontal size={16} />
                      </button>
                    </div>
                  </div>
                  
                  <div className="flex flex-wrap gap-4 mt-1 text-xs text-gray-500">
                    <div className="flex items-center gap-1">
                   
                      <span> {task.description}</span>
                    </div>

                  </div>
                </div>
              </div>
            ))}
          </div>
          
          {tasks.length === 0 && (
            <div className="py-12 flex flex-col items-center justify-center text-center">
              <div className="p-3 bg-gray-100 rounded-full mb-3">
                <ClipboardList size={24} className="text-gray-400" />
              </div>
              <h3 className="text-gray-600 font-medium mb-1">No tasks found</h3>
              <p className="text-gray-500 text-sm mb-4">Create your first task to get started</p>
              <button className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg shadow-sm transition-colors">
                <PlusCircle size={16} />
                <span className="text-sm font-medium">Add Task</span>
              </button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default FollowUpPanel;
