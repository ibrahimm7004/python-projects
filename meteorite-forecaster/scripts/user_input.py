import pandas as pd

df = pd.read_csv('C:/Users/hp/Desktop/uni/sem4/ds_proj/excel_files/predicted_dataset1.csv')

cols = ['Radius', 'Volume', 'Density', 'Mass', 'Velocity', 'Radiated Energy', 'Impact Energy']

df = df.sort_values(by=['Impact Energy'])

diff = df['Impact Energy'].diff()

# Select the 20 rows with the largest gaps between consecutive 'Impact Energy' values
idx = diff.nlargest(20).index

# Extract the desired columns for the selected rows
cols = ['Radius', 'Volume', 'Density', 'Mass', 'Velocity', 'Radiated Energy', 'Impact Energy']
df_new = df.loc[idx, cols]

df_new.to_csv('C:/Users/hp/Desktop/uni/sem4/ds_proj/excel_files/output.csv', index=False)


