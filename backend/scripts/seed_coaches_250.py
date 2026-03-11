"""
Seed script: Add 250 additional diverse coach profiles for demo purposes.

Coaches span a wide range of experience levels, certifications, specialties,
geographic locations, availability patterns, and culture fits. Designed to
produce realistic variety for FitScore matching demos.

Usage:
    cd backend
    pip install psycopg2-binary
    python scripts/seed_coaches_250.py

Requires DATABASE_URL env var or uses the hardcoded default below.
"""

import json
import os
import random
from datetime import datetime, timedelta

import psycopg2

# ── Config ───────────────────────────────────────────────────────────────────
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://neondb_owner:npg_5iQSl1JqIsTK@ep-orange-hall-afkktrid-pooler.c-2.us-west-2.aws.neon.tech/neondb?sslmode=require",
)
NUM_COACHES = 250
EMAIL_DOMAIN = "fithire-demo.dev"

# ── Name pools (expanded for uniqueness) ────────────────────────────────────
FIRST_NAMES_F = [
    "Sofia", "Camila", "Valentina", "Lucia", "Mariana", "Daniela", "Priya",
    "Ananya", "Mei", "Yuki", "Aisha", "Fatima", "Zara", "Amara", "Nia",
    "Imani", "Keiko", "Sakura", "Hana", "Riya", "Sana", "Leila", "Nadia",
    "Ingrid", "Astrid", "Freya", "Sienna", "Bianca", "Celeste", "Dahlia",
    "Jade", "Ruby", "Sierra", "Sage", "Quinn", "Reese", "Brynn", "Sloane",
    "Harlow", "Wren", "Tessa", "Maren", "Kira", "Lena", "Ivy", "Esme",
    "Thea", "Iris", "Cora", "Ada", "Elise", "Fiona", "Greta", "Holly",
    "Juno", "Kaia", "Lyra", "Mila", "Nina", "Opal", "Petra", "Rosalie",
]
FIRST_NAMES_M = [
    "Mateo", "Santiago", "Emilio", "Diego", "Rafael", "Arjun", "Rohan",
    "Kai", "Kenji", "Hiroshi", "Idris", "Kofi", "Jabari", "Tariq", "Zain",
    "Soren", "Lars", "Axel", "Nico", "Luca", "Marco", "Theo", "Hugo",
    "Felix", "Oscar", "Jasper", "Beckett", "Reed", "Knox", "Wells",
    "Rhys", "Finn", "Declan", "Atlas", "Bodhi", "Cash", "Crew", "Dane",
    "Elio", "Gage", "Heath", "Jett", "Kade", "Lane", "Nash", "Pierce",
    "Remy", "Shane", "Tate", "Vance", "Wade", "Wyatt", "Asher", "Beau",
    "Clay", "Drew", "Evan", "Grant", "Hayes", "Ivan", "Joel", "Kent",
]
LAST_NAMES = [
    "Okafor", "Nakamura", "Singh", "Patel", "Chen", "Kim", "Park", "Li",
    "Tanaka", "Sharma", "Gupta", "Muller", "Schmidt", "Weber", "Fischer",
    "Costa", "Ferreira", "Santos", "Silva", "Oliveira", "Johansson", "Berg",
    "Lindgren", "O'Brien", "O'Connor", "McCarthy", "Sullivan", "Walsh",
    "Kowalski", "Novak", "Petrovic", "Volkov", "Ivanov", "Dubois", "Laurent",
    "Moreau", "Russo", "Romano", "Bianchi", "Van der Berg", "De Vries",
    "Yamamoto", "Sato", "Watanabe", "Kobayashi", "Hashimoto",
    "Fernandez", "Vasquez", "Delgado", "Rios", "Medina", "Vargas",
    "Castillo", "Guerrero", "Romero", "Herrera", "Aguilar", "Soto",
    "Ramos", "Mendez", "Salazar", "Contreras", "Fuentes", "Cardenas",
    "Stone", "Frost", "Rivers", "Banks", "Fields", "Winters", "Cross",
    "Barrett", "Holt", "Kane", "Marsh", "Quinn", "Steele", "Vaughn",
    "Spencer", "Dawson", "Burke", "Chambers", "Dunn", "Reeves", "Thornton",
    "Blackwell", "Whitfield", "Donovan", "Gallagher", "Hampton", "Jennings",
    "Malone", "Norris", "Pittman", "Shelton", "Underwood", "Wilder",
]

