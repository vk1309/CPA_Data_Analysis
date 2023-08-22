import matplotlib.pyplot as plt

class AggregatedStatistics:  
  @staticmethod
  def getAggregatedChart(resDf, xlabel, ylabel, title, aggregateCol, figSize):
    value_counts = resDf[aggregateCol].value_counts()
    # Plot bar graph
    plt.figure(figsize=figSize)
    ax = value_counts.plot(kind='bar')
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    plt.xticks(rotation=45, ha='right')

    # Add value labels to the bars
    for i, count in enumerate(value_counts):
        ax.text(i, count + 0.25, str(count), ha='center')
    plt.show()
    # plt.savefig(f"{title}.png")
    # plt.close()

