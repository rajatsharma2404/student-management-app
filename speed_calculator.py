import sys

from PyQt6.QtWidgets import QGridLayout, QWidget, QLabel, \
    QLineEdit, QApplication, QPushButton, QComboBox


class SpeedCalculator(QWidget):

    def __init__(self):
        super().__init__()
        grid = QGridLayout()
        self.setWindowTitle("Speed Calculator")

        distance_label = QLabel("Distance(only in KMs)")
        self.distance_line_edit = QLineEdit()

        time_label = QLabel("Time")
        self.time_line_edit = QLineEdit()

        #button to calculate speed
        calculate_button = QPushButton("Calculate Speed")
        calculate_button.clicked.connect(self.calculate_speed)
        self.output_label = QLabel("")



        self.combobox = QComboBox(self)
        self.combobox.addItem("Kilometer per hour")
        self.combobox.addItem("mile per hour")


        grid.addWidget(distance_label, 0, 0)
        grid.addWidget(self.distance_line_edit, 0, 1)
        grid.addWidget(self.combobox, 0, 2)
        grid.addWidget(time_label, 1, 0)
        grid.addWidget(self.time_line_edit,1, 1)
        grid.addWidget(calculate_button,2,0)
        grid.addWidget(self.output_label,3, 0)

        self.setLayout(grid)

    def calculate_speed(self):
        measurement_type = self.combobox.currentText()
        if measurement_type == "Kilometer per hour":
            speed = int(self.distance_line_edit.text())/int(self.time_line_edit.text())
            self.output_label.setText(f"Speed is {speed} kilometre per hour")
        else:
            distance_in_miles = 1.6 * float(self.distance_line_edit.text())
            speed = distance_in_miles/float(self.time_line_edit.text())
            self.output_label.setText(f"Speed is {speed} miles per hour")

app = QApplication(sys.argv)
speed_calculator = SpeedCalculator()
speed_calculator.show()
sys.exit(app.exec())
