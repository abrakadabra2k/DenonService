Descpription: Change the Output of a Denon AVR to AUX1 via Telnet (Denon fixed IP at 192.168.178.21) 

Save the contents of SetDenonAux1.py script to /home/moode/SetDenonAux1.py
Save the contents of Denon.service script to /lib/systemd/system/Denon.service
Run the following commands
    sudo systemctl enable Denon
    sudo service Denon start
    
Denon's telnet descpription: https://assets.denon.com/documentmaster/uk/avr1713_avr1613_protocol_v860.pdf
Tested on an AVR-X1600H with Moode 9.1.3
