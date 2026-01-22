import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
from pathlib import Path
import os
import csv

# Set page configuration
st.set_page_config(page_title="Econophysics Random Walk", page_icon="📈", layout="wide")

LOG_PATH = Path("download_logs.csv")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")


def log_download(name: str, title: str) -> None:
    """Append download metadata to CSV log with a timestamp."""
    cleaned_name = name.strip()
    if not cleaned_name:
        return

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    is_new_file = not LOG_PATH.exists()
    with LOG_PATH.open("a", newline="") as f:
        writer = csv.writer(f)
        if is_new_file:
            writer.writerow(["timestamp", "name", "title"])
        writer.writerow([datetime.utcnow().isoformat(), cleaned_name, title])

# Title
st.title("Econophysics Random Walk")

# Data Input Section
st.header("1. Data Input")

# Option to upload file or generate default data
data_option = st.radio("Choose data source:", ["Upload File (Excel/CSV)", "Generate Default Random Walk"])

df = None

if data_option == "Upload File (Excel/CSV)":
    uploaded_file = st.file_uploader("Upload your file", type=['csv', 'xlsx', 'xls'])
    
    if uploaded_file is not None:
        try:
            # Read the file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success("File uploaded successfully!")
            
            # Show original columns
            st.write("Original columns:", list(df.columns))
            
            # Normalize columns to 'Time' and 'Price'
            if len(df.columns) >= 2:
                # Assume first column is Time and second is Price
                df.columns = ['Time', 'Price'] + list(df.columns[2:])
                df = df[['Time', 'Price']]
                st.info("Columns normalized to 'Time' and 'Price'")
            else:
                st.error("File must have at least 2 columns")
                df = None
                
        except Exception as e:
            st.error(f"Error reading file: {e}")
            df = None
else:
    # Generate default random walk
    st.write("Generating default random walk (Time 0-15, Price start 100)")
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Generate time steps
    time = np.arange(0, 16)
    
    # Generate random walk starting at 100
    price = [100]
    for i in range(15):
        # Random walk: add random change from normal distribution
        change = np.random.normal(0, 2)
        price.append(price[-1] + change)
    
    df = pd.DataFrame({
        'Time': time,
        'Price': price
    })
    
    st.success("Default random walk generated!")

# Edit Data Section
if df is not None:
    st.header("2. Edit Data")
    st.write("You can manually edit the data below:")
    
    # Display data editor
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    
    # Plot Section
    st.header("3. Random Walk Visualization")

    # Allow users to set a document title that is shown on the chart and used for downloads
    document_title = st.text_input("Documentation title", value="Random Walk Report")
    cleaned_title = document_title.strip() or "Random Walk Report"
    download_name = "_".join(cleaned_title.split()) or "random_walk_report"

    # Create plotly line chart
    fig = px.line(
        edited_df,
        x='Time',
        y='Price',
        title=cleaned_title,
        labels={'Price': 'Price (₹)'},
        markers=True
    )
    
    # Update layout
    fig.update_traces(line=dict(color='blue', width=2),
                     marker=dict(size=8, color='red'))
    
    fig.update_layout(
        xaxis_title='Time',
        yaxis_title='Price (₹)',
        hovermode='x unified',
        showlegend=False,
        title=dict(font=dict(size=22), x=0.02)
    )
    
    # Display the plot
    st.plotly_chart(fig, use_container_width=True)

    # Require a name for logging before allowing download
    downloader_name = st.text_input("Your name (stored privately with download)", value="")

    # Download chart as PNG with the chosen title on top
    image_bytes = fig.to_image(format="png", width=1200, height=800, scale=2, engine="kaleido")
    st.download_button(
        label="Download visualization (PNG)",
        data=image_bytes,
        file_name=f"{download_name}.png",
        mime="image/png",
        disabled=not downloader_name.strip(),
        on_click=log_download,
        args=(downloader_name, cleaned_title)
    )
    
    # Information Section
    st.header("4. Observation")
    st.info("**Observation:** No smooth trend. Irregular fluctuations characteristic of a random walk.")
    
    # Additional statistics
    with st.expander("View Statistics"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Starting Price", f"₹{edited_df['Price'].iloc[0]:.2f}")
        with col2:
            st.metric("Ending Price", f"₹{edited_df['Price'].iloc[-1]:.2f}")
        with col3:
            st.metric("Max Price", f"₹{edited_df['Price'].max():.2f}")
        with col4:
            st.metric("Min Price", f"₹{edited_df['Price'].min():.2f}")

else:
    st.warning("Please upload a file or generate default random walk to continue.")

# Admin-only download log view (hidden unless query params include admin flag and correct token)
params = st.experimental_get_query_params()
is_admin = params.get("admin", ["0"])[0] == "1"
provided_token = params.get("token", [""])[0]

if is_admin:
    st.header("Admin: Download Log")
    if not ADMIN_TOKEN:
        st.warning("ADMIN_TOKEN environment variable is not set; admin view is disabled.")
    elif provided_token != ADMIN_TOKEN:
        st.error("Unauthorized: invalid token.")
    else:
        if LOG_PATH.exists():
            log_df = pd.read_csv(LOG_PATH)
            st.dataframe(log_df, use_container_width=True)
            st.download_button(
                label="Download log CSV",
                data=LOG_PATH.read_bytes(),
                file_name="download_logs.csv",
                mime="text/csv"
            )
        else:
            st.info("No downloads have been logged yet.")
