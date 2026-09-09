from tqdm import tqdm
import time

# Loop with progress bar
for i in tqdm(range(4), desc="Processing"):
    time.sleep(0.5)  # simulate work
