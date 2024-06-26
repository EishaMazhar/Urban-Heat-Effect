import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from column_map import COLUMN_NAMES_MAP
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS

st.set_option('deprecation.showPyplotGlobalUse', False)

# Google Sheets URL
sheet_url = "https://docs.google.com/spreadsheets/d/1CWYqKdx3MQP1eRqU1Bb4nBNh5frm1a4KX_FV8-xN9T0/edit?usp=sharing"
csv_export_url = sheet_url.replace('/edit?usp=sharing', '/export?format=csv')

# Load data from Google Sheets
data = pd.read_csv(csv_export_url)
df = data.dropna(axis=1, how='all')

# Fixing SettingWithCopyWarning
df['city'] = df['Which Indian city?'].combine_first(df['Which Pakistani City'])
df = df.drop(["Timestamp", 'Which Indian city?',
             'Which Pakistani City'], axis=1)
df = df.rename(columns=COLUMN_NAMES_MAP)

# Display the first few rows of the DataFrame
st.title("Urban Heat Island Effect Mitigation Strategies")
st.write("Our platform aims to provide a comprehensive overview of the Urban Heat Island Effect and the various strategies that can be implemented to mitigate it. The data presented here is collected through crowdsourcing and is open to contributions from the public in India & Pakistan. If you have any information that you would like to share, please feel free to reach out to us.")
st.write(df.head(10))

# Bar plot for country counts
st.subheader("Number of Responses by Country")
country_counts = df.groupby('country').size()
country_counts.plot(kind='barh', color=sns.color_palette('Dark2'))
plt.gca().spines[['top', 'right']].set_visible(False)
st.pyplot()


st.subheader("Hot and cool hours of the day")
st.image("india_times.jpeg", caption='Hottest hours of the day',
         use_column_width=True)
st.image("pakistan_times.jpeg",
         caption='Hottest hours of the day', use_column_width=True)


# Sidebar for selecting country and city
st.sidebar.title("Filters")
selected_country = st.sidebar.selectbox(
    "Select Country", options=df['country'].unique())
filtered_data_country = df[df['country'] == selected_country]

selected_city = st.sidebar.selectbox(
    "Select City", options=filtered_data_country['city'].unique())
filtered_data = filtered_data_country[filtered_data_country['city']
                                      == selected_city]

# Main area for visualizations
st.header(f"Data for {selected_city}, {selected_country}")

# Distribution plots for residential, commercial, and density ratings
st.subheader("Distribution of Ratings")
fig, axs = plt.subplots(1, 3, figsize=(18, 6))

sns.histplot(filtered_data['rate_residential'], bins=5, kde=True, ax=axs[0])
axs[0].set_title('Residential Rating Distribution')
axs[0].set_xlabel('Residential Rating')
axs[0].set_ylabel('Count')

sns.histplot(filtered_data['rate_commercial'], bins=5, kde=True, ax=axs[1])
axs[1].set_title('Commercial Rating Distribution')
axs[1].set_xlabel('Commercial Rating')
axs[1].set_ylabel('Count')

sns.histplot(filtered_data['rate_density'], bins=10, kde=True, ax=axs[2])
axs[2].set_title('Density Rating Distribution')
axs[2].set_xlabel('Density Rating')
axs[2].set_ylabel('Count')

plt.tight_layout()
st.pyplot(fig)

# Radar chart for months reported
st.subheader("Radar Chart for Reported Months")

# Process the month data
all_months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
month_counts = {month: 0 for month in all_months}

for months in filtered_data['reported_months'].dropna():
    for month in months.split(', '):
        month_counts[month] += 1

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=list(month_counts.values()),
    theta=list(month_counts.keys()),
    fill='toself',
    name='Reported Months'
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, max(month_counts.values())]
        )),
    showlegend=False
)

st.plotly_chart(fig)

# Word cloud for descriptive columns


def generate_wordcloud(text):
    stopwords = set(STOPWORDS)
    stopwords.update(['areas', 'description', 'describe', 'people', 'evenly'])
    stopwords.remove('no')
    stopwords.remove('not')
    wordcloud = WordCloud(
        stopwords=stopwords, background_color='white', width=800, height=400).generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()


# wordcloud select box
wordcloud_columns = ['describe_greenery', 'describe_why_cooler', 'describe_indoor_cooling_methods', 'describe_indoor_improvements', 'describe_outdoor_improvements', 'describe_health_effect',
                     'describe_routine_alteration', 'describe_recovery_measures']
selected_word_cloud = st.selectbox(
    "Select Word Cloud", options=wordcloud_columns)

st.subheader(f"Word Cloud for {selected_word_cloud}")

# Combine all descriptions into a single string
combined_text = ' '.join(
    filtered_data[selected_word_cloud].dropna().astype(str))
generate_wordcloud(combined_text)
st.pyplot()

# Detailed area description
st.subheader("List of Reported Areas")
for idx, row in filtered_data.iterrows():
    st.write(f"{row['area']} (Zipcode: {row['zipcode']})")

# Note: No need for `st.run()`
