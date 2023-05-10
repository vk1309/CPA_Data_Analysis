import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import date


# 'Program of Study',
# 'Admit Term', 
# 'Campus', 
# 'Had Appointment?',
# 'Care Unit',
# 'Scheduled Services',
# 'Scheduled Course Name',
# 'Scheduled Course Number',
# 'Location',
# 'Scheduled Meeting Type',
# 'Appointment Type',
# 'Appointment Created By', 
# 'Appointment Comment',
# 'Attendance Created By', 
# 'Staff Organizer Name', 
# 'Staff Organizer ID',
# 'Staff Organizer Email',
# 'Cancelled?', 
# 'Cancellation Reason',
# 'Cancellation Comment', 
# 'Cancelled By', 
# 'Month'

class CpaDataAnalysis:
  def __init__(self, files, updateProgressBar, updateStatus):
    self.files = files
    self.updateProgressBar = updateProgressBar
    # self.dfs = {}
    self.updateStatus = updateStatus

  def preprocessor(self, file):
    # add month column to df and strip campus whitespace
    curFile = pd.read_excel(file)
    month = file.split("/")[-1].split(".")[0]
    curFile["Month"] = month.lower().capitalize()
    curFile['Campus'] = curFile['Campus'].apply(lambda x: x.strip())
    return curFile

  def getMonthChart(self, file):

    try:     
      df = self.preprocessor(file)
      # self.dfs[file] = df
      targetColumns = ['Program of Study','Campus','Care Unit','Scheduled Services','Had Appointment?', "Cancelled?"]
      # create folder with file name and change directory
      month = file.split("/")[-1].split(".")[0]
      os.chdir(os.getcwd())
      os.mkdir(month)
      os.chdir(f"{os.getcwd()}/{month}")
      for col in targetColumns:
        # Create a new DataFrame that groups the data by the values in the column
        grouped_df = df.groupby(col).size().reset_index(name='counts').sort_values(by='counts', ascending=False)
        
        # Set the plot style
        plt.style.use('ggplot')
        
        plt.figure(figsize=(20,6))

        # Create a bar plot of the counts
        # limit pandas bar plot width
        bars = plt.bar(grouped_df[col], grouped_df['counts'], color=(0.2, 0.4, 0.6, 0.6))
        
        # Set the x-axis label
        plt.xlabel(col)

        # Set the y-axis label
        plt.ylabel('Count')
        plotTitle = f'Counts by {col}'
        plt.title(plotTitle)

        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + 0.35, yval + 0.5, yval)
        
        # Show the plot
        # plt.show()
        # save plot
        plt.savefig(f"{plotTitle}.png")
      self.updateProgressBar()
      self.updateStatus(f"Finished plotting for {file}")
      os.chdir("../")
    except Exception as e:
      print("Error processing data frame...")
      self.updateStatus(f"Error when processing individual monthly data")

  def getMonthComparisons(self):
    pass

  # main function
  def run(self):
    # create folder to save files
    for file in self.files:
      print(file)
      self.getMonthChart(file)
    self.updateStatus("Done!")

