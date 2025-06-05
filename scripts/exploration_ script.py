import pandas as pd
import plotly.express as px
import os

# Set working directory to your data folder
data_dir = r'C:\Users\Dell\Downloads\FASDH25-portfolio3\data\dataframes\title'
os.chdir(data_dir)

# Load the data
df = pd.read_csv('title.csv')

# Add title length column
df['title_length'] = df['title'].str.len()

# Find longest title
longest_idx = df['title_length'].idxmax()
print("Longest title:", df.loc[longest_idx, 'title'])

# Total length of all titles
total_length = df['title_length'].sum()
print("Total length of all titles:", total_length)

# Create output directory path
output_dir = r'C:\Users\Dell\Downloads\FASDH25-portfolio3\outputs'

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Export top 20 longest titles
top_20 = df.sort_values(by='title_length', ascending=False).head(20)
top_20.to_csv(os.path.join(output_dir, 'top_20_longest_titles.csv'), index=False)

# Create 'date' column (YYYY-MM-DD)
df['date'] = df['year'].astype(str) + '-' + df['month'].astype(str).str.zfill(2) + '-' + df['day'].astype(str).str.zfill(2)

# Filter articles from Jan–Jun 2023 and export
filtered_articles = df[(df['year'] == 2023) & (df['month'] <= 6)]
filtered_articles.to_csv(os.path.join(output_dir, 'wajahat-ali-6m2023.csv'), index=False)

# War-terms list
war_words = ['war', 'attack', 'kill', 'bomb', 'dead', 'siege', 'missile', 'battle', 'strike', 
             'casualty', 'conflict', 'assault', 'airstrike', 'raid', 'ambush']

# Flag titles containing war terms
df['war_term'] = df['title'].str.lower().apply(lambda text: any(word in text for word in war_words))

# Count war-term titles by year
counts_per_year = df.groupby('year')['war_term'].sum().reset_index()

# Plot the trend
fig = px.line(counts_per_year, x='year', y='war_term',
              title='War-Related Terms in Article Titles Over Time',
              labels={'war_term': 'Number of Titles', 'year': 'Year'},
              markers=True)

fig.update_traces(line=dict(color='firebrick'))
fig.update_layout(template='simple_white')

# Save the figure
fig.write_html(os.path.join(output_dir, 'war_words_titles_trend.html'))
print(f'Plot successfully saved to: {output_dir}')
