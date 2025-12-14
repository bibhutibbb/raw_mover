import os
import shutil
import sys
from PyQt5 import QtWidgets, QtCore, QtGui

__version__ = "1.0.0.0"

class RawMoverWorker(QtCore.QObject):
    progress_updated = QtCore.pyqtSignal(int)
    log_message = QtCore.pyqtSignal(str)
    status_message = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal()
    
    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path

    def get_raw_extensions(self):
        return ['.nef', '.cr2', '.cr3', '.arw', '.dng', '.rw2', '.orf', '.pef', '.raf', '.srw', '.x3f']

    def get_jpg_extensions(self):
        return ['.jpg', '.jpeg', '.png']

    def run(self):
        folder_path = self.folder_path
        if not folder_path:
            self.status_message.emit("Please select a folder first.")
            self.finished.emit()
            return

        self.log_message.emit("Starting RAW file moving process...")
        self.status_message.emit("")

        raw_extensions = self.get_raw_extensions()
        jpg_extensions = self.get_jpg_extensions()

        try:
            all_files = os.listdir(folder_path)
        except FileNotFoundError:
            self.status_message.emit("Folder not found.")
            self.finished.emit()
            return

        raw_files = {os.path.splitext(f)[0].lower(): f for f in all_files if os.path.splitext(f)[1].lower() in raw_extensions}
        jpg_files = {os.path.splitext(f)[0].lower() for f in all_files if os.path.splitext(f)[1].lower() in jpg_extensions}

        paired_basenames = jpg_files.intersection(raw_files.keys())

        if not paired_basenames:
            self.log_message.emit("No paired RAW and JPG files found.")
            self.finished.emit()
            return

        output_folder = os.path.join(folder_path, "RAW_Files")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            self.log_message.emit(f"Created folder: {output_folder}")

        total_files_to_move = len(paired_basenames)
        moved_count = 0
        
        for i, basename in enumerate(paired_basenames):
            raw_filename = raw_files[basename]
            source_path = os.path.join(folder_path, raw_filename)
            destination_path = os.path.join(output_folder, raw_filename)

            try:
                shutil.move(source_path, destination_path)
                self.log_message.emit(f"Moved: {raw_filename}")
                moved_count += 1
            except Exception as e:
                self.log_message.emit(f"Error moving {raw_filename}: {e}")
            
            # Emit progress
            progress = int((i + 1) / total_files_to_move * 100)
            self.progress_updated.emit(progress)

        self.status_message.emit(f"Moved {moved_count} RAW files to '{output_folder}'.")
        self.finished.emit()


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"RAW Mover v{__version__}")
        self.init_ui()

        # Set application icon
        app_icon_path = os.path.join(os.path.dirname(__file__), 'app_icon.ico')
        if os.path.exists(app_icon_path):
            self.setWindowIcon(QtGui.QIcon(app_icon_path))
        else:
            print(f"Warning: Application icon not found at {app_icon_path}")

    def init_ui(self):
        # Main layout
        main_layout = QtWidgets.QVBoxLayout()

        # Folder selection frame (Tkinter frame -> QWidget with HBox layout)
        folder_selection_widget = QtWidgets.QWidget()
        folder_selection_layout = QtWidgets.QHBoxLayout(folder_selection_widget)
        
        self.label = QtWidgets.QLabel("Select a folder:")
        self.folder_path_input = QtWidgets.QLineEdit()
        self.browse_button = QtWidgets.QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_folder)

        folder_selection_layout.addWidget(self.label)
        folder_selection_layout.addWidget(self.folder_path_input)
        folder_selection_layout.addWidget(self.browse_button)
        folder_selection_layout.setContentsMargins(0, 0, 0, 0) # Remove extra margins

        # Add drag and drop instruction label
        self.drag_drop_label = QtWidgets.QLabel("Or drag and drop a folder here.")
        self.drag_drop_label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.drag_drop_label)

        main_layout.addWidget(folder_selection_widget)

        # Controls and progress frame
        controls_widget = QtWidgets.QWidget()
        controls_layout = QtWidgets.QVBoxLayout(controls_widget)

        self.start_button = QtWidgets.QPushButton("Start Moving RAWs")
        self.start_button.clicked.connect(self.start_moving)
        controls_layout.addWidget(self.start_button)

        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        controls_layout.addWidget(self.progress_bar)

        self.progress_text_edit = QtWidgets.QTextEdit()
        self.progress_text_edit.setReadOnly(True)
        controls_layout.addWidget(self.progress_text_edit)

        self.status_label = QtWidgets.QLabel("")
        controls_layout.addWidget(self.status_label)
        controls_layout.setContentsMargins(0, 0, 0, 0) # Remove extra margins

        main_layout.addWidget(controls_widget)
        self.setLayout(main_layout)

        # Footer
        footer_widget = QtWidgets.QWidget()
        footer_layout = QtWidgets.QVBoxLayout(footer_widget)
        footer_layout.setContentsMargins(0, 10, 0, 0) # Add some top margin

        # Credit label with clickable link
        credit_text = 'Created by Bibhuti. <a href="https://www.facebook.com/bibhutithecoolboy">Facebook</a>'
        self.credit_label = QtWidgets.QLabel(credit_text)
        self.credit_label.setOpenExternalLinks(True) # Make links clickable
        self.credit_label.setAlignment(QtCore.Qt.AlignCenter)
        footer_layout.addWidget(self.credit_label)

        # Donation message
        self.donation_message_label = QtWidgets.QLabel(
            "If you find this tool useful, please consider donating. If you need any custom tools, contact me via Facebook."
        )
        self.donation_message_label.setAlignment(QtCore.Qt.AlignCenter)
        footer_layout.addWidget(self.donation_message_label)

        # Donate button
        self.donate_button = QtWidgets.QPushButton("Donate")
        self.donate_button.clicked.connect(self.show_qr_code)
        footer_layout.addWidget(self.donate_button)

        main_layout.addWidget(footer_widget)
        self.setLayout(main_layout) # This line was already present, effectively setting the layout again

        # Set some padding for the main window content
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Enable drag and drop for the main window
        self.setAcceptDrops(True)

    def show_qr_code(self):
        qr_dialog = QtWidgets.QDialog(self)
        qr_dialog.setWindowTitle("Donate - QR Code")
        qr_layout = QtWidgets.QVBoxLayout(qr_dialog)

        qr_label = QtWidgets.QLabel("Scan to Donate:")
        qr_label.setAlignment(QtCore.Qt.AlignCenter)
        qr_layout.addWidget(qr_label)

        # Assuming 'payment_qr_code.png' is in the same directory as the script
        qr_image_path = os.path.join(os.path.dirname(__file__), 'payment_qr_code.png')
        if os.path.exists(qr_image_path):
            pixmap = QtGui.QPixmap(qr_image_path)
            if not pixmap.isNull():
                image_label = QtWidgets.QLabel()
                image_label.setPixmap(pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)) # Scale to 200x200, maintain aspect ratio
                image_label.setAlignment(QtCore.Qt.AlignCenter)
                qr_layout.addWidget(image_label)
            else:
                qr_layout.addWidget(QtWidgets.QLabel("Error: Could not load QR code image."))
        else:
            qr_layout.addWidget(QtWidgets.QLabel(f"QR code image not found at: {qr_image_path}"))
            
        qr_dialog.exec_()


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            # Check if any of the URLs is a local directory
            for url in event.mimeData().urls():
                if url.isLocalFile() and os.path.isdir(url.toLocalFile()):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            if url.isLocalFile() and os.path.isdir(url.toLocalFile()):
                self.folder_path_input.setText(url.toLocalFile())
                event.acceptProposedAction()
                return
        event.ignore()


    def browse_folder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_path_input.setText(folder)

    def get_raw_extensions(self):
        return ['.nef', '.cr2', '.cr3', '.arw', '.dng', '.rw2', '.orf', '.pef', '.raf', '.srw', '.x3f']

    def get_jpg_extensions(self):
        return ['.jpg', '.jpeg', '.png']

    def start_moving(self):
        folder_path = self.folder_path_input.text()
        if not folder_path:
            self.status_label.setText("Please select a folder first.")
            return

        self.progress_text_edit.clear()
        self.status_label.setText("")
        self.progress_bar.setValue(0)
        self.start_button.setEnabled(False) # Disable button during operation

        # Create a QThread object
        self.thread = QtCore.QThread()
        # Create a worker object
        self.worker = RawMoverWorker(folder_path)
        # Move worker to the thread
        self.worker.moveToThread(self.thread)

        # Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater) # Ensure thread object is deleted
        self.thread.finished.connect(self._cleanup_thread_and_worker) # New cleanup slot
        
        self.worker.finished.connect(self.on_moving_finished) # Re-enable button and reset progress bar
        
        self.worker.progress_updated.connect(self.update_progress_bar)
        self.worker.log_message.connect(self.append_log_message)
        self.worker.status_message.connect(self.update_status_message)

        # Start the thread
        self.thread.start()

    def on_moving_finished(self):
        self.start_button.setEnabled(True) # Re-enable button
        self.progress_bar.setValue(0) # Reset progress bar
        # Ensure a final status message is displayed, though worker already emits one
        if not self.status_label.text().startswith("Moved"): # Only if worker didn't set a specific success message
             self.status_label.setText("Process completed!")

    def _cleanup_thread_and_worker(self):
        # This slot is called when the QThread has truly finished and is about to be deleted.
        self.thread = None
        self.worker = None


    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def append_log_message(self, message):
        self.progress_text_edit.append(message)

    def update_status_message(self, message):
        self.status_label.setText(message)

    def get_raw_extensions(self):
        return ['.nef', '.cr2', '.cr3', '.arw', '.dng', '.rw2', '.orf', '.pef', '.raf', '.srw', '.x3f']

    def get_jpg_extensions(self):
        return ['.jpg', '.jpeg', '.png']

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
