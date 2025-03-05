# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 23:14:41 2022

@author: Helio
"""

import tkinter.filedialog

root = tkinter.Tk()
root.withdraw()

filtro = (("Entrada", "*.txt"), ("All files", "*"))
nomeArq = tkinter.filedialog.askopenfilename(filetypes = filtro)

print(nomeArq)

root.destroy()

root.mainloop()

