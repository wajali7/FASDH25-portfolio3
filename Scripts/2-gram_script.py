# Import necessary libraries
import pandas as pd  # For data manipulation and analysis
import plotly.express as px  # For creating interactive visualizations
import plotly.graph_objects as go  # For more customized visualizations
from nltk.corpus import stopwords  # For accessing stopwords list
import nltk  # Natural Language Toolkit for text processing(2)
import os  # For operating system dependent functionality
from pathlib import Path  # For object-oriented filesystem paths(1)
from datetime import datetime  # For date and time operations

# Download stopwords if not already downloaded(2)
nltk.download('stopwords')

# Get the directory where the script is located
script_dir = Path(__file__).parent

# Construct paths to input and output directories
csv_path = script_dir.parent / 'data' / 'dataframes' / 'n-grams' / '2-gram' / '2-gram-year-month.csv'  # Path to input CSV file
output_folder = script_dir.parent / 'Outputs'  # Path to output directory
os.makedirs(output_folder, exist_ok=True)  # Create output directory if it doesn't exist

# Load and prepare data
df = pd.read_csv(csv_path)  # Read the CSV file into a pandas DataFrame
df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'].astype(str))  # Create a datetime column from year and month

# Filter bigrams to remove noise and focus on meaningful terms(2)
stop_words = set(stopwords.words('english'))  # Get English stopwords
important_words = ['gaza', 'israel', 'palestine', 'hamas', 'idf', 'strike', 'air', 'war', 
                  'conflict', 'bombing', 'civilians', 'militants', 'rocket', 'ceasefire', 'attacks']  # Keywords of interest

# Function to identify useless bigrams (those composed entirely of stopwords)(2)
def is_useless(bigram):
    return all(word in stop_words for word in bigram.lower().split())

# Function to identify important bigrams (those containing our keywords)(2)
def is_important(bigram):
    return any(word in bigram.lower() for word in important_words)

# Apply filters to the data
df_clean = df[~df['2-gram'].apply(is_useless)]  # Remove useless bigrams
df_meaningful = df_clean[df_clean['2-gram'].apply(is_important)]  # Keep only important bigrams

# Get top 10 bigrams overall by summing counts across all time periods
top_10_bigrams = df_meaningful.groupby('2-gram')['count-sum'].sum().nlargest(10).index  # Get names of top 10 bigrams
df_top = df_meaningful[df_meaningful['2-gram'].isin(top_10_bigrams)]  # Filter dataframe to only include top 10 bigrams

# 1. Time Series Visualization with Plotly
# Create an interactive line chart showing frequency of top bigrams over time
fig_time = px.line(df_top, 
                  x='date',  # X-axis: date
                  y='count-sum',  # Y-axis: frequency count
                  color='2-gram',  # Color lines by bigram
                  title='Top 10 Bigrams Frequency Over Time',
                  labels={'count-sum': 'Frequency', 'date': 'Date', '2-gram': 'Bigram'},
                  height=600)
fig_time.update_layout(hovermode='x unified')  # Show all data when hovering over x-axis
# Save visualization as HTML and PNG
fig_time.write_html(output_folder / "bigrams_time_series.html")
fig_time.write_image(output_folder / "bigrams_time_series.png")

# 2. Prepare data for Gephi (network visualization software)
# Create nodes file (bigrams)
nodes = pd.DataFrame({
    'Id': df_top['2-gram'].unique(),  # Unique identifier for each bigram
    'Label': df_top['2-gram'].unique()  # Display label (same as ID in this case)
})
nodes.to_csv(output_folder / "gephi_nodes.csv", index=False)  # Save nodes to CSV

# Create edges file (co-occurrence over time)
# Here we'll create a simple edge list showing bigram frequency by time period
edges = df_top[['date', '2-gram', 'count-sum']].copy()  # Create copy of relevant columns
edges['Source'] = edges['date'].dt.strftime('%Y-%m')  # Convert date to string format for source
edges['Target'] = edges['2-gram']  # Bigram as target
edges['Weight'] = edges['count-sum']  # Frequency count as edge weight
edges[['Source', 'Target', 'Weight']].to_csv(output_folder / "gephi_edges.csv", index=False)  # Save edges to CSV

# 3. Additional visualization: Heatmap of bigram frequency by month
# Create pivot table for heatmap data (dates vs bigrams with frequency counts)
heatmap_data = df_top.pivot_table(index='date', columns='2-gram', values='count-sum', aggfunc='sum')
# Create heatmap visualization
fig_heat = go.Figure(data=go.Heatmap(
    z=heatmap_data.values.T,  # Transposed frequency values
    x=heatmap_data.index,  # Dates on x-axis
    y=heatmap_data.columns,  # Bigrams on y-axis
    colorscale='Viridis'  # Color scheme
))
# Configure heatmap layout
fig_heat.update_layout(
    title='Bigram Frequency Heatmap',
    xaxis_title='Date',
    yaxis_title='Bigram',
    height=800  # Taller height to accommodate all bigrams
)
# Save heatmap visualization
fig_heat.write_html(output_folder / "bigrams_heatmap.html")

# Print confirmation message
print(f"All outputs saved to: {output_folder}")
