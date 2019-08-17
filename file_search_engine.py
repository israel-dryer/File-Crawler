import os
import pickle
import PySimpleGUI as sg 
sg.ChangeLookAndFeel('Dark')


class Gui:
    def __init__(self):
        self.layout = [[sg.Text('Search Term', size=(10,1)), 
                        sg.Input(size=(45,1), focus=True, key="TERM"), 
                        sg.Radio('Contains', group_id='choice', key="CONTAINS", default=True), 
                        sg.Radio('StartsWith', group_id='choice', key="STARTSWITH"), 
                        sg.Radio('EndsWith', group_id='choice', key="ENDSWITH")],
                       [sg.Text('Root Path', size=(10,1)), 
                        sg.Input('C:/', size=(45,1), key="PATH"), 
                        sg.FolderBrowse('Browse', size=(10,1)), 
                        sg.Button('Re-Index', size=(10,1), key="_INDEX_"), 
                        sg.Button('Search', size=(10,1), bind_return_key=True, key="_SEARCH_")],
                       [sg.Output(size=(100,30))]]
        self.window = sg.Window('File Search Engine').Layout(self.layout)

class SearchEngine:
    def __init__(self):
        self.file_index = [] # directory listing returned by os.walk()
        self.results = [] # search results returned from search method
        self.matches = 0 # count of records matched
        self.records = 0 # count of records searched

    def create_new_index(self, values):
        ''' create a new index of the root; then save to self.file_index and to pickle file '''
        root_path = values['PATH']
        self.file_index = [(root, files) for root, dirs, files in os.walk(root_path) if files]

        # save index to file
        with open('file_index.pkl','wb') as f:
            pickle.dump(self.file_index, f)

    def load_existing_index(self):
        ''' load an existing index into the program '''
        try:
            with open('file_index.pkl','rb') as f:
                self.file_index = pickle.load(f)
        except:
            self.file_index = []

    def search(self, values):
        ''' search for the term based on teh type in the index;
            the types of search include: contains, startswith, endswith;
            save the results to file '''
        self.results.clear()
        self.matches = 0
        self.records = 0
        term = values['TERM']

        # search for matches and count results
        for path, files in self.file_index:
            for file in files:
                self.records +=1
                if (values['CONTAINS'] and term.lower() in file.lower() or 
                    values['STARTSWITH'] and file.lower().startswith(term.lower()) or 
                    values['ENDSWITH'] and file.lower().endswith(term.lower())):

                    result = path.replace('\\','/') + '/' + file
                    self.results.append(result)
                    self.matches +=1
                else:
                    continue 
        
        # save results to file
        with open('search_results.txt','w') as f:
            for row in self.results:
                f.write(row + '\n')

def test3():
    ''' test the gui interface'''
    g = Gui()

    while True:
        event, values = g.window.Read()
        print(event, values)


def main():
    g = Gui()
    s = SearchEngine()
    s.load_existing_index() # load if exists, otherwise return empty list

    while True:
        event, values = g.window.Read()

        if event is None:
            break
        if event == '_INDEX_':
            s.create_new_index(values)
            print()
            print(">> New index created")
            print()
        if event == '_SEARCH_':
            s.search(values)

            # print the results to output element
            print()
            for result in s.results:
                print(result)
            
            print()
            print(">> Searched {:,d} records and found {:,d} matches".format(s.records, s.matches))
            print(">> Results saved in working directory as search_results.txt.")



main()            
