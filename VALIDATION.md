# Recorded validation and output curation

## Local run: 2026-09-24

A new virtual environment used Python 3.11.16 on Windows and installed the
unchanged `requirements.txt`. All direct pins were retained, including
Matplotlib 3.8.3 and IPython 8.22.2. `python -m pip check` reported no broken
requirements. Transitive packages are not fully locked; this run resolved
nbconvert 7.17.1, nbclient 0.11.0, ipykernel 7.3.0, and matplotlib-inline 0.2.2.

`python scripts/validate_repository.py` passed for all three notebooks and all
ten data files. Its observed row counts matched `DATA.md`.
`python -m unittest discover -s tests -v` passed all five SCG numerical and plot
tests. See `SCG_REVIEW.md` for their scope.

Every notebook was executed in its own fresh kernel with nbconvert and a
300-second per-cell timeout. Wall-clock times below include kernel startup.
The first pass used `MPLBACKEND=Agg`, matching the existing CI backend. A
second pass used the inline backend to regenerate embedded figures.

| Notebook | Agg pass | Inline pass | Saved PNG plots |
| --- | ---: | ---: | ---: |
| `DTEK0042_Exercise_2.ipynb` | 8.38 s, passed | 8.86 s, passed | 10 |
| `DTEK0042_Exercise_3.ipynb` | 5.95 s, passed | 6.93 s, passed | 9 |
| `DTEK0042_Exercise_4_FINAL.ipynb` | 7.28 s, passed | 6.40 s, passed | 3 |

No execution failed. This local run used Windows, whereas GitHub Actions uses
Ubuntu; it is not a claim of identical platform behavior.

## Warnings and review

- The Agg pass warned that its non-interactive canvas cannot show figures.
  Agg results were kept out of the committed notebooks so they would not
  replace embedded plots with warning text.
- Exercise 4's nine-sample feature-extraction demonstration caused SciPy to
  shorten Welch's default `nperseg` from 256 to 9. The inline notebook retains
  this warning, with the machine-specific environment path redacted. Actual
  recording segments contain 1,000 samples. The demonstration and its
  methodology were not changed.
- The local Jupyter launcher logged a Windows Proactor/ZeroMQ selector-thread
  warning and a kernel TCP transport warning. They did not interrupt either
  execution pass. No warning filters or permissive execution flags were used.

All 22 rendered plots were visually inspected. The refreshed outputs contain
no saved errors, and every code cell has an execution count. Printed values
remain exploratory outputs, subject to the limitations in the README.
Exercise 3's refreshed SDNN and RMSSD values differ slightly from the old saved
outputs. Its analysis source is unchanged; the current run's values are retained
without interpreting those differences as a methodological correction.
The SCG plot now has separate, correctly colored legend entries for `Noisy`
and `Normal`; its preprocessing and PCA scores are unchanged by that edit.

The curation retained code and markdown, refreshed outputs and Python metadata,
and removed obsolete output-renderer IDs and old execution timestamps. Three PNG previews were exported
byte-for-byte from the selected saved outputs with `scripts/export_previews.py`.
The previews total approximately 186 KiB.

## Repeat the checks

From the repository root in the Python 3.11 environment:

```sh
python -m pip check
python scripts/validate_repository.py
python -m unittest discover -s tests -v
```

The unchanged clean-kernel CI execution command is in
[`.github/workflows/validate.yml`](.github/workflows/validate.yml).
For output curation in PowerShell, write an inline run to a temporary directory:

```powershell
$env:MPLBACKEND = 'module://matplotlib_inline.backend_inline'
$outputDir = Join-Path ([IO.Path]::GetTempPath()) ('biosignal-' + [guid]::NewGuid())
New-Item -ItemType Directory $outputDir | Out-Null
foreach ($notebook in Get-ChildItem DTEK0042_*.ipynb) {
    python -m nbconvert --to notebook --execute $notebook.Name --output-dir $outputDir --ExecutePreprocessor.timeout=300
    if ($LASTEXITCODE -ne 0) { throw "Notebook execution failed: $($notebook.Name)" }
}
```

Review the temporary notebooks before transferring their outputs to the
tracked notebooks. Preserve warnings and analysis source; omit transient
execution timestamps and workstation paths. After updating the saved outputs,
run `python scripts/export_previews.py`, inspect the images, and review
`git diff --check` and the complete diff before committing.

## Remaining review boundaries

Publication permission and provenance remain undocumented, as described in
`RIGHTS.md` and `DATA.md`; this work does not resolve or grant rights. The SCG
numerical review does not replace domain input. Exercise 3's metric review,
directory restructuring, and renaming remain outside this change.
