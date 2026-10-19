"""
ftir.py

Load FTIR spectra and run the dissertation's elastic net on them.

The model predicts starvation resistance (the line EMMean from a parametric
survival fit, log scale) from an ATR-FTIR spectrum of a female Drosophila
melanogaster. It was trained on 108 DGRP line-mean spectra; leave-one-line-out
CV R² = 0.673 (MSc dissertation, Edinburgh Napier University, 2026).

Because the model is linear on standardised inputs, each prediction splits
exactly into intercept + one contribution per wavenumber:

    pred = intercept + Σ_j coef_j · (x_j − mean_j) / scale_j

Those contributions are summed into named spectral bands, which is what the
agent reports as the explanation. No SHAP or approximation needed.
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd

# Verified from all six dissertation .dat files: 3900, 3898, …, 456 step -2
EXPECTED_WNS = tuple(range(3900, 454, -2))  # 1723 wavenumbers
META_COLS = {"Genot.", "Sex", "Age", "Diet", "StoTime"}

# Approximate assignments for biological mid-IR spectra (Baker et al. 2014,
# Nature Protocols, PMID 24992094). Bands are half-open [low, high).
BANDS = [
    ("O-H / N-H stretch (water, protein)",       3050, 3901),
    ("C-H stretch (lipid acyl chains)",          2800, 3050),
    ("Ester C=O stretch (triglycerides)",        1700, 1800),
    ("Amide I (protein C=O)",                    1600, 1700),
    ("Amide II (protein N-H bend)",              1500, 1600),
    ("CH2/CH3 bending (lipid, protein)",         1350, 1500),
    ("C-O / P=O (carbohydrate, phosphate)",       900, 1350),
    ("Low fingerprint <900 (unassigned)",         450,  900),
]
OTHER_BAND = "1800-2800 (few biological absorbances)"

DEFAULT_MODEL_PATH = Path(__file__).parent / "artifacts" / "enet_starvation.joblib"


class SpectrumError(ValueError):
    """The input does not look like a spectrum this model can score."""


# ── Loading ───────────────────────────────────────────────────────────────────

def load_dat(path):
    """Load a dissertation .dat file → (meta, spectra). Simplified ftir_loader."""
    df = pd.read_csv(path, sep="\t")
    meta = df[[c for c in df.columns if c in META_COLS]].copy()
    spectra = df[[c for c in df.columns if c not in META_COLS]].astype(float)
    spectra.columns = [int(c) for c in spectra.columns]
    if tuple(spectra.columns) != EXPECTED_WNS:
        raise SpectrumError(f"{Path(path).name}: unexpected wavenumber axis")
    if "Sex" in meta:
        meta["Sex"] = meta["Sex"].replace({"S": "F"})  # 'S' = female (data owner)
    return meta.reset_index(drop=True), spectra.reset_index(drop=True)


def parse_spectra(df):
    """
    Normalise a user table into (labels, spectra) with columns = EXPECTED_WNS.

    Accepts either layout:
      wide : one row per spectrum, one column per wavenumber
             (any non-numeric columns are treated as labels)
      long : two numeric columns, wavenumber and absorbance (one spectrum)
    """
    if df.shape[1] == 2 and df.shape[0] > 100:
        wn = pd.to_numeric(df.iloc[:, 0], errors="coerce")
        ab = pd.to_numeric(df.iloc[:, 1], errors="coerce")
        if wn.notna().all() and ab.notna().all():
            df = pd.DataFrame([ab.values], columns=wn.round().astype(int).values)

    wn_cols, label_cols = {}, []
    for c in df.columns:
        try:
            wn_cols[c] = int(round(float(c)))
        except (TypeError, ValueError):
            label_cols.append(c)

    spectra = df[list(wn_cols)].rename(columns=wn_cols)
    missing = sorted(set(EXPECTED_WNS) - set(spectra.columns), reverse=True)
    if missing:
        raise SpectrumError(
            f"{len(missing)} of {len(EXPECTED_WNS)} expected wavenumbers missing "
            f"(model needs 3900→456 cm⁻¹ at 2 cm⁻¹ steps; first missing: {missing[:3]})"
        )
    spectra = spectra[list(EXPECTED_WNS)].apply(pd.to_numeric, errors="coerce")
    if spectra.isna().any().any():
        raise SpectrumError("spectrum contains non-numeric or empty absorbance values")

    if label_cols:
        labels = df[label_cols].astype(str).agg(" ".join, axis=1).tolist()
    else:
        labels = [f"spectrum_{i + 1}" for i in range(len(spectra))]
    return labels, spectra.reset_index(drop=True)


# ── Prediction ────────────────────────────────────────────────────────────────

def load_model(path=DEFAULT_MODEL_PATH):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"No trained model at {path}. Run scripts/train_model.py first "
            "(needs the dissertation FTIR data, see README)."
        )
    return joblib.load(path)


def _band_of(wn):
    for name, lo, hi in BANDS:
        if lo <= wn < hi:
            return name
    return OTHER_BAND


def predict(bundle, spectra, labels=None, top_k=5):
    """
    Score each spectrum and explain it.

    Returns one dict per spectrum: prediction, band contributions (sorted by
    absolute size), top individual wavenumbers, and applicability warnings.
    """
    scaler, model = bundle["scaler"], bundle["model"]
    X = spectra[list(EXPECTED_WNS)].to_numpy(dtype=float)
    Z = scaler.transform(X)
    contrib = Z * model.coef_                     # (n, 1723)
    preds = model.intercept_ + contrib.sum(axis=1)

    wns = np.array(EXPECTED_WNS)
    band_names = np.array([_band_of(w) for w in wns], dtype=object)
    lo, hi = bundle["target_range"]
    labels = labels or [f"spectrum_{i + 1}" for i in range(len(X))]

    results = []
    for i in range(len(X)):
        bands = {}
        for name in dict.fromkeys(band_names):
            total = float(contrib[i, band_names == name].sum())
            if total != 0.0:
                bands[name] = round(total, 4)
        bands = dict(sorted(bands.items(), key=lambda kv: -abs(kv[1])))

        order = np.argsort(-np.abs(contrib[i]))[:top_k]
        top_wns = [
            {"wavenumber": int(wns[j]), "band": str(band_names[j]),
             "contribution": round(float(contrib[i, j]), 4)}
            for j in order if contrib[i, j] != 0
        ]

        warnings = []
        if not lo <= preds[i] <= hi:
            warnings.append(
                f"prediction {preds[i]:.3f} is outside the training range "
                f"[{lo:.3f}, {hi:.3f}]: extrapolating"
            )
        extreme = float(np.mean(np.abs(Z[i]) > 5))
        if extreme > 0.05:
            warnings.append(
                f"{extreme:.0%} of wavenumbers are >5 SD from the training "
                "spectra: input may be from a different instrument, preprocessing "
                "or population"
            )

        results.append({
            "label": labels[i],
            "predicted_emmean": round(float(preds[i]), 4),
            "intercept": round(float(model.intercept_), 4),
            "band_contributions": bands,
            "top_wavenumbers": top_wns,
            "warnings": warnings,
        })
    return results


def model_card(bundle):
    """Facts about the model the agent must state alongside any prediction."""
    return {k: bundle[k] for k in (
        "target", "training_data", "n_training_lines", "alpha", "l1_ratio",
        "n_nonzero_coefficients", "cv_r2_reported", "known_limitations",
    )}
