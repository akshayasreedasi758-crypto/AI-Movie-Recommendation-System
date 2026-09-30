import csv
import os
from sqlalchemy.orm import Session
from backend.database import Base, engine, SessionLocal
from backend.models import Movie, User
from backend.auth import hash_password

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data", "movies.csv")

Base.metadata.create_all(bind=engine)
db: Session = SessionLocal()

try:
    if db.query(Movie).count() == 0:
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                db.add(Movie(
                    title=row["title"],
                    genres=row["genres"],
                    overview=row["overview"],
                    keywords=row["keywords"],
                    cast=row["cast"],
                    director=row["director"],
                    rating=float(row["rating"]),
                    vote_count=int(row.get("vote_count") or 0),
                    poster_url=row.get("poster_url") or "",
                ))
        db.commit()
        print("Movie data imported.")

    if not db.query(User).filter_by(email="admin@example.com").first():
        db.add(User(
            name="Administrator",
            email="admin@example.com",
            password_hash=hash_password("admin123"),
            is_admin=True,
        ))
        db.commit()
        print("Demo admin created.")

finally:
    db.close()
