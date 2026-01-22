# RandomWalk

Econophysics Random Walk Streamlit Application for visualizing stock price random walk behavior.

## Features

- **Data Input**: Upload Excel/CSV files or generate default random walk data (Time 0-15, Price starting at 100)
- **Data Editing**: Interactive data editor for manual adjustments
- **Visualization**: Plotly line chart showing random walk with markers
- **Analysis**: Display observation about random walk characteristics and statistics

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## How to Use

1. **Choose Data Source**: Select either to upload a file (Excel/CSV) or generate a default random walk
2. **Edit Data**: Use the interactive data editor to manually adjust values if needed
3. **View Visualization**: See the random walk plotted as a line chart with markers
4. **Read Observation**: Understand the characteristics of random walk behavior

## Requirements

- Python 3.8+
- streamlit
- plotly
- pandas
- numpy
- openpyxl (for Excel support)