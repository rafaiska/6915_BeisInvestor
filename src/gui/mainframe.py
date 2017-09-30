import tkinter
import tkinter.filedialog
import webbrowser
import src.gui.resultsframe


def bovespa_callback(event):
    webbrowser.open_new(
        r'http://www.bmfbovespa.com.br/pt_br/servicos/market-data/historico/mercado-a-vista/cotacoes-historicas/')

def browse_file(box):
    box.delete(0, tkinter.END)
    box.insert(0, tkinter.filedialog.askopenfilename(initialdir='./data'))


class MainFrame(tkinter.Frame):
    def __init__(self, root, analyzer):
        super().__init__(master=root)
        self.root = root
        welcomelabel_text = ('Welcome to BIT v0.1.0\n'
                             'Choose a BOVESPA historic file to continue:\n')
        self.welcomelabel = tkinter.Label(self, text=welcomelabel_text)
        self.linklabel = tkinter.Label(self, text='(Files for download can be found on this link)', fg='blue', cursor='hand2')
        self.linklabel.bind("<Button-1>", bovespa_callback)
        self.welcomelabel.grid(column=0, row=0)
        self.linklabel.grid(column=0, row=2)

        self.fileselectionfield = tkinter.Entry(master=self)
        self.browsebutton = tkinter.Button(
            master=self, text='Browse', command=lambda: browse_file(self.fileselectionfield))
        self.analyzebutton = tkinter.Button(
            master=self, text='Analyze', command=lambda: analyzer(self.fileselectionfield.get()))
        self.fileselectionfield.grid(column=0, row=1)
        self.browsebutton.grid(column=1, row=1)
        self.analyzebutton.grid(column=2, row=1)

        self.results_frame = src.gui.resultsframe.ResultsFrame(master=self)
        self.results_frame.grid(column=0,row=3)

    def set_best_to_invest(self, best_to_invest):
        self.results_frame.set_best_to_invest(best_to_invest)

