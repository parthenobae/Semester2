import csv
import requests
import os

# Path to your CSV file
csv_file = "people_data.csv"

# Folder to save images
folder = "Investigation/static/criminals"
os.makedirs(folder, exist_ok=True)

# Read names from CSV
with open(csv_file, newline='') as f:
    reader = csv.DictReader(f)
    names = [row["name"] for row in reader]

# Download images for each name
for i, name in enumerate(names):
    # URL of random AI face
    url = "https://thispersondoesnotexist.com"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Clean name for filename (remove spaces, etc.)
        clean_name = name.replace(" ", "_")
        
        # Save image as name.jpg
        filename = os.path.join(folder, f"{clean_name}.jpg")
        with open(filename, "wb") as img_file:
            img_file.write(response.content)
        
        print(f"Downloaded image {i+1} for {name}")
        
    except Exception as e:
        print(f"Failed to download for {name}: {e}")
