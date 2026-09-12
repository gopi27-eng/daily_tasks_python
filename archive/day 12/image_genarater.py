import cv2
import numpy as np
import random

# Possible destinations and statuses
cities = ["GUWAHATI", "DELHI", "MUMBAI", "CHENNAI", "KOLKATA", "HYDERABAD", "BENGALURU", "PUNE"]
statuses = ["HEAVY CARGO", "FRAGILE", "HANDLE WITH CARE", "PERISHABLE"]

for i in range(100):
    # Create blank image
    img = np.zeros((250, 600, 3), dtype=np.uint8)
    
    # Random flight ID and city
    flight_id = f"QJ-{100 + i}"
    city = random.choice(cities)
    
    # Random weight between 1000–10000 kg
    weight = random.randint(1000, 10000)
    
    # Random cargo status
    status = random.choice(statuses)
    
    # Draw text
    cv2.putText(img, flight_id, (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
    cv2.putText(img, city, (50, 130), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
    cv2.putText(img, f"{status}", (50, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(img, f"{weight} KG", (50, 220), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Save image
    cv2.imwrite(f"cargo_label_{i+1}.png", img)

print("✅ 100 cargo label images generated successfully!")
