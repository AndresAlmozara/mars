from __future__ import annotations

from pathlib import Path

import yaml
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    MinMaxScaler,
    OneHotEncoder,
    RobustScaler,
    StandardScaler,
)

try:
    from sklearn.preprocessing import TargetEncoder
except ImportError:  # pragma: no cover
    TargetEncoder = None


def load_preprocessing_recipes(
    recipes_path: str | Path | None = None,
) -> dict:
    """
    Load preprocessing recipes from YAML.

    If no path is provided, the default convention is used:
    configs/preprocessing_recipes.yaml

    Parameters
    ----------
    recipes_path : str | Path | None, default=None
        Optional path to the recipes YAML file.

    Returns
    -------
    dict
        Parsed recipes dictionary.

    Raises
    ------
    FileNotFoundError
        If the recipes file does not exist.
    ValueError
        If the YAML file is empty or invalid.
    """
    if recipes_path is None:
        project_root = Path(__file__).resolve().parents[2]
        recipes_path = project_root / "configs" / "preprocessing_recipes.yaml"
    else:
        recipes_path = Path(recipes_path)

    if not recipes_path.exists():
        raise FileNotFoundError(
            f"Preprocessing recipes file not found: {recipes_path}"
        )

    with open(recipes_path, "r", encoding="utf-8") as file:
        recipes_config = yaml.safe_load(file)

    if recipes_config is None:
        raise ValueError(f"Recipes file is empty: {recipes_path}")

    if not isinstance(recipes_config, dict):
        raise ValueError(
            "Preprocessing recipes file must define a YAML dictionary/object "
            "at top level."
        )

    return recipes_config


def get_selected_recipe_name(config: dict) -> str:
    """
    Read the selected preprocessing recipe name from config.

    Expected config structure:
    {
        "preprocessing": {
            "recipe": "scaled_ohe_simple"
        }
    }

    Parameters
    ----------
    config : dict
        Project configuration dictionary.

    Returns
    -------
    str
        Selected recipe name.

    Raises
    ------
    ValueError
        If preprocessing.recipe is missing or invalid.
    """
    preprocessing_cfg = config.get("preprocessing", {})

    if not isinstance(preprocessing_cfg, dict):
        raise ValueError("'preprocessing' section must be a dictionary.")

    recipe_name = preprocessing_cfg.get("recipe")

    if not isinstance(recipe_name, str) or not recipe_name.strip():
        raise ValueError("'preprocessing.recipe' must be a non-empty string.")

    return recipe_name


def get_recipe_config(
    config: dict,
    recipes_path: str | Path | None = None,
) -> dict:
    """
    Resolve the selected recipe configuration from the recipes catalog.

    Parameters
    ----------
    config : dict
        Project configuration dictionary.
    recipes_path : str | Path | None, default=None
        Optional path to the recipes YAML file.

    Returns
    -------
    dict
        Selected recipe configuration dictionary.

    Raises
    ------
    ValueError
        If the recipes catalog is malformed or the selected recipe does not exist.
    """
    recipe_name = get_selected_recipe_name(config)
    recipes_config = load_preprocessing_recipes(recipes_path=recipes_path)

    recipes_root = recipes_config.get("recipes")
    if not isinstance(recipes_root, dict):
        raise ValueError(
            "Recipes YAML must contain a top-level 'recipes' dictionary."
        )

    if recipe_name not in recipes_root:
        available_recipes = sorted(recipes_root.keys())
        raise ValueError(
            f"Unknown preprocessing recipe '{recipe_name}'. "
            f"Available recipes: {available_recipes}"
        )

    recipe_cfg = recipes_root[recipe_name]

    if not isinstance(recipe_cfg, dict):
        raise ValueError(
            f"Recipe '{recipe_name}' must be defined as a dictionary."
        )

    return recipe_cfg


def make_numeric_imputer(strategy: str = "median") -> SimpleImputer:
    """
    Create a numeric imputer.

    Parameters
    ----------
    strategy : str, default="median"
        Supported strategies: "mean", "median", "most_frequent", "constant"

    Returns
    -------
    SimpleImputer
        Configured numeric imputer.

    Raises
    ------
    ValueError
        If the strategy is not supported.
    """
    supported_strategies = {"mean", "median", "most_frequent", "constant"}

    if strategy not in supported_strategies:
        raise ValueError(
            f"Unsupported numeric imputation strategy '{strategy}'. "
            f"Supported: {supported_strategies}"
        )

    if strategy == "constant":
        return SimpleImputer(strategy="constant", fill_value=0)

    return SimpleImputer(strategy=strategy)


def make_categorical_imputer(
    strategy: str = "most_frequent",
    fill_value: str = "missing",
) -> SimpleImputer:
    """
    Create a categorical imputer.

    Parameters
    ----------
    strategy : str, default="most_frequent"
        Supported strategies: "most_frequent", "constant"
    fill_value : str, default="missing"
        Value used when strategy is "constant".

    Returns
    -------
    SimpleImputer
        Configured categorical imputer.

    Raises
    ------
    ValueError
        If the strategy is not supported.
    """
    supported_strategies = {"most_frequent", "constant"}

    if strategy not in supported_strategies:
        raise ValueError(
            f"Unsupported categorical imputation strategy '{strategy}'. "
            f"Supported: {supported_strategies}"
        )

    if strategy == "constant":
        return SimpleImputer(strategy="constant", fill_value=fill_value)

    return SimpleImputer(strategy=strategy)


