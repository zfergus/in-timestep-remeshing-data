import pathlib
import re
import pandas as pd

results = [[
    "../results/ball-wall/3D-noremesh-nref0/2023_03_20_16_16_01_759",
    "../results/ball-wall/3D-noremesh-nref1/2023_03_20_16_29_09_880",
    "../results/ball-wall/3D-noremesh-nref2/2023_03_20_16_38_16_660",
    "../results/ball-wall/3D-noremesh-nref3/2023_03_20_17_26_45_789",
    "../results/ball-wall/3D/2023_03_22_15_15_25_159",
], [
    "../results/masticator/3D-noremesh-nref0/2023_03_20_17_30_56_803",
    "../results/masticator/3D-noremesh-nref1/2023_03_20_17_47_00_837",
    "../results/masticator/3D-noremesh-nref2/2023_03_20_17_56_02_753",
    "../results/masticator/3D-noremesh-nref3/2023_03_20_18_13_10_779",
    "../results/masticator/3D/2023_03_22_15_15_26_226",
], [
    "../results/rollers/monkey-soft-hard-noremesh-nref0/2023_03_23_21_55_12_177",
    "../results/rollers/monkey-soft-hard-noremesh-nref1/2023_03_20_19_17_38_820",
    "../results/rollers/monkey-soft-hard-noremesh-nref2/2023_03_20_19_18_39_023",
    "../results/rollers/monkey-soft-hard-noremesh-nref3/2023_03_20_19_19_40_403",
    "../results/rollers/monkey-soft-hard/2023_03_23_21_55_12_067",
], [
    "../results/spikes3d/drop-ball-noremesh-nref0/2023_03_20_18_19_18_337",
    "../results/spikes3d/drop-ball-noremesh-nref1/2023_03_20_18_20_12_971",
    "../results/spikes3d/drop-ball-noremesh-nref2/2023_03_20_18_27_18_623",
    "../results/spikes3d/drop-ball-noremesh-nref3/2023_03_08_20_59_14_558",
    "../results/spikes3d/drop-ball/2023_03_22_15_20_30_448",
], [
    "../results/twisting-beam/twisting-beam-noremesh-nref0/2023_03_20_18_18_15_509",
    "../results/twisting-beam/twisting-beam-noremesh-nref1/2023_03_20_18_19_12_461",
    "../results/twisting-beam/twisting-beam-noremesh-nref2/2023_03_20_18_19_12_307",
    "../results/twisting-beam/twisting-beam-noremesh-nref3/2023_03_20_18_19_12_379",
    "../results/twisting-beam/twisting-beam/2023_03_22_15_20_30_423",
]]

for scene in results:
    for dir in scene:
        dir = pathlib.Path(dir)
        if (dir / "stats.csv").exists():
            continue

        stats = {}

        important_lines = []
        try:
            print(f"Reading {(dir / 'log.txt').resolve()}")
            with open(dir / "log.txt") as f:
                lines = f.readlines()
        except:
            print(f"Failed to read {(dir / 'log.txt').resolve()}")
            continue
        for i, line in enumerate(lines):
            if re.match(".*/*  t=.*", line):
                step = int(re.findall(".* (\d+)/.*", line)[0])
                stats[step] = {
                    "time": float(re.findall(".* t=(.+)", line)[0]),
                    "forward": float(re.findall(".*: (\d+\.?\d*) s, .* s, .* s", lines[i+1])[0]),
                    "remeshing": float(re.findall(".*: (\d+\.?\d*) s, .* s, .* s", lines[i+2])[0]),
                    "global_relaxation": float(re.findall(".*: (\d+\.?\d*) s, .* s, .* s", lines[i+3])[0]),
                    "peak_mem": float(re.findall(".*: (\d+\.?\d*) GiB", lines[i+4])[0]),
                }

        df = pd.DataFrame(stats).T
        df.to_csv(dir / "stats.csv")

scenes = ["ball-wall", "masticator", "gorilla-rollers", "drop-ball", "twisting-beam"]
nrefs  = ["nref0", "nref1", "nref2", "nref3", "ours"]
df = pd.DataFrame(index=scenes, columns=nrefs)
mem_df = pd.DataFrame(index=scenes, columns=nrefs)
progress = pd.DataFrame(index=scenes, columns=nrefs)
for i, scene in enumerate(results):
    for j, dir in enumerate(scene):
        dir = pathlib.Path(dir)
        if not (dir / "stats.csv").exists():
            continue
        stats = pd.read_csv(dir / "stats.csv")
        try:
            df.iloc[i, j] = (stats["forward"] + stats["remeshing"] + stats["global_relaxation"]).mean()
            mem_df.iloc[i, j] = stats["peak_mem"].max()
            progress.iloc[i, j] = stats["time"].max()
        except:
            pass

print("Average time per step")
print(df)
print("\nPeak memory usage")
print(mem_df)
print("\nFinal timestep")
print(progress)