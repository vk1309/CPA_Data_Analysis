import matplotlib.pyplot as plt
import logging

class MonthWiseComparison:
  @staticmethod
  def numberOfCancelledMeetingsByMonth(merged_df):
    # Group data by month and cancelled status
    grouped_df = merged_df.groupby('Month')['Cancelled?'].value_counts()

    # Plot bar graph
    ax = grouped_df.unstack().plot(kind='bar')
    for i in ax.containers:
        ax.bar_label(i, label_type='edge')

    ax.set_ylabel('Count')
    ax.set_xlabel('Month')
    #plt.subplots_adjust(left=0.107, bottom=0.286, right=0.567, top=0.933, wspace=0.2, hspace=0.2)
    plt.show()
    # plt.savefig("numberOfCancelledMeetingsByMonth.png")
    # plt.close()

  @staticmethod
  def numberOfStudentsByCampusByMonth(merged_df):
    # Group data by month and campus
    grouped_df = merged_df.groupby(['Month', 'Campus']).size().unstack()

    # Plot bar graph
    plt.figure(figsize=(12, 6))
    ax = grouped_df.plot(kind='bar', stacked=True)
    ax.set_ylabel('Count')
    ax.set_xlabel('Month')
    ax.set_title('Distribution of Campuses Month-wise')

    plt.legend(title='Campus', bbox_to_anchor=(1, 1))
    plt.xticks(rotation=45, ha='right')

    # plt.tight_layout()
    plt.show()
    # plt.savefig("DistributionOfCampusesMonthWise.png")
    # plt.close()

  
  @staticmethod
  def numberOfServicesByCampusByMonth(merged_df):
    # Group data by month and campus
    grouped_df = merged_df.groupby(['Month', 'Scheduled Services']).size().unstack()

    # Plot bar graph
    plt.figure(figsize=(12, 6))
    ax = grouped_df.plot(kind='bar', stacked=True)
    ax.set_ylabel('Count')
    ax.set_xlabel('Month')
    ax.set_title('Distribution of Campuses Scheduled Services wise')

    plt.legend(title='Campus', bbox_to_anchor=(1, 1))
    plt.xticks(rotation=45, ha='right')

    # plt.tight_layout()
    plt.show()
    # plt.savefig("DistributionOfCampusesScheduledServicesWise.png")
    # plt.close()


  @staticmethod
  def numberOfStudentsFromDifferentProgramsByMonth(merged_df):
    # Group data by month and campus
    grouped_df = merged_df.groupby(['Month', 'Program of Study']).size().unstack()

    # Plot bar graph
    plt.figure(figsize=(12, 6))
    ax = grouped_df.plot(kind='bar', stacked=True)
    ax.set_ylabel('Count')
    ax.set_xlabel('Month')
    ax.set_title('Distribution of Campuses Program wise')

    plt.legend(title='Campus', bbox_to_anchor=(1, 1))
    plt.xticks(rotation=45, ha='right')
    plt.show()
    # plt.savefig("numberOfStudentsFromDifferentProgramsByMonth.png")
    # plt.close()