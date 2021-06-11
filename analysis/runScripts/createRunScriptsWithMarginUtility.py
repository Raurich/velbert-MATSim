def write_file(pt_const, bike_const, car_const, pt_margin, output):
    script = """#!/bin/bash --login
#$ -cwd
#$ -N velbert
#$ -m be
#$ -M p.heinrich@campus.tu-berlin.de
#$ -j y
#$ -o job-log-1pct{4}
#$ -l h_rt=80000
#$ -l mem_free=4G
#$ -pe mp 4

RUN_ID="velbert-v1.0-1pct"
JAR="./matsim-velbert-0.0.1-SNAPSHOT-margin.jar"
MAIN_CLASS="org.matsim.velbert.RunVelbert"

ARGS="{0} {1} {2} {3} ./input/config.xml --config:controler.runId $RUN_ID --config:plans.inputPlansFile matsim-velbert-v1.0-1pct.plans.xml.gz --config:controler.outputDirectory ./output-$RUN_ID-{4}"

# make sure java is present
module add java/11

# start matsim
java -cp $JAR -Xmx16G $MAIN_CLASS $ARGS"""

    f = open(f"velbertRun{output}.sh", "w", newline="\n")
    f.write(script.format(pt_const, bike_const, car_const, pt_margin, output))
    f.close()

    f = open(f"qsubRun.sh", "a", newline="\n")
    f.write(f"qsub velbertRun{output}.sh \n")
    f.close()


pt_options = [-5, -9, -13]
bike_options = [-4]
car_options = [0]
pt_margin = [-5, -7, -9]

count = 106

for p in pt_options:
    for b in bike_options:
        for c in car_options:
            for p_m in pt_margin:
                write_file(p, b, c, p_m, count)
                print(f"Id {count}: {p}, {b}, {c}")
                count += 1
