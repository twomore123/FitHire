"""
Database seeding script for FitHire
Creates initial test data: Brand, Region, Location, and User
"""

from app.db.session import SessionLocal, engine
from app.models.brand import Brand, Region, Location
from app.models.user import User
from app.db.session import Base

def seed_database():
    """Seed database with initial test data"""

    # Create all tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Check if data already exists
        existing_brand = db.query(Brand).first()
        if existing_brand:
            print("✅ Database already seeded!")
            return

        # Create a test brand
        brand = Brand(
            name="FitHire Demo Gym",
            slug="fithire-demo"
        )
        db.add(brand)
        db.flush()  # Get the brand ID

        # Create a test region
        region = Region(
            brand_id=brand.id,
            name="San Francisco Bay Area",
            slug="sf-bay-area"
        )
        db.add(region)
        db.flush()  # Get the region ID

        # Create test locations
        locations_data = [
            {"name": "Downtown SF Studio", "city": "San Francisco", "state": "CA"},
            {"name": "Oakland Fitness Center", "city": "Oakland", "state": "CA"},
            {"name": "San Jose Gym", "city": "San Jose", "state": "CA"},
        ]

        for loc_data in locations_data:
            location = Location(
                brand_id=brand.id,
                region_id=region.id,
                **loc_data
            )
            db.add(location)

        # Create a test user (for coach profiles to reference)
        user = User(
            clerk_user_id="test_user_123",
            brand_id=brand.id,
            email="test@fithire.com",
            first_name="Test",
            last_name="User",
            role="coach"
        )
        db.add(user)

        db.commit()
        print("✅ Database seeded successfully!")
        print(f"   Created Brand: {brand.name}")
        print(f"   Created Region: {region.name}")
        print(f"   Created {len(locations_data)} locations")
        print(f"   Created Test User: {user.email}")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🌱 Seeding database...")
    seed_database()
