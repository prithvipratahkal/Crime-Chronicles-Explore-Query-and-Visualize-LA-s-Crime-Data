import React, { useState } from 'react';
import '../styles/ChatHistory.css';


function ChatHistory() {
    const [messages, setMessages] = useState([
        { sender: 'user', text: "What's the crime rate in LA this week?" },
        { sender: 'chatbot', text: "The crime rate in LA has decreased by 10% this week." },
        { sender: 'user', text: "Can you provide a report on the traffic accidents?" },
        { sender: 'chatbot', text: "Yes, traffic accidents have been increasing in downtown LA over the last month." },
    // More messages can be added dynamically here
      ]);

  return (
    <div className="chat-history">
      <h2>Chat History</h2>
      <div className="chat-history-items">
        {messages.map((message, index) => (
            <div
                key={index}
                className={`message ${message.sender}`}
            >
                <div className="message-content">
                    {message.text}
                </div>
            </div>
            ))}
      </div>
    </div>
  );
}

export default ChatHistory;
