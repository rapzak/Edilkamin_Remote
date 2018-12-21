##
## This file is part of the libsigrokdecode project.
##
## Copyright (C) 2016 Robert Bosch Car Multimedia GmbH
## Authors: Oleksij Rempel
##              <fixed-term.Oleksij.Rempel@de.bosch.com>
##              <linux@rempel-privat.de>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, see <http://www.gnu.org/licenses/>.
##

import sigrokdecode as srd

class Decoder(srd.Decoder):
    api_version = 3
    id = 'edil_rem'
    name = 'edil_rem'
    longname = 'Edilkamin_Remote'
    desc = 'Synchronous Serial Interface (32bit) protocol.'
    license = 'gplv2+'
    inputs = ['spi']
    outputs = ['edil_remote']
    options = (
        {'id': 'raw_data', 'desc': 'Show Raw Data', 'default': 'True', 'values':('True','False')},
        {'id': 'txt_data', 'desc': 'Show Text Data', 'default': 'True', 'values':('True','False')},
        {'id': 'byte_data', 'desc': 'Show Byte Data', 'default': 'True', 'values':('True','False')},
        {'id': 'rx_data', 'desc': 'Show RX Data', 'default': 'True', 'values':('True','False')},
        {'id': 'tx_data', 'desc': 'Show TX Data', 'default': 'True', 'values':('True','False')},
        {'id': 'rx_hide_txt', 'desc': 'Hide readable txt in byte', 'default': 'True', 'values':('True','False')},
    )
    annotations = (
        ('tx', 'TX'),
        ('rx', 'RX'),
        ('adr', 'ADR'),
        ('p_rx', 'Parsed RX'),
        ('p_tx', 'Parsed TX'),
        ('p_rx_b', 'Parsed RX Bytes'),
        ('p_tx_b', 'Parsed TX Bytes'),

    )
    annotation_rows = (
        ('data', 'Data', (0, 1,2)),
        ('P_data', 'Parsed Data', (3, 4,)),
        ('P_data_byte', 'Parsed Data Byte', (5, 6,)),
    )

    def __init__(self):
        self.reset()

    def reset(self):
        self.ss_cmd, self.es_cmd = 0, 0
        self.mosi_bytes = []
        self.miso_bytes = []
        self.es_array = []
        self.rx_size = 0
        self.tx_size = 0

    def start(self):
        self.out_ann = self.register(srd.OUTPUT_ANN)

    def reset_data(self):
        self.mosi_bytes = []
        self.miso_bytes = []
        self.es_array = []



                      
    def put_tx_data(self,ss,es, data):
        self.put(ss, es, self.out_ann, [0, ['TX:0x%02X' % (data)]])
    def put_rx_data(self,ss,es, data):
        self.put(ss, es, self.out_ann, [1, ['RX:0x%02X' % (data)]])
    def put_adr(self,ss,es, data):
        self.put(ss, es, self.out_ann, [2, ['ADR:0x%02X' % (data)]])

    def put_p_tx(self,ss,es, data):
        self.put(ss, es, self.out_ann, [3, ['TX:%s' % (data)]])
    def put_p_rx(self,ss,es, data):
        self.put(ss, es, self.out_ann, [4, ['RX:%s' % (data)]])
    def put_p_tx_b(self,ss,es, data):
        self.put(ss, es, self.out_ann, [5, ['TX:%s' % (data)]])
    def put_p_rx_b(self,ss,es, data):
        self.put(ss, es, self.out_ann, [6, ['RX:%s' % (data)]])

                      
    def decode(self, ss, es, data):
        ptype, mosi, miso = data
        




        # Don't care about anything else.
        if ptype != 'TRANSFER':
            return
            
        #print(data)
        
        
        cmd_type = mosi[0]
        cmd_adr =  mosi[0].val&0x3f
        cmd_dir =  "write" if mosi[0].val&0x80 else "read"
        cmd_inc =  "inc" if mosi[0].val&0x40 else ""
        cmd_data_len = len(mosi)-1
        
        #print("-------CMD_ADDR:" + str(cmd_adr) +  "-----CMD_DIR:"+cmd_dir+"-----"+ str(cmd_data_len)+"------"+cmd_inc)

        #Write the adress
        if self.options['raw_data'] == 'True' and (self.options['rx_data'] == 'True' or self.options['tx_data'] == 'True' ):
            self.put_adr(mosi[0].ss,mosi[0].es,cmd_adr)

        #Write the TX data
        if cmd_dir == "write":          
            for b in mosi[1:]:
                if self.options['raw_data'] == 'True' and self.options['tx_data'] == 'True':
                    self.put_tx_data(b.ss,b.es,b.val)
        #Write the RX data
        if cmd_dir == "read":          
            for b in miso[1:]:
                if self.options['raw_data'] == 'True' and self.options['rx_data'] == 'True':
                    self.put_rx_data(b.ss,b.es,b.val)        
        
        #TX_Data
        if cmd_adr == 0x20:
            parsed_data_string =""
            parsed_data_bytes =[]
            for b in mosi[1:]:
                parsed_data_string =  parsed_data_string + chr(b.val)
                parsed_data_bytes.append(b.val)
            if self.options['txt_data'] == 'True' and self.options['tx_data'] == 'True':    
                self.put_p_tx(miso[1].ss,miso[len(miso)-1].es,parsed_data_string)
            if self.options['byte_data'] == 'True' and self.options['tx_data'] == 'True':
                self.put_p_tx_b(miso[1].ss,miso[len(miso)-1].es,''.join('{:02x} '.format(x) for x in parsed_data_bytes))
        
        #RX_Data
        if cmd_adr == 0x21:
            parsed_data_string =""
            parsed_data_bytes =[]
            for b in miso[1:]:
                parsed_data_string =  parsed_data_string + chr(b.val)
                parsed_data_bytes.append(b.val)
            
            if self.options['txt_data'] == 'True' and self.options['rx_data'] == 'True':
                self.put_p_rx(miso[1].ss,miso[len(miso)-1].es,parsed_data_string)
            if  self.options['rx_hide_txt'] == 'False' and len( miso ) < 15: 
                if self.options['byte_data'] == 'True' and self.options['rx_data'] == 'True':
                    self.put_p_rx_b(miso[1].ss,miso[len(miso)-1].es,''.join('{:02x} '.format(x) for x in parsed_data_bytes))



