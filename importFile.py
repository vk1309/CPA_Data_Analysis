import pandas as pd
import os 

# STAFF_NAME_TO_CAMPUS_MAP = {
#   "Chidsey, Patrick (Co-op Advisor)": "Seattle",
#   "Escalera, Austin (Graduate Advisor)": "Seattle",
#   "Winter, Megan (Graduate Advisor)": "Seattle",
#   "Mesch, Francisco (Co-op Advisor)": "Seattle",
#   "Ramakrishna, Ujwala (Graduate Advisor)": "Seattle",
#   "Gill, Michaela (Graduate Advisor)":	"Portland",
#   "Hunt, Kathleen (Co-op Advisor)": "Silicon Valley",
#   "Olson, Annastatius (Graduate Advisor)": "Silicon Valley",
#   "Xiong, Chung (Graduate Advisor)":	"Silicon Valley",
#   "Kelley, Cailyn (Graduate Advisor)":	"Boston",
#   "Selinger, Ethan (Co-op Advisor)":	"Boston",
#   "Poudiougou, Marie (Graduate Advisor)":	"Boston",
#   "Lambert, Alexis (Graduate Advisor)":	"Boston",
#   "Payamshad, Mahya (Graduate Advisor)":	"Vancouver",
# }


# CPA_NAME_TO_CAMPUS_MAP = {

# }

# files = os.listdir("/Users/justinlee/Desktop/cpa/")

class FileImporter:
  def __init__(self):
    self.files = []

  def start(self):
    res = input('please choose to import file via absolute filepath (1) or import a whole folder (2):')
    if res == str(1):
      self.addFile()
    if res == str(2):
      self.fetchAllFilesFromFolder()

  def addFile(self):
    while True:
      fileName = input("Please enter absolute path for file: ")
      self.files.append(fileName)
      pressed = input("press x to break")
      if pressed == "x":
        break


  def reset(self):
    self.files = []

  def fetchAllFilesFromFolder(self):
    try:
      folderPath = input("please enter full absoulte path of folder")
      allFiles = os.listdir(folderPath)
      for fileName in allFiles:
        self.files.append(os.path.join(folderPath, fileName))
    except Exception as e:
      print("Exception: ", e)



class CpaDataCleaner:
  OUTPUT_FILE_NAME = "cleaned.xlsx"

  def __init__(self,inputFilePath, staffNameToCampusMap, cpaNameToCampusMap):
    self.filePath = inputFilePath
    self.staffNameToCampusMap = staffNameToCampusMap 
    self.cpaNameToCampusMap = cpaNameToCampusMap 


  def readFile(self):
    self.file = pd.read_excel(self.filePath)
    # print(self.file)

  def cleanupAdmitTerm(self):
    # replace Admit Term: with empty string
    try:
      self.file['Admit Term'] = self.file['Admit Term'].apply(lambda row: row.split("Admit Term: ")[1])
      print("clean up admit term succeeded.")
    except:
      print("clean up admit term failed.")
  
  # use Assigned Staff to get StudentCampus column
  def addStudentCampusColumn(self):
    def getStudentCampus(data):
      for k,v in self.staffNameToCampusMap.items():
        if k in data:
          return v
      return ""
    try:
      print(self.file['Assigned Staff'])
      self.file['Student Campus'] = self.file['Assigned Staff'].apply(lambda x: getStudentCampus(x))
      print("add student campus column succeeded.")
    except Exception as e:
      print(f"add student campus column failed. {e}")

  # see which CPA's campus: Staff Organizer Name
  # use new column name: CPA Campus
  def addCpaCampusColumn(self):
    def cpaLookUp(key):
      key = key.lstrip().rstrip()
      if key not in self.cpaNameToCampusMap:
        return ''
      return self.cpaNameToCampusMap[key]
    try:
      self.file['CPA Campus'] = self.file['Staff Organizer Name'].apply(lambda x: cpaLookUp(x))
      print("add cpa campus column succeeded.")
    except:
      print("add cpa campus column failed.")

  # compare StudentCampus with CPA Campus ==> output boolean
  # if different, then True
  # Cross Campus
  def addIsCrossCampusAppointmentColumn(self):
    try:
      self.file['Cross Campus'] = self.file['CPA Campus'] != self.file['Student Campus']
      print("add cross campus column succeeded.")
    except:
      print("add cross campus column failed.")

  def write(self):
    try:
      self.file.to_excel(self.OUTPUT_FILE_NAME, index=False)
      print(f"Cleaned file has been saved to {self.OUTPUT_FILE_NAME}.")
    except:
      print("write failed.")

  def execute(self):
    self.readFile()
    self.cleanupAdmitTerm()
    self.addStudentCampusColumn()
    self.addCpaCampusColumn()
    self.addIsCrossCampusAppointmentColumn()
    # write


importer = FileImporter()
importer.start()
print(importer.files)

# def main():
#   try:
#     filePath = input("Input absolute file path of cpa data file: ")
#     dataCleaner = CpaDataCleaner(filePath, STAFF_NAME_TO_CAMPUS_MAP, CPA_NAME_TO_CAMPUS_MAP)
#     dataCleaner.execute()
#   except Exception as e:
#     print("Clean up failed")
#     print(e)


# if __name__ == "__main__":
#   main()





