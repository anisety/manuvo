import React, { useRef, useState, useCallback } from 'react';
import Webcam from 'react-webcam';

const App: React.FC = () => {
  const webcamRef = useRef<Webcam>(null);
  const [recognizedGesture, setRecognizedGesture] = useState<string>('...');
  const [feedback, setFeedback] = useState<string>('Point your hand at the camera');
  const [isProcessing, setIsProcessing] = useState<boolean>(false);

  const captureAndRecognize = useCallback(async () => {
    if (webcamRef.current && !isProcessing) {
      const imageSrc = webcamRef.current.getScreenshot();
      if (imageSrc) {
        setIsProcessing(true);
        try {
          const response = await fetch('http://localhost:5000/recognize', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image: imageSrc }),
          });

          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }

          const data = await response.json();
          setRecognizedGesture(data.gesture);
          setFeedback(`Confidence: ${data.confidence}`);
        } catch (error) {
          console.error("Error recognizing gesture:", error);
          setFeedback('Could not connect to server');
        } finally {
          setIsProcessing(false);
        }
      }
    }
  }, [webcamRef, isProcessing]);

  // Automatically capture every 500ms
  React.useEffect(() => {
    const interval = setInterval(() => {
      captureAndRecognize();
    }, 500);
    return () => clearInterval(interval);
  }, [captureAndRecognize]);

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <h1 className="text-4xl font-bold mb-4 text-gray-800">Manuvo - Real-Time ASL Recognition</h1>
      <div className="w-full max-w-2xl mx-auto bg-white rounded-lg shadow-xl overflow-hidden">
        <Webcam
          audio={false}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          className="w-full"
          videoConstraints={{
            width: 1280,
            height: 720,
            facingMode: "user"
          }}
        />
        <div className="p-6 bg-gray-50">
          <h2 className="text-2xl font-semibold text-gray-700">Real-time Feedback</h2>
          <p className="text-xl mt-2">
            Recognized Gesture: 
            <span className="font-bold text-blue-600 ml-2">{recognizedGesture}</span>
          </p>
          <p className="text-md mt-1 text-gray-600">
            Feedback: 
            <span className="italic ml-2">{feedback}</span>
          </p>
        </div>
      </div>
      <footer className="mt-6 text-center text-gray-500">
        <p>Powered by Mediapipe & React</p>
      </footer>
    </div>
  );
};

export default App;

