import numpy as np
import pandas as pd
import pytest

from model.ftir import EXPECTED_WNS, SpectrumError, model_card, parse_spectra, predict


def test_contributions_sum_to_prediction(bundle, spectra):
    res = predict(bundle, spectra.iloc[:3])
    expected = bundle["model"].predict(bundle["scaler"].transform(spectra.iloc[:3].to_numpy()))
    for r, e in zip(res, expected):
        assert r["predicted_emmean"] == pytest.approx(e, abs=1e-3)
        total = r["intercept"] + sum(r["band_contributions"].values())
        assert total == pytest.approx(e, abs=1e-3)


def test_signal_lands_in_ester_band(bundle, spectra):
    res = predict(bundle, spectra.iloc[:5])
    top_bands = [next(iter(r["band_contributions"])) for r in res]
    assert top_bands.count("Ester C=O stretch (triglycerides)") >= 4


def test_out_of_domain_spectrum_is_flagged(bundle, spectra):
    weird = spectra.iloc[[0]] * 50
    warnings = predict(bundle, weird)[0]["warnings"]
    assert any("SD from the training" in w for w in warnings)


def test_parse_wide_with_labels(spectra):
    df = spectra.iloc[:2].copy()
    df.columns = [str(c) for c in df.columns]
    df.insert(0, "line", ["DGRP1", "DGRP2"])
    labels, out = parse_spectra(df)
    assert labels == ["DGRP1", "DGRP2"]
    assert list(out.columns) == list(EXPECTED_WNS)


def test_parse_long_two_column(spectra):
    long = pd.DataFrame({"wavenumber": EXPECTED_WNS[::-1], "absorbance": spectra.iloc[0, ::-1].values})
    labels, out = parse_spectra(long)
    assert out.shape == (1, len(EXPECTED_WNS))
    assert np.allclose(out.iloc[0].values, spectra.iloc[0].values)


def test_parse_rejects_wrong_axis():
    df = pd.DataFrame(np.ones((1, 100)), columns=range(4000, 3800, -2))
    with pytest.raises(SpectrumError, match="missing"):
        parse_spectra(df)


def test_model_card_has_limitations(bundle):
    assert model_card(bundle)["known_limitations"]
