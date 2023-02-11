import sys
import cv2
from PyQt5 import Qt, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QFont
import os

class Converter():
    def convert(self, file_path, fps, output_dir):
        if file_path:
            # Open the video file
            video = cv2.VideoCapture(file_path)
            self.progress_bar.setValue(0)
            
            # Get the number of frames in the video
            frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Set the frame rate
            frame_rate = fps
            
            # Calculate the time between frames
            time_between_frames = int(round(1000/frame_rate, 3))
                        
            # Set the starting frame
            frame_idx = 0
            counter = 0
            
            # Start the while loop to process each frame
            while frame_idx < frame_count:
                
                # Get the current frame
                ret, frame = video.read()

                # Break the loop if there are no more frames
                if not ret:
                    break

                # Only process the frame if it's one of the desired frames
                if frame_idx % fps == 0:
                    # Save the current frame as an image
                    cv2.imwrite(os.path.join(output_dir, '{0:04d}.jpg'.format(counter)), frame)
                    counter += 1
                    
                # Increment the frame index
                frame_idx += 1

                self.progress_bar.setValue((int((frame_idx / frame_count) * 100)))

                # Wait for the specified amount of time before processing the next frame
                if cv2.waitKey(time_between_frames) & 0xFF == ord('q'):
                    break
            
            # Release the video
            video.release()
            self.progress_bar.setValue(100)
        else:
            print("Error: No file selected.")