import React, { useState } from 'react';
import { PlusCircle, Check, CalendarDays, AlertCircle } from 'lucide-react';
import { Task } from '@/utils/dashboardTypes';

interface FollowUpPanelProps {
  data: Task[];
}

const FollowUpPanel: React.FC<FollowUpPanelProps> = ({ data }) => {
  const [tasks, setTasks] = useState<Task[]>(data);

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

  return (
    <div className="animate-in fade-in duration-500">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-semibold text-gray-900">Follow-up Tasks</h1>
        <button className="bg-black text-white flex items-center gap-2 px-4 py-2 rounded-lg hover:bg-gray-800 transition-colors">
          <PlusCircle size={16} />
          <span>Add Task</span>
        </button>
      </div>

      <div className="space-y-4">
        {tasks.map((task) => (
          <div
            key={task.id}
            className="bg-white p-4 rounded-xl border border-gray-100 shadow-sm flex items-start gap-4 hover:shadow-md transition-shadow"
          >
            <button
              onClick={() => toggleTaskCompletion(task.id)}
              className={`flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                task.completed
                  ? 'bg-green-500 border-green-500 text-white'
                  : 'border-gray-300'
              }`}
            >
              {task.completed && <Check size={14} />}
            </button>
            <div className="flex-grow">
              <div className="flex justify-between">
                <h3
                  className={`font-medium ${
                    task.completed ? 'text-gray-400 line-through' : 'text-gray-900'
                  }`}
                >
                  {task.title}
                </h3>
                <div
                  className={`text-xs font-medium rounded-full px-2 py-1 ${
                    task.priority === 'high'
                      ? 'bg-red-50 text-red-700'
                      : task.priority === 'medium'
                      ? 'bg-yellow-50 text-yellow-700'
                      : 'bg-blue-50 text-blue-700'
                  }`}
                >
                  {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
                </div>
              </div>
              <div className="flex gap-4 mt-2 text-sm text-gray-500">
                <div className="flex items-center gap-1">
                  <CalendarDays size={14} />
                  <span>Due: {task.dueDate}</span>
                </div>
                <div className="flex items-center gap-1">
                  <AlertCircle size={14} />
                  <span>Assignee: {task.assignee}</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-8 bg-white p-6 rounded-2xl shadow-md">
        <h2 className="text-lg font-medium mb-4 text-gray-700">Task Summary</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-gray-50 p-4 rounded-xl border border-gray-100 flex flex-col items-center">
            <div className="text-2xl font-semibold text-gray-900">{tasks.length}</div>
            <div className="text-sm text-gray-500">Total Tasks</div>
          </div>
          <div className="bg-red-50 p-4 rounded-xl border border-red-100 flex flex-col items-center">
            <div className="text-2xl font-semibold text-red-600">
              {tasks.filter(t => t.priority === 'high' && !t.completed).length}
            </div>
            <div className="text-sm text-red-500">High Priority</div>
          </div>
          <div className="bg-green-50 p-4 rounded-xl border border-green-100 flex flex-col items-center">
            <div className="text-2xl font-semibold text-green-600">
              {tasks.filter(t => t.completed).length}
            </div>
            <div className="text-sm text-green-500">Completed</div>
          </div>
          <div className="bg-blue-50 p-4 rounded-xl border border-blue-100 flex flex-col items-center">
            <div className="text-2xl font-semibold text-blue-600">
              {tasks.filter(t => t.assignee === 'You' && !t.completed).length}
            </div>
            <div className="text-sm text-blue-500">Assigned to You</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FollowUpPanel;