# ── Certifications (grouped by category for realistic combos) ───────────────
CERT_PERSONAL_TRAINING = ["NASM-CPT", "ACE-CPT", "ISSA-CPT", "NSCA-CSCS", "ACSM-CPT"]
CERT_GROUP_FITNESS = ["ACE-GFI", "AFAA-GFI", "Les Mills Certified", "Zumba Certified"]
CERT_YOGA = ["RYT-200", "RYT-500", "Yoga Alliance E-RYT"]
CERT_PILATES = ["Pilates Mat", "Pilates Reformer", "BASI Pilates", "Stott Pilates"]
CERT_SPECIALTY = [
    "CrossFit L1", "CrossFit L2", "TRX-STC", "Kettlebell Cert",
    "Spinning Cert", "USAW-L1", "Pre/Postnatal Cert", "Youth Fitness Cert",
    "Senior Fitness Cert", "Corrective Exercise Specialist", "NASM-PES",
    "NASM-CES", "Precision Nutrition L1", "ISSA-SFN", "NASM-FNS",
]
CERT_SAFETY = ["CPR/AED", "First Aid"]
ALL_CERTS = (
    CERT_PERSONAL_TRAINING + CERT_GROUP_FITNESS + CERT_YOGA +
    CERT_PILATES + CERT_SPECIALTY + CERT_SAFETY
)

