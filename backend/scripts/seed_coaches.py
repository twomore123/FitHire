"""
Seed script: Generate 200+ realistic fake coach profiles.

Usage:
    cd backend
    pip install psycopg2-binary faker
    python scripts/seed_coaches.py

Requires DATABASE_URL env var or uses the hardcoded default below.
"""

import json
import os
import random
from datetime import datetime, timedelta

import psycopg2
from psycopg2.extras import execute_values

# ── Config ───────────────────────────────────────────────────────────────────
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://neondb_owner:npg_5iQSl1JqIsTK@ep-orange-hall-afkktrid-pooler.c-2.us-west-2.aws.neon.tech/neondb?sslmode=require",
)
NUM_COACHES = 220

# ── Realistic data pools ─────────────────────────────────────────────────────
FIRST_NAMES_F = [
    "Emma", "Olivia", "Ava", "Sophia", "Isabella", "Mia", "Charlotte", "Amelia",
    "Harper", "Evelyn", "Abigail", "Emily", "Madison", "Luna", "Chloe", "Layla",
    "Riley", "Aria", "Zoe", "Nora", "Lily", "Eleanor", "Hannah", "Lillian",
    "Addison", "Aubrey", "Ellie", "Stella", "Natalie", "Leah", "Savannah",
    "Brooklyn", "Bella", "Claire", "Skylar", "Lucy", "Paisley", "Everly",
    "Anna", "Caroline", "Nova", "Genesis", "Emilia", "Kennedy", "Samantha",
    "Maya", "Willow", "Kinsley", "Naomi", "Aaliyah", "Elena", "Sarah",
    "Ariana", "Allison", "Gabriella", "Alice", "Madelyn", "Valentina",
    "Hailey", "Jasmine", "Gianna", "Aurora", "Piper", "Violet",
]
FIRST_NAMES_M = [
    "Liam", "Noah", "Oliver", "Elijah", "James", "William", "Benjamin",
    "Lucas", "Henry", "Alexander", "Mason", "Michael", "Ethan", "Daniel",
    "Jacob", "Logan", "Jackson", "Levi", "Sebastian", "Jack", "Aiden",
    "Owen", "Samuel", "Ryan", "Nathan", "Caleb", "Christian", "Hunter",
    "Eli", "Isaiah", "Thomas", "Aaron", "Lincoln", "Charles", "Jose",
    "Christopher", "Maverick", "Josiah", "Carson", "Ezra", "Jaxon",
    "Cooper", "Jordan", "Tyler", "Cameron", "Adrian", "Miles", "Leo",
    "Grayson", "Vincent", "Cole", "Dominic", "Kai", "Marcus", "Tristan",
    "Derek", "Brody", "Andre", "Dante", "Xavier", "Max", "Zane", "Blake",
]
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
    "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green",
    "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz",
    "Parker", "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris",
    "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan",
    "Cooper", "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos",
    "Kim", "Cox", "Ward", "Richardson", "Watson", "Brooks", "Chavez",
    "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes",
    "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long",
    "Ross", "Foster", "Jimenez", "Powell",
]

CERTIFICATIONS = [
    "NASM-CPT", "ACE-CPT", "ISSA-CPT", "NSCA-CSCS", "ACSM-CPT",
    "RYT-200", "RYT-500", "ACE-GFI", "NASM-PES", "NASM-CES",
    "AFAA-GFI", "CrossFit L1", "CrossFit L2", "Pilates Mat",
    "Pilates Reformer", "TRX-STC", "Kettlebell Cert", "Spinning Cert",
    "Precision Nutrition L1", "ISSA-SFN", "NASM-FNS", "USAW-L1",
    "CPR/AED", "First Aid", "Pre/Postnatal Cert", "Youth Fitness Cert",
    "Senior Fitness Cert", "Corrective Exercise Specialist",
]