def make_scaler(name: str = "standard"):
    """
    Create a scaler for numeric features.

    Parameters
    ----------
    name : str, default="standard"
        Supported scalers: "standard", "minmax", "robust", "none"

    Returns
    -------
    transformer
        Sklearn scaler object or "passthrough" if no scaling is requested.

    Raises
    ------
    ValueError
        If the scaler name is not supported.
    """
    supported_scalers = {"standard", "minmax", "robust", "none"}

    if name not in supported_scalers:
        raise ValueError(
            f"Unsupported scaler '{name}'. Supported: {supported_scalers}"
        )

    if name == "standard":
        return StandardScaler()

    if name == "minmax":
        return MinMaxScaler()

    if name == "robust":
        return RobustScaler()

    return "passthrough"


def make_encoder(name: str = "onehot"):
    """
    Create an encoder for categorical features.

    Parameters
    ----------
    name : str, default="onehot"
        Supported encoders: "onehot", "target"

    Returns
    -------
    transformer
        Configured categorical encoder.

    Raises
    ------
    ValueError
        If the encoder name is not supported or unavailable.
    """
    supported_encoders = {"onehot", "target"}

    if name not in supported_encoders:
        raise ValueError(
            f"Unsupported encoder '{name}'. Supported: {supported_encoders}"
        )

    if name == "onehot":
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)

    if name == "target":
        if TargetEncoder is None:
            raise ValueError(
                "TargetEncoder is not available in the current scikit-learn "
                "installation. Upgrade scikit-learn or choose a different recipe."
            )
        return TargetEncoder()

    raise ValueError(f"Unsupported encoder '{name}'.")


def build_numeric_pipeline(
    imputer_strategy: str = "median",
    scaler_name: str = "standard",
) -> Pipeline:
    """
    Build a numeric preprocessing pipeline:
    imputation -> scaling
    """
    return Pipeline(
        steps=[
            ("imputer", make_numeric_imputer(strategy=imputer_strategy)),
            ("scaler", make_scaler(name=scaler_name)),
        ]
    )


def build_categorical_encoded_pipeline(
    imputer_strategy: str = "most_frequent",
    encoder_name: str = "onehot",
    fill_value: str = "missing",
) -> Pipeline:
    """
    Build a categorical preprocessing pipeline:
    imputation -> encoding
    """
    return Pipeline(
        steps=[
            (
                "imputer",
                make_categorical_imputer(
                    strategy=imputer_strategy,
                    fill_value=fill_value,
                ),
            ),
            ("encoder", make_encoder(name=encoder_name)),
        ]
    )


def build_preprocessor(
    numeric_features: list[str],
    categorical_features: list[str],
    config: dict,
) -> ColumnTransformer:
    """
    Build the final ColumnTransformer using the selected preprocessing recipe.

    The selected recipe is read from:
    config["preprocessing"]["recipe"]

    The recipe definition is loaded from:
    configs/preprocessing_recipes.yaml

    Parameters
    ----------
    numeric_features : list[str]
        List of numeric feature names.
    categorical_features : list[str]
        List of categorical feature names.
    config : dict
        Project configuration dictionary.

    Returns
    -------
    ColumnTransformer
        Final sklearn preprocessor for the dataset.
    """
    recipe_cfg = get_recipe_config(config)

    numeric_cfg = recipe_cfg.get("numeric", {})
    categorical_cfg = recipe_cfg.get("categorical", {})

    if not isinstance(numeric_cfg, dict):
        raise ValueError("Recipe 'numeric' block must be a dictionary.")

    if not isinstance(categorical_cfg, dict):
        raise ValueError("Recipe 'categorical' block must be a dictionary.")

    categorical_mode = categorical_cfg.get("mode")

    transformers = []

    if numeric_features:
        numeric_pipeline = build_numeric_pipeline(
            imputer_strategy=numeric_cfg.get("imputer", "median"),
            scaler_name=numeric_cfg.get("scaler", "standard"),
        )
        transformers.append(("numeric", numeric_pipeline, numeric_features))

    if categorical_features:
        if categorical_mode == "ignore":
            # Do not include categorical columns in the final preprocessor.
            pass

        elif categorical_mode == "native":
            # Preserve categorical columns as-is for models that can consume them
            # natively (for example, certain boosted tree implementations).
            transformers.append(
                ("categorical_native", "passthrough", categorical_features)
            )

        else:
            categorical_pipeline = build_categorical_encoded_pipeline(
                imputer_strategy=categorical_cfg.get("imputer", "most_frequent"),
                encoder_name=categorical_cfg.get("encoder", "onehot"),
                fill_value=categorical_cfg.get("fill_value", "missing"),
            )
            transformers.append(
                ("categorical", categorical_pipeline, categorical_features)
            )

    return ColumnTransformer(
        transformers=transformers,
        remainder="drop",
        verbose_feature_names_out=False,
    )
