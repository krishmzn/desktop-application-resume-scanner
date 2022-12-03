import tkinter as tk
import pandas as pd
import os

from PyPDF2 import PdfReader
from collections import Counter


# -------------------------------------------------------
#  Tkinter GUI part
# -------------------------------------------------------
root = tk.Tk()
try:
    root.iconbitmap('components/icon.ico')
except:
    pass
root.title("Resume Analyzer")
root.geometry("400x510")


def retrievedata():
    ''' get data stored '''
    global list_data
    list_data = []
    try:
        file = pd.read_csv('components/save.csv')
        file = list(file[:])
        file = file[:-1]
        list_data = file
    except:
        pass

def reload_data():
    for d in list_data:
        listbox.insert(0, d)


def add_item(event=1):
    global list_data
    if content.get() != "":
        listbox.insert(tk.END, content.get())
        list_data.append(content.get())
        content.set("")


def delete():
    global list_data
    listbox.delete(0, tk.END)
    list_data = []


def delete_selected():

    try:
        selected = listbox.get(listbox.curselection())
        listbox.delete(listbox.curselection())
        list_data.pop(list_data.index(selected))
        # reload_data()
        # # listbox.selection_clear(0, END)
        listbox.selection_set(0)
        listbox.activate(0)
        listbox.event_generate("&lt;&lt;ListboxSelect>>")
        print(listbox.curselection())
    except:
        pass

def quit():
 global root
 try:
  os.mkdir("components")
 except FileExistsError:
  # directory already exists
  pass
 with open("components/save.csv", "w", encoding="utf-8") as file:
  for d in list_data:
   file.write(d + ",")
 main()
 root.destroy()

# LISTBOX

tk.Label(root, text=' ').pack()
tk.Label(root, text='Start typing keyword one by one below:').pack()

content = tk.StringVar()
entry = tk.Entry(root, textvariable=content)
entry.pack()

tk.Label(root, text='Press enter to add keyword to the list below').pack()

entry.bind('<Return>', add_item)

tk.Label(root, text='-------------------------------------------').pack()

tk.Label(root, text='| Keyword List |').pack()

listbox = tk.Listbox(root)
listbox.pack()
entry.bind("&lt;Return>", add_item)

button_delete = tk.Button(text="Clear All Items", command=delete)
button_delete.pack()

button_delete_selected = tk.Button(text="Delete Selected", command=delete_selected)
button_delete_selected.pack()

tk.Label(root, text='-------------------------------------------').pack()

bquit = tk.Button(root, text="Save List and Start Analysis", command=quit)
bquit.pack()

# -------------------------------------------------------
# Resume Checking part
# -------------------------------------------------------
def main():
    # Convet txt to list
    savetxt = pd.read_csv('components/save.csv')

    keys_received = savetxt
    keycheck = [ ]
    paragraph = [ ]
    person = [ ]
    match_percentage = [ ]
    char = [',', '[', ']', '(', ')', '-', '_', '.']

    # Converting key received to lowercase for analysis
    for i in keys_received:
        print(i)
        i = i.lower()
        keycheck.append(i)

    # first converting df to list then removing final element of list
    keycheck = list(keycheck[:])
    keycheck = keycheck[:-1]
    print(keycheck)

    path = os.getcwd() + '/resumes'
    for filename in os.listdir(path):
        if filename.endswith('.pdf'):
            # print(filename)
            new_path = os.path.join(path, filename)
            reader = PdfReader(new_path)
            NumPages = reader.getNumPages()
            print(filename)

            i = 0
            text = ''
            for i in range(NumPages):
                page = reader.pages[i]
                text = text + page.extract_text()
                # print(i)
            # print('finish looping through pages')
            # print(text)
            
            word_occurance = Counter(text.split()).most_common()
            # print(word_occurance)

            analysis_list = [ ]
            result = [ ]

            # converting tuple's first element to string and then list 
            for wd in word_occurance:
                wd = str(wd[0])
                analysis_list.append(wd)
                # print(wd)
            # print(analysis_list)

            # Analyzing words
            for i in keycheck:
                for word in analysis_list:
                    word = str(word)
                    word = word.lower()

                    # removing characters form string
                    for cr in char:
                        word = word.replace(str(cr), '')
                    # print(word)

                    # checking if the text in the words have keywords
                    if i == word:
                        result.append(i)
                        # print(i)
            result = list(set(result))
            # print(result)
            
            no_of_kwds = len(keycheck)
            no_of_result = len(result)
            match_precent = (no_of_result/no_of_kwds)*100
            # print(match_precent)
            print('-----------------------------------------------------')
            person.append(filename)
            match_percentage.append(match_precent)

    # creating df
    data = {'Candidate':person, 'Profile_Match':match_percentage}
    df = pd.DataFrame(data) 
    print(df)
    # Creating csv
    try:
        os.mkdir("resumes/report")
    except FileExistsError:
        # directory already exists
        pass
    df.to_csv('resumes/report/report.csv', index = False, encoding='utf-8')
    print('csv created suscessfully')

retrievedata()
reload_data()
root.mainloop()