'''
CPA Report Generator

Constructs a GUI based on Tkinter to allow users to upload monthly CPA reports and generate graphs and 
potentially a pdf report based on the data.
'''

import os
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.messagebox import showinfo


class App(tk.Tk):
    
    WIDTH =800
    HEIGHT = 500
    ALLOWED_FILES = [("Excel files", "*.xlsx"), ("XLS files", "*.xls")]
    selectedFiles = set()
    LEFT_BG_COLOR = "#0B2447"
    RIGHT_BG_COLOR = "#F6F1F1"
    errors = []

    def __init__(self):
        super().__init__()
        self.title("Career Peer Advisor Report Generator")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}") 
        self.generateInitLayout()


    def generateReport(self):
      print(self.selectedFiles)
      self.startProgressBar()
    
    def generateInitLayout(self):
      # left layout 
      self.leftFrame = tk.Frame(self, width=400, height=500, bg=self.LEFT_BG_COLOR)
      self.leftFrame .pack(side="left", fill="both", expand=True)
      # right layout
      self.rightFrame = tk.Frame(master=self, width=200, height=500, bg=self.RIGHT_BG_COLOR)
      self.rightFrame.pack(side="left", fill="both", expand=True)
      self.populateLeftLayout()
      self.populateRightLayout()
      
    # width: 400 * 500 
    def populateLeftLayout(self):
      self.createFileOrDirectoryUploadOption()
        
    
    # width: 200 * 500
    def populateRightLayout(self):
      #padx=10, pady=5
      tk.Label(master=self.rightFrame, bg=self.RIGHT_BG_COLOR, fg="black", text="Selected Files", font=("Arial", 30)).pack()
      # selected files
      self.selectedFilesFrame = tk.Frame(master=self.rightFrame, bg=self.RIGHT_BG_COLOR)
      self.selectedFilesFrame.pack(fill="both", expand=True)
      # generate report btn
      style = ttk.Style()
      style.configure("Custom.TButton", background=self.RIGHT_BG_COLOR, foreground="black", font=("Arial", 15), padding=5)
      style.map("Custom.TButton", foreground=[('pressed', 'green')])

      button = ttk.Button(master=self.rightFrame, text="Generate Report", style="Custom.TButton", command=self.generateReport)
      button.pack(pady=20)

      # progress bar
      self.progressBar = ttk.Progressbar(master=self.rightFrame, orient="horizontal", length=200, mode="determinate")
      self.progressBar.pack(pady=(5,0))

      # status of processing
      self.processStatus = tk.Label(master=self.rightFrame, bg=self.RIGHT_BG_COLOR, fg="black", text="", font=("Arial", 15)).pack(pady=10)


    def startProgressBar(self):
        # progress bar information
        PROGRESSBAR_MIN = 0
        PROGRESSBAR_MAX = 5000
        self.bytes = PROGRESSBAR_MIN
        self.maxbytes = PROGRESSBAR_MAX
        self.progressBar["value"] = PROGRESSBAR_MIN
        self.progressBar["maximum"] = PROGRESSBAR_MAX
        self.updateProgressBar()


    def updateProgressBar(self):
        '''simulate reading 500 bytes; update progress bar'''
        self.bytes += 500
        self.progressBar["value"] = self.bytes
        if self.bytes < self.maxbytes:
            self.after(200, self.updateProgressBar) # call itself after 100 ms


    def createFileOrDirectoryUploadOption(self):
        FILE = "File"
        DIR = "Directory"
        # label
        tk.Label(master=self.leftFrame, text="Do you want to upload a file or a directory?", foreground="white", background=self.LEFT_BG_COLOR, font=("Arial", 15), pady=10).pack()

        # create ttk style
        dropdownStyle = ttk.Style()
        dropdownStyle.theme_use('clam')
        dropdownStyle.configure('Combo.TButton', foreground="black", background="white")
        dropdownStyle.configure('Combo.TLabel', foreground="black", background="white", font=("Arial", 30))
        dropdownStyle.map('Combo.TCombobox', fieldbackground=[('readonly', 'white')], selectbackground=[('readonly', 'white')], selectforeground=[('readonly', 'black')])
        
        dropdown = ttk.Combobox(master=self.leftFrame, values=[FILE, DIR], width=20, justify="left", state="readonly", style='Combo.TCombobox')
        dropdown.pack(padx=10, pady=10)

        ##
        def callback(*args):
          if dropdown.get() == FILE:
              self.createAddFileButton()
          else:
            self.createDirectoryField()
        dropdown.bind("<<ComboboxSelected>>", callback)


    def createAddFileButton(self):
        
      style = ttk.Style()
      style.configure("AddFile.TButton", background=self.RIGHT_BG_COLOR, foreground="black", font=("Arial", 10))
      
      addFileButton = ttk.Button(master=self.leftFrame, text="Add a file to upload", command=self.createFileField, style="AddFile.TButton")
      addFileButton.pack(pady=5)


    def createFileField(self):
        # create label
        fileLabel = tk.Label(master=self.selectedFilesFrame, bg=self.RIGHT_BG_COLOR, fg="black", text="", font=("Arial", 15))

        # helper function to select a file
        def selectFile():
          fileName = askopenfilename(title="select", filetypes=self.ALLOWED_FILES)
          if fileName:
              showinfo(title = "Selected file is: ", message=fileName)              
              # show file name on the right side
              if fileName not in self.selectedFiles:
                self.selectedFiles.add(fileName)
                fileLabel["text"] = fileName
                fileLabel.pack()
              chooseFileButton["text"] = fileName.split("/")[-1]
          else:
              showinfo(title = "You haven't selected a file")
        chooseFileButton = ttk.Button(master=self.leftFrame, text="Choose file for analysis", command=selectFile, style="AddFile.TButton")
        chooseFileButton.pack(pady=5)

    def createDirectoryField(self):
        def selectDir():
          userDir = askdirectory(title="select a folder", mustexist=True)
          if userDir:
            showinfo(title = "Selected folder is: ", message=userDir)
            for file in os.listdir(userDir):
               if os.path.isfile(os.path.join(userDir, file)) and (file.endswith(".xlsx") or file.endswith(".xls")):
                  fileName = os.path.join(userDir, file)
                  if fileName not in self.selectedFiles:
                    self.selectedFiles.add(fileName)
                    # create tkinter label for each file, and add to right layout
                    tk.Label(master=self.selectedFilesFrame, bg=self.RIGHT_BG_COLOR, fg="black", text=fileName, font=("Arial", 15)).pack()
          else:
            showinfo(title = "You haven't selected a folder")
        style = ttk.Style()
        style.configure("AddFile.TButton", background=self.RIGHT_BG_COLOR, foreground="black", font=("Arial", 10))
        addFolderButton = ttk.Button(master=self.leftFrame, text="Choose folder for upload", command=selectDir, style="AddFile.TButton")
        addFolderButton.pack()

# main
app = App()
app.mainloop()