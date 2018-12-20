
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 19:29:02 2018

@author: pi
"""

import tkinter as tk
import threading
import time
import spi as rm_spi


class ui(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.ui_created = False
        self.start()
        while not (self.ui_ready()):
            time.sleep(0.1)

        
    def stop(self):
        self.root.quit()  

    def ui_ready(self):
        return self.ui_created
        
    def set_text(self,text_data):

        if len(text_data)<9:
            self.label_data_up.set(text_data)
        else:
            up = text_data[:8]
            down = text_data[-(len(text_data)-8):]
            self.label_data_up.set(up)
            self.label_data_down.set(down)

    

    def set_cb_pwr(self,cb):
        self.button_pwr.config(command=cb)
    def set_cb_plus(self,cb):
        self.button_plus.config(command=cb)
    def set_cb_minus(self,cb):
        self.button_minus.config(command=cb)
    def set_cb_a(self,cb):
        self.button_a.config(command=cb)
    def set_cb_m(self,cb):
        self.button_m.config(command=cb)
        
    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.stop)
        self.label_data_up = tk.StringVar()
        self.label_data_down = tk.StringVar()
        self.root.title("Remote")
        self.label_up = tk.Label(self.root, fg="dark green",textvariable=self.label_data_up)
        self.label_up.pack()
        self.label_down = tk.Label(self.root, fg="dark green",textvariable=self.label_data_down)
        self.label_down.pack()
        
        frame= tk.Frame(self.root)
        frame.pack()
        
        self.button_pwr = tk.Button(frame, text="power",width=15, command=self.root.destroy)
        self.button_plus = tk.Button(frame, text="+",width=15, command=self.root.destroy)
        self.button_minus = tk.Button(frame, text="-",width=15, command=self.root.destroy)
        self.button_plus.pack(side=tk.LEFT)
        self.button_pwr.pack(side=tk.LEFT)
        self.button_minus.pack(side=tk.LEFT)
        frame1= tk.Frame(self.root)
        frame1.pack()
        self.button_a = tk.Button(frame1, text="A",width=22, command=self.root.destroy)
        self.button_m = tk.Button(frame1, text="M",width=22, command=self.root.destroy)
        self.button_a.pack(side=tk.LEFT)
        self.button_m.pack(side=tk.LEFT)
        self.ui_created = True
        self.root.mainloop() 


    
    
if __name__ == "__main__":
    
    
    
    def callb():
        print("Kasper")
        
    def print_callback(tekst):
        l_ui.set_text (tekst[1:])
        
    l_ui = ui()    
    rm = rm_spi.edilkamin(print_callback)    
        

    #l_ui.set_text('12345678123456789')
    l_ui.set_cb_a(rm.tx_A_key)
    l_ui.set_cb_m(rm.tx_M_key)
    l_ui.set_cb_minus(rm.tx_minus_key)
    l_ui.set_cb_plus(rm.tx_plus_key)
    l_ui.set_cb_pwr(rm.tx_power_key)
    
    for i in range(10000):
        pass#print(i)
    
    print ("end")