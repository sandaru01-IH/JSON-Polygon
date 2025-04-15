# JSON-Polygon
 Polygon Visualizer with OpenStreetMap Basemap A desktop application built with PyQt5, Matplotlib, and GeoPandas that visualizes geographical polygons from JSON coordinate data. The application provides a simple GUI to paste, validate, and display WGS84-format polygons over an interactive OpenStreetMap (OSM) basemap.

# Features
🖼️ Visualize Polygon from JSON: Paste coordinate arrays in {"lat": ..., "lng": ...} format.

🧭 Accurate Mapping: Uses GeoPandas and Shapely to project polygons without distortion.

🌐 OSM Basemap Integration: Includes a high-quality OpenStreetMap tile overlay via contextily.

🎨 Styled Output: Polygons rendered with labeled points, light blue fill, and neat gridless display.

⚙️ User-Friendly GUI: Developed in PyQt5 with support for:

Load Sample Data
Error Validation
Polygon Auto-Fit View

# Getting Started
Clone the repo and install dependencies

bash
Copy
Edit
git clone https://github.com/sandaru01-IH/JSON-polygon.git
cd JSON-polygon
pip install -r requirements.txt
python JSON-polygon.py
To build a standalone .exe:

bash
Copy
Edit
pyinstaller --onefile --windowed polygon_visualizer_osm.py
📦 Dependencies
PyQt5

Matplotlib

GeoPandas

Shapely

Contextily

📂 Sample JSON Format
json
Copy
Edit
[
  { "lng": 103.62659, "lat": 1.5783 },
  { "lng": 103.62661, "lat": 1.5792 },
  { "lng": 103.62662, "lat": 1.5801 }
]
🧠 Use Cases
Quick QA of coordinate datasets

Educational tool for understanding GIS projections

Visualizing polygon boundaries from APIs or shapefiles

📜 License
MIT License – free for personal and commercial use.
