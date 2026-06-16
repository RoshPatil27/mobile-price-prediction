"""
Generates a synthetic dataset that mirrors the structure, value ranges, and
feature-target relationships of the well-known Kaggle "Mobile Price
Classification" dataset (20 hardware specs -> price_range 0-3).

We can't download the original file from inside this environment (no
internet access), so this script builds a statistically faithful
replacement: same columns, same value ranges, same approximate
distributions, and the same dominant signal (RAM is by far the strongest
predictor of price_range, followed by battery_power and pixel resolution).

Run:
    python generate_dataset.py
Produces:
    train.csv  (2000 rows, 21 columns)
"""

import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)
N = 2000


def make_dataset(n=N):
    data = {
        "battery_power": RNG.integers(501, 1999, n),
        "blue": RNG.integers(0, 2, n),
        "clock_speed": np.round(RNG.uniform(0.5, 3.0, n), 1),
        "dual_sim": RNG.integers(0, 2, n),
        "fc": RNG.integers(0, 20, n),
        "four_g": RNG.integers(0, 2, n),
        "int_memory": RNG.integers(2, 65, n),
        "m_dep": np.round(RNG.uniform(0.1, 1.0, n), 1),
        "mobile_wt": RNG.integers(80, 201, n),
        "n_cores": RNG.integers(1, 9, n),
        "pc": RNG.integers(0, 21, n),
        "px_height": RNG.integers(0, 1961, n),
        "px_width": RNG.integers(500, 1999, n),
        "ram": RNG.integers(256, 3999, n),
        "sc_h": RNG.integers(5, 20, n),
        "sc_w": RNG.integers(0, 19, n),
        "talk_time": RNG.integers(2, 21, n),
        "three_g": RNG.integers(0, 2, n),
        "touch_screen": RNG.integers(0, 2, n),
        "wifi": RNG.integers(0, 2, n),
    }

    df = pd.DataFrame(data)

    # fc (front camera) should not exceed pc (primary camera) - matches the
    # logical constraint seen in the real dataset
    df["fc"] = np.minimum(df["fc"], df["pc"])

    # ---- Build price_range as a function of the most influential specs ----
    # RAM dominates (correlation ~0.92 in the real dataset), with smaller
    # contributions from battery power and screen resolution, plus noise.
    score = (
        0.72 * _norm(df["ram"])
        + 0.10 * _norm(df["battery_power"])
        + 0.07 * _norm(df["px_width"])
        + 0.07 * _norm(df["px_height"])
        + 0.04 * _norm(df["int_memory"])
        + RNG.normal(0, 0.06, n)  # irreducible noise
    )

    # Convert continuous score into 4 balanced classes (0-3) via quartiles
    quartiles = np.quantile(score, [0.25, 0.5, 0.75])
    price_range = np.digitize(score, quartiles)
    df["price_range"] = price_range

    return df


def _norm(series):
    s = series.astype(float)
    return (s - s.min()) / (s.max() - s.min())


if __name__ == "__main__":
    df = make_dataset()
    df.to_csv("train.csv", index=False)
    print(f"Saved train.csv with shape {df.shape}")
    print(df["price_range"].value_counts().sort_index())
    print(df.describe().T[["min", "max", "mean"]])
