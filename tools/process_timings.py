import pathlib
import re
import pandas as pd
import numpy as np

results = [[
    "../results/spikes3d/restart_031-noremesh-nref0/2023_04_13_21_55_40_484",
    "../results/spikes3d/restart_031-noremesh-nref1/2023_04_13_21_55_40_512",
    "../results/spikes3d/restart_031-noremesh-nref2/2023_04_13_21_55_40_525",
    "../results/spikes3d/restart_031-noremesh-nref3/2023_04_19_13_40_13_148",
    "../results/spikes3d/restart_031/2023_04_13_21_55_40_703",
], [
    "../results/masticator/3D-noremesh-nref0/2023_04_09_17_19_20_759",
    "../results/masticator/3D-noremesh-nref1/2023_04_09_17_23_20_567",
    "../results/masticator/3D-noremesh-nref2/2023_04_09_18_20_29_496",
    "../results/masticator/3D-noremesh-nref3/2023_04_09_20_14_41_972",
    "../results/masticator/3D/2023_04_09_17_19_20_809",
], [
    "../results/rollers/monkey-soft-hard-noremesh-nref0/2023_04_19_00_30_36_700",
    "../results/rollers/monkey-soft-hard-noremesh-nref1/2023_04_19_00_30_36_671",
    "../results/rollers/monkey-soft-hard-noremesh-nref2/2023_04_19_00_30_36_704",
    "../results/rollers/monkey-soft-hard-noremesh-nref3/2023_04_19_00_26_32_295",
    "../results/rollers/monkey-soft-hard/2023_04_19_10_11_00_432",
], [
    "../results/twisting-beam/twisting-beam-noremesh-nref0/2023_04_10_19_53_48_263",
    "../results/twisting-beam/twisting-beam-noremesh-nref1/2023_04_10_19_55_48_223",
    "../results/twisting-beam/twisting-beam-noremesh-nref2/2023_04_10_20_04_48_871",
    "../results/twisting-beam/twisting-beam-noremesh-nref3/2023_04_10_19_53_48_278",
    "../results/twisting-beam/twisting-beam/2023_04_10_19_53_48_283",
], [
    "../results/ball-wall/3D-noremesh-nref0/2023_04_09_17_19_21_476",
    "../results/ball-wall/3D-noremesh-nref1/2023_04_09_17_19_20_847",
    "../results/ball-wall/3D-noremesh-nref2/2023_04_09_17_19_20_806",
    "../results/ball-wall/3D-noremesh-nref3/2023_04_09_17_19_20_847",
    "../results/ball-wall/3D/2023_04_09_17_19_20_812",
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

scenes = [
    r"Ball on spikes (\cref{fig:teaser})",
    r"Masticator (\cref{fig:masticator-remeshing-demo})",
    r"Gorilla rollers (\cref{fig:gorilla-rollers})",
    r"Bar-twist (\cref{fig:bar-remeshing-demo})",
    r"Impacting ball (\cref{fig:sphere-remeshing-demo})",
]
nrefs  = ["UR 0", "UR 1", "UR 2", "UR 3", "Ours"]

max_steps = [0] * len(scenes)
for i, scene in enumerate(results):
    dir = pathlib.Path(scene[-1])
    assert((dir / "stats.csv").exists())
    stats = pd.read_csv(dir / "stats.csv")
    max_steps[i] = stats.shape[0]
    if i == 2:
        max_steps[i] -= 1

def int_format(x):
    if x > 1e6:
        return r"{:d}M".format(int(x // 1e6))
    if x > 1e3:
        return r"{:d}k".format(int(x // 1e3))
    return "{:d}".format(x)

df = pd.DataFrame(index=scenes, columns=nrefs)
mem_df = df.copy()
dof_df = pd.DataFrame(index=scenes, columns=nrefs[:-1]+["Ours (min,avg,max)"])
progress = df.copy()
for i, scene in enumerate(results):
    for j, dir in enumerate(scene):
        dir = pathlib.Path(dir)
        if not (dir / "stats.csv").exists():
            continue
        stats = pd.read_csv(dir / "stats.csv")
        try:
            df.iloc[i, j] = (stats["forward"] + stats["remeshing"] + stats["global_relaxation"])[:max_steps[i]].mean()
            mem_df.iloc[i, j] = stats["peak_mem"][:max_steps[i]].max()
            if (j == 4):
                dof_df.iloc[i, j] = (
                    int_format(stats["#V"][:max_steps[i]].min() * 3) + ", "
                    + int_format(stats["#V"][:max_steps[i]].mean() * 3) + ", "
                    + int_format(stats["#V"][:max_steps[i]].max() * 3)
                )
            else:
                dof_df.iloc[i, j] = int_format(stats["#V"][:max_steps[i]].min() * 3)
            progress.iloc[i, j] = min(stats.shape[0], max_steps[i]) # stats["time"][:max_steps[i]].max()
        except:
            pass

def float_format(x):
    if x >= 1000:
        return r"{:d}\,{:05.1f}".format(int(x // 1000), x % 1000)
    return "{:.1f}".format(x)

def format_latex(df, format=float_format):
    return df.to_latex(float_format=format).replace(r"\textbackslash ", "\\").replace(r"\{", "{").replace(r"\}", "}").replace("llllll", "lrrrrr")

# df_latex = format_latex(df)
# mem_df_latex = format_latex(mem_df)
dof_df_latex = format_latex(dof_df, format=None)
# print(f"""\
# Average running time per step (\\unit{{\\s}})
# {df_latex}

# \\vspace{{1em}}

# Peak memory (\\unit{{\\gibi\\byte}})
# {mem_df_latex}

# \\vspace{{1em}}

# Number of \\Ac{{DOF}}
# {dof_df_latex}
# """)

df = pd.concat([df, mem_df], axis=1)
df_latex = format_latex(df)

print(f"""\
Average running time per step (\\unit{{\\s}})
{df_latex}

\\vspace{{1em}}

Number of \\Ac{{DOF}}
{dof_df_latex}
""")

print("\nNumber of timestep")
print(progress)