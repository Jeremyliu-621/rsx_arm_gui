"""
RSX Arm GUI - Control interface
"""

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QComboBox, QGroupBox, QTextEdit
)
from PyQt5.QtCore import Qt


def load_stylesheet(filename='styles.css'):
    """Load CSS stylesheet from file"""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return f.read()
    return ""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RSX Arm Control System")
        self.setGeometry(100, 100, 1400, 900)
        self.path_planning_mode = False
        self.init_ui()
        self.show_sample_data()
        
    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Top bar: Title (centered)
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        title = QLabel("RSX Arm Control System")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        top_bar.addWidget(title)
        top_bar.addStretch()
        main_layout.addLayout(top_bar)
        
        # Main content area: Split into left (controls), center (camera), right (joint states)
        content_layout = QHBoxLayout()
        
        # Left panel: Controls and joint angles
        left_panel = QVBoxLayout()
        left_panel.setSpacing(10)
        
        # Control Panel
        control_group = QGroupBox("Control Panel")
        control_layout = QVBoxLayout()
        camera_topic_layout = QHBoxLayout()
        camera_topic_layout.addWidget(QLabel("Camera Topic:"))
        self.camera_topic_combo = QComboBox()
        self.camera_topic_combo.addItems(["/camera/image_raw", "/camera/color/image_raw", "/camera/rgb/image_raw"])
        camera_topic_layout.addWidget(self.camera_topic_combo)
        control_layout.addLayout(camera_topic_layout)
        self.path_planning_btn = QPushButton("Enable Path Planning Mode")
        self.path_planning_btn.setObjectName("path_planning_button")
        self.path_planning_btn.setCheckable(True)
        self.path_planning_btn.toggled.connect(self.on_path_planning_toggle)
        control_layout.addWidget(self.path_planning_btn)
        control_group.setLayout(control_layout)
        left_panel.addWidget(control_group)
        
        # Joint angles display
        angles_group = QGroupBox("Joint Angles (rad)")
        angles_layout = QVBoxLayout()
        self.joint_angles_display = QTextEdit()
        self.joint_angles_display.setObjectName("joint_angles_display")
        self.joint_angles_display.setReadOnly(True)
        self.joint_angles_display.setMaximumHeight(200)
        self.joint_angles_display.setPlainText("Waiting for joint angle data...")
        angles_layout.addWidget(self.joint_angles_display)
        angles_group.setLayout(angles_layout)
        left_panel.addWidget(angles_group)
        
        # Emergency Stop - in left panel bottom
        estop_frame = QFrame()
        estop_frame.setObjectName("estop_frame")
        estop_layout = QVBoxLayout(estop_frame)
        estop_label = QLabel("🛑 EMERGENCY STOP")
        estop_label.setObjectName("estop_label")
        estop_label.setAlignment(Qt.AlignCenter)
        self.estop_btn = QPushButton("E-STOP (DISARMED)")
        self.estop_btn.setObjectName("estop_button")
        self.estop_btn.setCheckable(True)
        self.estop_btn.setMinimumHeight(50)
        self.estop_btn.toggled.connect(self.on_estop)
        estop_layout.addWidget(estop_label)
        estop_layout.addWidget(self.estop_btn)
        left_panel.addWidget(estop_frame)
        
        left_panel.addStretch()
        content_layout.addLayout(left_panel, 1)
        
        # Center panel: Camera feed and 3D view stacked
        center_panel = QVBoxLayout()
        center_panel.setSpacing(10)
        
        # Live Camera Feed
        camera_group = QGroupBox("Live Camera Feed")
        camera_layout = QVBoxLayout()
        self.camera_display = QLabel("Camera feed placeholder\n(Subscribe to topic when available)")
        self.camera_display.setObjectName("camera_display")
        self.camera_display.setAlignment(Qt.AlignCenter)
        self.camera_display.setMinimumWidth(500)
        camera_layout.addWidget(self.camera_display)
        camera_group.setLayout(camera_layout)
        center_panel.addWidget(camera_group)
        
        # 3D View (shown when path planning is active)
        self.view3d_group = QGroupBox("3D Arm Visualization & Target Position")
        self.view3d_group.setObjectName("view3d_group")
        self.view3d_group.setVisible(False)
        view3d_layout = QVBoxLayout()
        self.view3d_display = QLabel("Interactive 3D view placeholder\n(Arm model and target position will be displayed here in path planning mode)")
        self.view3d_display.setObjectName("view3d_display")
        self.view3d_display.setAlignment(Qt.AlignCenter)
        self.view3d_display.setMinimumWidth(500)
        view3d_layout.addWidget(self.view3d_display)
        self.view3d_group.setLayout(view3d_layout)
        center_panel.addWidget(self.view3d_group)
        
        center_panel.addStretch()
        content_layout.addLayout(center_panel, 2)
        
        # Right panel: Joint states
        right_panel = QVBoxLayout()
        states_group = QGroupBox("Joint States")
        states_layout = QVBoxLayout()
        self.joint_states_display = QTextEdit()
        self.joint_states_display.setObjectName("joint_states_display")
        self.joint_states_display.setReadOnly(True)
        self.joint_states_display.setPlainText("Waiting for joint state data...")
        states_layout.addWidget(self.joint_states_display)
        states_group.setLayout(states_layout)
        right_panel.addWidget(states_group)
        content_layout.addLayout(right_panel, 1)
        main_layout.addLayout(content_layout)
        
        # Bottom bar: Status only
        bottom_bar = QHBoxLayout()
        bottom_bar.addStretch()
        self.status_label = QLabel("Status: Ready")
        self.status_label.setObjectName("status_label")
        bottom_bar.addWidget(self.status_label)
        main_layout.addLayout(bottom_bar)
        
        # Load and apply external stylesheet
        stylesheet = load_stylesheet()
        if stylesheet:
            self.setStyleSheet(stylesheet)
    
    def show_sample_data(self):
        """Show sample data in displays"""
        sample_states = {
            'joint1': {'position': 0.1, 'velocity': 0.0, 'effort': 0.0, 'homed': True, 'homing': False},
            'joint2': {'position': 0.2, 'velocity': 0.0, 'effort': 0.0, 'homed': True, 'homing': False},
            'joint3': {'position': -0.1, 'velocity': 0.0, 'effort': 0.0, 'homed': False, 'homing': True},
            'joint4': {'position': 0.3, 'velocity': 0.0, 'effort': 0.0, 'homed': True, 'homing': False},
        }
        sample_angles = {name: state['position'] for name, state in sample_states.items()}
        self.update_joint_states(sample_states)
        self.update_joint_angles(sample_angles)
    
    def on_estop(self, checked):
        """Handle emergency stop button"""
        if checked:
            self.estop_btn.setText("E-STOP (ARMED)")
            self.status_label.setText("Status: ⚠️ EMERGENCY STOP ACTIVE")
        else:
            self.estop_btn.setText("E-STOP (DISARMED)")
            self.status_label.setText("Status: Ready")
    
    def on_path_planning_toggle(self, checked):
        """Toggle path planning mode"""
        self.path_planning_mode = checked
        if checked:
            self.path_planning_btn.setText("Disable Path Planning Mode")
            self.view3d_group.setVisible(True)
            self.status_label.setText("Status: Path planning mode enabled - 3D visualization active")
        else:
            self.path_planning_btn.setText("Enable Path Planning Mode")
            self.view3d_group.setVisible(False)
            self.status_label.setText("Status: Ready")
    
    def update_joint_states(self, states):
        """Update joint states display"""
        text = "Joint Name        | Position (rad) | Velocity | Effort | Status\n" + "-" * 70 + "\n"
        for name, state in sorted(states.items()):
            homed = state.get('homed', False)
            homing = state.get('homing', False)
            status = "HOMED" if homed else ("HOMING" if homing else "NOT HOMED")
            status_color = "🟢" if homed else ("🟡" if homing else "🔴")
            text += f"{name:15s} | {state['position']:13.4f} | {state['velocity']:7.3f} | {state['effort']:6.2f} | {status_color} {status}\n"
        self.joint_states_display.setPlainText(text)
    
    def update_joint_angles(self, angles):
        """Update joint angles display"""
        text = "Joint Angles (radians):\n" + "=" * 40 + "\n"
        for name, angle in sorted(angles.items()):
            text += f"{name:15s}: {angle:10.4f}\n"
        self.joint_angles_display.setPlainText(text)


def main():
    app = QApplication(sys.argv)
    
    # Load global stylesheet if it exists
    stylesheet = load_stylesheet()
    if stylesheet:
        app.setStyleSheet(stylesheet)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
