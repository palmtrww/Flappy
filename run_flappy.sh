#!/bin/bash

clear

echo -en "\033]0;Flappy\a"
echo -en "Flappy"

run()
{
    echo 'Installing Requirments' 
    pip3 install -r requirements.txt
    clear
    echo 'Finished Installing Requirments'
    echo 'Finally! Time to run the bot!'
    python3 run.py
         
}
run