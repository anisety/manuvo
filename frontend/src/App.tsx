import React, { useRef, useState, useCallback } from 'react';
import Webcam from 'react-webcam';

const App: React.FC = () => {
  const webcamRef = useRef<Webcam>(null);
  const [recognizedGesture, setRecognizedGesture] = useState<string>('...');
  const [feedback, setFeedback] = useState<string>('Point your hand at the camera');

  const capture = useCallback(async () => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      if (imageSrc) {
        // In a real app, you'd send this to the backend
        // For now, we'll simulate a response
        const mockGesture = ['A', 'B', 'C', 'Hello', 'Thank you'][Math.floor(Math.random() * 5)];
        setRecognizedGesture(mockGesture);
        setFeedback('Good job!');
        
        // Example of how you might send to a backend
        /*
        try {
          const response = await fetch('http://localhost:5000/recognize', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image: imageSrc }),
          });
          const data = await response.json();
          setRecognizedGesture(data.gesture);
          setFeedback(`Confidence: ${data.confidence}`);
        } catch (error) {
          console.error("Error recognizing gesture:", error);
          setFeedback('Could not connect to server');
        }
        */
      }
    }
  }, [webcamRef]);

  // Automatically capture every 2 seconds
  React.useEffect(() => {
    const interval = setInterval(() => {
      capture();
    }, 2000);
    return () => clearInterval(interval);
  }, [capture]);

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <h1 className="text-4xl font-bold mb-4">Manuvo ASL Recognition</h1>
      <div className="w-full max-w-2xl mx-auto bg-white rounded-lg shadow-md overflow-hidden">
        <Webcam
          audio={false}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          className="w-full"
        />
        <div className="p-4">
          <h2 className="text-2xl font-semibold">Real-time Feedback</h2>
          <p className="text-lg mt-2">Recognized Gesture: <span className="font-bold text-blue-600">{recognizedGesture}</span></p>
          <p className="text-md mt-1">Feedback: <span className="italic">{feedback}</span></p>
        </div>
      </div>
    </div>
  );
};

export default App;

