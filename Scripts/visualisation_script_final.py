import pandas as pd
import plotly.express as px
import os

# Paths
title_dir = r'C:\Users\Dell\Downloads\FASDH25-portfolio3\data\dataframes\title'
length_dir = r'C:\Users\Dell\Downloads\FASDH25-portfolio3\data\dataframes\length'
output_dir = r'C:\Users\Dell\Downloads\FASDH25-portfolio3\outputs'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load data
df_titles = pd.read_csv(os.path.join(title_dir, 'title.csv'))
df_titles['title_length'] = df_titles['title'].str.len()
df_titles_filtered = df_titles[(df_titles['year'] >= 2017) & (df_titles['year'] <= 2023)].copy() #help from chat-gpt see AI doc (1)

df_length_year_month = pd.read_csv(os.path.join(length_dir, 'length-year-month.csv'))
df_length_year_month["date"] = pd.to_datetime(df_length_year_month["year"].astype(str) + "-" +
                                             df_length_year_month["month"].astype(str).str.zfill(2))

# Figure 1: Total Article Length Per Month 
fig1 = px.line(
    df_length_year_month,
    x="date",
    y="length-sum",
    title="Total Article Length Per Month (2017–2023)",
    labels={"date": "Date", "length-sum": "Total Length (words)"},
    markers=True,
    template="plotly_white"
)
fig1.update_layout(title_x=0.5, xaxis=dict(rangeslider_visible=True))
fig1.write_html(os.path.join(output_dir, 'visualisation_total_article_length_per_month.html'))

# Figure 2: Average Article Length Per Month
fig2 = px.line(
    df_length_year_month,
    x="date",
    y="length-mean",
    title="Average Article Length Per Month (2017–2023)",
    labels={"date": "Date", "length-mean": "Average Length (words)"},
    markers=True,
    template="plotly_white"
)
fig2.update_layout(title_x=0.5, xaxis=dict(rangeslider_visible=True))
fig2.write_html(os.path.join(output_dir, 'visualisation_average_article_length_per_month.html'))

# Figure 3: Number of Articles Published per Year 

# Bar chart with color gradient
# Recreate the filtered titles DataFrame
df_titles = pd.read_csv(os.path.join(title_dir, 'title.csv'))
df_titles_filtered = df_titles[(df_titles['year'] >= 2017) & (df_titles['year'] <= 2023)].copy()

# Create article counts per year
article_counts = df_titles_filtered.groupby('year').size().reset_index(name='article_count').sort_values('year')

fig3 = px.bar(
    article_counts,
    x='year',
    y='article_count',
    title='Number of Articles Published per Year (2017–2023)',
    labels={'year': 'Year', 'article_count': 'Number of Articles'},
    text='article_count',
    color='article_count',  # Color by value
    color_continuous_scale='Viridis',  # Color scale
    template="plotly_white"
)

fig3.update_traces(textposition='outside')

# Add annotation for year with max articles
max_row = article_counts.loc[article_counts['article_count'].idxmax()] #help from chat-gpt see AI doc (2)
fig3.add_annotation(
    x=max_row['year'],
    y=max_row['article_count'],
    text=f"Highest: {max_row['article_count']}",
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=-50
)

fig3.update_layout(
    title_x=0.5,
    yaxis=dict(dtick=1),
    coloraxis_showscale=False  # Hide color scale legend if not needed
)

fig3.write_html(os.path.join(output_dir, 'exploration_article_counts_per_year_pretty.html'))
fig3.show()


#Figure 4: Number of Titles Containing War-related Terms per Year 
war_words = ['war', 'attack', 'kill', 'bomb', 'dead', 'siege', 'missile', 'battle']
df_titles_filtered['war_term'] = df_titles_filtered['title'].str.lower().apply(
    lambda text: any(word in text for word in war_words)  #help taken fromchat-gpt see AI doc (3)
)
war_counts_per_year = df_titles_filtered.groupby('year')['war_term'].sum().reset_index()
fig4 = px.line(
    war_counts_per_year,
    x='year',
    y='war_term',
    title='Number of Article Titles Containing War-related Terms (2017–2023)',
    labels={'year': 'Year', 'war_term': 'Number of War-related Titles'},
    markers=True,
    template="plotly_white"
)
fig4.update_traces(textposition='top center')
fig4.update_layout(title_x=0.5, yaxis=dict(dtick=1))
fig4.write_html(os.path.join(output_dir, 'visualisation_war_terms_titles_per_year.html'))


