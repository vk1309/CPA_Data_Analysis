import pandas as pd
import matplotlib.pyplot as plt
import os
from MonthWiseComparison import MonthWiseComparison
from AggregatedStatistics import AggregatedStatistics
import logging

class CpaDataAnalysis:
  def __init__(self, files, updateProgressBar, updateStatus):
    self.files = files
    self.updateProgressBar = updateProgressBar
    self.updateStatus = updateStatus
    self.error = ""

  def preprocessor(self, file):
    # add month column to df and strip campus whitespace
    logging.info(f"Reading in {file}")
    curFile = pd.read_excel(file)
    month = file.split("/")[-1].split(".")[0]
    curFile["Month"] = month.lower().capitalize()
    curFile['Campus'] = curFile['Campus'].apply(lambda x: x.strip())
    logging.info(f"{file} preprocessing finished")
    return curFile

  def getMonthChart(self, file):
    try:     
      df = self.preprocessor(file)
      targetColumns = ['Program of Study','Campus','Care Unit','Scheduled Services','Had Appointment?', "Cancelled?"]
      # create folder with file name and change directory
      month = file.split("/")[-1].split(".")[0]
      os.chdir(os.getcwd())
      os.mkdir(month)
      os.chdir(f"{os.getcwd()}/{month}")
      logging.info(f"Created folder, and plot month chart.")

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
        
        # save plot
        plt.savefig(f"{plotTitle}.png")
        plt.close()


      self.updateProgressBar()
      self.updateStatus(f"Finished plotting for {file}")
      os.chdir("../")
    except Exception as e:
      self.error = "Error when processing individual monthly data"

  def mergeMonths(self):
    commonColumns = set()
    dfs = []
    for file in self.files:
      curDf = self.preprocessor(file)
      dfs.append(curDf)
      if len(commonColumns) == 0:
        commonColumns = set(curDf.columns)
      else:
        commonColumns = commonColumns.intersection(curDf.columns)
    
    commonColumns = list(commonColumns)

    resDf = pd.DataFrame()
    if len(dfs) > 0:
      resDf = dfs[0]
    else:
      raise ValueError("")
      
    # merge all pd dataframes
    for i in range(1, len(dfs)):
      resDf = pd.merge(resDf, dfs[i], on=commonColumns, how='outer')

    # data cleaning
    resDf = resDf.replace('MS Computer Science - Align', 'MSCS Computer Science - Align') 

    return resDf

  def getMonthComparisons(self, resDf):
    try:
      logging.info("Plot month wise comparison chart")
      # plot comparison graphs
      MonthWiseComparison.numberOfCancelledMeetingsByMonth(resDf)
      MonthWiseComparison.numberOfStudentsByCampusByMonth(resDf) 
      MonthWiseComparison.numberOfServicesByCampusByMonth(resDf)
      MonthWiseComparison.numberOfStudentsFromDifferentProgramsByMonth(resDf)
      logging.info("Finish plotting month wise comparison chart.")
      self.updateProgressBar()
      self.updateStatus("Sucessfully finished monthwise comparison")
    except Exception as e:
      logging.exception(f"month wise comparison failed with exception : {e}")
      self.error = f"Error happened when plotting: {e}" 
      
  def getAggregatedChart(self):
    charts = [
      {
        "xlabel": "Location",
        "ylabel": "Count",
        "title": "Counts by Location",
        "aggregateCol": "Location",
        "figSize": (10,7)
      },
      {
        "xlabel": "Program of Study",
        "ylabel": "Count",
        "title": "Counts by Program of Study",
        "aggregateCol": "Program of Study",
        "figSize": (10,7)
      },
      {
        "xlabel": "Scheduled Services",
        "ylabel": "Count",
        "title": "Counts by Scheduled Services",
        "aggregateCol": "Scheduled Services",
        "figSize": (10, 8)
      },
      {
        "xlabel": "Appointments Cancelled",
        "ylabel": "Count",
        "title": "Counts by Cancelled or not",
        "aggregateCol": "Cancelled?",
        "figSize": (10,7)
      },
      {
        "xlabel": "Staff name",
        "ylabel": "Count",
        "title": "Counts by Assigned Staff",
        "aggregateCol": "Assigned Staff",
        "figSize": (10,7)  
      },
      {
        "xlabel": "Admit Term",
        "ylabel": "Count",
        "title": "Counts by Admit Term",
        "aggregateCol": "Admit Term",
        "figSize": (10,7)  
      },
      {
        "xlabel": "Month",
        "ylabel": "Count",
        "title": "Counts by Monthwise Distribution",
        "aggregateCol": "Month",
        "figSize": (10,7)  
      }
    ]
    # change directory
    os.chdir(os.getcwd())
    folderName = "Aggregated Charts"
    os.mkdir(folderName)
    os.chdir(f"{os.getcwd()}/{folderName}") 
    # save aggregated charts
    for chartData in charts:
      try:
        AggregatedStatistics.getAggregatedChart(self.resDf, chartData["xlabel"], chartData["ylabel"], chartData["title"], chartData["aggregateCol"], chartData["figSize"])
      except Exception as e:
        errMsg = "Aggregated chart: {chartData['title']}, failed with exception : {e}"
        print(errMsg)
        logging.exception(errMsg)
        continue

    os.chdir("../")

  # main function
  def run(self):
    try:
      # get month chart
      for file in self.files:
        self.getMonthChart(file)

      # get month wise comparison chart
      mergedDf = self.mergeMonths()
      self.getMonthComparisons(mergedDf)
      self.updateStatus("Done!")
    except:
      self.updateStatus(self.error)
      




