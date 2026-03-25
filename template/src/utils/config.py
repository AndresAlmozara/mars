from pathlib import Path

import yaml


def load_config(path: str | Path) -> dict:
    """
    Load a YAML configuration file and return it as a dictionary.

    Parameters
    ----------
    path : str | Path
        Path to the YAML config file.

    Returns
    -------
    dict
        Configuration dictionary.

    Raises
    ------
    FileNotFoundError
        If the config file does not exist.
    ValueError
        If the YAML content is empty or invalid.
    """
    config_path = Path(path)

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if config is None:
        raise ValueError(f"Config file is empty: {config_path}")

    if not isinstance(config, dict):
        raise ValueError("Config file must define a YAML dictionary/object at top level.")

    return config


def _validate_dataset_section(config: dict) -> None:
    dataset_cfg = config["dataset"]

    if not isinstance(dataset_cfg, dict):
        raise ValueError("'dataset' section must be a dictionary.")

    required_dataset_keys = ["path", "file_type"]
    missing_dataset_keys = [key for key in required_dataset_keys if key not in dataset_cfg]

    if missing_dataset_keys:
        raise ValueError(
            f"Missing required keys in 'dataset' section: {missing_dataset_keys}"
        )

    if not isinstance(dataset_cfg["path"], str) or not dataset_cfg["path"].strip():
        raise ValueError("'dataset.path' must be a non-empty string.")

    if not isinstance(dataset_cfg["file_type"], str) or not dataset_cfg["file_type"].strip():
        raise ValueError("'dataset.file_type' must be a non-empty string.")

    optional_string_keys = ["sep", "encoding"]
    for key in optional_string_keys:
        if key in dataset_cfg and not isinstance(dataset_cfg[key], str):
            raise ValueError(f"'dataset.{key}' must be a string if provided.")


def _validate_target_section(config: dict) -> None:
    target_cfg = config["target"]

    if not isinstance(target_cfg, dict):
        raise ValueError("'target' section must be a dictionary.")

    if "column" not in target_cfg:
        raise ValueError("Missing required key in 'target' section: ['column']")

    if not isinstance(target_cfg["column"], str) or not target_cfg["column"].strip():
        raise ValueError("'target.column' must be a non-empty string.")


def _validate_features_section(config: dict) -> None:
    features_cfg = config["features"]

    if not isinstance(features_cfg, dict):
        raise ValueError("'features' section must be a dictionary.")

    required_feature_keys = ["numeric", "categorical"]
    missing_feature_keys = [
        key for key in required_feature_keys if key not in features_cfg
    ]

    if missing_feature_keys:
        raise ValueError(
            f"Missing required keys in 'features' section: {missing_feature_keys}"
        )

    if not isinstance(features_cfg["numeric"], list):
        raise ValueError("'features.numeric' must be a list.")

    if not isinstance(features_cfg["categorical"], list):
        raise ValueError("'features.categorical' must be a list.")


def _validate_cleaning_section(config: dict) -> None:
    cleaning_cfg = config["cleaning"]

    if not isinstance(cleaning_cfg, dict):
        raise ValueError("'cleaning' section must be a dictionary.")

    expected_bool_keys = [
        "normalize_column_names",
        "strip_string_columns",
        "replace_empty_strings_with_nan",
        "drop_duplicate_rows",
    ]

    for key in expected_bool_keys:
        if key in cleaning_cfg and not isinstance(cleaning_cfg[key], bool):
            raise ValueError(f"'cleaning.{key}' must be a boolean.")

    if "drop_columns" in cleaning_cfg and not isinstance(cleaning_cfg["drop_columns"], list):
        raise ValueError("'cleaning.drop_columns' must be a list.")

    if "row_filters" in cleaning_cfg and not isinstance(cleaning_cfg["row_filters"], list):
        raise ValueError("'cleaning.row_filters' must be a list.")


