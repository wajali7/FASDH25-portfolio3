# importing all important libraries
import pandas as pd
import plotly.express as px
import os # to save visualizations as html format

# Load the dataset
df = pd.read_csv(r"C:\Users\DELL\Downloads\FASDH25-portfolio3\data\dataframes\topic-model\topic-model.csv")

# Create a new column called date from year, month and day columns
df["date"] = pd.to_datetime(df[["year", "month", "day"]])
# It creates both daily-level analysis (date) and monthly grouping (year_month) for flexible time-based visualizations
df["year_month"] = df["year"].astype(str) + "-" + df["month"].astype(str).str.zfill(2) 

# Filter out unassigned topics
df = df[df["Topic"] != -1].copy()

# Combine the 4 topic keywords into a single label per topic
df["Topic_Label"] = df[["topic_1", "topic_2", "topic_3", "topic_4"]].agg(", ".join, axis=1)

# Counts the articles for each topic and selects the 5 with the highest count
# and creates a new table containing rows only from the 5 topics
top_topics = df["Topic"].value_counts().nlargest(5).index
df_top_topics = df[df["Topic"].isin(top_topics)]

# Ensure output folder exists so it will be easy to save all outputs
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'outputs')) # save all graphs and visualisation in outputs folder
os.makedirs(output_dir, exist_ok=True) # Help from ChatGPT




                            # Figure 1: Article Count per Topic

# Count how many articles are in each topic
topic_counts = df["Topic"].value_counts().sort_index().reset_index()
topic_counts.columns = ["Topic", "Article Count"] # rename the columns of table

# sort the table to get the topic with most articles at first
topic_counts = topic_counts.sort_values("Article Count", ascending=False)

# create a bar chart
fig1 = px.bar(
    topic_counts,
    x="Topic",
    y="Article Count",
    title="Article Count per Topic",
    text_auto=True, # This shows the numbers directly on the bars
    height=400
)
#save output
fig1.write_html(os.path.join(output_dir, "fig1_article_count.html"))


                        # Figure 2: Monthly Topic Trends for Top 5 Topics
                   
# Bar graph to show topic trends by month
monthly_trend = df_top_topics.groupby(["year_month", "Topic_Label"]).size().reset_index(name="Article Count")
fig2 = px.bar(monthly_trend,
              x="year_month",
              y="Article Count",
              color="Topic_Label",
              barmode="group",
              facet_col="Topic_Label",
              facet_col_wrap=2,
              title="Monthly Topic Trends for Top 5 Topics",
              text_auto=True,
              height=600
)

fig2.update_layout(xaxis_tickangle=45)

# save output
fig2.write_html(os.path.join(output_dir, "fig2_monthly_trends.html"))



                          # Figure 3: Top 5 Keywords per Topic

# find most used words per topic 
keyword_df = df[["Topic_Label", "topic_1", "topic_2", "topic_3", "topic_4"]].melt(id_vars="Topic_Label", value_name="Keyword")

# Groups both topic and keywords and counts how many times each keyword appears
top_words = keyword_df.groupby(["Topic_Label", "Keyword"]).size().reset_index(name="Frequency")

# sorts keywords by topic in ascending order
top_words = top_words.sort_values(["Topic_Label", "Frequency"], ascending=[True, False])
top5_keywords_df = top_words.groupby("Topic_Label").head(5)

# Filter keywords to top 5 topics only 
top5_keywords_df = top5_keywords_df[top5_keywords_df["Topic_Label"].isin(df_top_topics["Topic_Label"].unique())]

# create a horizontal bar chart 
fig3 = px.bar(
    top5_keywords_df,
    x="Frequency",
    y="Keyword",
    color="Keyword", 
    facet_col="Topic_Label",
    facet_col_wrap=2,
    orientation="h", 
    height=800,
    title="Top 5 Keywords per Topic (Horizontal View)"
)

# save output
fig3.write_html(os.path.join(output_dir, "fig3_top_keywords.html"))



                              # Figure 4: Average Word Count per Topic
                  
# Group data by topic and calculate the avarage word count per acrticle for each topic
average_count = df.groupby("Topic_Label")["Count"].mean().reset_index(name="Average_Word_Count")

# create a bar graph showing avarage word count per topic
fig4 = px.bar(
    average_count,
    x="Topic_Label",
    y="Average_Word_Count",
    title="Average Word Count per Topic",
    text_auto=True,
    height=600
)

# save output
fig4.write_html(os.path.join(output_dir, "fig4_avg_word_count.html"))


