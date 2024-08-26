import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
from datetime import timedelta
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import nltk
import os

# Get the current working directory
current_dir = os.getcwd()
data_path = os.path.join(current_dir, 'Consumer Complaint Database', 'Cleaned_CCDB.csv')

# Load the data
df = pd.read_csv(data_path)


#%% Most common complaints and sub-issues

# Analyze top 10 most common types of complaints
complaint_counts = df['Product'].value_counts().nlargest(10)


# Create a bar plot
plt.figure(figsize=(14, 10))
sns.barplot(x=complaint_counts.index, y=complaint_counts.values)
plt.title('Top 10 Product Categories by Number of Complaints', fontsize=16)
plt.xlabel('Product Category', fontsize=12)
plt.ylabel('Number of Complaints', fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=10)
max_count = complaint_counts.max()
plt.ylim(0, max_count * 1.1)
plt.tight_layout()
plt.show()

# Analyze sub-issues within the most common product category
top_product = complaint_counts.index[0]
sub_issue_counts = df[df['Product'] == top_product]['Sub_Issue'].value_counts().nlargest(10)

plt.figure(figsize=(14, 10))
sns.barplot(x=sub_issue_counts.index, y=sub_issue_counts.values)
plt.title(f'Top 10 Sub-Issues for {top_product}', fontsize=16)
plt.xlabel('Sub-Issue', fontsize=12)
plt.ylabel('Number of Complaints', fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=10)
max_count = sub_issue_counts.max()
plt.ylim(0, max_count * 1.1)
plt.tight_layout()
plt.show()

#%% Time-based trends and information


# Convert date columns to datetime
df['Date_Received'] = pd.to_datetime(df['Date_Received'])
df['Date_Submitted'] = pd.to_datetime(df['Date_Submitted'])

# Group by month and count complaints
monthly_complaints = df.resample('ME', on='Date_Received').size()

# Plot time series
plt.figure(figsize=(16, 8))
sns.lineplot(x=monthly_complaints.index, y=monthly_complaints.values, marker='o')
plt.title('Number of Complaints by Month', fontsize=16)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Number of Complaints', fontsize=12)
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)
for i, v in enumerate(monthly_complaints.values):
    plt.text(monthly_complaints.index[i], v, f'{v:,}', ha='center', va='bottom')
plt.tight_layout()
plt.show()

# Daily Trend
daily_complaints = df.resample('D', on='Date_Received').size()

