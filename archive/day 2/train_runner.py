import sys
from pathlib import Path
from typing import Optional
from loguru import logger
from omegaconf import DictConfig, OmegaConf
import typer

app = typer.Typer(
    help="Production ML model training orchestrator with dynamic CLI overrides."
)


@app.command()
def run(
    config_path: Path = typer.Option(
        Path("config.yaml"),
        "--config-path",
        "-c",
        help="Path to the base YAML config file.",
    ),
    batch_size: Optional[int] = typer.Option(
        None, "--batch-size", "-b", help="Override data.batch_size"
    ),
    learning_rate: Optional[float] = typer.Option(
        None, "--learning-rate", "-lr", help="Override model.learning_rate"
    ),
    model_name: Optional[str] = typer.Option(
        None, "--model-name", "-m", help="Override model.name"
    ),
) -> None:
    # 1. Path validation
    if not config_path.exists():
        raise typer.BadParameter(
            f"Config file not found at '{config_path}'", param_hint="--config-path"
        )

    # 2. Load Base YAML
    base_config: DictConfig = OmegaConf.load(config_path)
    overrides: dict[str, dict] = {}

    # 3. Validate and build override dictionary
    if batch_size is not None:
        if batch_size <= 0:
            raise typer.BadParameter(
                "Batch size must be greater than zero.", param_hint="--batch-size"
            )
        overrides.setdefault("data", {})["batch_size"] = batch_size

    if learning_rate is not None:
        if learning_rate <= 0:
            raise typer.BadParameter(
                "Learning rate must be greater than zero.",
                param_hint="--learning-rate",
            )
        overrides.setdefault("model", {})["learning_rate"] = learning_rate

    if model_name is not None:
        overrides.setdefault("model", {})["name"] = model_name

    # 4. Merge configs (Rightmost takes precedence)
    override_config: DictConfig = OmegaConf.create(overrides)
    cfg: DictConfig = OmegaConf.merge(base_config, override_config)

    # 5. Configure Dynamic Logging
    logger.remove()
    log_level = cfg.get("logging", {}).get("log_level", "INFO")
    logger.add(sys.stderr, level=log_level)

    # 6. Output & Simulated Pipeline Execution
    logger.info("Resolved Configuration:\n" + OmegaConf.to_yaml(cfg))
    logger.info(
        f"Initializing {cfg.model.name} with batch size {cfg.data.batch_size} and LR {cfg.model.learning_rate}"
    )


if __name__ == "__main__":
    app()