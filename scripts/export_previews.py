"""Export selected saved notebook plots unchanged for the README."""

import base64
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
# Notebook, unique code fragment, PNG index within that cell, output filename.
PREVIEWS = (
    ("DTEK0042_Exercise_2.ipynb", "ECG Signal first 5000 samples (filtered)", 1, "ecg-filtered.png"),
    ("DTEK0042_Exercise_3.ipynb", "plt.xlim([100,120])", 1, "ppg-peaks.png"),
    ("DTEK0042_Exercise_4_FINAL.ipynb", "pca_out = my_pca.fit_transform", 0, "scg-pca.png"),
)


def main():
    destination = ROOT / "assets"
    destination.mkdir(exist_ok=True)
    for notebook_name, marker, image_index, filename in PREVIEWS:
        notebook = json.loads((ROOT / notebook_name).read_text(encoding="utf-8"))
        cells = [
            cell for cell in notebook["cells"]
            if cell["cell_type"] == "code" and marker in "".join(cell["source"])
        ]
        if len(cells) != 1:
            raise ValueError(f"{notebook_name}: expected one preview cell for {marker!r}")
        images = [
            output["data"]["image/png"]
            for output in cells[0].get("outputs", [])
            if "image/png" in output.get("data", {})
        ]
        if len(images) <= image_index:
            raise ValueError(f"{notebook_name}: rerun with the inline backend to save plots")
        png = base64.b64decode("".join(images[image_index]), validate=True)
        if not png.startswith(b"\x89PNG\r\n\x1a\n"):
            raise ValueError(f"{notebook_name}: selected output is not a PNG")
        (destination / filename).write_bytes(png)
        print(f"exported {filename} ({len(png):,} bytes)")


if __name__ == "__main__":
    main()
