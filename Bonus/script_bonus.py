import os
import pandas as pd
import plotly.express as px

# Paths
articles_dir = r'C:\Users\Dell\Downloads\FASDH25-portfolio3\data\articles'
output_dir = r'C:\Users\Dell\Downloads\FASDH25-portfolio3\Bonus'

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Step 1: Create dataset from article files
article_data = []

for filename in os.listdir(articles_dir):
    if filename.endswith(".txt"):
        file_path = os.path.join(articles_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if len(lines) >= 1:
                title = lines[0].strip()
                content = ''.join(lines[1:]).strip()
                
                # Try to parse date from filename (adjust if needed)
                try:
                    date_part = filename.split('_')[0]
                    date = pd.to_datetime(date_part).date()
                except Exception:
                    date = None
                
                article_data.append({'title': title, 'date': date, 'content': content})

df_articles = pd.DataFrame(article_data)

# Save the dataset CSV
dataset_path = os.path.join(output_dir, 'articles_dataset.csv')
df_articles.to_csv(dataset_path, index=False, encoding='utf-8')

print(f"Dataset created at: {dataset_path}")

# Step 2: Load dataset and visualise
df = pd.read_csv(dataset_path, parse_dates=['date'])

# Basic exploration
print(f"Number of articles: {len(df)}")
print("Columns:", df.columns)
print(df.head())

# Group articles by date to count articles per day
articles_per_date = df.groupby('date').size().reset_index(name='article_count')

# Visualisation: Number of articles published over time
fig = px.bar(
    articles_per_date,
    x='date',
    y='article_count',
    title='Number of Articles Published Over Time',
    labels={'date': 'Publication Date', 'article_count': 'Number of Articles'},
    color='article_count',
    color_continuous_scale='Viridis'
)

fig.update_layout(title_x=0.5)
fig.show()

# Save visualization HTML
fig.write_html(os.path.join(output_dir, 'articles_published_over_time.html'))
print("Visualization saved to Bonus folder.")
