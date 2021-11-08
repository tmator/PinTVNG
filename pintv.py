import serial
import logging

from omxplayer.player import OMXPlayer
from time import sleep

reading="0"

#video loop
LOOP_PATH = "videos/loop.mp4"

#to store matrix/lamp->movie
matrixArray=[]
cpt=0

#logging
logging.basicConfig(level=logging.INFO)
pintv_log = logging.getLogger("PinTV")


#player exit callback
def playerExit(code):
    pintv_log.info("Exit video sample")
    loop.set_position(0) 
    sleep(0.1)
    loop.play() 



#create arrays (matrixs / lamps) from csv
def createFilenameArray():
    global cpt
    global matrixArray
    matrixArray=[0 for i in range(64)]
    f = open("data.txt", "r")
    for x in f:
        pintv_log.info("swictch / lamp "+str(x).rstrip())
        matrixArray[cpt]=str(x).rstrip()
        cpt+=1


createFilenameArray()


#open serial port
port = serial.Serial(
 port='/dev/ttyACM0',
 baudrate = 9600,
 parity=serial.PARITY_NONE,
 stopbits=serial.STOPBITS_ONE,
 bytesize=serial.EIGHTBITS,
 timeout=1
)



#create loop player
loop = OMXPlayer(LOOP_PATH, args=['--loop','--no-osd'], dbus_name='org.mpris.MediaPlayer2.omxplayer0')


#play loop
sleep(1)
loop.play()

while True:
    #waiting on serial port
    bytesToRead = port.in_waiting
    if(bytesToRead > 0):
        #read data on serial port from arduino
        #matrix/lamp 1-64 
        res = port.read(bytesToRead).decode('utf-8').rstrip()
        port.reset_input_buffer()
        reading=res

    if (reading!="0" and reading!=""):
        if(matrixArray[int(reading)-1]!="none"):
            sample_path="videos/"+matrixArray[int(reading)-1]
            sample = OMXPlayer(sample_path, args=['--no-osd'], dbus_name='org.mpris.MediaPlayer2.omxplayer1')
            sample.exitEvent += lambda _, exit_code: playerExit(exit_code)
            loop.pause()
            sample.play()
        reading="0"