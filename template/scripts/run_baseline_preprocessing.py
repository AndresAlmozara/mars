import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd
from src.data.io import load_dataset, save_dataframe
from src.data.split import make_dataset_splits, split_features_target
from src.preprocessing.cleaning import run_basic_cleaning
from src.preprocessing.pipeline_builder import build_preprocessor
from src.preprocessing.typing import get_feature_groups
from src.utils.config import load_and_validate_config
from src.utils.paths import get_config_path


def resolve_project_root(config_path: str | Path) -> Path:
    """
    Resolve the project root from the config path.

    Assumes the config file lives under:
        <project_root>/configs/config.yaml
    """
    return Path(config_path).resolve().parent.parent


def resolve_config_relative_path(
    path_value: str | Path,
    config_path: str | Path,
) -> Path:
    """
    Resolve a path declared in config.

    Rules
    -----
    - If the path is already absolute, return it resolved.
    - If relative, resolve it against the project root inferred from config_path.
    """
    path = Path(path_value)

    if path.is_absolute():
        return path.resolve()

    project_root = resolve_project_root(config_path)
    return (project_root / path).resolve()


def to_dataframe(
    transformed_data: Any,
    feature_names: list[str] | None = None,
) -> pd.DataFrame:
    """
    Convert transformed sklearn output into a pandas DataFrame.

    Handles dense arrays, sparse matrices, and similar sklearn outputs.
    """
    if hasattr(transformed_data, "toarray"):
        transformed_data = transformed_data.toarray()

    return pd.DataFrame(transformed_data, columns=feature_names)


def get_split_config(config: dict) -> dict:
    """
    Read split configuration directly from the validated config.
    """
    return config["split"]


def get_outputs_config(config: dict) -> dict:
    """
    Read output configuration with sensible defaults.
    """
    outputs_cfg = config.get("outputs", {})

    return {
        "save_cleaned_data": outputs_cfg.get("save_cleaned_data", False),
        "save_processed_data": outputs_cfg.get("save_processed_data", True),
        "processed_dir": outputs_cfg.get("processed_dir", "data/processed"),
        "cleaned_data_filename": outputs_cfg.get(
            "cleaned_data_filename",
            "cleaned_data.csv",
        ),
        "split_metadata_filename": outputs_cfg.get(
            "split_metadata_filename",
            "split_metadata.json",
        ),
    }


def get_output_path(
    filename: str,
    outputs_cfg: dict,
    config_path: str | Path,
) -> Path:
    """
    Resolve an output path for a file stored in the processed output directory.

    Relative output directories are resolved against the project root inferred
    from config_path, not against the current working directory.
    """
    processed_dir = outputs_cfg.get("processed_dir", "data/processed")
    resolved_processed_dir = resolve_config_relative_path(processed_dir, config_path)
    resolved_processed_dir.mkdir(parents=True, exist_ok=True)
    return resolved_processed_dir / filename


