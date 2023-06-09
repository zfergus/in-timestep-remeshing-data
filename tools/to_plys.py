from rclone import Rclone
import shutil
import numpy as np
import pathlib
import xml.etree.ElementTree as ET
import meshio
import igl
from tqdm import tqdm


def resolve_path(path, root: pathlib.Path) -> pathlib.Path:
    path = pathlib.Path(path)
    if path.is_absolute():
        return path
    return (root / path).resolve()


def parse_vtm(path):
    tree = ET.parse(path)
    root = tree.getroot()
    blocks = root.find("vtkMultiBlockDataSet").findall("Block")
    # assert(len(blocks) == 1)
    for block in blocks:
        # if block.get("name") == "Volume":
        if block.get("name") == "Surface":
            break
    datasets = block.findall("DataSet")
    for dataset in datasets:
        # if dataset.get("name") == "data":
        # if dataset.get("name") == "contact":
        if dataset.get("name") == "surface":
            break
    return resolve_path(dataset.attrib["file"], path.parent)


def parse_pvd(path):
    tree = ET.parse(path)
    root = tree.getroot()
    frames = root.find("Collection").findall("DataSet")
    assert (len(frames) > 0)

    meshes = []
    for f in map(lambda f: f.attrib["file"], frames):
        f = resolve_path(f, path.parent)
        if f.suffix == ".vtm":
            f = parse_vtm(f)
        meshes.append(resolve_path(f, path.parent))

    return meshes


def load_mesh(path):
    mesh = meshio.read(path)

    V, I, J, _ = igl.remove_duplicate_vertices(
        mesh.points, np.array([], dtype=int), 1e-7)

    CV = []  # codim vertices
    E = []  # edges
    F = []  # triangles
    for cells in mesh.cells:
        if cells.type == "triangle":
            F.append(J[cells.data])
        elif cells.type == "tetra":
            F.append(igl.boundary_facets(J[cells.data]))
        elif cells.type == "line":
            E.append(J[cells.data])
        elif cells.type == "vertex":
            CV.append(J[cells.data])
        else:
            raise Exception("Unsupported cell type: {}".format(cells.type))

    cells = []
    if F:
        cells.append(("triangle", np.vstack(F).astype("int32")))
    if E:
        cells.append(("line", np.vstack(E).astype("int32")))
    if CV:
        cells.append(("vertex", np.vstack(CV).astype("int32")))

    if "solution" in mesh.point_data:
        # V += mesh.point_data["solution"][I]
        point_data = {"U": mesh.point_data["solution"][I]}
    else:
        point_data = {}

    mesh = meshio.Mesh(points=V, cells=cells, point_data=point_data)

    return mesh


sim_files = results = [
    "../results/ball-wall/3D-noremesh-nref0/2023_04_09_17_19_21_476",
    "../results/ball-wall/3D-noremesh-nref1/2023_04_09_17_19_20_847",
    "../results/ball-wall/3D-noremesh-nref2/2023_04_09_17_19_20_806",
    "../results/ball-wall/3D-noremesh-nref3/2023_04_09_17_19_20_847",
    "../results/ball-wall/3D/2023_04_09_17_19_20_812",
    #
    "../results/masticator/3D-noremesh-nref0/2023_04_09_17_19_20_759",
    "../results/masticator/3D-noremesh-nref1/2023_04_09_17_23_20_567",
    "../results/masticator/3D-noremesh-nref2/2023_04_09_18_20_29_496",
    "../results/masticator/3D-noremesh-nref3/2023_04_09_20_14_41_972",
    "../results/masticator/3D/2023_04_09_17_19_20_809",
    #
    "../results/rollers/monkey-soft-hard-noremesh-nref0/2023_04_19_00_30_36_700",
    "../results/rollers/monkey-soft-hard-noremesh-nref1/2023_04_19_00_30_36_671",
    "../results/rollers/monkey-soft-hard-noremesh-nref2/2023_04_19_00_30_36_704",
    "../results/rollers/monkey-soft-hard-noremesh-nref3/2023_04_19_00_26_32_295",
    "../results/rollers/monkey-soft-hard/2023_04_19_10_11_00_432",
    #
    "../results/spikes3d/restart_031-noremesh-nref0/2023_04_13_21_55_40_484",
    "../results/spikes3d/restart_031-noremesh-nref1/2023_04_13_21_55_40_512",
    "../results/spikes3d/restart_031-noremesh-nref2/2023_04_13_21_55_40_525",
    "../results/spikes3d/restart_031-noremesh-nref3/2023_04_19_13_40_13_148",
    "../results/spikes3d/restart_031/2023_04_13_21_55_40_703",
    #
    "../results/twisting-beam/twisting-beam-noremesh-nref0/2023_04_10_19_53_48_263",
    "../results/twisting-beam/twisting-beam-noremesh-nref1/2023_04_10_19_55_48_223",
    "../results/twisting-beam/twisting-beam-noremesh-nref2/2023_04_10_20_04_48_871",
    "../results/twisting-beam/twisting-beam-noremesh-nref3/2023_04_10_19_53_48_278",
    "../results/twisting-beam/twisting-beam/2023_04_10_19_53_48_283",
]
sim_files = [pathlib.Path(f).resolve() / "sim.pvd" for f in sim_files]

with open(pathlib.Path.home() / ".config" / "rclone" / "rclone.conf") as f:
    cfg = f.read()
rclone = Rclone(cfg)

for f in sim_files:
    if not f.exists():
        continue

    print(f)
    meshes = []
    if f.suffix == ".pvd":
        meshes = parse_pvd(f)
    else:
        meshes.append(f)

    out_dir = f.parent / "plys"

    if "noremesh" not in str(f):
        meshes = meshes[0::3]
        # if out_dir.exists():
        #     shutil.rmtree(out_dir)

    out_dir.mkdir(parents=True, exist_ok=True)

    any_new_meshes = False
    for i, mesh in enumerate(tqdm(meshes)):
        if (out_dir / f"{i:04d}.ply").exists():
            continue
        any_new_meshes = True
        mesh = load_mesh(mesh)
        U = mesh.point_data["U"]
        mesh.point_data = {}
        meshio.write(out_dir / f"rest_{i:04d}.ply", mesh)
        mesh.points += U
        meshio.write(out_dir / f"deformed_{i:04d}.ply", mesh)

    if any_new_meshes:
        remote_path = "drive:remeshing-plys" + "/" + str(
            f.parent.relative_to("/scratch/zjf214/remeshing-project-results"))
        print(f"Uploading to {remote_path}")
        rclone.copy(str(out_dir), remote_path)

    remote_path = "drive:remeshing-csv" + "/" + str(
        f.parent.relative_to("/scratch/zjf214/remeshing-project-results"))
    print(f"Uploading to {remote_path}")
    # for csv in list(f.parent.glob("*.csv")) + list(f.parent.glob("log.txt")):
    #    rclone.copy(csv, remote_path)
