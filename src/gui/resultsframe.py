import tkinter


class ResultsFrame(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master=master)
        self.best_to_invest_label = tkinter.Label(master=self)
        self.best_to_invest_label.grid(row=0, column=0)

    def set_best_to_invest(self, best_to_invest):
        if best_to_invest is None:
            beststr = 'Error: could not find best stock to invest'
        else:
            beststr = 'Best to invest in: '
            beststr += best_to_invest['company']
            beststr += '\n\tProbability of closing high (> 2%): {:.2f}'.format(best_to_invest['u_chance'])
            beststr += '\n\tProbability of closing stable (-2% <= p <= 2%): {:.2f}'.format(best_to_invest['s_chance'])
            beststr += '\n\tProbability of closing down (< -2%): {:.2f}'.format(best_to_invest['d_chance'])
        self.best_to_invest_label.configure(text=beststr)
