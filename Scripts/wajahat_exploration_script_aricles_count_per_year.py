import pandas as pd
import plotly.express as px
import os

# Path to articles directory
articles_dir = r'C:\Users\Dell\Downloads\FASDH25-portfolio3\data\articles'
output_dir = r'C:\Users\Dell\Downloads\FASDH25-portfolio3\outputs'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Read all article filenames and extract years
import glob

files = glob.glob(os.path.join(articles_dir, '*.txt'))

# Extract year from filename (format: YYYY-MM-DD_XXXX.txt)
years = [int(os.path.basename(f).split('-')[0]) for f in files]

# Create DataFrame
df_articles = pd.DataFrame({'year': years})

# Count articles per year
article_counts = df_articles.groupby('year').size().reset_index(name='article_count')
article_counts = article_counts.sort_values('year')

# Print to console
print("Number of Articles per Year:")
print(article_counts)

# Save counts as CSV
csv_path = os.path.join(output_dir, 'article_counts_per_year.csv')
article_counts.to_csv(csv_path, index=False)
print(f"Article counts saved to {csv_path}")

# Create bar chart with labels
fig_bar = px.bar(
    article_counts,
    x='year',
    y='article_count',
    title='Number of Articles Published per Year',
    labels={'year': 'Year', 'article_count': 'Number of Articles'},
    text='article_count'
)

# Save bar chart as HTML file
html_path = os.path.join(output_dir, 'article_counts_per_year_bar_chart.html')
fig_bar.write_html(html_path)
print(f"Bar chart saved to {html_path}")

# Optionally display the plot (comment out if running in non-GUI environment)
fig_bar.show()
