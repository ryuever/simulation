import csv, os, sys
from tkinter import *
from tkinter.filedialog import askopenfilename
from SL_Error import MyError

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

filenames = []
company = ['First', 'Second', 'Third']
state = False

class ProcessCSV(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        formRow = ''
        requestRow = ''
        self.makeForm(parent)
        self.makeRequest(parent)        

    def fileDialog(self, entry):
        print(entry)
        filename = askopenfilename()
        filenames.append(filename)
        entry.insert(0, filename)
        entry.pack()
        print(filenames)
    
    def onClick(self):
        global state
        state = not state
    
    def makeForm(self, parent):
        for i in range(5):
            formRow = Frame(parent)        
            entry = Entry(formRow)
            button = Button(formRow, text='select a file', command=(lambda entry=entry:self.fileDialog(entry)))
            print('entry is {}'.format(entry))
            formRow.pack(side=TOP, fill=X, padx=5, pady=5)
            button.pack(side=LEFT)
            entry.pack(side=RIGHT, expand=YES, fill=X)

    def makeRequest(self, parent):
        requestRow = Frame(parent)
        cancel = Button(requestRow, text='cancel')
        submit = Button(requestRow, text='Summit', padx=10, pady=10, command=(lambda:csv2xml()))
        checkButton = Checkbutton(requestRow, text="Export to same file ?",command=(lambda:self.onClick()))
        requestRow.pack(side=TOP, fill=X, padx=5, pady=5)
        cancel.pack(side=LEFT)
        checkButton.pack(side=RIGHT)
        submit.pack(side=RIGHT)

def csv2xml():
    desFile = ''
    print(filenames)
    for srcFile in filenames:
        basename = os.path.basename(srcFile)
        for item in company:
            if item in basename:
                sender = item
                break            
        filename, fileExt = os.path.splitext(srcFile)
    
        if state:
            if desFile:
                if item not in desFile:
                    raise MyError("File should be from the same company")
            else:
                desFile = os.path.dirname(srcFile) + '/' + item + '.xml'
        else:
            desFile = filename + '.xml'
        xmlData = open(desFile, 'w')
        xmlData.write('<?xml version="1.0"?>' + "\n")
        # there must be only one top-level tag
        xmlData.write('<root>' + "\n")
        xmlData.write('  <data sender="' + sender + '">\n')

        rowNum = 0
        with open(srcFile, newline='') as csvFile:
            csvData = csv.reader(csvFile)
            for row in csvData:
                print(row)
                eleNum = len(row)
                if rowNum == 0:
                    tags = row
                    # replace spaces w/ underscores in tag names
                    for i in range(eleNum):
                        tags[i] = tags[i].replace(' ', '_')
                else: 
                    xmlData.write('    <value ' )
                    for i in range(eleNum-1):
                        xmlData.write(tags[i] + '="' + row[i] +'" ')
                    xmlData.write('>')
                    xmlData.write(row[eleNum-1])
                    xmlData.write('</value>\n')
                rowNum += 1
            xmlData.write('  </data>' + "\n")
            xmlData.write('</root>')
            xmlData.close()

if __name__=='__main__':
    root = Tk()
    temp = ProcessCSV(root)
    root.mainloop()