SPECIALTIES = [
    "HIIT", "Strength Training", "Cycling", "Yoga", "Pilates",
    "CrossFit", "Boxing", "Kickboxing", "Barre", "Dance Fitness",
    "Functional Training", "Olympic Lifting", "Powerlifting",
    "Bodybuilding", "Mobility", "Flexibility", "Cardio", "TRX",
    "Kettlebell Training", "Boot Camp", "Circuit Training",
    "Core Training", "Nutrition Coaching", "Weight Loss",
    "Sports Performance", "Rehabilitation", "Prenatal Fitness",
    "Senior Fitness", "Group Fitness", "Personal Training",
    "Meditation", "Breathwork", "Swim Coaching", "Running Coaching",
    "Triathlon Coaching", "Martial Arts",
]

TIME_SLOTS = [
    "Mon AM", "Mon PM", "Tue AM", "Tue PM", "Wed AM", "Wed PM",
    "Thu AM", "Thu PM", "Fri AM", "Fri PM", "Sat AM", "Sat PM",
    "Sun AM", "Sun PM",
]

LIFESTYLE_TAGS = [
    "wellness", "community", "high-energy", "mindfulness", "competitive",
    "holistic", "body-positive", "results-driven", "luxury", "boutique",
    "outdoor-enthusiast", "tech-savvy", "eco-conscious", "family-friendly",
]
MOVEMENT_TAGS = [
    "technical-precision", "dynamic-flow", "explosive-power",
    "mind-body-connection", "rhythm-based", "endurance-focused",
    "flexibility-oriented", "functional-movement", "strength-focused",
]
INSTRUCTION_TAGS = [
    "motivational", "educational", "hands-on", "demo-heavy",
    "voice-led", "music-driven", "data-informed", "intuitive",
    "compassionate", "high-intensity-cueing", "calm-and-grounding",
]

# US cities with state – weighted toward fitness-heavy metros
CITIES = [
    ("Los Angeles", "CA"), ("San Diego", "CA"), ("San Francisco", "CA"),
    ("Santa Monica", "CA"), ("Irvine", "CA"), ("Pasadena", "CA"),
    ("Long Beach", "CA"), ("Oakland", "CA"), ("Sacramento", "CA"),
    ("New York", "NY"), ("Brooklyn", "NY"), ("Manhattan", "NY"),
    ("Queens", "NY"), ("Jersey City", "NJ"), ("Hoboken", "NJ"),
    ("Miami", "FL"), ("Fort Lauderdale", "FL"), ("Tampa", "FL"),
    ("Orlando", "FL"), ("Jacksonville", "FL"), ("Naples", "FL"),
    ("Austin", "TX"), ("Houston", "TX"), ("Dallas", "TX"),
    ("San Antonio", "TX"), ("Plano", "TX"), ("Fort Worth", "TX"),
    ("Chicago", "IL"), ("Naperville", "IL"), ("Evanston", "IL"),
    ("Denver", "CO"), ("Boulder", "CO"), ("Colorado Springs", "CO"),
    ("Seattle", "WA"), ("Portland", "OR"), ("Scottsdale", "AZ"),
    ("Phoenix", "AZ"), ("Nashville", "TN"), ("Atlanta", "GA"),
    ("Charlotte", "NC"), ("Raleigh", "NC"), ("Boston", "MA"),
    ("Washington", "DC"), ("Arlington", "VA"), ("Bethesda", "MD"),
    ("Minneapolis", "MN"), ("Salt Lake City", "UT"), ("Honolulu", "HI"),
    ("San Juan", "PR"), ("Las Vegas", "NV"),
]

