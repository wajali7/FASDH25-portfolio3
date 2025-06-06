import pandas as pd
import plotly.express as px
import os

# Paths
title_dir = r'C:\Users\Dell\Downloads\FASDH25-portfolio3\data\dataframes\title'
length_dir = r'C:\Users\Dell\Downloads\FASDH25-portfolio3\data\dataframes\length'
output_dir = r'C:\Users\Dell\Downloads\FASDH25-portfolio3\outputs'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load title.csv
df_titles = pd.read_csv(os.path.join(title_dir, 'title.csv'))
df_titles['title_length'] = df_titles['title'].str.len()
df_titles_filtered = df_titles[(df_titles['year'] >= 2017) & (df_titles['year'] <= 2023)].copy()

# Load length-year-month.csv
df_length_year_month = pd.read_csv(os.path.join(length_dir, 'length-year-month.csv'))
# Create date column in YYYY-MM format
df_length_year_month["date"] = df_length_year_month["year"].astype(str) + "-" + df_length_year_month["month"].astype(str).str.zfill(2)
df_length_year_month["date"] = pd.to_datetime(df_length_year_month["date"])

# Line graph for total article length per month
fig1_total_length = px.line(
    df_length_year_month,
    x="date",
    y="length-sum",
    title="Total Article Length Per Month (2017–2023)",
    markers=True,
    labels={"length-sum": "Total Length (words)"}
)
fig1_total_length.update_layout(xaxis_title="Date", yaxis_title="Total Length (words)", title_x=0.5)
fig1_total_length.show()
fig1_total_length.write_html(os.path.join(output_dir, 'total_article_length_per_month.html'))

# Line graph for average article length per month
fig2_avg_length = px.line(
    df_length_year_month,
    x="date",
    y="length-mean",
    title="Average Article Length Per Month (2017–2023)",
    markers=True,
    labels={"length-mean": "Average Length (words)"}
)
fig2_avg_length.update_layout(xaxis_title="Date", yaxis_title="Average Length (words)", title_x=0.5)
fig2_avg_length.show()
fig2_avg_length.write_html(os.path.join(output_dir, 'average_article_length_per_month.html'))

# Article counts per year (total articles)
article_counts = df_titles_filtered.groupby('year').size().reset_index(name='article_count').sort_values('year')
print("\nNumber of Articles Published Per Year:")
print(article_counts)

# Bar chart for article counts per year
fig3_bar = px.bar(
    article_counts,
    x='year',
    y='article_count',
    title='Number of Articles Published per Year',
    labels={'year': 'Year', 'article_count': 'Number of Articles'},
    text='article_count'
)
fig3_bar.update_traces(textposition='outside')
fig3_bar.update_layout(xaxis_title='Year', yaxis_title='Number of Articles', title_x=0.5)
fig3_bar.show()
fig3_bar.write_html(os.path.join(output_dir, 'article_counts_per_year_bar_chart.html'))

# War words
war_words = ['war', 'attack', 'kill', 'bomb', 'dead', 'siege', 'missile', 'battle']

# Add war term flag
df_titles_filtered['war_term'] = df_titles_filtered['title'].str.lower().apply(
    lambda text: any(word in text for word in war_words))

# War word counts per year
war_counts_per_year = df_titles_filtered.groupby('year')['war_term'].sum().reset_index()

# Print war counts per year
print("Number of Article Titles Containing War-related Terms Per Year:")
print(war_counts_per_year)

# Line graph — War-related titles per year
fig4_line = px.line(
    war_counts_per_year,
    x='year',
    y='war_term',
    title='Number of Article Titles Containing War-related Terms (2017–2023)',
    labels={'year': 'Year', 'war_term': 'Number of War-related Titles'},
    markers=True
)
fig4_line.update_traces(textposition='top center')
fig4_line.update_layout(xaxis_title='Year', yaxis_title='Number of Titles Mentioning War Terms', title_x=0.5)
fig4_line.show()
fig4_line.write_html(os.path.join(output_dir, 'exploration_war_words_over_years.html'))


print("Figure 1: Total Article Length Per Month (2017–2023) — Done")
print("Figure 2: Average Article Length Per Month (2017–2023) — Done")
print("Figure 3: Number of Articles Published per Year — Done")
print("Figure 4: War-related Titles Per Year — Done")

