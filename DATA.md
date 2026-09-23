# Data reference

The repository includes every recording loaded by the notebooks. The facts
below are derived from the committed files and notebook instructions. The
files have no embedded headers, and no external provenance, collection
protocol, physical units, participant information, consent statement, or data
license is included. Those details should not be inferred.

## File inventory

| Files | Rows | Columns | Delimiter | Notebook interpretation |
| --- | ---: | ---: | --- | --- |
| `ECG_800hz.txt` | 700,001 | 1 | whitespace | ECG amplitude sampled at 800 Hz |
| `PPG_record.txt` | 43,404 | 4 | comma | timestamp, red, infrared, and green; infrared is analyzed at 132 Hz |
| `dataset/Noisy_data_1.txt` | 6,099 | 3 | whitespace | noisy SCG axes; column 3 (Z-axis) is analyzed at 200 Hz |
| `dataset/Noisy_data_2.txt` | 6,199 | 3 | whitespace | noisy SCG axes; column 3 (Z-axis) is analyzed at 200 Hz |
| `dataset/Noisy_data_3.txt` | 7,300 | 3 | whitespace | noisy SCG axes; column 3 (Z-axis) is analyzed at 200 Hz |
| `dataset/Noisy_data_4.txt` | 6,700 | 3 | whitespace | noisy SCG axes; column 3 (Z-axis) is analyzed at 200 Hz |
| `dataset/Normal_data_1.txt` | 12,000 | 3 | whitespace | normal SCG axes; column 3 (Z-axis) is analyzed at 200 Hz |
| `dataset/Normal_data_2.txt` | 12,000 | 3 | whitespace | normal SCG axes; column 3 (Z-axis) is analyzed at 200 Hz |
| `dataset/Normal_data_3.txt` | 14,000 | 3 | whitespace | normal SCG axes; column 3 (Z-axis) is analyzed at 200 Hz |
| `dataset/Normal_data_4.txt` | 12,000 | 3 | whitespace | normal SCG axes; column 3 (Z-axis) is analyzed at 200 Hz |

“Normal” and “Noisy” reproduce the filenames and notebook labels; the
repository does not define a clinical meaning for them. The PPG notebook calls
its detected peak spacings “RR intervals,” but they are derived from PPG rather
than a simultaneously recorded ECG.

## Integrity expectations

The validation script checks that every expected file exists, contains only
finite numeric values, and has the documented number of columns. It does not
establish signal quality, provenance, clinical validity, or permission to use
the recordings.

See [`RIGHTS.md`](RIGHTS.md) before copying or redistributing any recording.