BIOS = [
    "Passionate about helping clients achieve their fitness goals through personalized training programs.",
    "Certified fitness professional with a focus on functional movement and injury prevention.",
    "Dedicated to creating inclusive, high-energy group fitness experiences that leave you feeling empowered.",
    "Former collegiate athlete turned fitness coach. I bring discipline, energy, and science-backed programming.",
    "Specializing in mind-body connection through yoga and mobility work. Every body is welcome in my classes.",
    "High-intensity training specialist who believes in pushing limits while maintaining proper form.",
    "Holistic wellness coach combining fitness, nutrition, and mindfulness for total body transformation.",
    "Group fitness enthusiast with a talent for building community and making workouts feel like a party.",
    "Strength and conditioning specialist helping athletes and everyday movers perform at their best.",
    "Experienced personal trainer focused on sustainable lifestyle changes, not quick fixes.",
    "Boutique fitness instructor passionate about the details — form, music, energy, and connection.",
    "Movement specialist blending traditional strength training with modern functional fitness techniques.",
    "Energetic cycling instructor who creates playlists and ride experiences that keep people coming back.",
    "Yoga teacher and meditation guide helping busy professionals find balance and reduce stress.",
    "CrossFit coach dedicated to building strong, capable humans through varied functional movements.",
    "Pilates instructor focused on core strength, posture correction, and graceful movement patterns.",
    "Boot camp style trainer who thrives on motivating groups and creating team camaraderie.",
    "Nutrition-certified coach who combines training with dietary guidance for complete wellness.",
    "Senior fitness specialist making exercise accessible, safe, and enjoyable for older adults.",
    "Pre and postnatal fitness expert helping moms stay strong and healthy through every stage.",
    "Boxing and kickboxing coach bringing combat sport intensity to fitness in a safe, fun environment.",
    "Trail runner and outdoor fitness enthusiast who loves taking workouts beyond the gym walls.",
    "Dance fitness instructor bringing joy, rhythm, and serious cardio to every class.",
    "Rehabilitation-focused trainer working with clients recovering from injury or managing chronic conditions.",
    "Tech-savvy coach who uses wearables and data to optimize training programs and track progress.",
]


