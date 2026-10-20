import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, str(Path(__file__).parent.parent))
from model.ftir import EXPECTED_WNS  # noqa: E402


@pytest.fixture
def spectra():
    rng = np.random.default_rng(0)
    return pd.DataFrame(rng.normal(1.0, 0.1, (20, len(EXPECTED_WNS))), columns=list(EXPECTED_WNS))


@pytest.fixture
def bundle(spectra):
    """A small model with the same structure as the real one, on synthetic data."""
    X = spectra.to_numpy()
    y = 2 + 5 * (X[:, EXPECTED_WNS.index(1760)] - 1)  # signal in the ester C=O band
    scaler = StandardScaler().fit(X)
    model = ElasticNet(alpha=0.01, l1_ratio=0.9, max_iter=5000).fit(scaler.transform(X), y)
    return {
        "scaler": scaler, "model": model, "target": "test target",
        "training_data": "synthetic", "n_training_lines": len(y),
        "target_range": (float(y.min()), float(y.max())), "alpha": 0.01,
        "l1_ratio": 0.9, "n_nonzero_coefficients": int((model.coef_ != 0).sum()),
        "cv_r2_reported": None, "known_limitations": ["synthetic"],
    }


class FakeLLM:
    """Replays a scripted list of assistant messages; records what it was sent."""

    def __init__(self, replies):
        self.replies = list(replies)
        self.sent = []
        self.n_requests = 0
        self.model = "fake"

    def chat(self, messages, tools=None):
        self.sent.append({"messages": [dict(m) for m in messages], "tools": tools})
        self.n_requests += 1
        return self.replies.pop(0)


def tool_call(name, arguments, id_="call_1"):
    return {"role": "assistant", "content": None, "tool_calls": [
        {"id": id_, "type": "function", "function": {"name": name, "arguments": arguments}}]}


def network_enabled():
    import os
    return os.getenv("RUN_NETWORK_TESTS") == "1"
