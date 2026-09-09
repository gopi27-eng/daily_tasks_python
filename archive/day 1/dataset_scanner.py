import os
import sys
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

PROJECT_DIR: Path = Path(__file__).resolve().parent
DATA_DIR: str = os.getenv("DATA_DIR", "data_store")
LOG_DIR: str = os.getenv("LOG_FILE", "logs/pipeline")
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

logger.remove()
logger.add(sys.stderr, level=LOG_LEVEL)
logger.add(
    PROJECT_DIR / LOG_DIR,
    level=LOG_LEVEL,
    rotation="1 MB",
    retention="10 days",
    compression="zip",
)

def bootstrap_mock_data(base_path: Path) -> tuple[Path, Path]:
    raw_dir = base_path / "raw"
    processed_dir = base_path / "processed"

    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    (raw_dir / "test.csv").write_text("id,feature,label\n1,0.25,0\n2,0.85,1\n")
    (raw_dir / "mock.csv").write_text("id,feature,label\n1,0.25,0\n2,0.85,1\n")
    (raw_dir / "mock.txt").write_text("this is the text file!")

    return raw_dir, processed_dir

def scan_dataset_dir(base_dir: Path) -> tuple[list[dict[str, object]], int]:
    manifest: list[dict[str, object]] = []
    total_data_size = 0

    if not base_dir.exists():
        logger.error(f"Target directory does not exist: {base_dir}")
        return manifest, total_data_size

    for item in base_dir.rglob("*"):
        if item.is_file():
            file_size = item.stat().st_size
            total_data_size += file_size

            if item.suffix.lower() == ".csv":
                rel_path = item.relative_to(base_dir)
                manifest.append(
                    {
                        "filename": item.name,
                        "rel_path": str(rel_path),
                        "size_bytes": file_size,
                    }
                )
        else:
            # Skip directories silently
            continue

    logger.info(
        f"Scan completed. Total CSVs found: {len(manifest)}, "
        f"Total Size: {total_data_size} bytes"
    )
    return manifest, total_data_size

if __name__ == "__main__":
    base_data_path = PROJECT_DIR / DATA_DIR
    raw, processed = bootstrap_mock_data(base_data_path)

    logger.info(f"Base data directory: {base_data_path}")
    dataset_manifest, total_size = scan_dataset_dir(base_data_path)
    logger.info(f"Manifest: {dataset_manifest}")
