from __future__ import annotations

from typing import Any

import pandas as pd
from sklearn.model_selection import train_test_split


def split_features_target(
    df: pd.DataFrame,
    target_col: str,
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Split a DataFrame into features (X) and target (y).

    Parameters
    ----------
    df : pd.DataFrame
        Input dataset containing both features and target.
    target_col : str
        Name of the target column.

    Returns
    -------
    tuple[pd.DataFrame, pd.Series]
        X (features) and y (target).

    Raises
    ------
    ValueError
        If the target column is not present in the DataFrame.
    """
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in DataFrame.")

    X = df.drop(columns=[target_col])
    y = df[target_col]

    return X, y


def _get_stratify_target(y: pd.Series, stratify: bool) -> pd.Series | None:
    """
    Return the target vector for stratification if requested.
    """
    return y if stratify else None


def _make_train_test_split(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float,
    random_state: int,
    stratify: bool,
) -> dict[str, dict[str, pd.DataFrame | pd.Series]]:
    """
    Create a train/test split and return it in structured form.
    """
    stratify_target = _get_stratify_target(y, stratify)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify_target,
    )

    return {
        "train": {"X": X_train, "y": y_train},
        "test": {"X": X_test, "y": y_test},
    }


def _make_train_valid_test_split(
    X: pd.DataFrame,
    y: pd.Series,
    train_size: float,
    valid_size: float,
    test_size: float,
    random_state: int,
    stratify: bool,
) -> dict[str, dict[str, pd.DataFrame | pd.Series]]:
    """
    Create a train/valid/test split in two steps:
    1. hold out the test split
    2. split the remaining data into train and valid
    """
    stratify_target = _get_stratify_target(y, stratify)

    X_remaining, X_test, y_remaining, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify_target,
    )

    remaining_total = train_size + valid_size
    valid_relative_size = valid_size / remaining_total

    stratify_remaining = _get_stratify_target(y_remaining, stratify)

    X_train, X_valid, y_train, y_valid = train_test_split(
        X_remaining,
        y_remaining,
        test_size=valid_relative_size,
        random_state=random_state,
        stratify=stratify_remaining,
    )

    return {
        "train": {"X": X_train, "y": y_train},
        "valid": {"X": X_valid, "y": y_valid},
        "test": {"X": X_test, "y": y_test},
    }


def _build_requested_proportions(split_config: dict[str, Any]) -> dict[str, float]:
    """
    Build the requested split proportions from the config.
    """
    strategy = split_config["strategy"]

    if strategy == "train_test":
        test_size = float(split_config["test_size"])
        return {
            "train": 1.0 - test_size,
            "test": test_size,
        }

    if strategy == "train_valid_test":
        return {
            "train": float(split_config["train_size"]),
            "valid": float(split_config["valid_size"]),
            "test": float(split_config["test_size"]),
        }

    raise ValueError(f"Unsupported split strategy: {strategy}")


def _build_actual_sizes(
    splits: dict[str, dict[str, pd.DataFrame | pd.Series]],
) -> dict[str, int]:
    """
    Build actual row counts for each split.
    """
    actual_sizes: dict[str, int] = {}

    for split_name, split_data in splits.items():
        X_split = split_data["X"]
        actual_sizes[split_name] = len(X_split)

    return actual_sizes


def _build_split_metadata(
    split_config: dict[str, Any],
    splits: dict[str, dict[str, pd.DataFrame | pd.Series]],
    target_col: str | None = None,
) -> dict[str, Any]:
    """
    Build basic metadata describing the split strategy and outputs.
    """
    metadata = {
        "strategy": split_config["strategy"],
        "target_column": target_col,
        "stratify": split_config.get("stratify", False),
        "random_state": split_config.get("random_state", 42),
        "requested_proportions": _build_requested_proportions(split_config),
        "actual_sizes": _build_actual_sizes(splits),
    }

    return metadata


def make_dataset_splits(
    X: pd.DataFrame,
    y: pd.Series,
    split_config: dict[str, Any],
    target_col: str | None = None,
) -> dict[str, Any]:
    """
    Create dataset splits according to a declarative split config.

    Supported strategies
    --------------------
    - train_test
    - train_valid_test

    Parameters
    ----------
    X : pd.DataFrame
        Feature matrix.
    y : pd.Series
        Target vector.
    split_config : dict[str, Any]
        Split configuration dictionary.
    target_col : str | None, default=None
        Optional target column name to include in metadata.

    Returns
    -------
    dict[str, Any]
        Dictionary with:
        - 'splits': structured split outputs
        - 'metadata': split metadata

    Raises
    ------
    ValueError
        If the strategy is missing or unsupported.
    """
    strategy = split_config.get("strategy")
    random_state = split_config.get("random_state", 42)
    stratify = split_config.get("stratify", False)

    if strategy is None:
        raise ValueError("Split config must include a 'strategy' key.")

    if strategy == "train_test":
        splits = _make_train_test_split(
            X=X,
            y=y,
            test_size=float(split_config["test_size"]),
            random_state=random_state,
            stratify=stratify,
        )

    elif strategy == "train_valid_test":
        splits = _make_train_valid_test_split(
            X=X,
            y=y,
            train_size=float(split_config["train_size"]),
            valid_size=float(split_config["valid_size"]),
            test_size=float(split_config["test_size"]),
            random_state=random_state,
            stratify=stratify,
        )

    else:
        raise ValueError(
            f"Unsupported split strategy: {strategy}. "
            "Supported strategies are: 'train_test', 'train_valid_test'."
        )

    metadata = _build_split_metadata(
        split_config=split_config,
        splits=splits,
        target_col=target_col,
    )

    return {
        "splits": splits,
        "metadata": metadata,
    }
