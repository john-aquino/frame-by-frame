# ui.py
from PyQt5 import Qt, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QLineEdit, QMessageBox
from PyQt5.QtGui import QFont
import os
import cv2
from converter import Converter

class Ui_MainWindow(object):
    def setupUi(self, main_window):
        self.converter = Converter
        self.file_path = None
        self.output_folder = None
        self.main_window = main_window
        self.setWindowIcon(QtGui.QIcon('./assets/logo.png'))
        main_window.setWindowTitle("Frame by Frame")
        main_window.setObjectName("main_window")
        main_window.resize(500, 500)
        
        window_width = main_window.frameGeometry().width()
        window_height = main_window.frameGeometry().height()
        
        central_widget = QtWidgets.QWidget(main_window)
        self.central_widget = central_widget
        main_window.setCentralWidget(central_widget)

        vbox = QVBoxLayout(central_widget)
        self.vbox = vbox
        vbox.setAlignment(QtCore.Qt.AlignCenter)

        # Create logo label
        logo = QtWidgets.QLabel(central_widget)
        logo_pixmap = QtGui.QPixmap('./assets/logo.png')

        if logo_pixmap.isNull():
            print("Error: failed to load image")
        else:
            logo_pixmap = logo_pixmap.scaled(100, 100, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            logo.setPixmap(logo_pixmap)
            logo.setAlignment(QtCore.Qt.AlignCenter)

        # Create Header
        header = QLabel("Frame by Frame", central_widget)
        header.setFont(QFont("Helvetica", 20, QFont.Bold))
        header.setStyleSheet("color: #333;")
        header.setAlignment(QtCore.Qt.AlignCenter)
        vbox.addWidget(logo)
        vbox.addWidget(header)
        
        # FPS Input
        hbox_fps = QHBoxLayout(central_widget)
        hbox_fps.setAlignment(QtCore.Qt.AlignCenter)
        fps_label = QLabel("Enter FPS:", central_widget)
        fps_textbox = QtWidgets.QLineEdit(central_widget)
        self.fps_textbox = fps_textbox
        fps_textbox.setMaximumWidth(50)
        fps_label.setMaximumWidth(50)
        hbox_fps.addWidget(fps_label)
        hbox_fps.addWidget(fps_textbox)
        vbox.addLayout(hbox_fps)
        
        # Create a push button for selecting the output folder
        self.select_output_folder_button = QtWidgets.QPushButton()
        self.select_output_folder_button.setText("Select output folder")
        self.select_output_folder_button.clicked.connect(self.select_output_folder)
        output_button_hbox = QHBoxLayout(central_widget)
        output_button_hbox.setAlignment(QtCore.Qt.AlignCenter)
        output_button_hbox.addWidget(self.select_output_folder_button)
        vbox.addLayout(output_button_hbox)
        
        # Create label for ouput_folder
        self.output_folder_label = QtWidgets.QLabel()
        self.output_folder_label.setFont(QFont("Helvetica", 8, QFont.Bold))
        self.output_folder_label.setAlignment(QtCore.Qt.AlignCenter)
        vbox.addWidget(self.output_folder_label)
        
        # Create "Open" and "Convert" buttons
        openButtonHbox = QHBoxLayout(central_widget)
        openButton = QtWidgets.QPushButton("Select Video", central_widget)
        openButton.clicked.connect(self.openVideo)
        openButton.setMaximumWidth(100)
        openButtonHbox.setAlignment(QtCore.Qt.AlignCenter)
        openButtonHbox.addWidget(openButton)
        vbox.addLayout(openButtonHbox)
        
        # Add label to display the image
        self.image_label = QtWidgets.QLabel()
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        self.vbox.addWidget(self.image_label)

        # Add label to display the file name
        self.file_name_label = QtWidgets.QLabel()
        self.file_name_label.setFont(QFont("Helvetica", 8, QFont.Bold))
        self.file_name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.vbox.addWidget(self.file_name_label)
        
        # Create Convert Button
        convertButtonHbox = QHBoxLayout(central_widget)
        convertButton = QtWidgets.QPushButton("Convert", central_widget)
        convertButton.clicked.connect(self.convertVideo)
        convertButton.setMaximumWidth(100) 
        convertButtonHbox.setAlignment(QtCore.Qt.AlignCenter)
        convertButtonHbox.addWidget(convertButton)
        vbox.addLayout(convertButtonHbox)
        
        # Set up the progress bar
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setGeometry(QtCore.QRect(30, 60, 181, 23))
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setObjectName("progress_bar")
        self.progress_bar.setAlignment(QtCore.Qt.AlignCenter)

        self.vbox.addWidget(self.progress_bar)
        self.converter.progress_bar = self.progress_bar
        
        # Created by text
        created_by = QLabel("Created by John Aquino", central_widget)
        created_by.setAlignment(QtCore.Qt.AlignCenter)
        created_by.setStyleSheet("color: #333;")
        vbox.addStretch()
        vbox.addWidget(created_by)
        
        
        # Show window
        main_window.show()
    
    def openVideo(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self.main_window, "QFileDialog.getOpenFileName()", "", "All Files (*);;Video Files (*.mp4 *.avi)", options=options)
        if file_path:
            self.file_path = file_path
            self.show_filename()
    
    def select_output_folder(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        options |= QtWidgets.QFileDialog.Directory
        options |= QtWidgets.QFileDialog.ShowDirsOnly
        selected_folder = QtWidgets.QFileDialog.getExistingDirectory(self.main_window, "Select Output Folder", options=options)
        print(selected_folder)
        if selected_folder:
            self.output_folder = selected_folder
            self.output_folder_label.setText("Output folder: " + str(self.output_folder))

        
    def convertVideo(self):
        if not self.file_path:
            QMessageBox.warning(self.main_window, 'Error', 'No video file selected')
        if not self.output_folder:
            QMessageBox.warning(self.main_window, 'Error', 'No output folder selected')
        else:
            try:
                fps = int(self.fps_textbox.text())
                if fps > 60 or fps < 0:
                    raise ValueError("")
            except ValueError:
                QMessageBox.warning(self.main_window, 'Error', 'Invalid FPS value')
                return
            Converter().convert(self.file_path, fps, self.output_folder)
    
    def show_filename(self):
        file_name = os.path.basename(self.file_path)
        self.update_file_name(file_name)
        
        # Load first frame of the video
        cap = cv2.VideoCapture(self.file_path)
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        qImg = QtGui.QImage(frame.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        self.update_image(pixmap)
        cap.release()
        
    def update_image(self, pixmap):
        # Update the image in the image label
        self.image_label.setPixmap(pixmap.scaled(100, 100, QtCore.Qt.AspectRatioMode.KeepAspectRatio))

    def update_file_name(self, file_name):
        # Update the file name in the file name label
        self.file_name_label.setText("File name: " + file_name)