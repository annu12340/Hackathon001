import React, { useState } from 'react';
import { X, Send } from 'lucide-react';
import axios from 'axios';

interface ChatDrawerProps {
  isOpen: boolean;
  onClose: () => void;
}

interface Message {
  text: string;
  isUser: boolean;
}

const ChatDrawer = ({ isOpen, onClose }: ChatDrawerProps) => {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    { text: 'Hi there! How can I help you with your Node.js application today?', isUser: false },
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!message.trim()) return;
    
    // Add user message
    setMessages(prev => [...prev, { text: message, isUser: true }]);
    setMessage('');
    setIsLoading(true);
    
    try {
      // Make API call to backend
      const response = await axios.post('/api/chat/query', {
        message: message
      });

      // Add response to messages
      setMessages(prev => [
        ...prev, 
        { 
          text: response.data.data || "I've processed your query. How else can I help?", 
          isUser: false 
        }
      ]);
    } catch (error) {
      // Add error message
      setMessages(prev => [
        ...prev, 
        { 
          text: "Sorry, I encountered an error processing your query. Please try again.", 
          isUser: false 
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={`fixed inset-y-0 right-0 w-80 sm:w-96 bg-white shadow-2xl transform transition-all duration-300 ease-in-out z-50 flex flex-col ${isOpen ? 'translate-x-0' : 'translate-x-full'}`}>
      {/* Header */}
      <div className="p-4 border-b border-gray-200 flex justify-between items-center bg-blue-500 text-white">
        <h2 className="font-semibold">Support Chat</h2>
        <button onClick={onClose} className="p-1 rounded-full hover:bg-blue-600">
          <X size={18} />
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 p-4 overflow-y-auto space-y-4">
        {messages.map((msg, idx) => (
          <div 
            key={idx} 
            className={`flex ${msg.isUser ? 'justify-end' : 'justify-start'}`}
          >
            <div 
              className={`p-3 rounded-xl max-w-[80%] ${
                msg.isUser 
                  ? 'bg-blue-500 text-white rounded-br-none' 
                  : 'bg-gray-100 text-gray-800 rounded-bl-none'
              }`}
            >
              {msg.text}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="p-3 rounded-xl bg-gray-100 text-gray-800 rounded-bl-none">
              Processing...
            </div>
          </div>
        )}
      </div>

      {/* Input */}
      <div className="p-4 border-t border-gray-200">
        <div className="flex items-center gap-2">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Type your message..."
            className="flex-1 p-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={isLoading}
          />
          <button 
            onClick={handleSend} 
            disabled={!message.trim() || isLoading}
            className="p-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            <Send size={18} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatDrawer;
