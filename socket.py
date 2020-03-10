# Configure Data-Output types 3, 17 and 20
# and the IP where the python script is running (port 49000) in X-Plane.  

UDP_PORT = 49005

from socket import socket
import requests 

import struct 
#import requests
import socket
import time


HOST = '169.254.152.170';
WEB_PORT = 3001;
JAVA_PORT = 4000;

def DecodeDataMessage(message):
  # Message consists of 4 byte type and 8 times a 4byte float value.
  # Write the results in a python dict. 
  values = {}
  typelen = 4
  type = int.from_bytes(message[0:typelen], byteorder='little')
  data = message[typelen:]
  dataFLOATS = struct.unpack("<ffffffff",data)
  if type == 3:
    values["speed"]=dataFLOATS[0]
  elif type == 17:
    values["pitch"]=dataFLOATS[0]
    values["roll"]=dataFLOATS[1]
    values["heading"]=dataFLOATS[2]
    values["heading2"]=dataFLOATS[3]
  elif type == 20:
    values["latitude"]=dataFLOATS[0]
    values["longitude"]=dataFLOATS[1]
    values["altitude MSL"]=dataFLOATS[2]
    values["altitude AGL"]=dataFLOATS[3]
    values["altitude 2"]=dataFLOATS[4]
    values["altitude 3"]=dataFLOATS[5]
  else:
    print("  Type ", type, " not implemented: ",dataFLOATS)
  return values

def DecodePacket(data):
  # Packet consists of 5 byte header and multiple messages. 
  valuesout = {}
  headerlen = 5
  header = data[0:headerlen]
  messages = data[headerlen:]
  if(header==b'DATA*'):
    # Divide into 36 byte messages
    messagelen = 36
    for i in range(0,int((len(messages))/messagelen)):
      message = messages[(i*messagelen) : ((i+1)*messagelen)]
      values = DecodeDataMessage(message)
      valuesout.update( values )
  else:
    print("Packet type not implemented. ")
    print("  Header: ", header)
    print("  Data: ", messages)
  return valuesout

def main():

  # Open a Socket on UDP Port 49000
  UDP_IP = ""
  sock = socket.socket(socket.AF_INET, # Internet
                       socket.SOCK_DGRAM) # UDP
  sock.bind((UDP_IP, UDP_PORT))



  # s = socket.socket()          
  # print ("Socket successfully created")
  # s.connect((HOST, JAVA_PORT)) 
  # viewType = ('RESET')
  # s.send(bytes(viewType , encoding="UTF-8"))
  # s.close()

  # s = socket.socket()          
  # print ("Socket successfully created")
  # s.connect((HOST, JAVA_PORT)) 
  # viewType = ('SIM_OFF')
  # s.send(bytes(viewType , encoding="UTF-8"))
  # s.close()
    
  # time.sleep(1)


  # s = socket.socket()          
  # print ("Socket successfully created")
  # s.connect((HOST, JAVA_PORT)) 
  # viewType = ('SIM_ON')
  # s.send(bytes(viewType , encoding="UTF-8"))
  # s.close()
   
  # time.sleep(1)

  # s = socket.socket()          
  # print ("Socket successfully created")
  # s.connect((HOST, JAVA_PORT)) 
  # viewType = ('PRY:BOTH:0:0:100')
  # s.send(bytes(viewType , encoding="UTF-8"))
  # s.close()
  
  # time.sleep(1)


  while True:
    # Receive a packet
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    
    # Decode the packet. Result is a python dict (like a map in C) with values from X-Plane.
    # Example:
    # {'latitude': 47.72798156738281, 'longitude': 12.434000015258789, 
    #   'altitude MSL': 1822.67, 'altitude AGL': 0.17, 'speed': 4.11, 
    #   'roll': 1.05, 'pitch': -4.38, 'heading': 275.43, 'heading2': 271.84}
    values = DecodePacket(data)
    print('Pitch: '+ str(values["pitch"]))
    print('Roll: '+ str(values["roll"]))


    # s = socket.socket()          
    # s.connect((HOST, JAVA_PORT)) 
    # viewType = 'PRY:BOTH:' + str(int(values["pitch"]))+':'+str(int(values["roll"]))+':100'
    # s.send(bytes(viewType , encoding="UTF-8"))
    # s.close() 

    print()

if __name__ == '__main__':
  main()
