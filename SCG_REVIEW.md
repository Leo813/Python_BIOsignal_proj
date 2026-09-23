# SCG normalization and PCA review

This is a numerical review of `DTEK0042_Exercise_4_FINAL.ipynb`, not a domain
validation or a replacement analysis. No external project records or domain
review were available. The feature extraction and PCA inputs remain unchanged.

## What the notebook does

- `_slicing` keeps complete 1,000-sample segments and discards the remainder.
  At the notebook's 200 Hz sampling rate, each segment represents five seconds.
- `feature_extraction` returns eight time-domain statistics followed by ten
  sums of Welch PSD values in 4 Hz bins from 0 up to, but excluding, 40 Hz.
  It scales the signal samples before calculating the PSD; the eight
  time-domain statistics use the unscaled segment.
- The `Standardize Features` cell loops over those 18-value vectors and calls
  `prep.scale(elm)` on each vector separately. Each segment is therefore
  centered and scaled across its different feature values.
- `PCA(n_components=2)` receives those row-scaled vectors. The plot colors
  points using the `Noisy` and `Normal` filename prefixes.

## Numerical findings

`tests/test_scg_preprocessing.py` executes the notebook's actual scaling cell
on a small synthetic matrix. Four checks establish that:

1. Each resulting row has mean zero and standard deviation one; feature
   columns are not generally centered or standardized.
2. Adding a common offset to a row or multiplying it by a positive factor
   leaves that row's standardized representation unchanged.
3. Rescaling a single feature column changes the row-scaled representation.
   A feature-wise scaling comparison is invariant to that positive unit change.
4. PCA's variances agree with an independent SVD of the centered input matrix.

A fifth check executes the notebook's plotting cell and verifies that the two
legend entries and plotted point groups match their filename labels.

The distinction between row and column scaling follows the
[scikit-learn scaling API](https://scikit-learn.org/1.4/modules/generated/sklearn.preprocessing.scale.html).
[PCA centers its inputs but does not standardize feature scales](https://scikit-learn.org/1.4/modules/generated/sklearn.decomposition.PCA.html).
It therefore does not undo the preceding choice of scaling axis.

Run the checks from the repository root in the pinned environment:

```sh
python -m unittest discover -s tests -v
```

These are characterization tests, not an assertion that row scaling is the
appropriate scientific method. If a later reviewed change replaces it, update
the tests and saved outputs together.

## Questions deliberately left open

The repository does not establish whether absolute feature magnitudes should
be retained, how the mixed feature scales should be weighted, or whether the
filename labels support a predictive task. Domain review is still needed to
choose preprocessing and interpret any separation in the plot. A change to
feature-wise scaling would change the analysis and needs a separate review.

The scatter plot alone does not demonstrate noise removal, clinical meaning,
or predictive performance. The existing course observation is retained with
an adjacent interpretation note. The plot's legend now correctly identifies
both filename-label groups; this presentation fix does not change PCA scores.
