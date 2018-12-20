#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 21:30:15 2018

@author: pi
"""
import time
import spidev
import threading
from datetime import datetime
import sys
import json

class edilkamin(threading.Thread):
    
    def __init__(self,cb_text):
        
        threading.Thread.__init__(self)
        self.text_cb = cb_text    
        self.start()
        self.rolling_byte = 0
        
    def stop(self):
        pass 
    
    def run(self):
        self.tx_buffer = None
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.spi.max_speed_hz = 2000000

        start_time = time.time()
        while(True):
            self.init_tranciever()
            if  (time.time() - start_time > 0.5):
                #print (time.time() - start_time )
                start_time = time.time()
                
                self.rolling_byte = (self.rolling_byte-1)&0xff
     
            if self.tx_buffer == None:
                self.tx_no_key()
            else:
                self.tx_packet(self.tx_buffer)
                self.tx_buffer = None
 
                
                
            rx_data = self.rx_packet()
            if not rx_data ==  False:
                if len(rx_data)>8:
                    #print (''.join(chr(e) for e in rx_data))
                    self.text_cb(''.join(chr(e) for e in rx_data))
                    #t_ui.set_text(''.join(chr(e) for e in rx_data))
                #else:
                #    print (rx_data)
                    
                    
                    
            #time.sleep(0.06)
            
        
            
    def tx_register(self,l_spi,adr,value):
        l_spi.xfer([adr|0x80]+value)
        
    
    
    def rx_register(self,l_spi,adr):
        return l_spi.xfer([adr,0])[1]
    
    def rx_register_x(self,l_spi,adr,i):
        value= [0]*i
        return l_spi.xfer([adr]+value)
    
    
    def init_tranciever(self):
        self.tx_register(self.spi,0x1d, [0x01]) #reset
        time.sleep(0.05)
        self.tx_register(self.spi,0x00, [0x57])
        self.tx_register(self.spi,0x1b, [0x55])
        self.tx_register(self.spi,0x1c, [0x05])
        self.tx_register(self.spi,0x03, [0x0e])
        self.tx_register(self.spi,0x0c, [0xc0]) 
        self.tx_register(self.spi,0x0d, [0x44])
        self.tx_register(self.spi,0x0e, [0x00])
        self.tx_register(self.spi,0x0f, [0x00])
        self.tx_register(self.spi,0x24, [0x04,0x33,0x33])
        self.tx_register(self.spi,0x10, [0xEE])
        self.tx_register(self.spi,0x15, [0x14])
        self.tx_register(self.spi,0x16, [0x14])
        self.tx_register(self.spi,0x1f, [0x00])
        self.tx_register(self.spi,0x1e, [0x08])
        self.tx_register(self.spi,0x32, [0x3c])
        self.tx_register(self.spi,0x35, [0x14])
        self.tx_register(self.spi,0x0b, [0xa3])
        self.tx_register(self.spi,0x06, [0x48]) #88
        self.tx_register(self.spi,0x11, [0x05])
        self.tx_register(self.spi,0x12, [0x0e])
        self.tx_register(self.spi,0x14, [0x8f])
        time.sleep(0.05)
    
    def tx_packet(self,tx_data):
        self.tx_register(self.spi,0x02, [0x40]) # tx clr
        self.tx_register(self.spi,0x0e, [0xa0]) # A0 GPIO Setup
        self.tx_register(self.spi,0x01, [len(tx_data)]) # setup length
        #tx_register(self.spi,0x20, [0x12,0x34,0x00,0xaa,0x10,0xc8,0x80])
        self.tx_register(self.spi,0x20, tx_data)
        self.tx_register(self.spi,0x02, [0xbf]) #82 start tx with irq
        time.sleep(0.0015) # change to check of bit with timeout
        if self.rx_register(self.spi,0x04)&2>0:
            return True
        else:
            return False
        
        
    def rx_packet(self):
        self.tx_register(self.spi,0x0e, [0x00]) # 0 GPIO Setup - Enable RX upper bit must be 0
        self.tx_register(self.spi,0x05, [0x87]) #Start recieve
        time.sleep(0.05)
        rx_irq_status = self.rx_register(self.spi,0x07)
        rx_status = self.rx_register(self.spi,0x08)
        if rx_status&16==0 and rx_irq_status&1==0 and rx_irq_status&2==2:
            return self.rx_register_x(self.spi,0x21,self.rx_register(self.spi,0x09)) #read bytes
        else:
            #print("RX_IRQ_STATUS: "+str(rx_irq_status))
            #print("RX_STATUS: "+str(rx_status))
    
            return False

    def tx_no_key(self):
        return self.tx_packet([0x12,0x34,0x00,0xaa,0x14,self.rolling_byte,0x00])
    def tx_minus_key(self):
        self.tx_buffer = [0x12,0x34,0x90,0x3a,0x11,self.rolling_byte,0x00]
    def tx_plus_key(self):
        self.tx_buffer = [0x12,0x34,0x84,0x2e,0x11,self.rolling_byte,0x00]
    def tx_A_key(self):
        self.tx_buffer = [0x12,0x34,0x82,0x28,0x11,self.rolling_byte,0x00]
    def tx_M_key(self):
        self.tx_buffer = [0x12,0x34,0x88,0x22,0x11,self.rolling_byte,0x00]
    def tx_power_key(self):
        self.tx_buffer = [0x12,0x34,0x81,0x2b,0x11,self.rolling_byte,0x00]
   
    
if __name__ == "__main__":

    def print_callback(text_data):
        #print("RX - " + text_data)
        if len(text_data)<9:
            print(text_data)
        else:
        
            up = text_data[:9]
            #down = text_data[-(len(text_data)-9):]
            
            if "Power" == str(up[1:6]):
                #print (str(up[1:6]))
                #print(str(up[8:9]))
                print (json.dumps({str(up[1:6]):int(up[8:9])}))
                if int(up[8:9]) > 0 and int(up[8:9]) < 6:
                    global current_power
                    current_power = int(up[8:9])
            #print(str(down))
        
        
    rm = edilkamin(print_callback)
    while(True):
        try:
            line = sys.stdin.readline()
            data = json.loads(line)
            if data["Power"] < 6 and data["Power"] > 0:
                delta = data["Power"] - current_power
                print (delta)
                if delta > 0: 
                    for i in range(abs(delta)):
                        print ("større")
                        rm.tx_plus_key()
                        time.sleep(0.2)
                elif delta < 0:
                    for i in range(abs(delta)):
                        print ("mindre")
                        rm.tx_minus_key()
                        time.sleep(0.2)
        except KeyboardInterrupt:
            break
        except:
            print ("Error")
        

        














#

