#!/bin/bash --login
#$ -cwd
#$ -N velbert
#$ -m be
#$ -M p.heinrich@campus.tu-berlin.de
#$ -j y
#$ -o job-log-1pct42
#$ -l h_rt=80000
#$ -l mem_free=4G
#$ -pe mp 4

RUN_ID="velbert-v1.0-1pct"
JAR="./matsim-velbert-0.0.1-SNAPSHOT.jar"
MAIN_CLASS="org.matsim.velbert.RunVelbert"

ARGS="-20 -5 0 ./input/config.xml --config:controler.runId $RUN_ID --config:plans.inputPlansFile matsim-velbert-v1.0-1pct.plans.xml.gz --config:controler.outputDirectory ./output-$RUN_ID-42"

# make sure java is present
module add java/11

# start matsim
java -cp $JAR -Xmx16G $MAIN_CLASS $ARGS