# ── Specialties (broader range) ─────────────────────────────────────────────
SPECIALTIES = [
    "HIIT", "Strength Training", "Cycling", "Yoga", "Pilates", "CrossFit",
    "Boxing", "Kickboxing", "Barre", "Dance Fitness", "Functional Training",
    "Olympic Lifting", "Powerlifting", "Bodybuilding", "Mobility",
    "Flexibility", "Cardio", "TRX", "Kettlebell Training", "Boot Camp",
    "Circuit Training", "Core Training", "Nutrition Coaching", "Weight Loss",
    "Sports Performance", "Rehabilitation", "Prenatal Fitness",
    "Senior Fitness", "Group Fitness", "Personal Training", "Meditation",
    "Breathwork", "Swim Coaching", "Running Coaching", "Triathlon Coaching",
    "Martial Arts", "Rock Climbing", "Rowing", "Aqua Fitness",
    "Adaptive Fitness", "Parkour", "Calisthenics", "Suspension Training",
    "Animal Flow", "Plyometrics", "Speed & Agility",
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
    "fun", "premium",
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

# ── Cities (expanded) ───────────────────────────────────────────────────────
CITIES = [
    ("Los Angeles", "CA"), ("San Diego", "CA"), ("San Francisco", "CA"),
    ("Santa Monica", "CA"), ("Irvine", "CA"), ("Pasadena", "CA"),
    ("Long Beach", "CA"), ("Oakland", "CA"), ("Sacramento", "CA"),
    ("San Jose", "CA"), ("Berkeley", "CA"),
    ("New York", "NY"), ("Brooklyn", "NY"), ("Manhattan", "NY"),
    ("Queens", "NY"), ("Astoria", "NY"), ("Williamsburg", "NY"),
    ("Jersey City", "NJ"), ("Hoboken", "NJ"), ("Princeton", "NJ"),
    ("Miami", "FL"), ("Fort Lauderdale", "FL"), ("Tampa", "FL"),
    ("Orlando", "FL"), ("Jacksonville", "FL"), ("Naples", "FL"),
    ("Boca Raton", "FL"), ("Coral Gables", "FL"),
    ("Austin", "TX"), ("Houston", "TX"), ("Dallas", "TX"),
    ("San Antonio", "TX"), ("Plano", "TX"), ("Fort Worth", "TX"),
    ("Chicago", "IL"), ("Naperville", "IL"), ("Evanston", "IL"),
    ("Denver", "CO"), ("Boulder", "CO"), ("Colorado Springs", "CO"),
    ("Seattle", "WA"), ("Bellevue", "WA"), ("Tacoma", "WA"),
    ("Portland", "OR"), ("Bend", "OR"),
    ("Scottsdale", "AZ"), ("Phoenix", "AZ"), ("Tempe", "AZ"),
    ("Nashville", "TN"), ("Memphis", "TN"), ("Knoxville", "TN"),
    ("Atlanta", "GA"), ("Savannah", "GA"), ("Decatur", "GA"),
    ("Charlotte", "NC"), ("Raleigh", "NC"), ("Asheville", "NC"),
    ("Boston", "MA"), ("Cambridge", "MA"), ("Brookline", "MA"),
    ("Washington", "DC"), ("Arlington", "VA"), ("Bethesda", "MD"),
    ("Minneapolis", "MN"), ("St. Paul", "MN"),
    ("Salt Lake City", "UT"), ("Park City", "UT"),
    ("Honolulu", "HI"), ("Las Vegas", "NV"), ("Reno", "NV"),
    ("Charleston", "SC"), ("Greenville", "SC"),
    ("Pittsburgh", "PA"), ("Philadelphia", "PA"),
    ("Detroit", "MI"), ("Ann Arbor", "MI"),
    ("Indianapolis", "IN"), ("Columbus", "OH"), ("Cincinnati", "OH"),
    ("Milwaukee", "WI"), ("Madison", "WI"),
    ("New Orleans", "LA"), ("Baton Rouge", "LA"),
    ("Kansas City", "MO"), ("St. Louis", "MO"),
    ("Omaha", "NE"), ("Des Moines", "IA"),
    ("Richmond", "VA"), ("Virginia Beach", "VA"),
    ("Boise", "ID"), ("Tucson", "AZ"), ("Albuquerque", "NM"),
]

# ── Coach archetypes for realistic variety ──────────────────────────────────
# Each archetype defines tendencies for cert selection, specialties, tags, etc.
ARCHETYPES = [
    {
        "name": "yoga_instructor",
        "weight": 15,
        "cert_pools": [CERT_YOGA, CERT_SAFETY],
        "specialty_bias": ["Yoga", "Meditation", "Breathwork", "Flexibility", "Mobility"],
        "lifestyle_bias": ["mindfulness", "holistic", "wellness", "community"],
        "movement_bias": ["mind-body-connection", "flexibility-oriented", "dynamic-flow"],
        "instruction_bias": ["calm-and-grounding", "intuitive", "compassionate"],
        "exp_range": (1, 20),
    },
    {
        "name": "strength_coach",
        "weight": 15,
        "cert_pools": [CERT_PERSONAL_TRAINING, CERT_SPECIALTY, CERT_SAFETY],
        "specialty_bias": ["Strength Training", "Powerlifting", "Olympic Lifting", "Bodybuilding", "Functional Training"],
        "lifestyle_bias": ["competitive", "results-driven", "high-energy"],
        "movement_bias": ["strength-focused", "explosive-power", "technical-precision"],
        "instruction_bias": ["educational", "hands-on", "data-informed"],
        "exp_range": (2, 25),
    },
    {
        "name": "group_fitness",
        "weight": 20,
        "cert_pools": [CERT_GROUP_FITNESS, CERT_PERSONAL_TRAINING, CERT_SAFETY],
        "specialty_bias": ["Group Fitness", "HIIT", "Boot Camp", "Circuit Training", "Dance Fitness", "Cardio"],
        "lifestyle_bias": ["high-energy", "community", "fun", "body-positive"],
        "movement_bias": ["rhythm-based", "dynamic-flow", "endurance-focused"],
        "instruction_bias": ["motivational", "music-driven", "high-intensity-cueing", "voice-led"],
        "exp_range": (1, 15),
    },
    {
        "name": "pilates_specialist",
        "weight": 10,
        "cert_pools": [CERT_PILATES, CERT_SAFETY],
        "specialty_bias": ["Pilates", "Barre", "Core Training", "Flexibility", "Rehabilitation"],
        "lifestyle_bias": ["boutique", "wellness", "body-positive", "luxury"],
        "movement_bias": ["technical-precision", "mind-body-connection", "flexibility-oriented"],
        "instruction_bias": ["educational", "hands-on", "demo-heavy"],
        "exp_range": (2, 18),
    },
    {
        "name": "crossfit_athlete",
        "weight": 10,
        "cert_pools": [CERT_SPECIALTY, CERT_PERSONAL_TRAINING, CERT_SAFETY],
        "specialty_bias": ["CrossFit", "Olympic Lifting", "Functional Training", "Kettlebell Training", "Plyometrics"],
        "lifestyle_bias": ["competitive", "community", "high-energy", "results-driven"],
        "movement_bias": ["explosive-power", "functional-movement", "strength-focused"],
        "instruction_bias": ["motivational", "high-intensity-cueing", "hands-on"],
        "exp_range": (1, 12),
    },
    {
        "name": "combat_sports",
        "weight": 8,
        "cert_pools": [CERT_GROUP_FITNESS, CERT_PERSONAL_TRAINING, CERT_SAFETY],
        "specialty_bias": ["Boxing", "Kickboxing", "Martial Arts", "HIIT", "Speed & Agility"],
        "lifestyle_bias": ["competitive", "high-energy", "results-driven"],
        "movement_bias": ["explosive-power", "rhythm-based", "endurance-focused"],
        "instruction_bias": ["motivational", "demo-heavy", "high-intensity-cueing"],
        "exp_range": (2, 20),
    },
    {
        "name": "cycling_instructor",
        "weight": 8,
        "cert_pools": [CERT_GROUP_FITNESS, CERT_SAFETY],
        "specialty_bias": ["Cycling", "Cardio", "HIIT", "Triathlon Coaching"],
        "lifestyle_bias": ["high-energy", "community", "tech-savvy", "competitive"],
        "movement_bias": ["rhythm-based", "endurance-focused", "dynamic-flow"],
        "instruction_bias": ["music-driven", "motivational", "voice-led"],
        "exp_range": (1, 10),
    },
    {
        "name": "rehab_specialist",
        "weight": 5,
        "cert_pools": [CERT_PERSONAL_TRAINING, CERT_SPECIALTY, CERT_SAFETY],
        "specialty_bias": ["Rehabilitation", "Mobility", "Corrective Exercise Specialist", "Senior Fitness", "Adaptive Fitness"],
        "lifestyle_bias": ["holistic", "wellness", "family-friendly", "body-positive"],
        "movement_bias": ["functional-movement", "flexibility-oriented", "mind-body-connection"],
        "instruction_bias": ["compassionate", "educational", "hands-on", "intuitive"],
        "exp_range": (3, 25),
    },
    {
        "name": "outdoor_adventure",
        "weight": 5,
        "cert_pools": [CERT_PERSONAL_TRAINING, CERT_SPECIALTY, CERT_SAFETY],
        "specialty_bias": ["Running Coaching", "Triathlon Coaching", "Rock Climbing", "Swim Coaching", "Boot Camp"],
        "lifestyle_bias": ["outdoor-enthusiast", "community", "eco-conscious", "competitive"],
        "movement_bias": ["endurance-focused", "functional-movement", "explosive-power"],
        "instruction_bias": ["motivational", "data-informed", "hands-on"],
        "exp_range": (2, 18),
    },
    {
        "name": "wellness_generalist",
        "weight": 4,
        "cert_pools": [CERT_PERSONAL_TRAINING, CERT_SPECIALTY, CERT_SAFETY],
        "specialty_bias": ["Nutrition Coaching", "Weight Loss", "Personal Training", "Meditation", "Breathwork"],
        "lifestyle_bias": ["holistic", "wellness", "mindfulness", "body-positive"],
        "movement_bias": ["mind-body-connection", "functional-movement", "flexibility-oriented"],
        "instruction_bias": ["compassionate", "intuitive", "educational"],
        "exp_range": (1, 15),
    },
]

# ── Bios (expanded & varied) ────────────────────────────────────────────────
BIOS = [
    "I believe fitness should be challenging AND fun. My classes are a blend of science-backed programming and contagious energy.",
    "Former D1 athlete who found a passion for coaching after retirement. I help everyone from beginners to competitive athletes.",
    "15+ years in the fitness industry, specializing in transformative body composition programs with a focus on sustainable habits.",
    "I teach yoga because I've seen how it changes lives — physically, mentally, and spiritually. All levels welcome.",
    "My training style is technical and methodical. I believe proper form is the foundation of every fitness goal.",
    "Started as a group fitness participant, fell in love with instructing, and never looked back. Community is everything.",
    "Certified strength coach who geeks out on programming periodization and progressive overload principles.",
    "Dance background turned fitness career. I bring choreography, rhythm, and pure joy to every class I teach.",
    "As a former physical therapist, I bring a rehab-minded approach to every training session.",
    "Mom of three who found her calling in prenatal and postpartatal fitness. I understand the journey firsthand.",
    "CrossFit changed my life, and now I want to share that transformation with others. Scalable programming for all levels.",
    "Pilates instructor with a keen eye for alignment. I help clients build core strength that translates to everyday life.",
    "Boxing coach for 10+ years. I make combat fitness accessible, safe, and incredibly rewarding.",
    "Trail runner, cyclist, and all-around outdoor fitness enthusiast. Let's take the workout outside!",
    "Nutrition-first approach to fitness. I believe 80% of results happen in the kitchen, and I coach both sides.",
    "I work primarily with seniors and those returning from injury. Patience and progress, not perfection.",
    "High-energy cycling instructor — my rides are a party on a bike with a killer soundtrack.",
    "Bodyweight and calisthenics specialist. You don't need a gym to build an incredible physique.",
    "Kettlebell enthusiast who loves the simplicity and effectiveness of single-implement training.",
    "Meditation and breathwork guide helping stressed professionals find calm in the chaos.",
    "Former competitive gymnast turned flexibility and mobility coach. Movement quality over quantity.",
    "I coach triathletes from their first sprint to Ironman. Structured plans, real results.",
    "Boot camp-style trainer who builds teams, not just bodies. Accountability and camaraderie are my superpowers.",
    "Movement specialist blending yoga, animal flow, and functional training into creative, flowing sessions.",
    "Data-driven personal trainer. I use wearables, body composition analysis, and progress tracking to optimize results.",
    "Inclusive fitness advocate. I create spaces where everyone — regardless of size, ability, or background — can thrive.",
    "Former Marine turned fitness professional. Discipline, structure, and mental toughness are core to my coaching philosophy.",
    "Rowing and aqua fitness instructor bringing low-impact, high-result training to every session.",
    "Speed and agility coach working with youth athletes and weekend warriors alike.",
    "TRX and suspension training specialist. Bodyweight training reimagined for total-body results.",
    "I blend Eastern movement practices with Western exercise science for a holistic training experience.",
    "Passionate about adaptive fitness and making exercise accessible to people of all abilities.",
    "HIIT specialist who keeps sessions under 45 minutes — efficient, effective, and intense.",
    "Barre instructor bringing ballet-inspired conditioning to fitness enthusiasts of all backgrounds.",
    "I focus on the mind-muscle connection. Slow, controlled movements build better bodies.",
    None,  # Some coaches haven't filled in their bio
    None,
    None,
]


def pick_archetype() -> dict:
    """Weighted random selection of a coach archetype."""
    weights = [a["weight"] for a in ARCHETYPES]
    return random.choices(ARCHETYPES, weights=weights, k=1)[0]


def generate_coach(index: int) -> dict:
    """Generate a single coach profile based on a random archetype."""
    archetype = pick_archetype()

    is_female = random.random() < 0.55
    first = random.choice(FIRST_NAMES_F if is_female else FIRST_NAMES_M)
    last = random.choice(LAST_NAMES)
    city, state = random.choice(CITIES)

    # Experience varies by archetype
    lo, hi = archetype["exp_range"]
    years_exp = random.randint(lo, hi)

    # Certs: pick from archetype-relevant pools, with some randomness
    cert_pool = []
    for pool in archetype["cert_pools"]:
        cert_pool.extend(pool)
    # Deduplicate
    cert_pool = list(set(cert_pool))
    num_certs = min(random.randint(1, 3) + (years_exp // 5), len(cert_pool))
    num_certs = max(1, num_certs)
    chosen_certs = random.sample(cert_pool, min(num_certs, len(cert_pool)))

    # Occasionally add a random cert from outside the archetype
    if random.random() < 0.25 and len(chosen_certs) < 8:
        extra = random.choice([c for c in ALL_CERTS if c not in chosen_certs])
        chosen_certs.append(extra)

    cert_objects = []
    for cert in chosen_certs:
        exp_date = datetime.now() + timedelta(days=random.randint(60, 1200))
        cert_objects.append({
            "name": cert,
            "verified": random.random() < 0.65,
            "expiration": exp_date.strftime("%Y-%m-%d"),
        })

    # Specialties: bias toward archetype, with some random additions
    specialties = list(set(random.sample(
        archetype["specialty_bias"],
        min(random.randint(2, 4), len(archetype["specialty_bias"])),
    )))
    # Add 0-2 random extra specialties
    extras = [s for s in SPECIALTIES if s not in specialties]
    specialties.extend(random.sample(extras, min(random.randint(0, 2), len(extras))))

    # Availability: varied patterns
    # Some coaches are very available, some only a few slots
    availability_pattern = random.choices(
        ["minimal", "part_time", "full_time", "weekends_only"],
        weights=[15, 35, 35, 15],
        k=1,
    )[0]
    if availability_pattern == "minimal":
        num_slots = random.randint(2, 4)
    elif availability_pattern == "part_time":
        num_slots = random.randint(4, 7)
    elif availability_pattern == "full_time":
        num_slots = random.randint(7, 12)
    else:  # weekends_only
        weekend_slots = ["Sat AM", "Sat PM", "Sun AM", "Sun PM"]
        num_slots = random.randint(2, 4)
        available_times = sorted(
            random.sample(weekend_slots, num_slots),
            key=TIME_SLOTS.index,
        )
        # Skip the general slot generation
        num_slots = 0

    if num_slots > 0:
        available_times = sorted(
            random.sample(TIME_SLOTS, min(num_slots, len(TIME_SLOTS))),
            key=TIME_SLOTS.index,
        )

    # Tags: bias toward archetype with some randomness
    lifestyle = list(set(random.sample(
        archetype["lifestyle_bias"],
        min(random.randint(1, 3), len(archetype["lifestyle_bias"])),
    )))
    if random.random() < 0.3:
        extra_tag = random.choice([t for t in LIFESTYLE_TAGS if t not in lifestyle])
        lifestyle.append(extra_tag)

    movement = list(set(random.sample(
        archetype["movement_bias"],
        min(random.randint(1, 2), len(archetype["movement_bias"])),
    )))
    if random.random() < 0.25:
        extra_tag = random.choice([t for t in MOVEMENT_TAGS if t not in movement])
        movement.append(extra_tag)

    instruction = list(set(random.sample(
        archetype["instruction_bias"],
        min(random.randint(1, 2), len(archetype["instruction_bias"])),
    )))
    if random.random() < 0.25:
        extra_tag = random.choice([t for t in INSTRUCTION_TAGS if t not in instruction])
        instruction.append(extra_tag)

    bio = random.choice(BIOS)

    # Profile completeness: newer/less experienced coaches tend to have less complete profiles
    if years_exp <= 2:
        completeness = round(random.uniform(0.40, 0.75), 2)
    elif years_exp <= 5:
        completeness = round(random.uniform(0.55, 0.90), 2)
    else:
        completeness = round(random.uniform(0.70, 1.0), 2)

    # Verification: more experienced coaches more likely verified
    verified_at = None
    verify_chance = min(0.3 + (years_exp * 0.03), 0.8)
    if random.random() < verify_chance:
        days_ago = random.randint(1, 365)
        verified_at = datetime.utcnow() - timedelta(days=days_ago)

    now = datetime.utcnow()
    created_days_ago = random.randint(1, 500)
    created_at = now - timedelta(days=created_days_ago)
    last_updated = created_at + timedelta(days=random.randint(0, created_days_ago))

    return {
        "first_name": first,
        "last_name": last,
        "email": f"{first.lower()}.{last.lower().replace(' ', '')}.{index}@{EMAIL_DOMAIN}",
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

    # Use the first brand in the DB
    cur.execute("SELECT id FROM brands LIMIT 1")
    row = cur.fetchone()
    if row:
        brand_id = row[0]
        print(f"Using existing brand_id={brand_id}")
    else:
        cur.execute(
            "INSERT INTO brands (name, slug, created_at, updated_at) VALUES (%s, %s, %s, %s) RETURNING id",
            ("FitHire Demo", "fithire-demo", datetime.utcnow(), datetime.utcnow()),
        )
        brand_id = cur.fetchone()[0]
        print(f"Created brand 'FitHire Demo' with id={brand_id}")
        conn.commit()

    # Generate coaches
    coaches_data = [generate_coach(i) for i in range(1, NUM_COACHES + 1)]
    print(f"Generated {len(coaches_data)} coach profiles. Inserting...")

    inserted = 0
    skipped = 0
    for c in coaches_data:
        try:
            # Check if email already exists
            cur.execute("SELECT id FROM users WHERE email = %s", (c["email"],))
            if cur.fetchone():
                skipped += 1
                continue

            # Create user
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
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"  Error inserting {c['email']}: {e}")
            continue

    # Print summary
    cur.execute("SELECT COUNT(*) FROM coaches")
    total = cur.fetchone()[0]

    print(f"\nDone! Inserted {inserted}/{NUM_COACHES} coaches ({skipped} skipped as duplicates).")
    print(f"Total coaches in DB: {total}")

    # Distribution stats
    print("\n── Archetype distribution (by specialty) ──")
    cur.execute("""
        SELECT s.specialty, COUNT(*)
        FROM coaches, jsonb_array_elements_text(specialties) AS s(specialty)
        GROUP BY s.specialty
        ORDER BY COUNT(*) DESC
        LIMIT 15
    """)
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[1]}")

    cur.execute("SELECT AVG(years_experience), MIN(years_experience), MAX(years_experience) FROM coaches")
    avg, mn, mx = cur.fetchone()
    print(f"\nExperience: avg={avg:.1f} yrs, min={mn}, max={mx}")

    cur.execute("SELECT state, COUNT(*) FROM coaches GROUP BY state ORDER BY COUNT(*) DESC LIMIT 10")
    print("\nTop 10 states:")
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[1]}")

    conn.close()


if __name__ == "__main__":
    print(f"Seeding {NUM_COACHES} additional diverse coach profiles...\n")
    main()
