import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor
from PyQt5.QtCore import Qt, QTimer


class DroneMap(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('UAV Map')

        self.map_label = QLabel(self)
        self.map_label.setGeometry(0, 0, self.width(), self.height())
        self.map_label.setAlignment(Qt.AlignCenter)
        # Requirement arrengments for map

        self.drone_position = [self.width() // 2, self.height() // 2]
        # Starting location for your drone

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_map)
        self.timer.start(100)  # Update every 0.1 seconds
        # Line of code that will update its position on the map as the drone moves

        self.direction = [0, 0]
        self.update_map()
        # Direction for x and y axes

    def resizeEvent(self, event):
        self.map_label.setGeometry(0, 0, self.width(), self.height())
        self.drone_position = [self.width() // 2, self.height() // 2]
        self.update_map()
        # Sets the window size to 0.0 point in the upper left corner of the opened window.

    def update_map(self):
        api_key = "YOUR__API__KEY"
        latitude = 51.506318
        longitude = -0.078650
        zoom = 15
        map_url = (f"https://maps.googleapis.com/maps/api/staticmap?center={latitude},"
                   f"{longitude}&zoom={zoom}&size={self.width()}x{self.height()}&key={api_key}")
        response = requests.get(map_url)

        # Variables such as api_key, latitude, longitude, and zoom are used to specify a specific
        # location and zoom level via the Google Maps API.
        # The map_url variable creates the URL that will be used to make requests from the
        # Google Maps API. This URL contains the specified location and size.
        # The response variable receives the response from the Google Maps API.

        if response.status_code == 200:
            with open("map_image.png", "wb") as f:
                f.write(response.content)
            pixmap = QPixmap("map_image.png").scaled(self.width(), self.height(), Qt.KeepAspectRatio,
                                                     Qt.SmoothTransformation)

            # Drawing the drone on the map
            painter = QPainter(pixmap)
            painter.setBrush(QBrush(Qt.red))
            painter.drawEllipse(self.drone_position[0], self.drone_position[1], 20, 20)  # Drone as a red circle
            painter.end()

            self.map_label.setPixmap(pixmap)
        else:
            print("Failed to fetch map image")

        self.drone_position[0] += self.direction[0]
        self.drone_position[1] += self.direction[1]

        # The content of the response from the Google Maps API is written to a file called map_image.png,
        # and this image is then sized to be loaded into the QLabel widget. To add a drone on the map, a red circle
        # is drawn (representing the drone). Drawings are assigned to a QPixmap object for insertion into the QLabel
        # widget. The drone's location is updated based on the self.direction variable. However, I did not define the
        # self.direction variable in this method. I will explain below where this variable comes from and how it is
        # used, because it is a necessary and important variable to accurately update the drone's position.

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Up:
            self.direction = [0, -10]
        elif key == Qt.Key_Down:
            self.direction = [0, 10]
        elif key == Qt.Key_Left:
            self.direction = [-10, 0]
        elif key == Qt.Key_Right:
            self.direction = [10, 0]

    # For keyPressEvent() method:
    # It works when a key is pressed on the keyboard.
    # The self.direction variable is determined according to the key pressed:
    # If the up arrow key is pressed, self.direction is set to [0, -10] (drone moves up).
    # If the down arrow key is pressed, self.direction is set to [0, 10] (drone moves down).
    # If the left arrow key is pressed, self.direction is set to [-10, 0] (drone moves left).
    # If the right arrow key is pressed, self.direction is set to [10, 0] (drone moves right).

    def keyReleaseEvent(self, event):
        self.direction = [0, 0]

    # For keyReleaseEvent() method:
    # It works when a key is released from the keyboard.
    # self.direction is set to [0, 0], meaning there is no movement
    # in any direction (the drone stops).


if __name__ == '__main__':
    app = QApplication(sys.argv)
    map_window = DroneMap()
    map_window.resize(800, 600)  #
    map_window.show()
    sys.exit(app.exec_())

# This block runs when the Python file is run directly.
# A PyQt application is created (using QApplication).
# An instance of the DroneMap() class is created as the main window of the application.
# The main loop of the PyQt application is started (using app.exec_()).
# When the application terminates, the system exit code is returned and
# the program is terminated (using sys.exit()).
