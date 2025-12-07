import React, { useState, useEffect } from 'react';
import './ChatbotWidget.css'; // Optional CSS file

function ChatbotWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Backend API base URL - using window object for Docusaurus compatibility
  const API_BASE_URL = typeof window !== 'undefined'
    ? (window.ENV?.REACT_APP_API_BASE_URL || 'http://localhost:8000')  // Backend running on port 8000
    : 'http://localhost:8000';  // Backend running on port 8000

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const sendMessage = async () => {
    if (input.trim() === '' || isLoading) return;

    const userMessage = { text: input, sender: 'user' };
    setMessages(prevMessages => [...prevMessages, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: input,
          context: '' // Context can be provided if available (e.g., from highlighted text)
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const botResponse = { text: data.response, sender: 'bot' };
        setMessages(prevMessages => [...prevMessages, botResponse]);
      } else {
        const errorData = await response.json();
        const botResponse = { text: `Error: ${errorData.detail || 'Failed to get response'}`, sender: 'bot' };
        setMessages(prevMessages => [...prevMessages, botResponse]);
      }
    } catch (error) {
      const botResponse = { text: `Error: ${error.message}`, sender: 'bot' };
      setMessages(prevMessages => [...prevMessages, botResponse]);
    } finally {
      setIsLoading(false);
    }
  };

  // Function to handle sending a message when Enter key is pressed
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chatbot-widget">
      {!isOpen ? (
        <button onClick={toggleChat} className="chatbot-toggle">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H16.41L16.42 17.08C16.7 17.7 16.86 18.36 16.89 19.04L16.9 19.5C16.9 19.78 16.68 20 16.4 20H16.06C15.58 20 15.13 19.8 14.8 19.47L14.68 19.35L14.63 19.3C14.28 18.95 13.84 18.74 13.37 18.7L13 18.67L10 15.67C9.23 14.9 8.78 13.86 8.78 12.76V11C8.78 9.9 9.23 8.86 10 8.09L13 5.09C13.77 4.32 14.81 3.87 15.91 3.87H19C19.5304 3.87 20.0391 4.08075 20.4142 4.45584C20.7893 4.83093 21 5.3396 21 5.87V15Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M9 12H15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M9 8H11" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M9 16H11" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          <span>AI Assistant</span>
        </button>
      ) : (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <div className="chatbot-title">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H16.41L16.42 17.08C16.7 17.7 16.86 18.36 16.89 19.04L16.9 19.5C16.9 19.78 16.68 20 16.4 20H16.06C15.58 20 15.13 19.8 14.8 19.47L14.68 19.35L14.63 19.3C14.28 18.95 13.84 18.74 13.37 18.7L13 18.67L10 15.67C9.23 14.9 8.78 13.86 8.78 12.76V11C8.78 9.9 9.23 8.86 10 8.09L13 5.09C13.77 4.32 14.81 3.87 15.91 3.87H19C19.5304 3.87 20.0391 4.08075 20.4142 4.45584C20.7893 4.83093 21 5.3396 21 5.87V15Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M9 12H15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M9 8H11" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M9 16H11" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              <span>AI Book Assistant</span>
            </div>
            <button onClick={toggleChat} className="chatbot-close">✕</button>
          </div>

          <div className="chatbot-messages">
            {messages.length === 0 ? (
              <div className="chatbot-welcome">
                <div className="welcome-icon">
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H16.41L16.42 17.08C16.7 17.7 16.86 18.36 16.89 19.04L16.9 19.5C16.9 19.78 16.68 20 16.4 20H16.06C15.58 20 15.13 19.8 14.8 19.47L14.68 19.35L14.63 19.3C14.28 18.95 13.84 18.74 13.37 18.7L13 18.67L10 15.67C9.23 14.9 8.78 13.86 8.78 12.76V11C8.78 9.9 9.23 8.86 10 8.09L13 5.09C13.77 4.32 14.81 3.87 15.91 3.87H19C19.5304 3.87 20.0391 4.08075 20.4142 4.45584C20.7893 4.83093 21 5.3396 21 5.87V15Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M9 12H15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M9 8H11" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M9 16H11" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </div>
                <h3>Hello! I'm your AI Assistant</h3>
                <p>Ask me questions about AI, robotics, and related topics from the book.</p>
                <p>You can also paste text for summarization or ask for explanations.</p>
              </div>
            ) : (
              messages.map((msg, index) => (
                <div key={index} className={`message ${msg.sender}`}>
                  <div className="message-content">{msg.text}</div>
                </div>
              ))
            )}
            {isLoading && (
              <div className="message bot">
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="chatbot-input">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask a question or paste text to summarize..."
              disabled={isLoading}
            />
            <button onClick={sendMessage} disabled={isLoading || input.trim() === ''}>
              {isLoading ? (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 2V6M12 18V22M6 12H2M22 12H18M19.0784 19.0784L16.25 16.25M19.0784 4.99994L16.25 7.82837M4.92157 19.0784L7.74999 16.25M4.92157 4.99994L7.74999 7.82837" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              ) : (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M22 2L11 13M22 2L15 22L11 13M11 13L2 9L22 2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              )}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default ChatbotWidget;