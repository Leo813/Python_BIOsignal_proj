"""Characterize current SCG preprocessing; these are not clinical validity tests.

The row-scaling assertions document the existing limitation. Revisit them if
a separately reviewed methodology change replaces that behavior.
"""

import json
from pathlib import Path
import unittest

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy.testing import assert_allclose
from sklearn import preprocessing as prep
from sklearn.decomposition import PCA


ROOT = Path(__file__).resolve().parents[1]


def notebook_scale(features):
    notebook = json.loads(
        (ROOT / "DTEK0042_Exercise_4_FINAL.ipynb").read_text(encoding="utf-8")
    )
    cells = [
        "".join(cell["source"])
        for cell in notebook["cells"]
        if cell["cell_type"] == "code"
        and "standardised_features =" in "".join(cell["source"])
    ]
    if len(cells) != 1:
        raise ValueError("Expected exactly one SCG standardization cell")
    namespace = {"features": features.copy(), "prep": prep}
    exec(compile(cells[0], "SCG standardization cell", "exec"), namespace)
    return np.asarray(namespace["standardised_features"])


class SCGPreprocessingReview(unittest.TestCase):
    def setUp(self):
        # Deliberately different feature scales, with no constant columns.
        self.features = np.array([
            [1., 10., 100.], [2., 30., 400.],
            [4., 20., 200.], [8., 60., 300.],
        ])

    def test_notebook_scales_rows_not_feature_columns(self):
        actual = notebook_scale(self.features)
        expected = (
            self.features - self.features.mean(axis=1, keepdims=True)
        ) / self.features.std(axis=1, keepdims=True)
        assert_allclose(actual, expected, atol=1e-12)
        assert_allclose(actual.mean(axis=1), 0, atol=1e-12)
        assert_allclose(actual.std(axis=1), 1, atol=1e-12)
        self.assertFalse(np.allclose(actual.mean(axis=0), 0))

    def test_row_scaling_discards_per_row_offset_and_positive_scale(self):
        transformed = self.features * np.array([[2.], [3.], [4.], [5.]]) + 17
        assert_allclose(notebook_scale(transformed), notebook_scale(self.features))

    def test_feature_unit_change_affects_row_scaling(self):
        changed_units = self.features * np.array([1000., 1., 1.])
        self.assertFalse(np.allclose(
            notebook_scale(changed_units), notebook_scale(self.features)
        ))
        # A column-scaled comparison is unit-invariant for positive rescaling.
        assert_allclose(prep.scale(changed_units), prep.scale(self.features))

    def test_pca_variance_matches_centered_svd(self):
        scaled = notebook_scale(self.features)
        model = PCA(n_components=2)
        scores = model.fit_transform(scaled)
        centered = scaled - scaled.mean(axis=0)
        singular_values = np.linalg.svd(centered, compute_uv=False)
        assert_allclose(model.mean_, scaled.mean(axis=0))
        assert_allclose(
            model.explained_variance_, singular_values[:2] ** 2 / (len(scaled) - 1)
        )
        assert_allclose(scores.mean(axis=0), 0, atol=1e-12)

    def test_pca_plot_labels_match_point_groups(self):
        notebook = json.loads(
            (ROOT / "DTEK0042_Exercise_4_FINAL.ipynb").read_text(encoding="utf-8")
        )
        source = next(
            "".join(cell["source"]) for cell in notebook["cells"]
            if cell["cell_type"] == "code"
            and "pca_out = my_pca.fit_transform" in "".join(cell["source"])
        )
        labels = np.array(["Noisy", "Normal", "Noisy", "Normal"])
        namespace = {
            "standardised_features": notebook_scale(self.features),
            "labels": labels, "PCA": PCA, "pd": pd, "plt": plt,
        }
        from unittest.mock import patch
        try:
            # Only avoid opening a display; execute the actual plotting cell.
            with patch.object(plt, "show"):
                exec(compile(source, "SCG PCA cell", "exec"), namespace)
            axes = plt.gca()
            self.assertEqual(
                [text.get_text() for text in axes.get_legend().get_texts()],
                ["Noisy", "Normal"],
            )
            self.assertEqual(len(axes.collections), 2)
            for collection, label in zip(axes.collections, ("Noisy", "Normal")):
                assert_allclose(
                    collection.get_offsets(), namespace["pca_out"][labels == label]
                )
        finally:
            plt.close("all")


if __name__ == "__main__":
    unittest.main()
