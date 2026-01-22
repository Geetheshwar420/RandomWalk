import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Econophysics Random Walk", page_icon="📈", layout="wide")

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
    
    # Create plotly line chart
    fig = px.line(edited_df, 
                  x='Time', 
                  y='Price',
                  title='Random Walk of Stock Price',
                  labels={'Time': 'Time', 'Price': 'Price (₹)'},
                  markers=True)
    
    # Update layout
    fig.update_traces(line=dict(color='blue', width=2),
                     marker=dict(size=8, color='red'))
    
    fig.update_layout(
        xaxis_title='Time',
        yaxis_title='Price (₹)',
        hovermode='x unified',
        showlegend=False
    )
    
    # Display the plot
    st.plotly_chart(fig, use_container_width=True)
    
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
