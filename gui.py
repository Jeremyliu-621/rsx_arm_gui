"""
RSX Arm GUI - Simple version with buttons and placeholders
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RSX Arm GUI")
        self.setGeometry(100, 100, 800, 600)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("RSX Arm Control")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        
        # Emergency Stop
        estop_frame = QFrame()
        estop_frame.setStyleSheet("border: 2px solid red; border-radius: 10px; padding: 10px;")
        estop_layout = QVBoxLayout(estop_frame)
        estop_label = QLabel("Emergency Stop")
        estop_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.estop_btn = QPushButton("E-STOP (DISARMED)")
        self.estop_btn.setCheckable(True)
        self.estop_btn.setStyleSheet("background-color: #333; color: white; font-size: 14px; padding: 10px;")
        self.estop_btn.toggled.connect(self.on_estop)
        estop_layout.addWidget(estop_label)
        estop_layout.addWidget(self.estop_btn)
        layout.addWidget(estop_frame)
        
        # Joint States Button
        joint_btn = QPushButton("View Joint States")
        joint_btn.setStyleSheet("background-color: #2563eb; color: white; font-size: 14px; padding: 10px;")
        joint_btn.clicked.connect(self.on_joint_states)
        layout.addWidget(joint_btn)
        
        # Joint Angles Button
        angles_btn = QPushButton("View Joint Angles")
        angles_btn.setStyleSheet("background-color: #2563eb; color: white; font-size: 14px; padding: 10px;")
        angles_btn.clicked.connect(self.on_joint_angles)
        layout.addWidget(angles_btn)
        
        # Camera Feed Button
        camera_btn = QPushButton("View Camera Feed")
        camera_btn.setStyleSheet("background-color: #2563eb; color: white; font-size: 14px; padding: 10px;")
        camera_btn.clicked.connect(self.on_camera)
        layout.addWidget(camera_btn)
        
        # 3D View Button
        view3d_btn = QPushButton("View 3D Arm Model")
        view3d_btn.setStyleSheet("background-color: #2563eb; color: white; font-size: 14px; padding: 10px;")
        view3d_btn.clicked.connect(self.on_3d_view)
        layout.addWidget(view3d_btn)
        
        # Path Planning Button
        path_btn = QPushButton("Path Planning Mode")
        path_btn.setStyleSheet("background-color: #2563eb; color: white; font-size: 14px; padding: 10px;")
        path_btn.clicked.connect(self.on_path_planning)
        layout.addWidget(path_btn)
        
        # Status label
        self.status_label = QLabel("Status: Ready")
        self.status_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
    
    def on_estop(self, checked):
        if checked:
            self.estop_btn.setText("E-STOP (ARMED)")
            self.estop_btn.setStyleSheet("background-color: #dc2626; color: white; font-size: 14px; padding: 10px;")
            self.status_label.setText("Status: Emergency Stop ARMED - Publishing to /rsx_gui/emergency_stop")
        else:
            self.estop_btn.setText("E-STOP (DISARMED)")
            self.estop_btn.setStyleSheet("background-color: #333; color: white; font-size: 14px; padding: 10px;")
            self.status_label.setText("Status: Emergency Stop disarmed")
    
    def on_joint_states(self):
        self.status_label.setText("Status: Placeholder - Would subscribe to /joint_states and display all joint states")
    
    def on_joint_angles(self):
        self.status_label.setText("Status: Placeholder - Would display joint angles")
    
    def on_camera(self):
        self.status_label.setText("Status: Placeholder - Would display live camera feed (topic selection available)")
    
    def on_3d_view(self):
        self.status_label.setText("Status: Placeholder - Would show interactive 3D view of arm")
    
    def on_path_planning(self):
        self.status_label.setText("Status: Placeholder - Would enable path planning mode with 3D view and target position")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
