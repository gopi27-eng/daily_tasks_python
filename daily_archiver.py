import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent
ARCHIVE_DIR = BASE_DIR / "archive"

def get_folder_name(archive_dir: Path):
    archive_dir.mkdir(exist_ok=True)

    day_folders = [d for d in archive_dir.iterdir() if d.is_dir() and d.name.lower().startswith("day")]

    if not day_folders:
        return archive_dir / "day 1"

    max_day = 0
    for folder in day_folders:
        try:
            day_num = int(folder.name.split(" ")[-1])
            max_day = max(max_day, day_num)
        except ValueError:
            continue

    next_day = max_day + 1
    return archive_dir / f"day {next_day}"

def move_to_archiver():
    current_py_file = Path(__file__).name
    patterns = ["*.py", "*.sql", "*.txt"]

    # Collect files matching any of the patterns
    files_to_move = [
        file
        for pattern in patterns
        for file in BASE_DIR.glob(pattern)
        if file.is_file() and file.name != current_py_file
    ]

    if not files_to_move:
        print("It seems you are not done today’s task. Kindly do it today’s task.")
        return

    new_folder = get_folder_name(ARCHIVE_DIR)
    new_folder.mkdir(exist_ok=True)
    print(f"Today folder created successfully: {new_folder.name}")

    # Move today’s files to today’s folder
    for file_path in files_to_move:
        destination = new_folder / file_path.name
        shutil.move(str(file_path), str(destination))
        print(f"Moved: {file_path.name} -> {new_folder.name}/")

    print("Daily archiving complete! Workspace is clean.")

if __name__ == "__main__":
    move_to_archiver()
