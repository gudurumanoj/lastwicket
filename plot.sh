#!/bin/bash

python plotter.py RP

if [ "$1" == "q" ]
then
    for val in `cat q_values.txt`
    do
        python cricket_states.py --balls 15 --runs 30 > statefile
        python encoder.py --states statefile --parameters data/cricket/sample-p1.txt --q $val > mdpfile
        python planner.py --mdp mdpfile > vpfile
        python decoder.py --value-policy vpfile --states statefile > output.txt

        python planner.py --policy RANDPOL.txt --mdp mdpfile > vpfile_rand
        
        python plotter.py SQ $val >> QSCORES.txt
    done

        python plotter.py QP
fi

if [ "$1" == "qf" ]
then
    python plotter.py QP
fi

if [ "$1" == "runs" ]
then

        python cricket_states.py --balls 15 --runs 30 > statefile
        python encoder.py --states statefile --parameters data/cricket/sample-p1.txt --q 0.25 > mdpfile
        python planner.py --mdp mdpfile > vpfile

        python planner.py --policy RANDPOL.txt --mdp mdpfile > vpfile_rand
        
        python plotter.py runs_plot

fi

if [ "$1" == "balls" ]
then

        python cricket_states.py --balls 15 --runs 30 > statefile
        python encoder.py --states statefile --parameters data/cricket/sample-p1.txt --q 0.25 > mdpfile
        python planner.py --mdp mdpfile > vpfile

        python planner.py --policy RANDPOL.txt --mdp mdpfile > vpfile_rand
        
        python plotter.py balls_plot

fi
