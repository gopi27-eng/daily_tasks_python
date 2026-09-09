from pathlib import Path
from omegaconf import OmegaConf
from loguru import logger

file_path = Path(__file__).parent / "config.yaml"

def load_yaml_config(yaml_path: Path):
    # Load YAML into OmegaConf
    config = OmegaConf.load(yaml_path)
    
    logger.info(f"Booting yaml file: {yaml_path}")
    
    # Extract values safely
    pipeline_name = config.pipeline.name
    lr = config.model.hyperparameters.learning_rate
    target = config.data.target_column
    
    logger.info(f"Successfully extracted pipeline_name: {pipeline_name} lr: {lr}, target: {target}")
    return config

# Run it
load_yaml_config(file_path)
