import pandas as pd


def validate_columns_exist(df: pd.DataFrame, columns: list[str]) -> None:
    """
    Validate that all specified columns exist in the DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    columns : list[str]
        Columns that must exist in the DataFrame.

    Raises
    ------
    ValueError
        If one or more columns are missing.
    """
    missing_columns = [col for col in columns if col not in df.columns]

    if missing_columns:
        raise ValueError(
            f"The following columns are missing from the DataFrame: {missing_columns}"
        )


def _validate_feature_list(name: str, value: object) -> list[str]:
    """
    Validate that a feature group is a list of non-empty strings.

    Parameters
    ----------
    name : str
        Name of the feature group for error messages.
    value : object
        Value to validate.

    Returns
    -------
    list[str]
        Validated feature list.

    Raises
    ------
    ValueError
        If the feature group is not a list of non-empty strings.
    """
    if not isinstance(value, list):
        raise ValueError(f"'{name}' must be a list.")

    if not all(isinstance(col, str) and col.strip() for col in value):
        raise ValueError(f"'{name}' must contain only non-empty strings.")

    return value


def get_target_column(config: dict) -> str:
    """
    Get the target column name from config.

    Expected structure:
    {
        "target": {
            "column": "target_column_name"
        }
    }

    Parameters
    ----------
    config : dict
        Project configuration dictionary.

    Returns
    -------
    str
        Target column name.

    Raises
    ------
    ValueError
        If target.column is not properly defined in config.
    """
    target_cfg = config.get("target")

    if not isinstance(target_cfg, dict):
        raise ValueError("'target' section must be a dictionary.")

    target_col = target_cfg.get("column")

    if not isinstance(target_col, str) or not target_col.strip():
        raise ValueError("Target column must be defined in config under 'target.column'.")

    return target_col


def get_feature_groups(df: pd.DataFrame, config: dict) -> dict:
    """
    Get target, numeric features, and categorical features from config.

    Feature roles are treated as explicit semantic declarations.
    They are not inferred automatically from dtypes, encodings, or
    superficial numeric appearance.

    Expected config structure:
    {
        "target": {
            "column": "target_column_name"
        },
        "cleaning": {
            "drop_columns": [...]
        },
        "features": {
            "numeric": [...],
            "categorical": [...]
        }
    }

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    config : dict
        Project configuration dictionary.

    Returns
    -------
    dict
        Dictionary with:
        - target: str
        - numeric_features: list[str]
        - categorical_features: list[str]

    Raises
    ------
    ValueError
        If the config structure is invalid, if target is included in
        feature lists, if duplicated features exist across groups, or if
        dropped columns are also declared as features.
    """
    target_col = get_target_column(config)

    features_cfg = config.get("features")
    if not isinstance(features_cfg, dict):
        raise ValueError("'features' section must be a dictionary.")

    numeric_features = _validate_feature_list(
        "features.numeric",
        features_cfg.get("numeric", []),
    )
    categorical_features = _validate_feature_list(
        "features.categorical",
        features_cfg.get("categorical", []),
    )

    cleaning_cfg = config.get("cleaning", {})
    if not isinstance(cleaning_cfg, dict):
        raise ValueError("'cleaning' section must be a dictionary.")

    drop_cols = _validate_feature_list(
        "cleaning.drop_columns",
        cleaning_cfg.get("drop_columns", []),
    )

    validate_columns_exist(df, [target_col])
    validate_columns_exist(df, numeric_features)
    validate_columns_exist(df, categorical_features)

    all_features = numeric_features + categorical_features

    if target_col in all_features:
        raise ValueError(
            f"Target column '{target_col}' must not be included in feature lists."
        )

    duplicated_features = sorted(set(numeric_features) & set(categorical_features))
    if duplicated_features:
        raise ValueError(
            "The following columns are declared as both numeric and categorical: "
            f"{duplicated_features}"
        )

    dropped_feature_overlap = sorted(set(drop_cols) & set(all_features))
    if dropped_feature_overlap:
        raise ValueError(
            "The following columns appear in both 'cleaning.drop_columns' and "
            f"'features': {dropped_feature_overlap}"
        )

    return {
        "target": target_col,
        "numeric_features": numeric_features,
        "categorical_features": categorical_features,
    }
