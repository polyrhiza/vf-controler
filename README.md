```text
 _  _  ____  ____  ____  __  ___   __   __      ____  __   ____  _  _       
/ )( \(  __)(  _ \(_  _)(  )/ __) / _\ (  )    (  __)/ _\ (  _ \( \/ )      
\ \/ / ) _)  )   /  )(   )(( (__ /    \/ (_/\   ) _)/    \ )   // \/ \      
 \__/ (____)(__\_) (__) (__)\___)\_/\_/\____/  (__) \_/\_/(__\_)\_)(_/      
          ___  __   __ _  ____  ____   __   __    ____  ____                
         / __)/  \ (  ( \(_  _)(  _ \ /  \ (  )  (  __)(  _ \               
        ( (__(  O )/    /  )(   )   /(  O )/ (_/\ ) _)  )   /               
         \___)\__/ \_)__) (__) (__\_) \__/ \____/(____)(__\_)  

A vertical farm controler to interface with Vertical Futures command line interface.

Currently, the override lights options uses a light calculator made from scratch specifically
for the Duckweed trays custom made for Plants For Space and are not relevent to regular INFT or 
AERO canals. Light recipies and the original light calculator provivded by Vertical Future will
eventually be implemented.

Current Functions:
- Create new SSH connection
- Save and open previous SSH connections
- Calculate total light output (um/m2/s) in each channel using DMX energy values.
- Calculate DMX energy values needed to produced desired light recipie
- Adjust fan speed in all canals.
- Add scheduled light recipes for all canals.
