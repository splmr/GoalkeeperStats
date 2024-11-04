import pandas as pd
import matplotlib.pyplot as plot
import seaborn as graph
from adjustText import adjust_text

graph.set(style="whitegrid")

# load data through csv
csvData = pd.read_csv('/Users//Documents/GK_EPL_20_21.csv', sep=',', header=0)

# all the columns with values we care about
columns_to_convert = [
    'Matches', 'Starts', 'Mins', 'Goals', 'Assists', 'Passes_Attempted',
    'Perc_Passes_Completed', 'Yellow_Cards', 'Red_Cards'
]
csvData[columns_to_convert] = csvData[columns_to_convert].apply(pd.to_numeric, errors='coerce')

# calculate Passes per Start
csvData['Passes_per_Start'] = csvData['Passes_Attempted'] / csvData['Starts'].replace(0, float('nan'))

# sort data alphabetically by Name
data_sorted = csvData.sort_values(by='Name')

data_sorted = data_sorted.dropna(subset=['Passes_per_Start', 'Perc_Passes_Completed'])

# Define color palette based on unique clubs
unique_clubs = data_sorted['Club'].unique()
palette = graph.color_palette("husl", len(unique_clubs))

#graph settings
plot.figure(figsize=(14, 10))
graph.scatterplot(x='Passes_per_Start', y='Perc_Passes_Completed', data=data_sorted, hue='Club', palette=palette, s=100)

# titles and axis
plot.title('Passes per Start vs Pass Completion Percentage', fontsize=18)
plot.xlabel('Passes per Start', fontsize=14)
plot.ylabel('Pass Completion Percentage (%)', fontsize=14)

# add names above points
texts = []
for i in range(data_sorted.shape[0]):
    text = plot.text(data_sorted['Passes_per_Start'].iloc[i],
                     data_sorted['Perc_Passes_Completed'].iloc[i],
                     data_sorted['Name'].iloc[i],
                     horizontalalignment='center', size='medium', color='black', weight='light')
    texts.append(text)
adjust_text(texts, expand_text=(1.05, 1.2), expand_points=(1.2, 1.3), force_text=0.5, arrowprops=dict(arrowstyle='-', color='gray', lw=0.5))

# add key
plot.legend(title='Club', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
plot.tight_layout()
plot.savefig('/Users//Documents/passesVsPass%.png', dpi=300, bbox_inches='tight')
print("Plot ran successfully")
plot.show()
