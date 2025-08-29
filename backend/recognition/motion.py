import cv2
import numpy as np

class MotionDetector:
    def __init__(self, bg_sub_history=100, bg_sub_threshold=50):
        """
        Initializes the motion detector.
        :param bg_sub_history: History for the background subtractor.
        :param bg_sub_threshold: Threshold for the background subtractor.
        """
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=bg_sub_history, varThreshold=bg_sub_threshold, detectShadows=True
        )

    def detect_motion(self, frame):
        """
        Detects motion in a given frame.
        :param frame: The video frame to process.
        :return: A tuple containing the motion mask and a list of contours.
        """
        # Apply the background subtractor to get the foreground mask
        fg_mask = self.bg_subtractor.apply(frame)

        # Clean up the mask to reduce noise
        # Apply a threshold to remove shadows and noise
        _, fg_mask = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)
        
        # Use morphological transformations to fill holes and remove small objects
        kernel = np.ones((3, 3), np.uint8)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel, iterations=2)

        # Find contours of moving objects
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        return fg_mask, contours

    def draw_motion_rectangles(self, frame, contours, min_area=500):
        """
        Draws bounding rectangles around detected motion areas.
        :param frame: The original frame to draw on.
        :param contours: The list of contours to draw.
        :param min_area: The minimum contour area to consider as motion.
        """
        for contour in contours:
            # Ignore small contours that are likely noise
            if cv2.contourArea(contour) < min_area:
                continue

            # Get the bounding box for the contour and draw it on the frame
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        return frame

if __name__ == '__main__':
    # Example usage with a webcam feed
    cap = cv2.VideoCapture(0)
    detector = MotionDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally for a more intuitive selfie-view
        frame = cv2.flip(frame, 1)

        # Detect motion
        mask, contours = detector.detect_motion(frame)

        # Draw rectangles around motion
        motion_frame = detector.draw_motion_rectangles(frame.copy(), contours)

        # Display the results
        cv2.imshow('Original Frame', frame)
        cv2.imshow('Motion Mask', mask)
        cv2.imshow('Motion Detected', motion_frame)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
