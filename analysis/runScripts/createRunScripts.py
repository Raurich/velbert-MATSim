def write_file(pt_const, bike_const, car_const, output):
    script = """#!/bin/bash --login
#$ -cwd
#$ -N velbert
#$ -m be
#$ -M p.heinrich@campus.tu-berlin.de
#$ -j y
#$ -o job-log-1pct{3}
#$ -l h_rt=80000
#$ -l mem_free=4G
#$ -pe mp 4

RUN_ID="velbert-v1.0-1pct"
JAR="./matsim-velbert-0.0.1-SNAPSHOT.jar"
MAIN_CLASS="org.matsim.velbert.RunVelbert"

ARGS="{0} {1} {2} ./input/config.xml --config:controler.runId $RUN_ID --config:plans.inputPlansFile matsim-velbert-v1.0-1pct.plans.xml.gz --config:controler.outputDirectory ./output-$RUN_ID-{3}"

# make sure java is present
module add java/11

# start matsim
java -cp $JAR -Xmx16G $MAIN_CLASS $ARGS"""

    f = open(f"velbertRun{output}.sh", "w", newline="\n")
    f.write(script.format(pt_const, bike_const, car_const, output))
    f.close()

    f = open(f"qsubRun.sh", "a", newline="\n")
    f.write(f"qsub velbertRun{output}.sh \n")
    f.close()


pt_options = [-20, -25, -30]
bike_options = [-3, -4, -5]
car_options = [0]

count = 40

for p in pt_options:
    for b in bike_options:
        for c in car_options:
            write_file(p, b, c, count)
            print(f"Id {count}: {p}, {b}, {c}")
            count += 1
