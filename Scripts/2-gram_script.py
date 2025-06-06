import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from nltk.corpus import stopwords
import nltk
import os
from pathlib import Path
from datetime import datetime

# Download stopwords if not already
nltk.download('stopwords')

# Get the directory where the script is located
script_dir = Path(__file__).parent

# Construct paths
csv_path = script_dir.parent / 'data' / 'dataframes' / 'n-grams' / '2-gram' / '2-gram-year-month.csv'
output_folder = script_dir.parent / 'Outputs'
os.makedirs(output_folder, exist_ok=True)

# Load and prepare data
df = pd.read_csv(csv_path)
df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'].astype(str))

# Filter bigrams
stop_words = set(stopwords.words('english'))
important_words = ['gaza', 'israel', 'palestine', 'hamas', 'idf', 'strike', 'air', 'war', 
                  'conflict', 'bombing', 'civilians', 'militants', 'rocket', 'ceasefire', 'attacks']

def is_useless(bigram):
    return all(word in stop_words for word in bigram.lower().split())

def is_important(bigram):
    return any(word in bigram.lower() for word in important_words)

df_clean = df[~df['2-gram'].apply(is_useless)]
df_meaningful = df_clean[df_clean['2-gram'].apply(is_important)]

# Get top 10 bigrams overall
top_10_bigrams = df_meaningful.groupby('2-gram')['count-sum'].sum().nlargest(10).index
df_top = df_meaningful[df_meaningful['2-gram'].isin(top_10_bigrams)]

# 1. Time Series Visualization with Plotly
fig_time = px.line(df_top, 
                  x='date', 
                  y='count-sum', 
                  color='2-gram',
                  title='Top 10 Bigrams Frequency Over Time',
                  labels={'count-sum': 'Frequency', 'date': 'Date', '2-gram': 'Bigram'},
                  height=600)
fig_time.update_layout(hovermode='x unified')
fig_time.write_html(output_folder / "bigrams_time_series.html")
fig_time.write_image(output_folder / "bigrams_time_series.png")

# 2. Prepare data for Gephi
# Create nodes file (bigrams)
nodes = pd.DataFrame({
    'Id': df_top['2-gram'].unique(),
    'Label': df_top['2-gram'].unique()
})
nodes.to_csv(output_folder / "gephi_nodes.csv", index=False)

# Create edges file (co-occurrence over time)
# Here we'll create a simple edge list showing bigram frequency by time period
edges = df_top[['date', '2-gram', 'count-sum']].copy()
edges['Source'] = edges['date'].dt.strftime('%Y-%m')
edges['Target'] = edges['2-gram']
edges['Weight'] = edges['count-sum']
edges[['Source', 'Target', 'Weight']].to_csv(output_folder / "gephi_edges.csv", index=False)

# 3. Additional visualization: Heatmap of bigram frequency by month
heatmap_data = df_top.pivot_table(index='date', columns='2-gram', values='count-sum', aggfunc='sum')
fig_heat = go.Figure(data=go.Heatmap(
    z=heatmap_data.values.T,
    x=heatmap_data.index,
    y=heatmap_data.columns,
    colorscale='Viridis'
))
fig_heat.update_layout(
    title='Bigram Frequency Heatmap',
    xaxis_title='Date',
    yaxis_title='Bigram',
    height=800
)
fig_heat.write_html(output_folder / "bigrams_heatmap.html")

print(f"All outputs saved to: {output_folder}")