def _validate_split_section(config: dict) -> None:
    split_cfg = config["split"]

    if not isinstance(split_cfg, dict):
        raise ValueError("'split' section must be a dictionary.")

    if "strategy" not in split_cfg:
        raise ValueError("Missing required key in 'split' section: ['strategy']")

    strategy = split_cfg["strategy"]

    if strategy not in {"train_test", "train_valid_test"}:
        raise ValueError(
            "'split.strategy' must be either 'train_test' or 'train_valid_test'."
        )

    if "random_state" in split_cfg and not isinstance(split_cfg["random_state"], int):
        raise ValueError("'split.random_state' must be an integer.")

    if "stratify" in split_cfg and not isinstance(split_cfg["stratify"], bool):
        raise ValueError("'split.stratify' must be a boolean.")

    if strategy == "train_test":
        if "test_size" not in split_cfg:
            raise ValueError(
                "Missing required key in 'split' section for strategy "
                "'train_test': ['test_size']"
            )

        test_size = split_cfg["test_size"]
        if not isinstance(test_size, (int, float)):
            raise ValueError("'split.test_size' must be a number.")
        if not 0 < float(test_size) < 1:
            raise ValueError("'split.test_size' must be between 0 and 1.")

    if strategy == "train_valid_test":
        required_size_keys = ["train_size", "valid_size", "test_size"]
        missing_size_keys = [key for key in required_size_keys if key not in split_cfg]

        if missing_size_keys:
            raise ValueError(
                "Missing required keys in 'split' section for strategy "
                f"'train_valid_test': {missing_size_keys}"
            )

        train_size = split_cfg["train_size"]
        valid_size = split_cfg["valid_size"]
        test_size = split_cfg["test_size"]

        for key, value in {
            "train_size": train_size,
            "valid_size": valid_size,
            "test_size": test_size,
        }.items():
            if not isinstance(value, (int, float)):
                raise ValueError(f"'split.{key}' must be a number.")
            if not 0 < float(value) < 1:
                raise ValueError(f"'split.{key}' must be between 0 and 1.")

        total = float(train_size) + float(valid_size) + float(test_size)
        if abs(total - 1.0) > 1e-8:
            raise ValueError(
                "'split.train_size' + 'split.valid_size' + 'split.test_size' "
                "must sum to 1.0."
            )


def _validate_preprocessing_section(config: dict) -> None:
    preprocessing_cfg = config["preprocessing"]

    if not isinstance(preprocessing_cfg, dict):
        raise ValueError("'preprocessing' section must be a dictionary.")

    if "recipe" not in preprocessing_cfg:
        raise ValueError("Missing required key in 'preprocessing' section: ['recipe']")

    recipe_name = preprocessing_cfg["recipe"]

    if not isinstance(recipe_name, str) or not recipe_name.strip():
        raise ValueError("'preprocessing.recipe' must be a non-empty string.")


def _validate_outputs_section(config: dict) -> None:
    outputs_cfg = config["outputs"]

    if not isinstance(outputs_cfg, dict):
        raise ValueError("'outputs' section must be a dictionary.")

    if "save_cleaned_data" in outputs_cfg and not isinstance(
        outputs_cfg["save_cleaned_data"], bool
    ):
        raise ValueError("'outputs.save_cleaned_data' must be a boolean.")

    if "save_processed_data" in outputs_cfg and not isinstance(
        outputs_cfg["save_processed_data"], bool
    ):
        raise ValueError("'outputs.save_processed_data' must be a boolean.")

    if "processed_dir" in outputs_cfg and not isinstance(outputs_cfg["processed_dir"], str):
        raise ValueError("'outputs.processed_dir' must be a string.")

    optional_string_keys = ["cleaned_data_filename", "split_metadata_filename"]
    for key in optional_string_keys:
        if key in outputs_cfg and not isinstance(outputs_cfg[key], str):
            raise ValueError(f"'outputs.{key}' must be a string.")


def validate_config(config: dict) -> None:
    """
    Validate that the config contains the minimum required sections
    for the reusable tabular preprocessing system.

    Expected minimum structure:
    {
        "dataset": {...},
        "target": {"column": "..."},
        "features": {
            "numeric": [...],
            "categorical": [...]
        },
        "cleaning": {...},
        "split": {...},
        "preprocessing": {
            "recipe": "..."
        },
        "outputs": {...}
    }

    Parameters
    ----------
    config : dict
        Configuration dictionary.

    Raises
    ------
    ValueError
        If required sections or keys are missing.
    """
    required_top_level_keys = [
        "dataset",
        "target",
        "features",
        "cleaning",
        "split",
        "preprocessing",
        "outputs",
    ]

    missing_top_level_keys = [
        key for key in required_top_level_keys if key not in config
    ]

    if missing_top_level_keys:
        raise ValueError(
            f"Missing required top-level config keys: {missing_top_level_keys}"
        )

    _validate_dataset_section(config)
    _validate_target_section(config)
    _validate_features_section(config)
    _validate_cleaning_section(config)
    _validate_split_section(config)
    _validate_preprocessing_section(config)
    _validate_outputs_section(config)


def load_and_validate_config(path: str | Path) -> dict:
    """
    Load a YAML config file and validate its minimum structure.

    Parameters
    ----------
    path : str | Path
        Path to the YAML config file.

    Returns
    -------
    dict
        Loaded and validated configuration dictionary.
    """
    config = load_config(path)
    validate_config(config)
    return config
