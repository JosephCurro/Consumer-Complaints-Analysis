# Consumer Complaints Database Analysis

## Project Overview
This project analyzes consumer complaint data from the Consumer Financial Protection Bureau (CFPB) for the state of California from August 1st 2023 to July 31st 2024. The analysis aims to uncover patterns in consumer complaints, identify common issues, and visualize trends over time.

## Data Source
The data used in this project comes from the Consumer Complaints Database hosted by the CFPB. It contains detailed information about consumer complaints regarding financial products and services.

Key Features
- Comprehensive data cleaning and preprocessing using MySQL
- Analysis of complaint categories and sub-issues
- Time-based trend analysis (daily, monthly, day of week)
- Text analysis of consumer narratives using natural language processing techniques
- Visualizations including bar plots, time series plots, and heatmaps

## Tools and Technologies Used
- MySQL for data cleaning and transformation
- Python for data analysis and visualization
- Libraries: pandas, matplotlib, seaborn, nltk

## Project Structure
1. Data Cleaning (MySQL)
   - Handling null/blank values
   - Standardizing text formats
   - Converting date formats
   - Removing unnecessary columns
   - Creating appropriate indexes

2. Data Analysis (Python)
   - Top complaint categories analysis
   - Time-based trend analysis (daily, monthly, day of week)
   - Text analysis of consumer narratives

3. Visualizations
   - Bar plots for top products and sub-issues
   - Time series plots for complaint trends
   - Heatmap for complaints by day and month
   - Word frequency and bigram analyses of consumer narratives

## Key Findings
- 'Credit reporting or other personal consumer benefits' itself accounts for nearly 60% of all complaints, dwarfing the next highest number of complaints.
- The top sub-issue within this complaint is 'information belongs to someone else', with several of the other top sub-issues being incorrect information or reporting. 
- There is an increase in number of complaints consistently from December through May, peaking at 7,380 complaints in May.
- Tuesday is on average the day with the most complaints received, while Sunday is the lowest.
- Some of the most common consumer narrative words and bigrams used make references to accessing credit reports, information about their account, and 15 U.S. Code § 1681a (defines terms used in the Fair Credit Reporting Act, enforced by the Consumer Financial Protection Bureau).
- After the peak in May, there is a steep drop into June and July for number of complaints. This is likely a result of incomplete data.

## Interpretation
- The trend of complaints rising from mid-winter to mid-spring aligns with tax season and typical financial review periods, may indicate a correlation.
- The combination of 'information belongs to someone else' being the top sub-issue within 'credit reporting or other personal consumer reports' and identity theft being the sixth most common bigram point to a need to enhance identity verification methods.
- The steep drop-off in complaints during June and July is likely an issue of data lag rather than a real life trend. The dataset cuts off on August 1st, 2024 which likely left out data from those months the bureau has yet to include. 

## Future Work
- Update the dataset with current information
- Account for data lag in the number of complaints received over the recent months.
- Analyze response times and outcomes of complaints.
- Investigate geographical patterns using ZIP code data (may need to filter only for data that does not anonymize the ZIP).
- Perform sentiment analysis on consumer narratives.
- Compare state-level data with national trends, and compare this year to previous years to find patterns.
- Do text analysis of complaints with the 'information belongs to someone else' sub-issue to determine if problem is linked to identity theft or due to a more benign error.

## How to Run
1. Execute the MySQL script to clean and transform the data
2. Run the Python scripts to perform analysis and generate visualizations

## Dependencies
- MySQL
- Python 3.12
- pandas
- matplotlib
- seaborn
- nltk
- os

## Contact
Joseph Curro
josephjcurro@gmail.com
