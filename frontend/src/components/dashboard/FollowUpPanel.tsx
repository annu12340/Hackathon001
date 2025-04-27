import React from 'react';
import { CheckSquare, Circle, Calendar } from 'lucide-react';
import { followUpTasks } from '@/utils/dashboardData';

const FollowUpPanel = () => {
  const [tasks, setTasks] = React.useState(followUpTasks);
  
  const toggleTaskCompletion = (taskId: number) => {
    setTasks(tasks.map(task => 
      task.id === taskId 
        ? { ...task, completed: !task.completed } 
        : task
    ));
  };
  
  return (
    <div className="animate-in fade-in duration-500">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold text-gray-800">Follow-up Tasks</h1>
        <button className="px-4 py-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 transition-colors flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
          </svg>
          Add Task
        </button>
      </div>
      
      <div className="bg-white rounded-2xl shadow-md overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th scope="col" className="pl-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-8">
                Status
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Task
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Due Date
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Assignee
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Priority
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {tasks.map(task => (
              <tr key={task.id} className={task.completed ? 'bg-gray-50' : ''}>
                <td className="pl-6 py-4 whitespace-nowrap">
                  <button onClick={() => toggleTaskCompletion(task.id)}>
                    {task.completed ? (
                      <CheckSquare className="w-5 h-5 text-green-500" />
                    ) : (
                      <Circle className="w-5 h-5 text-gray-300" />
                    )}
                  </button>
                </td>
                <td className="px-6 py-4">
                  <div className={`text-sm ${task.completed ? 'text-gray-500 line-through' : 'text-gray-900'}`}>
                    {task.title}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center text-sm text-gray-500">
                    <Calendar className="w-4 h-4 mr-1 text-gray-400" />
                    {task.dueDate}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {task.assignee}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                    ${task.priority === 'high' 
                      ? 'bg-red-100 text-red-800' 
                      : task.priority === 'medium'
                        ? 'bg-yellow-100 text-yellow-800'
                        : 'bg-green-100 text-green-800'
                    }`}>
                    {task.priority}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
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
