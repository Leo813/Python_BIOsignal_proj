# Biosignal Analysis Course Project

This course project filters and analyzes biosignal recordings through three Python Jupyter notebooks. The exercises cover electrocardiogram (ECG), photoplethysmogram (PPG), and seismocardiogram (SCG) signals, with code, plots, and observations for each analysis.

All datasets referenced by the notebooks are included in the repository. Keep the directory structure intact and run the notebooks from the repository root so their relative data paths resolve correctly.

## Project Structure

| Path | Contents |
| --- | --- |
| `DTEK0042_Exercise_2.ipynb` | ECG visualization, Fourier analysis, Butterworth band-pass filtering, and ECG/QRS analysis with BioSPPy. |
| `DTEK0042_Exercise_3.ipynb` | PPG power spectral density, band-pass filtering, peak detection, and heart-rate and variability calculations. |
| `DTEK0042_Exercise_4_FINAL.ipynb` | SCG segmentation, statistical and spectral feature extraction, and PCA visualization of normal and noisy recordings. |
| `ECG_800hz.txt` | Single-column ECG recording analyzed at 800 Hz. |
| `PPG_record.txt` | Comma-separated timestamp, red, infrared, and green channels. Exercise 3 analyzes the infrared channel at 132 Hz. |
| `dataset/` | Four `Normal_data_*.txt` and four `Noisy_data_*.txt` SCG recordings. Exercise 4 uses the third column (Z-axis) at 200 Hz. |

The notebooks are independent entry points; they do not import one another. There is no standalone application or command-line entry point.

## Setup

Use Python 3 and a Jupyter notebook environment. The saved notebook metadata records Python 3.8.5, but the repository does not specify supported versions or provide a dependency lockfile.

The notebook imports require:

- NumPy, SciPy, and Matplotlib for all three exercises.
- BioSPPy for Exercise 2.
- pandas and scikit-learn for Exercise 4.

To install these dependencies and Jupyter Notebook into your chosen Python environment:

```sh
python -m pip install notebook numpy scipy matplotlib biosppy pandas scikit-learn
```

This package list is based on the notebook imports; compatibility with current package versions has not been verified.

## Usage

1. Open a terminal in the repository root.
2. Start Jupyter Notebook:

   ```sh
   python -m notebook
   ```

3. Open the exercise you want to explore and select the Python environment containing the dependencies above.
4. Run its cells in order from top to bottom. Later cells depend on variables and functions defined earlier in the notebook.
5. Inspect the plots and printed results alongside the exercise instructions and observations.

### Filename note

Exercise 2's written data-import instruction refers to `ECG_800Hz.txt`, but the file in this repository—and the path used by the notebook's loading cell—is `ECG_800hz.txt`. On case-sensitive filesystems, use the repository filename with the lowercase `h`.

Exercise 4 currently uses Windows-style paths (`dataset\*.txt`) and backslash-based filename parsing. Running it unchanged on Linux, macOS, or Google Colab is not supported by those paths. Its initial data-loading cells also assume the glob results list noisy recordings before normal recordings.

The notebooks include instructions for exporting an HTML copy. For example, from the repository root:

```sh
jupyter nbconvert --to html DTEK0042_Exercise_2.ipynb
```

## Validation and limitations

There is no automated test suite or test command. Exercise 4 includes a small feature-extraction example that prints results for a synthetic signal, without assertions.

These notebooks are course exercises with saved outputs, rather than a validated analysis package. In particular, Exercise 3's interval averaging and RMSSD calculation need review, and its variability values remain in seconds despite the exercise requesting milliseconds. Exercise 4 standardizes each segment's feature vector individually before PCA, rather than standardizing feature columns across segments.
