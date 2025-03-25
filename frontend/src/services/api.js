import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// Create axios instance with base URL
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API service functions
export const ApiService = {
  // Send text to get a response
  sendMessage: async (messages, screenContext = null, audioContext = null) => {
    try {
      const response = await apiClient.post('/respond', {
        messages,
        screen_context: screenContext,
        audio_context: audioContext,
      });
      return response.data;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  },

  // Capture screen
  captureScreen: async () => {
    try {
      const response = await apiClient.post('/screen');
      return response.data;
    } catch (error) {
      console.error('Error capturing screen:', error);
      throw error;
    }
  },

  // Process audio
  processAudio: async (audioBlob) => {
    try {
      const formData = new FormData();
      formData.append('audio_file', audioBlob, 'recording.wav');
      
      const response = await apiClient.post('/listen', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      console.error('Error processing audio:', error);
      throw error;
    }
  },

  // Health check
  healthCheck: async () => {
    try {
      const response = await apiClient.get('/health');
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  },
}; 