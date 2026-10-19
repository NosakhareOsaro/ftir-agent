"""
train_model.py

Refit the dissertation's final elastic net on all 108 DGRP line-mean spectra
and save it as a joblib bundle for the agent's predict tool.

Same recipe as run_regularised_regression.py in the dissertation repo:
female flies only → mean spectrum per DGRP line → StandardScaler →
ElasticNetCV(cv=3, l1_ratio=[0.5, 0.9, 1.0], 30 alphas, tol=0.01).

Also writes a few example spectra to model/examples/ for the demo.

Usage:
  .venv/bin/python scripts/train_model.py --data-dir /path/to/FTIRproject
  .venv/bin/python scripts/train_model.py --data-dir ... --loo   # re-run LOO-CV (slow)

The FTIR data belongs to the Dobson lab and is not redistributed in this repo.
"""

import argparse
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import ElasticNetCV
from sklearn.metrics import r2_score
from sklearn.model_selection import LeaveOneOut
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
from model.ftir import DEFAULT_MODEL_PATH, EXPECTED_WNS, load_dat  # noqa: E402

L1_RATIOS = [0.5, 0.9, 1.0]
N_ALPHAS = 30


def make_model():
    return ElasticNetCV(cv=3, l1_ratio=L1_RATIOS, max_iter=5000, tol=0.01, alphas=N_ALPHAS)


def line_means(data_dir):
    meta, spectra = load_dat(data_dir / "FTIR-data" / "DGRPFTIR.dat")
    female = (meta["Sex"] == "F").values
    spectra = spectra[female].copy()
    spectra["Genot."] = meta.loc[female, "Genot."].values
    X_df = spectra.groupby("Genot.").mean()

    emmeans = pd.read_csv(data_dir / "Emmeans.csv")
    data = (X_df.reset_index()
            .merge(emmeans[["DGRP", "emmean"]], left_on="Genot.", right_on="DGRP")
            .sort_values("Genot.").reset_index(drop=True))
    return data, meta[female], spectra


def loo_r2(X, y):
    pred = np.zeros(len(y))
    for i, (tr, te) in enumerate(LeaveOneOut().split(X)):
        sc = StandardScaler().fit(X[tr])
        pred[te] = make_model().fit(sc.transform(X[tr]), y[tr]).predict(sc.transform(X[te]))
        print(f"\r  LOO fold {i + 1}/{len(y)}", end="", flush=True)
    print()
    return r2_score(y, pred)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=Path, required=True,
                    help="dissertation FTIRproject folder (has FTIR-data/ and Emmeans.csv)")
    ap.add_argument("--loo", action="store_true", help="re-run leave-one-line-out CV")
    args = ap.parse_args()

    data, fly_meta, fly_spectra = line_means(args.data_dir)
    wns = list(EXPECTED_WNS)
    X, y = data[wns].to_numpy(), data["emmean"].to_numpy()
    print(f"Training lines: {len(y)}  wavenumbers: {X.shape[1]}")

    cv_r2 = 0.673  # dissertation, leave-one-line-out
    if args.loo:
        cv_r2 = round(loo_r2(X, y), 3)
        print(f"LOO-CV R² = {cv_r2}")

    scaler = StandardScaler().fit(X)
    model = make_model().fit(scaler.transform(X), y)
    n_nonzero = int(np.sum(model.coef_ != 0))
    print(f"alpha={model.alpha_:.4g}  l1_ratio={model.l1_ratio_}  nonzero={n_nonzero}")

    bundle = {
        "scaler": scaler,
        "model": model,
        "target": "starvation resistance: line EMMean from a parametric survival "
                  "model of time to death under starvation (log scale; higher = "
                  "more resistant)",
        "training_data": "ATR-FTIR spectra of female D. melanogaster, averaged "
                         "per line, 108 DGRP lines, one lab (Dobson lab, Glasgow)",
        "n_training_lines": len(y),
        "target_range": (float(y.min()), float(y.max())),
        "alpha": float(model.alpha_),
        "l1_ratio": float(model.l1_ratio_),
        "n_nonzero_coefficients": n_nonzero,
        "cv_r2_reported": cv_r2,
        "known_limitations": [
            "Trained on line means; single-fly spectra are noisier than its training data.",
            "Did not transfer to the same trait measured in another lab "
            "(Morgante et al. 2015: r = 0.428 between labs' measurements).",
            "Showed no predictive signal for ~30 other DGRP phenotypes "
            "(lifespan, fecundity, chill coma, metabolic indices).",
            "Predictions for other species, sexes, diets or instruments are unvalidated.",
        ],
    }
    DEFAULT_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(bundle, DEFAULT_MODEL_PATH)
    print(f"Saved {DEFAULT_MODEL_PATH.relative_to(ROOT)}")

    # Examples for the demo: the most and least resistant lines (line means)
    # plus three single-fly spectra from a mid-ranked line.
    ex_dir = ROOT / "model" / "examples"
    ex_dir.mkdir(exist_ok=True)
    order = data.sort_values("emmean")
    for name, row in [("least_resistant", order.iloc[0]), ("most_resistant", order.iloc[-1])]:
        out = pd.DataFrame([row[wns].to_numpy()], columns=wns)
        out.insert(0, "line", row["Genot."])
        out.to_csv(ex_dir / f"{name}_line_mean.csv", index=False)
    mid = order.iloc[len(order) // 2]["Genot."]
    flies = fly_spectra[fly_spectra["Genot."] == mid].head(3)
    flies.insert(0, "line", flies.pop("Genot."))
    flies.to_csv(ex_dir / "single_flies_mid_line.csv", index=False)
    print(f"Examples written to {ex_dir.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
