import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Importing raw data
url = "https://raw.githubusercontent.com/a-mt/fcc-medical-data-visualizer/master/medical_examination.csv"
df = pd.read_csv(url)
df.dropna(how = 'any')

# Calculate bmi
bmi_cal = df['weight'] / (df['height'] / 100) ** 2
# If bmi > 25, the person is considered as OVERWEIGHT. Otherwise, people with bmi < 25 is considered NOT OVERWEIGTH. Define OVERWEIGHT as 1, and NOT OVERWEIGHT as 0
bmi_cal[bmi_cal < 25] = 0
bmi_cal[bmi_cal >= 25] = 1
# Assigning bmi data to dataframe new column 'overweight'
df['overweight'] = bmi_cal

#Normalize the data by making 0 always good and 1 always bad.
#If the value = 1, the value taken as 0. If the value > 1, the value taken as 1.
# normalizing glucose data
df.loc[df.cholesterol == 1, 'cholesterol'] = 0
df.loc[df.cholesterol > 1, 'cholesterol'] = 1

# normalizing cholesterol data
df.loc[df.gluc == 1, 'gluc'] = 0
df.loc[df.gluc > 1, 'gluc'] = 1

# Create Seaborn Catplot
def draw_catplot():
  # Create DataFrame for cat plot using `pd.melt` using the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
  df_cat = pd.melt(df,
                   id_vars='cardio',
                   var_name='variable',
                   value_vars=[
                     'alco', 'active', 'cholesterol', 'gluc', 'overweight',
                     'smoke'
                   ])
  # Group and reformat the data to split it by 'cardio'. Show the counts of each feature.
  df_cat = pd.melt(df,
                   var_name='variable',
                   value_vars=[
                     'active', 'alco', 'cholesterol', 'gluc', 'overweight',
                     'smoke'
                   ],
                   id_vars='cardio')
  # Draw the catplot
  fig = sns.catplot(data=df_cat,
                    kind="count",
                    x="variable",
                    hue="value",
                    col="cardio").set_axis_labels("variable", "total")
  fig = fig.fig
  # Save the Catplot figure
  fig.savefig('catplot.png')
  return fig


# Draw Heat Map
def draw_heatmap():
    df2 = df.copy()
   
    # Keep only the following patient segments that represent correct data
    df_heat = df2[(df2['ap_lo'] <= df2['ap_hi']) & 
                (df2['height'] >= df2['height'].quantile(0.025)) & (df2['height'] <= df2['height'].quantile(0.975)) & 
                (df2['weight'] >= df2['weight'].quantile(0.025)) & (df2['weight'] <= df2['weight'].quantile(0.975))]

    # calculate correlation matrix and store it in corr dataframe
    corr = df_heat.corr()
    
    # Set up the matplotlib figure
    plt.figure(figsize = (12,6))
    sns.set(rc={'axes.facecolor':'white', 'figure.facecolor':'white'})

    # Generate a mask for the upper triangle
    # ones_like builds a matrix of booleans with the same shape as corr
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Draw the heatmap with 'sns.heatmap()'
    fig = sns.heatmap(corr, mask=mask, square=True, linewidths=1, center=0.0, vmin=-0.1, vmax=0.3, annot=True, fmt='.1f').get_figure()

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig

