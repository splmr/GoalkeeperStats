import pandas as pd
import matplotlib.pyplot as plot
import seaborn as graph
from adjustText import adjust_text

graph.set(style="whitegrid")

# load data through csv
csvData = pd.read_csv('/Users//Documents/gkStats.csv', sep=',', header=0)


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

# Define the plotting function
def plot_graph(x, y, x_label, y_label, title, filename):
    plot.figure(figsize=(14, 10))
    graph.scatterplot(x=x, y=y, data=data_sorted, hue='Squad', palette=palette, s=100)

    plot.title(title, fontsize=18)
    plot.xlabel(x_label, fontsize=14)
    plot.ylabel(y_label, fontsize=14)

    texts = []
    for i in range(data_sorted.shape[0]):
        text = plot.text(data_sorted[x].iloc[i], data_sorted[y].iloc[i],
                         data_sorted['Squad'].iloc[i],
                         horizontalalignment='center',
                         size='medium',
                         color='black',
                         weight='light')
        texts.append(text)

    adjust_text(texts)
    plot.legend(title='Squad', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
    plot.tight_layout()
    #   save graphs as png to specified file location
   # plot.savefig(f'/Users//Documents/{filename}.png', dpi=300, bbox_inches='tight')
    plot.show()

# Plot Save% vs Clean Sheet %
plot_graph('Save%', 'Clean Sheet %', 'Save Percentage (%)', 'Clean Sheet Percentage (%)',
           'Save Percentage vs Clean Sheet Percentage', 'save_percentage_vs_clean_sheet')

# Plot Save% vs Goals Against per 90 minutes (GA90)
plot_graph('Save%', 'GA90', 'Save Percentage (%)', 'Goals Against per 90 mins',
           'Save Percentage vs Goals Against per 90 mins', 'save_percentage_vs_ga90')

# Plot Saves vs Shots on Target Against (SoTA)
plot_graph('Saves', 'SoTA', 'Saves', 'Shots on Target Against',
           'Saves vs Shots on Target Against', 'saves_vs_sota')

# Plot Goals Against vs Clean Sheets
plot_graph('GA', 'CS', 'Goals Against', 'Clean Sheets',
           'Goals Against vs Clean Sheets', 'goals_against_vs_clean_sheets')

print("All graphs generated successfully")
