import React, { useState, useEffect } from 'react';

const AudioRecorder = ({ onAudioCaptured, isListening, setIsListening }) => {
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [audioChunks, setAudioChunks] = useState([]);

  useEffect(() => {
    // Initialize media recorder when component mounts
    const initMediaRecorder = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const recorder = new MediaRecorder(stream);
        
        recorder.ondataavailable = (e) => {
          if (e.data.size > 0) {
            setAudioChunks((chunks) => [...chunks, e.data]);
          }
        };
        
        recorder.onstop = () => {
          const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
          onAudioCaptured(audioBlob);
          setAudioChunks([]);
        };
        
        setMediaRecorder(recorder);
      } catch (error) {
        console.error('Error accessing microphone:', error);
        alert('Could not access microphone. Please check permissions.');
      }
    };
    
    initMediaRecorder();
    
    // Cleanup function
    return () => {
      if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
      }
    };
  }, [onAudioCaptured]);

  useEffect(() => {
    if (!mediaRecorder) return;
    
    if (isListening) {
      mediaRecorder.start();
    } else if (mediaRecorder.state !== 'inactive') {
      mediaRecorder.stop();
    }
  }, [isListening, mediaRecorder]);

  return (
    <button 
      className={`voice-button ${isListening ? 'active' : ''}`} 
      onClick={() => setIsListening(!isListening)}
      disabled={!mediaRecorder}
    >
      {isListening ? 'Stop Listening' : 'Start Listening'}
    </button>
  );
};

export default AudioRecorder; 