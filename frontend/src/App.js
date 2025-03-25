import React, { useState, useEffect } from 'react';
import './App.css';
import { ApiService } from './services/api';
import AudioRecorder from './components/AudioRecorder';

function App() {
  const [inputText, setInputText] = useState('');
  const [messages, setMessages] = useState([]);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);

  // Check API connection on component mount
  useEffect(() => {
    const checkConnection = async () => {
      try {
        await ApiService.healthCheck();
        setIsConnected(true);
      } catch (error) {
        console.error('API connection failed:', error);
        setIsConnected(false);
      }
    };
    
    checkConnection();
  }, []);

  // Function to send text input to the API
  const sendMessage = async () => {
    if (!inputText.trim()) return;

    const userMessage = { role: 'user', content: inputText };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInputText('');

    try {
      let screenContext = null;
      try {
        const screenResponse = await ApiService.captureScreen();
        if (screenResponse.success) {
          screenContext = 'Screen data available';
        }
      } catch (error) {
        console.error('Error capturing screen:', error);
      }
      
      setIsSpeaking(true);
      const response = await ApiService.sendMessage(updatedMessages, screenContext);

      if (response.success) {
        const assistantMessage = { role: 'assistant', content: response.response };
        setMessages([...updatedMessages, assistantMessage]);
        
        if (!isMuted) {
          speakText(response.response);
        }
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages([
        ...updatedMessages,
        { role: 'assistant', content: 'Sorry, I encountered an error processing your request.' }
      ]);
    } finally {
      setIsSpeaking(false);
    }
  };

  // Function to handle audio captured from the recorder
  const handleAudioCaptured = async (audioBlob) => {
    setIsProcessing(true);
    try {
      const response = await ApiService.processAudio(audioBlob);
      if (response.success) {
        setMessages([...messages, { role: 'user', content: response.text }]);
      } else {
        console.error(response.error);
      }
    } catch (error) {
      console.error('Error processing audio:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  // Function for text-to-speech
  const speakText = (text) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      window.speechSynthesis.speak(utterance);
    }
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage();
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Kyle Assistant</h1>
        <div className="status-indicators">
          {!isConnected && <div className="status error">API Disconnected</div>}
          <span className={`status ${isListening ? 'listening' : ''}`}>Listening</span>
          <span className={`status ${isProcessing ? 'processing' : ''}`}>Processing</span>
          {isSpeaking && <div className="status speaking">Speaking...</div>}
        </div>
      </header>

      <div className="conversation-container">
        {messages.length === 0 ? (
          <div className="empty-state">
            <p>Hello! I'm Kyle, your AI assistant. How can I help you today?</p>
          </div>
        ) : (
          messages.map((message, index) => (
            <div key={index} className={`message ${message.role}`}>
              <div className="message-content">{message.content}</div>
            </div>
          ))
        )}
      </div>

      <div className="controls-container">
        <AudioRecorder 
          onAudioCaptured={handleAudioCaptured}
          isListening={isListening}
          setIsListening={setIsListening}
        />
        
        <button 
          className={`mute-button ${isMuted ? 'muted' : ''}`}
          onClick={() => setIsMuted(!isMuted)}
        >
          {isMuted ? 'Unmute' : 'Mute'}
        </button>
      </div>

      <form className="input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Type your message here..."
          disabled={isListening}
        />
        <button type="submit" disabled={!inputText.trim() || isListening}>Send</button>
      </form>
    </div>
  );
}

export default App; 