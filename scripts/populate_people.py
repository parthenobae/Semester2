import pandas as pd
from Investigation import create_app, db
from Investigation.models import Criminals  # Make sure the import path matches

app = create_app()

with app.app_context():
    # Load your CSV
    df = pd.read_csv("people_data.csv")

    # Prepare the data
    df["picture_filename"] = df["name"].str.lower() + ".jpg"

    # Insert each row into the People table
    for _, row in df.iterrows():
        person = Criminals(name=row["name"], image_file=row["picture_filename"])
        db.session.add(person)

    db.session.commit()
    print(f"Inserted {len(df)} people into the 'people' table.")
