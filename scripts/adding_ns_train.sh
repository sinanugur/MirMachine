#!/bin/bash

MICRORNA=$1

infernal_location="/cluster/work/projects/ec56/projects_work/mirmachine/infernal112/infernal-1.1.2/"

"$infernal_location/src/cmbuild" -O $MICRORNA.PRE.cmbuild.sto rebuilt.$MICRORNA.PRE.CM $MICRORNA.PRE.sto

"$infernal_location/easel/miniapps/esl-alistat" --iinfo $MICRORNA.PRE.iinfo $MICRORNA.PRE.cmbuild.sto

"$infernal_location/easel/miniapps/esl-alimanip" --outformat pfam --num-rf $MICRORNA.PRE.cmbuild.sto > num.$MICRORNA.PRE.cmbuild.sto

position=$(python /cluster/work/projects/ec56/projects_work/mirmachine/reinfernal/find_loop_end.py $MICRORNA.PRE.cmbuild.sto | awk '/Last/{match($0,/position: ([0-9]+)/,m); print m[1]}')

perl /cluster/work/projects/ec56/projects_work/mirmachine/reinfernal/ali-pfam-add-rfseqs-with-insert.pl -n 10 num.$MICRORNA.PRE.cmbuild.sto $position 2000 | grep -v ^\#\=GS > plus10.$MICRORNA.PRE.cmbuild.sto


"$infernal_location/src/cmbuild" -O tmp.$MICRORNA.PRE.cmbuild.sto plus10.$MICRORNA.PRE.cm plus10.$MICRORNA.PRE.cmbuild.sto

"$infernal_location/src/cmcalibrate" --nonull3 --cpu 10 plus10.$MICRORNA.PRE.cm 
