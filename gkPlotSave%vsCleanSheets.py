"""A python program to analyse goalkeeper data from Premier League and plot save% against clean sheets
Though at first glance, a high save % may indicate a top class goalkeeper and thus a good defensive record
The fact a goalkeeper has had to make those saves could also mean a poor back line and therefore less clean sheets
We expect the top performing teams on both axis to be those near the top of the table
We expect the poorest performing teams on both axis to be those near the bottom of the table
However, I expect a jumble in the middle of the graph and therefore an unclear overall relationship

"""
import pandas as pd
import matplotlib.pyplot as plot
import seaborn as graph
from adjustText import adjust_text

graph.set(style="whitegrid")

# load data through csv
csvData = pd.read_csv('YOUR FILE PATHgkStats.csv', sep=',', header=0)

# output data from first rows
print("Test data entries:")
print(csvData.head())

# all the columns with values we care about
columns_to_convert = ['GA', 'GA90', 'SoTA', 'Saves', 'Save%', 'W', 'D', 'L', 'CS', 'CS%', 'MP']

# pandas automatically converts to ints (if all values are whole like matches played) or floats if decimal points (% saves)
csvData[columns_to_convert] = csvData[columns_to_convert].apply(pd.to_numeric, errors='coerce')

# calculate our percentages using * 100
csvData['Save%'] = csvData['Saves'] / csvData['SoTA'].replace(0, float('nan')) * 100
csvData['Clean Sheet %'] = csvData['CS'] / csvData['MP'].replace(0, float('nan')) * 100

# sort alphabetically by team name to give a clear colour key
data_sorted = csvData.sort_values(by='Squad')
unique_squads = data_sorted['Squad'].unique()
palette = graph.color_palette("husl", len(unique_squads))

plot.figure(figsize=(14, 10)) # size for graph

# Using scatterplot
graph.scatterplot(x='Save%', y='Clean Sheet %', data=data_sorted, hue='Squad', palette=palette, s=100)

# addintg titles to axis
plot.title('Save Percentage vs Clean Sheet Percentage', fontsize=18)
plot.xlabel('Save Percentage (%)', fontsize=14)
plot.ylabel('Clean Sheet Percentage (%)', fontsize=14)

texts = []
# Add team names above the points to distinguish more clearly between teams
for i in range(data_sorted.shape[0]):
    text = plot.text(data_sorted['Save%'].iloc[i], data_sorted['Clean Sheet %'].iloc[i],
                     data_sorted['Squad'].iloc[i],
                     horizontalalignment='center',
                     size='medium',
                     color='black',
                     weight='light')
    texts.append(text)  # Store the text object for adjustment

# Using the adjust_text library to buffer text so no overlapping
adjust_text(texts)
# create a key for team name and colour
plot.legend(title='Squad', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
plot.tight_layout()  # Adjust layout to make sure everything fits
print("ran successfully")
#uncomment below to save graph (change file path)
#plot.savefig('/Users//Documents/save_percentage_vs_clean_sheet.png', dpi=300, bbox_inches='tight')  #
plot.show()
