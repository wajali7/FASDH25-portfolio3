# Importing pandas and plotly to work with DataFrames and make interective graphs
import pandas as pd
import plotly.express as px


# Load the dataset 
df = pd.read_csv(r"C:\Users\DELL\Downloads\FASDH25-portfolio3\data\dataframes\topic-model\topic-model.csv")


# Create a new column called date from year, month and day columns 
df["date"] = pd.to_datetime(df[["year", "month", "day"]])

# Count how many articles are in each topic
# It counts how many times a topic appears, then sorts them by topic number and converts the result into a new table
topic_counts = df["Topic"].value_counts().sort_index().reset_index()


# Renames the columns of the table to Topic and Article count 
topic_counts.columns = ["Topic", "Article Count"]

#Sort the table so the topic with the most articles comes first.

topic_counts = topic_counts.sort_values("Article Count", ascending=False)

# saving the output so i can access and look at the results
topic_counts.to_csv("../outputs/Suhrab-exploration-output/article_count_per_topic.csv", index=False)

# Create a bar chart to show that how many articles are present in each topic 
fig_topic_distribution = px.bar(
    topic_counts,
    x = "Topic",    
    y = "Article Count",    
    title = "Article Count per Topic",   
    text_auto = True,  # This shows the numbers directly on the bars
    height = 400   

)
# Show the graph
fig_topic_distribution.show()   



#filter out unassigned topics (Topic = -1)

df = df[df["Topic"] != -1].copy()

# Remove Stop Words as they don't add much meaning
# Copied from NLTK website
stop_words = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 
    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 
    'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 
    'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 
    'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 
    'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 
    'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 
    'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 
    'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 
    'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'
}

# Go through each of the 4 topic keyword columns in the DataFrame and remove stop words
# it checks if the word is in stop words list if present it removes it else keeps the word as is
for col in ["topic_1", "topic_2", "topic_3", "topic_4"]:
    def remove_stop_words(word):
        if word in stop_words:    
            return ""   
        return word   

    # Applying the stop word removal function to every word in each of the topic columns
    
    df[col] = df[col].apply(remove_stop_words)
    

# Combine the 4 topic keywords into a single label per topic
df["Topic_Label"] = df[["topic_1", "topic_2", "topic_3", "topic_4"]].agg(", ".join, axis=1)


# Counts the articles for each topic and selects the 5 with the highest count
top_topics = df["Topic"].value_counts().nlargest(5).index

# Creates a new table containing rows only from the 5 topics 
df_top_topics = df[df["Topic"].isin(top_topics)].copy()

#Find the Daily topic trends for each topic label
daily_trend = df_top_topics.groupby(["date", "Topic_Label"]).size().reset_index(name="Article Count")

# Create a line chart to show how article counts changed on daily basis for each top topic
fig_daily_facet = px.line(
    daily_trend,
    x = "date",
    y = "Article Count",
    color = "Topic_Label",  
    facet_col = "Topic_Label",   
    facet_col_wrap = 2,    
    title = "Daily Topic Trend Over Time for Top 5 Topics"
)

fig_daily_facet.write_html("../outputs/Suhrab-exploration-output/daily_topic_trend_top5.html")



# Count the number of articles written per topic each year 
# Group the DataFrame by Topic_Label and year and count the number of articles in each group
# and rename it to get a new DataFramae with a column called "Article Count"
grouped = df.groupby(["Topic_Label", "year"]).size().reset_index(name="Article_Count")

# Find the top 10 topics that have the highest total article counts across all years
top_ten_topics = grouped.groupby("Topic_Label")["Article_Count"].sum().nlargest(10).index

# Filter the DataFrame to get the toop 10 topics only 
grouped = grouped[grouped["Topic_Label"].isin(top_ten_topics)]


#Create the Bar chart 
fig = px.bar(
    grouped,
    x='year',
    y='Article_Count',
    color='Topic_Label',
    barmode='group',
    title='Article Counts by Topic and Year',
    labels={'Topic_Label': 'Topic', 'Article_Count': 'Number of Articles', 'year': 'Year'},
    text_auto = True,
    height = 500
)

fig.write_html("../outputs/Suhrab-exploration-output/article_counts_by_topic_and_year.html")

# Count how many times war is mentioned in the article titles 

# Filter the dataset to only keep the articles that beling to the top 10 topics 
filtered_df = df[df["Topic_Label"].isin(top_ten_topics)].copy()

# Check if the word war appears in each article title
war_occurrences = filtered_df ["title"].str.contains("war", case =False, na=False)

# Convert the True or False result into 1 (war mentioned) or 0 (not mentioned) and add a new column
filtered_df["war_mention"] = war_occurrences.astype(int)

# Group by year and sum the war_mention column to count how many articles mentioned war each year
war_counts_per_year = filtered_df.groupby("year")["war_mention"].sum().reset_index()

# Sort the results by year so the line chart appear in the right order 
war_counts_per_year = war_counts_per_year.sort_values("year")

# save war counts per year to csv file
war_counts_per_year.to_csv("../outputs/Suhrab-exploration-output/war_mentions_per_year.csv", index=False)

# Create line chart
fig_war_trend = px.line(
    war_counts_per_year,
    x="year",
    y="war_mention",
    markers=True,
    title="Number of times the word 'war' is mentioned per year (Top Topics)",
    labels={"war_mention": "Count of 'war' mentions", "year": "Year"}
)

# update x-axis to show every single year 
fig_war_trend.update_layout(xaxis=dict(dtick=1))  
fig_war_trend.show()