plt.figure(figsize=(20, 8))
sns.lineplot(x=daily_complaints.index, y=daily_complaints.values)
plt.title('Number of Complaints by Day', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Number of Complaints', fontsize=12)
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Day of Week Analysis
df['Day_of_Week'] = df['Date_Received'].dt.dayofweek
day_of_week_counts = df.groupby('Day_of_Week').size()
day_of_week_counts = day_of_week_counts.reindex(range(7), fill_value=0)  # Ensure all days are included

# Calculate the number of each day in the dataset
date_range = pd.date_range(start=df['Date_Received'].min(), end=df['Date_Received'].max())
day_counts = pd.Series([d.dayofweek for d in date_range]).value_counts().sort_index()

# Calculate average
day_of_week_avg = (day_of_week_counts / day_counts).reset_index()
day_of_week_avg.columns = ['Day_of_Week', 'Avg_Complaints']
day_of_week_avg['Day_Name'] = day_of_week_avg['Day_of_Week'].apply(lambda x: calendar.day_name[x])

plt.figure(figsize=(14, 8))
sns.barplot(x='Day_Name', y='Avg_Complaints', data=day_of_week_avg, 
            order=[calendar.day_name[i] for i in range(7)])
plt.title('Average Number of Complaints by Day of Week', fontsize=16)
plt.xlabel('Day of Week', fontsize=12)
plt.ylabel('Average Number of Complaints', fontsize=12)
plt.xticks(rotation=0)
for i, v in enumerate(day_of_week_avg['Avg_Complaints']):
    plt.text(i, v, f'{v:.1f}', ha='center', va='bottom')
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Monthly Distribution
df['Month'] = df['Date_Received'].dt.month
monthly_counts = df.groupby('Month').size().reset_index(name='Complaints')
monthly_counts['Month_Name'] = monthly_counts['Month'].apply(lambda x: calendar.month_abbr[x])

# Create a custom order for months from August to July
month_order = [calendar.month_abbr[i] for i in list(range(8, 13)) + list(range(1, 8))]

# Reorder the dataframe
monthly_counts['Month_Order'] = monthly_counts['Month'].apply(lambda x: (x - 8) % 12)
monthly_counts = monthly_counts.sort_values('Month_Order')

plt.figure(figsize=(14, 8))
sns.barplot(x='Month_Name', y='Complaints', data=monthly_counts, order=month_order)
plt.title('Number of Complaints by Month (August to July)', fontsize=16)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Number of Complaints', fontsize=12)
plt.xticks(rotation=0)

for i, v in enumerate(monthly_counts['Complaints']):
    plt.text(i, v, f'{v:,}', ha='center', va='bottom')

plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Heatmap of complaints by day of week and month
df['DayOfWeek'] = df['Date_Received'].dt.dayofweek
df['Month'] = df['Date_Received'].dt.month
heatmap_data = df.groupby(['Month', 'DayOfWeek']).size().unstack()
heatmap_data.index = heatmap_data.index.map(lambda x: calendar.month_abbr[x])
heatmap_data.columns = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

plt.figure(figsize=(16, 10))
sns.heatmap(heatmap_data, cmap='YlOrRd', annot=True, fmt='g')
plt.title('Heatmap of Complaints by Day of Week and Month', fontsize=16)
plt.xlabel('Day of Week', fontsize=12)
plt.ylabel('Month', fontsize=12)
plt.tight_layout()
plt.show()


#%% Text analysis

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Combine all narratives
text = ' '.join(df['Consumer_Narrative'].dropna())

# Get the default English stopwords
stop_words = set(stopwords.words('english'))

# Add custom words to remove
custom_stop_words = {'xxxx', 'xx', 'xxx'}  # Add any other unhelpful words here
stop_words = stop_words.union(custom_stop_words)

# Tokenize and remove stopwords
word_tokens = word_tokenize(text.lower())
filtered_text = [word for word in word_tokens if word.isalnum() and word not in stop_words]

# Count word frequencies
word_freq = Counter(filtered_text)

# Get the 20 most common words
top_words = word_freq.most_common(20)

# Create a bar plot of the most common words
plt.figure(figsize=(12, 6))
sns.barplot(x=[word for word, freq in top_words], y=[freq for word, freq in top_words])
plt.title('Top 20 Most Common Words in Consumer Narratives', fontsize=16)
plt.xlabel('Words', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Analyze most common bigrams
bigrams = list(nltk.bigrams(filtered_text))
bigram_freq = Counter(bigrams)

# Function to group similar legal references
def group_legal_references(bigram):
    word1, word2 = bigram
    if word1 == '15' and word2 in ['usc', 'code', '1681']:
        return ('15_USC', 1)
    elif word1 == '1681' and word2 == 'section':
        return ('1681_section', 1)
    else:
        return (bigram, 1)

# Group similar legal references in bigrams
grouped_bigrams = Counter()
for bigram, count in bigram_freq.items():
    grouped_bigram, _ = group_legal_references(bigram)
    grouped_bigrams[grouped_bigram] += count

# Get the 20 most common grouped bigrams
top_grouped_bigrams = grouped_bigrams.most_common(20)

# Create a bar plot of the most common grouped bigrams
plt.figure(figsize=(12, 6))
sns.barplot(x=[' '.join(bigram) if isinstance(bigram, tuple) else bigram for bigram, freq in top_grouped_bigrams], 
            y=[freq for bigram, freq in top_grouped_bigrams])
plt.title('Top 20 Most Common Bigrams (Grouped Legal References)', fontsize=16)
plt.xlabel('Bigrams', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

