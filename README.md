# PinTVNG
Interactive Pinball TV with  Raspberry PI


#Install

sudo apt-get install -y libdbus-1-3 libdbus-1-dev python3-pip omxplayer
pip install omxplayer-wrapper pyserial

All movies need to be in videos folder, the main movie (loop) need to be named loop.mp4

create data.txt file with movies names, each line corresponds to a switch/lamp in matrix, first line is first swicth, second line is second switch to the end (64)
If there is no movie associate to the switch/lamp put "none" in file (se example file).
