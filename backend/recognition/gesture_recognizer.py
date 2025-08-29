import mediapipe as mp
import cv2
import math

class GestureRecognizer:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            min_detection_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils

    def recognize(self, image):
        """
        Recognizes a gesture from a given image.
        :param image: The image to process (numpy array).
        :return: A tuple containing the gesture name and the annotated image.
        """
        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = self.hands.process(image)
        image.flags.writeable = True

        # Draw the hand annotations on the image.
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        gesture = "No hand detected"

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
                # Get landmarks
                landmarks = hand_landmarks.landmark
                
                # Simple gesture classification logic
                gesture = self._classify_gesture(landmarks)

        return gesture, image

    def _classify_gesture(self, landmarks):
        """
        Classifies a gesture based on hand landmarks.
        This is a simplified example. A real application would use a more robust model.
        """
        # Landmark indices for fingertips
        index_tip = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring_tip = landmarks[self.mp_hands.HandLandmark.RING_FINGER_TIP]
        pinky_tip = landmarks[self.mp_hands.HandLandmark.PINKY_TIP]

        # Landmark indices for finger bases (MCP joints)
        index_mcp = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]
        middle_mcp = landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
        ring_mcp = landmarks[self.mp_hands.HandLandmark.RING_FINGER_MCP]
        pinky_mcp = landmarks[self.mp_hands.HandLandmark.PINKY_FINGER_MCP]

        # Helper to check if a finger is extended
        def is_finger_extended(tip, mcp):
            return tip.y < mcp.y

        # Check for specific gestures
        index_extended = is_finger_extended(index_tip, index_mcp)
        middle_extended = is_finger_extended(middle_tip, middle_mcp)
        ring_extended = is_finger_extended(ring_tip, ring_mcp)
        pinky_extended = is_finger_extended(pinky_tip, pinky_mcp)

        if index_extended and middle_extended and ring_extended and pinky_extended:
            return "Open Palm"
        elif not index_extended and not middle_extended and not ring_extended and not pinky_extended:
            return "Fist"
        elif index_extended and middle_extended and not ring_extended and not pinky_extended:
            return "Victory"
        elif not index_extended and middle_extended and ring_extended and pinky_extended:
             return "Rock"
        elif index_extended and not middle_extended and not ring_extended and not pinky_extended:
             return "Pointing"

        return "Gesture not recognized"

    def __del__(self):
        self.hands.close()