def save_split_metadata(metadata: dict, output_path: str | Path) -> None:
    """
    Save split metadata as JSON.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2, ensure_ascii=False)


def save_processed_split_outputs(
    splits: dict,
    feature_names: list[str],
    target_col: str,
    outputs_cfg: dict,
    config_path: str | Path,
) -> list[str]:
    """
    Save processed X splits and raw y splits using a consistent naming scheme.
    """
    saved_filenames: list[str] = []

    for split_name, split_data in splits.items():
        X_processed = split_data["X_processed"]
        y_split = split_data["y"]

        x_filename = f"X_{split_name}_processed.csv"
        y_filename = f"y_{split_name}.csv"

        X_processed_df = to_dataframe(
            transformed_data=X_processed,
            feature_names=feature_names,
        )

        save_dataframe(
            X_processed_df,
            get_output_path(x_filename, outputs_cfg, config_path),
            file_type="csv",
            index=False,
        )
        saved_filenames.append(x_filename)

        save_dataframe(
            y_split.to_frame(name=target_col),
            get_output_path(y_filename, outputs_cfg, config_path),
            file_type="csv",
            index=False,
        )
        saved_filenames.append(y_filename)

    return saved_filenames


def _get_feature_names_or_fallback(preprocessor: Any, n_features: int) -> list[str]:
    """
    Return feature names from the fitted preprocessor when available.
    Fallback to generic names otherwise.
    """
    if hasattr(preprocessor, "get_feature_names_out"):
        try:
            return preprocessor.get_feature_names_out().tolist()
        except (AttributeError, ValueError, NotImplementedError):
            pass

    return [f"feature_{i}" for i in range(n_features)]


def run_preprocessing(config_path: str | Path | None = None) -> None:
    """
    Run the baseline preprocessing workflow:

    1. Load config
    2. Load raw dataset
    3. Apply safe table cleaning
    4. Read target / numeric / categorical feature groups
    5. Split X/y using the declared split strategy
    6. Build sklearn preprocessor from the selected recipe
    7. Fit on train and transform all relevant splits
    8. Save final processed outputs and split metadata
    """
    if config_path is None:
        config_path = get_config_path()

    config_path = Path(config_path).resolve()
    config = load_and_validate_config(config_path)

    dataset_cfg = config["dataset"]
    outputs_cfg = get_outputs_config(config)

    dataset_path = resolve_config_relative_path(
        dataset_cfg["path"],
        config_path,
    )

    df_raw = load_dataset(
        path=str(dataset_path),
        file_type=dataset_cfg["file_type"],
        sep=dataset_cfg.get("sep", ","),
        encoding=dataset_cfg.get("encoding", "utf-8"),
    )

    df_clean = run_basic_cleaning(df_raw, config)

    if outputs_cfg["save_cleaned_data"]:
        save_dataframe(
            df_clean,
            get_output_path(
                outputs_cfg["cleaned_data_filename"],
                outputs_cfg,
                config_path,
            ),
            file_type="csv",
            index=False,
        )

    feature_info = get_feature_groups(df_clean, config)
    target_col = feature_info["target"]
    numeric_features = feature_info["numeric_features"]
    categorical_features = feature_info["categorical_features"]

    X, y = split_features_target(df_clean, target_col=target_col)

    split_result = make_dataset_splits(
        X=X,
        y=y,
        split_config=get_split_config(config),
        target_col=target_col,
    )

    splits = split_result["splits"]
    split_metadata = split_result["metadata"]

    preprocessor = build_preprocessor(
        numeric_features=numeric_features,
        categorical_features=categorical_features,
        config=config,
    )

    X_train = splits["train"]["X"]
    y_train = splits["train"]["y"]

    preprocessor.fit(X_train, y_train)

    for split_data in splits.values():
        split_data["X_processed"] = preprocessor.transform(split_data["X"])

    n_features = splits["train"]["X_processed"].shape[1]
    feature_names = _get_feature_names_or_fallback(preprocessor, n_features)

    saved_filenames: list[str] = []

    if outputs_cfg["save_processed_data"]:
        saved_filenames.extend(
            save_processed_split_outputs(
                splits=splits,
                feature_names=feature_names,
                target_col=target_col,
                outputs_cfg=outputs_cfg,
                config_path=config_path,
            )
        )

        metadata_output_path = get_output_path(
            outputs_cfg["split_metadata_filename"],
            outputs_cfg,
            config_path,
        )
        save_split_metadata(split_metadata, metadata_output_path)
        saved_filenames.append(outputs_cfg["split_metadata_filename"])

    print("Baseline preprocessing completed successfully.")

    if saved_filenames:
        for filename in saved_filenames:
            print(f"Saved: {filename}")
    else:
        print(
            "No processed files were saved because "
            "'outputs.save_processed_data' is false."
        )


if __name__ == "__main__":
    custom_config_path = sys.argv[1] if len(sys.argv) > 1 else None
    run_preprocessing(custom_config_path)
