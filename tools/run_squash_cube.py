import pathlib
import subprocess

polyfem_bin = "/Users/zachary/Development/grad-research/polyfem/polyfem/build/release/PolyFEM_bin"
has_contact = True

root = pathlib.Path(__file__).parents[1]
scripts_dir = root / "scripts" / "squash" / "square"
output_dir = (root / "output" / "squash" / "square" /
              ("contact" if has_contact else "no_contact"))

for script in scripts_dir.glob("*.json"):
    if script.stem == "defaults":
        continue

    print(f"Running {script}")
    subprocess.run([str(polyfem_bin),
                    "-j", str(script),
                    "-o", str(output_dir / script.stem),
                    "--ngui"])
