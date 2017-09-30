import tkinter
import src.gui.mainframe
import src.agent.bayesnet_analyst
import src.util.hbovespa_parser


class MainWindow(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title('Bayes Investor Tool (BIT)')

        self.mainframe = src.gui.mainframe.MainFrame(root=self, analyzer=self.analyze_data)
        self.mainframe.pack()

        self.best_to_invest = None

    def analyze_data(self, hbovespa_filename):
        parser = src.util.hbovespa_parser.HBovespaParser(hbovespa_filename)
        analyst = src.agent.bayesnet_analyst.BayesAnalyst()
        if not parser.check_json():
            parser.parse()
        else:
            print('RESPECTIVE JSON FILE ALREADY EXISTS. BEGINNING ANALYSIS')
        self.best_to_invest = analyst.analyze_data(parser.outputfile)
        self.mainframe.set_best_to_invest(self.best_to_invest)

if __name__ == "__main__":
    mainwindow = MainWindow()
    mainwindow.mainloop()
