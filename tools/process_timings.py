import pathlib
import re
import pandas as pd

results = [[
    "../results/ball-wall/3D-noremesh-nref0/2023_04_09_17_19_21_476",
    "../results/ball-wall/3D-noremesh-nref1/2023_04_09_17_19_20_847",
    "../results/ball-wall/3D-noremesh-nref2/2023_04_09_17_19_20_806",
    "../results/ball-wall/3D-noremesh-nref3/2023_04_09_17_19_20_847",
    "../results/ball-wall/3D/2023_04_09_17_19_20_812",
], [
    "../results/masticator/3D-noremesh-nref0/2023_04_09_17_19_20_759",
    "../results/masticator/3D-noremesh-nref1/2023_04_09_17_23_20_567",
    "../results/masticator/3D-noremesh-nref2/2023_04_09_18_20_29_496",
    "../results/masticator/3D-noremesh-nref3/2023_04_09_20_14_41_972",
    "../results/masticator/3D/2023_04_09_17_19_20_809",
], [
    "../results/rollers/monkey-soft-hard-noremesh-nref0/2023_04_07_17_26_06_980",
    "../results/rollers/monkey-soft-hard-noremesh-nref1/2023_04_07_17_28_07_468",
    "../results/rollers/monkey-soft-hard-noremesh-nref2/2023_04_07_17_31_07_765",
    "../results/rollers/monkey-soft-hard-noremesh-nref3/2023_04_07_17_32_07_423",
    "../results/rollers/monkey-soft-hard/2023_04_10_20_22_50_759",
], [
    "../results/spikes3d/restart_031-noremesh-nref0/2023_04_13_21_55_40_484",
    "../results/spikes3d/restart_031-noremesh-nref1/2023_04_13_21_55_40_512",
    "../results/spikes3d/restart_031-noremesh-nref2/2023_04_13_21_55_40_525",
    "../results/spikes3d/restart_031-noremesh-nref3/xxx",
    "../results/spikes3d/restart_031/2023_04_13_21_55_40_703",
], [
    "../results/twisting-beam/twisting-beam-noremesh-nref0/2023_04_10_19_53_48_263",
    "../results/twisting-beam/twisting-beam-noremesh-nref1/2023_04_10_19_55_48_223",
    "../results/twisting-beam/twisting-beam-noremesh-nref2/2023_04_10_20_04_48_871",
    "../results/twisting-beam/twisting-beam-noremesh-nref3/2023_04_10_19_53_48_278",
    "../results/twisting-beam/twisting-beam/2023_04_10_19_53_48_283",
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

max_steps = [0] * len(scenes)
for i, scene in enumerate(results):
    dir = pathlib.Path(scene[-1])
    assert((dir / "stats.csv").exists())
    stats = pd.read_csv(dir / "stats.csv")
    max_steps[i] = stats.shape[0]

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
            df.iloc[i, j] = (stats["forward"] + stats["remeshing"] + stats["global_relaxation"])[:max_steps[i]].mean()
            mem_df.iloc[i, j] = stats["peak_mem"][:max_steps[i]].max()
            progress.iloc[i, j] = stats["time"][:max_steps[i]].max()
        except:
            pass

print("Average time per step")
print(df)
print("\nPeak memory usage")
print(mem_df)
print("\nFinal timestep")
print(progress)