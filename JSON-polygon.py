import sys
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QPushButton,
                             QVBoxLayout, QHBoxLayout, QWidget, QLabel)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import geopandas as gpd
from shapely.geometry import Polygon
import contextily as ctx


class MapCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        # Initial empty plot
        self.axes.set_title('WGS84 Polygon Visualization with Basemap')
        self.fig.tight_layout()

    def plot_polygon(self, coordinates):
        self.axes.clear()

        # Extract coordinates into shapely polygon
        polygon = Polygon([(point["lng"], point["lat"]) for point in coordinates])
        gdf = gpd.GeoDataFrame(index=[0], geometry=[polygon], crs="EPSG:4326")

        # Project to Web Mercator for contextily
        gdf_web_mercator = gdf.to_crs(epsg=3857)

        # Plot the polygon
        gdf_web_mercator.plot(ax=self.axes, edgecolor='black', facecolor='lightblue', linewidth=2, alpha=0.6)

        # Add basemap
        ctx.add_basemap(self.axes, crs=gdf_web_mercator.crs.to_string())

        # Set limits and title
        self.axes.set_xlim(gdf_web_mercator.total_bounds[[0, 2]])
        self.axes.set_ylim(gdf_web_mercator.total_bounds[[1, 3]])
        self.axes.set_title("Polygon on OpenStreetMap")
        self.axes.axis('off')
        self.draw()


class PolygonVisualizerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Coordinate Polygon Visualizer with OSM")
        self.setGeometry(100, 100, 1000, 600)
        self.initUI()

    def initUI(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        # Left layout
        left_layout = QVBoxLayout()
        input_label = QLabel("Paste JSON Coordinates")
        input_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.json_input = QTextEdit()
        self.json_input.setPlaceholderText("Paste JSON coordinates with 'lat' and 'lng' keys")

        button_layout = QHBoxLayout()
        self.visualize_btn = QPushButton("Visualize Polygon")
        self.visualize_btn.clicked.connect(self.visualize_polygon)
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_data)
        self.sample_btn = QPushButton("Load Sample Data")
        self.sample_btn.clicked.connect(self.load_sample_data)

        button_layout.addWidget(self.visualize_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.sample_btn)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red; font-weight: bold;")

        left_layout.addWidget(input_label)
        left_layout.addWidget(self.json_input)
        left_layout.addLayout(button_layout)
        left_layout.addWidget(self.error_label)

        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        left_widget.setMaximumWidth(400)

        # Right layout
        right_layout = QVBoxLayout()
        self.map_canvas = MapCanvas(self, width=6, height=6)
        map_label = QLabel("Polygon Visualization")
        map_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        right_layout.addWidget(map_label)
        right_layout.addWidget(self.map_canvas)

        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def visualize_polygon(self):
        try:
            json_text = self.json_input.toPlainText().strip()
            if not json_text:
                self.show_error("Please enter JSON coordinates.")
                return
            coordinates = json.loads(json_text)
            if not isinstance(coordinates, list) or len(coordinates) < 3:
                self.show_error("Need at least 3 coordinates to form a polygon.")
                return
            for point in coordinates:
                if not all(key in point for key in ("lat", "lng")):
                    self.show_error("Each point must have 'lat' and 'lng'.")
                    return
            self.error_label.setText("")
            self.map_canvas.plot_polygon(coordinates)
        except json.JSONDecodeError as e:
            self.show_error(f"Invalid JSON: {str(e)}")
        except Exception as e:
            self.show_error(f"Error: {str(e)}")

    def clear_data(self):
        self.json_input.clear()
        self.error_label.setText("")
        self.map_canvas.axes.clear()
        self.map_canvas.draw()

    def load_sample_data(self):
        sample_data = [
            {"lng": 103.62659, "lat": 1.5783},
            {"lng": 103.62661, "lat": 1.5792},
            {"lng": 103.62662, "lat": 1.5801},
            {"lng": 103.62663, "lat": 1.581},
            {"lng": 103.62664, "lat": 1.5819},
            {"lng": 103.62665, "lat": 1.5828},
            {"lng": 103.62666, "lat": 1.5837},
            {"lng": 103.62667, "lat": 1.5846},
            {"lng": 103.62668, "lat": 1.5855},
            {"lng": 103.6267, "lat": 1.5864},
            {"lng": 103.62659, "lat": 1.58728},
            {"lng": 103.62631, "lat": 1.58813}
        ]
        self.json_input.setPlainText(json.dumps(sample_data, indent=2))

    def show_error(self, message):
        self.error_label.setText(message)


def run_app():
    app = QApplication(sys.argv)
    window = PolygonVisualizerApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_app()