def generate_coach(i: int) -> dict:
    """Generate a single realistic fake coach profile."""
    is_female = random.random() < 0.55
    first = random.choice(FIRST_NAMES_F if is_female else FIRST_NAMES_M)
    last = random.choice(LAST_NAMES)
    city, state = random.choice(CITIES)

    years_exp = random.choices(
        range(1, 26),
        weights=[3, 5, 7, 8, 9, 10, 10, 9, 8, 7, 6, 5, 4, 3, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1],
        k=1,
    )[0]

    # More experienced coaches tend to have more certs
    num_certs = min(random.randint(1, 3) + (years_exp // 4), 8)
    certs = random.sample(CERTIFICATIONS, num_certs)
    cert_objects = []
    for cert in certs:
        exp_date = datetime.now() + timedelta(days=random.randint(60, 1200))
        cert_objects.append({
            "name": cert,
            "verified": random.random() < 0.7,
            "expiration": exp_date.strftime("%Y-%m-%d"),
        })

    num_specialties = random.randint(2, 6)
    specialties = random.sample(SPECIALTIES, num_specialties)

    num_slots = random.randint(3, 10)
    available_times = sorted(random.sample(TIME_SLOTS, num_slots), key=TIME_SLOTS.index)

    lifestyle = random.sample(LIFESTYLE_TAGS, random.randint(1, 4))
    movement = random.sample(MOVEMENT_TAGS, random.randint(1, 3))
    instruction = random.sample(INSTRUCTION_TAGS, random.randint(1, 3))

    bio = random.choice(BIOS) if random.random() < 0.85 else None

    # Profile completeness based on how much is filled in
    completeness = round(random.uniform(0.55, 1.0), 2)

    # Some coaches are verified
    verified_at = None
    if random.random() < 0.5:
        days_ago = random.randint(1, 365)
        verified_at = datetime.utcnow() - timedelta(days=days_ago)

    now = datetime.utcnow()
    created_days_ago = random.randint(1, 400)
    created_at = now - timedelta(days=created_days_ago)
    last_updated = created_at + timedelta(days=random.randint(0, created_days_ago))

    return {
        "first_name": first,
        "last_name": last,
        "email": f"{first.lower()}.{last.lower()}{i}@fakeemail.dev",
        "city": city,
        "state": state,
        "years_experience": years_exp,
        "certifications": json.dumps(cert_objects),
        "specialties": json.dumps(specialties),
        "available_times": json.dumps(available_times),
        "lifestyle_tags": json.dumps(lifestyle),
        "movement_tags": json.dumps(movement),
        "instruction_tags": json.dumps(instruction),
        "bio": bio,
        "profile_completeness": completeness,
        "verified_at": verified_at,
        "created_at": created_at,
        "last_updated": last_updated,
    }


def main():
    print(f"Connecting to database...")
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Ensure a brand exists (use existing or create "Coach 360")
    cur.execute("SELECT id FROM brands LIMIT 1")
    row = cur.fetchone()
    if row:
        brand_id = row[0]
        print(f"Using existing brand_id={brand_id}")
    else:
        cur.execute(
            "INSERT INTO brands (name, slug, created_at, updated_at) VALUES (%s, %s, %s, %s) RETURNING id",
            ("Coach 360", "coach360", datetime.utcnow(), datetime.utcnow()),
        )
        brand_id = cur.fetchone()[0]
        print(f"Created brand 'Coach 360' with id={brand_id}")
        conn.commit()

    # Generate coaches
    coaches_data = [generate_coach(i) for i in range(1, NUM_COACHES + 1)]
    print(f"Generated {len(coaches_data)} coach profiles. Inserting...")

    inserted = 0
    for c in coaches_data:
        try:
            # Create user first
            cur.execute(
                """INSERT INTO users (clerk_user_id, brand_id, email, first_name, last_name, role, created_at, updated_at)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                   RETURNING id""",
                (
                    f"fake_clerk_{c['email']}",
                    brand_id,
                    c["email"],
                    c["first_name"],
                    c["last_name"],
                    "coach",
                    c["created_at"],
                    c["last_updated"],
                ),
            )
            user_id = cur.fetchone()[0]

            # Create coach profile
            cur.execute(
                """INSERT INTO coaches
                   (user_id, brand_id, bio, city, state, years_experience,
                    certifications, specialties, available_times,
                    lifestyle_tags, movement_tags, instruction_tags,
                    profile_completeness, verified_at, last_updated, created_at)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    user_id,
                    brand_id,
                    c["bio"],
                    c["city"],
                    c["state"],
                    c["years_experience"],
                    c["certifications"],
                    c["specialties"],
                    c["available_times"],
                    c["lifestyle_tags"],
                    c["movement_tags"],
                    c["instruction_tags"],
                    c["profile_completeness"],
                    c["verified_at"],
                    c["last_updated"],
                    c["created_at"],
                ),
            )
            inserted += 1
        except Exception as e:
            conn.rollback()
            print(f"  Error inserting {c['email']}: {e}")
            continue

    conn.commit()

    # Print summary
    cur.execute("SELECT COUNT(*) FROM coaches")
    total = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM users WHERE role = 'coach'")
    total_users = cur.fetchone()[0]

    print(f"\nDone! Inserted {inserted}/{NUM_COACHES} coach profiles.")
    print(f"Total coaches in DB: {total}")
    print(f"Total coach users in DB: {total_users}")

    # Print distribution stats
    cur.execute("SELECT state, COUNT(*) FROM coaches GROUP BY state ORDER BY COUNT(*) DESC LIMIT 10")
    print("\nTop 10 states:")
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[1]}")

    cur.execute("SELECT AVG(years_experience), MIN(years_experience), MAX(years_experience) FROM coaches")
    avg, mn, mx = cur.fetchone()
    print(f"\nExperience: avg={avg:.1f} yrs, min={mn}, max={mx}")

    conn.close()


if __name__ == "__main__":
    main()
