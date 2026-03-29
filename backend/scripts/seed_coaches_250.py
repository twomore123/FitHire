"""
Seed script: Add 250 additional diverse coach profiles for demo purposes.

Strategy: Coaches are generated to *realistically match* the 10 seeded jobs.
~60% of coaches are placed in job cities with relevant certs so they pass
the hard gates (location, certs, availability). The remaining ~40% are spread
across other cities to show realistic non-matches and partial matches.

Within matching coaches, quality still varies widely: some are stellar
(high experience, many certs, full availability, great culture fit) and
some are borderline (just meet minimums, few extra certs, patchy availability).

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

# ── Name pools ──────────────────────────────────────────────────────────────
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
    "Moreau", "Russo", "Romano", "Bianchi", "Yamamoto", "Sato", "Watanabe",
    "Fernandez", "Vasquez", "Delgado", "Rios", "Medina", "Vargas",
    "Castillo", "Guerrero", "Romero", "Herrera", "Aguilar", "Soto",
    "Ramos", "Mendez", "Salazar", "Contreras", "Fuentes", "Cardenas",
    "Stone", "Frost", "Rivers", "Banks", "Fields", "Winters", "Cross",
    "Barrett", "Holt", "Kane", "Marsh", "Steele", "Vaughn",
    "Spencer", "Dawson", "Burke", "Chambers", "Dunn", "Reeves", "Thornton",
    "Blackwell", "Whitfield", "Donovan", "Gallagher", "Hampton", "Jennings",
    "Malone", "Norris", "Pittman", "Shelton", "Underwood", "Wilder",
]

# ── All certifications ──────────────────────────────────────────────────────
ALL_CERTS = [
    "NASM-CPT", "ACE-CPT", "ISSA-CPT", "NSCA-CSCS", "ACSM-CPT",
    "ACE-GFI", "AFAA-GFI", "Les Mills Certified", "Zumba Certified",
    "RYT-200", "RYT-500", "Yoga Alliance E-RYT",
    "Pilates Mat", "Pilates Reformer", "BASI Pilates", "Stott Pilates", "NCPT",
    "CrossFit L1", "CrossFit L2", "TRX-STC", "Kettlebell Cert",
    "Spinning Cert", "USAW-L1", "Pre/Postnatal Cert", "Youth Fitness Cert",
    "Senior Fitness Cert", "Corrective Exercise Specialist", "NASM-PES",
    "NASM-CES", "Precision Nutrition L1", "ISSA-SFN", "NASM-FNS",
    "CPR/AED", "First Aid",
]

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
    "Adaptive Fitness", "Calisthenics", "Animal Flow", "Plyometrics",
    "Speed & Agility",
]

TIME_SLOTS = [
    "Mon AM", "Mon PM", "Tue AM", "Tue PM", "Wed AM", "Wed PM",
    "Thu AM", "Thu PM", "Fri AM", "Fri PM", "Sat AM", "Sat PM",
    "Sun AM", "Sun PM",
]

ALL_LIFESTYLE_TAGS = [
    "wellness", "community", "high-energy", "mindfulness", "competitive",
    "holistic", "body-positive", "results-driven", "luxury", "boutique",
    "outdoor-enthusiast", "tech-savvy", "eco-conscious", "family-friendly",
    "fun", "premium",
]
ALL_MOVEMENT_TAGS = [
    "technical-precision", "dynamic-flow", "explosive-power",
    "mind-body-connection", "rhythm-based", "endurance-focused",
    "flexibility-oriented", "functional-movement", "strength-focused",
]
ALL_INSTRUCTION_TAGS = [
    "motivational", "educational", "hands-on", "demo-heavy",
    "voice-led", "music-driven", "data-informed", "intuitive",
    "compassionate", "high-intensity-cueing", "calm-and-grounding",
]

# ── Non-job cities for the ~40% of coaches that won't match on location ─────
OTHER_CITIES = [
    ("San Diego", "CA"), ("San Francisco", "CA"), ("Portland", "OR"),
    ("Seattle", "WA"), ("Atlanta", "GA"), ("Boston", "MA"),
    ("Philadelphia", "PA"), ("Detroit", "MI"), ("Dallas", "TX"),
    ("San Antonio", "TX"), ("Orlando", "FL"), ("Tampa", "FL"),
    ("Phoenix", "AZ"), ("Salt Lake City", "UT"), ("Minneapolis", "MN"),
    ("Raleigh", "NC"), ("Brooklyn", "NY"), ("Washington", "DC"),
    ("Las Vegas", "NV"), ("Honolulu", "HI"), ("Indianapolis", "IN"),
    ("Columbus", "OH"), ("Kansas City", "MO"), ("New Orleans", "LA"),
    ("Pittsburgh", "PA"), ("Boise", "ID"), ("Tucson", "AZ"),
    ("Madison", "WI"), ("Richmond", "VA"), ("Charleston", "SC"),
]

# ──────────────────────────────────────────────────────────────────────────────
# JOB-ALIGNED COACH TEMPLATES
#
# Each template targets a specific seeded job. Coaches generated from these
# templates will ALWAYS have the required certs and be in the right city, but
# vary in experience, extra certs, availability depth, and culture tag overlap.
# ──────────────────────────────────────────────────────────────────────────────

JOB_TEMPLATES = [
    {
        # MADabolic Charlotte — Part-Time Strength & Conditioning
        "city": "Charlotte", "state": "NC",
        "required_certs": ["NASM-CPT", "ACE-CPT"],
        "preferred_certs": ["NSCA-CSCS", "USAW-L1", "Kettlebell Cert"],
        "bonus_certs": ["CrossFit L1", "NASM-PES", "TRX-STC", "CPR/AED", "First Aid"],
        "min_exp": 2,
        "required_avail": ["Mon AM", "Wed AM", "Fri AM", "Sat AM"],
        "culture_tags": ["high-energy", "community", "competitive", "results-driven"],
        "specialty_pool": ["Strength Training", "HIIT", "Functional Training", "Olympic Lifting", "Boot Camp", "Kettlebell Training", "Circuit Training"],
        "lifestyle_pool": ["high-energy", "competitive", "results-driven", "community", "wellness"],
        "movement_pool": ["strength-focused", "explosive-power", "technical-precision", "functional-movement"],
        "instruction_pool": ["motivational", "hands-on", "educational", "high-intensity-cueing"],
        "count": 18,
    },
    {
        # MADabolic Nashville — Full-Time Head Trainer
        "city": "Nashville", "state": "TN",
        "required_certs": ["NASM-CPT"],
        "preferred_certs": ["NSCA-CSCS", "ACE-CPT", "NASM-PES"],
        "bonus_certs": ["CrossFit L1", "Kettlebell Cert", "USAW-L1", "Precision Nutrition L1", "CPR/AED"],
        "min_exp": 4,
        "required_avail": ["Mon AM", "Mon PM", "Tue AM", "Wed AM", "Wed PM", "Thu AM", "Fri AM"],
        "culture_tags": ["high-energy", "community", "competitive", "results-driven"],
        "specialty_pool": ["Strength Training", "Personal Training", "HIIT", "Functional Training", "Boot Camp", "Sports Performance"],
        "lifestyle_pool": ["high-energy", "competitive", "results-driven", "community"],
        "movement_pool": ["strength-focused", "explosive-power", "functional-movement", "technical-precision"],
        "instruction_pool": ["motivational", "hands-on", "educational", "high-intensity-cueing"],
        "count": 15,
    },
    {
        # MADabolic Austin — Weekend Specialist
        "city": "Austin", "state": "TX",
        "required_certs": ["NASM-CPT"],
        "preferred_certs": ["ACE-CPT", "NSCA-CSCS"],
        "bonus_certs": ["CrossFit L1", "Kettlebell Cert", "CPR/AED", "First Aid", "NASM-PES"],
        "min_exp": 1,
        "required_avail": ["Sat AM", "Sat PM", "Sun AM"],
        "culture_tags": ["high-energy", "community", "competitive", "results-driven"],
        "specialty_pool": ["Strength Training", "HIIT", "Functional Training", "Boot Camp", "CrossFit", "Kettlebell Training"],
        "lifestyle_pool": ["high-energy", "community", "competitive", "outdoor-enthusiast", "fun"],
        "movement_pool": ["strength-focused", "explosive-power", "functional-movement"],
        "instruction_pool": ["motivational", "hands-on", "high-intensity-cueing"],
        "count": 18,
    },
    {
        # MADabolic Denver — Evening Strength Coach
        "city": "Denver", "state": "CO",
        "required_certs": ["ACE-CPT"],
        "preferred_certs": ["NASM-CPT", "NSCA-CSCS"],
        "bonus_certs": ["CrossFit L1", "Kettlebell Cert", "USAW-L1", "CPR/AED", "First Aid"],
        "min_exp": 2,
        "required_avail": ["Mon PM", "Tue PM", "Wed PM", "Thu PM"],
        "culture_tags": ["high-energy", "community", "competitive", "results-driven"],
        "specialty_pool": ["Strength Training", "HIIT", "Functional Training", "Olympic Lifting", "Circuit Training", "Boot Camp"],
        "lifestyle_pool": ["high-energy", "competitive", "results-driven", "outdoor-enthusiast", "community"],
        "movement_pool": ["strength-focused", "explosive-power", "functional-movement", "technical-precision"],
        "instruction_pool": ["motivational", "hands-on", "educational", "high-intensity-cueing"],
        "count": 18,
    },
    {
        # Crunch Miami — Group Fitness All Formats
        "city": "Miami", "state": "FL",
        "required_certs": ["ACE-GFI"],
        "preferred_certs": ["NASM-CPT", "AFAA-GFI"],
        "bonus_certs": ["Les Mills Certified", "Zumba Certified", "Spinning Cert", "CPR/AED", "ACE-CPT"],
        "min_exp": 1,
        "required_avail": ["Mon AM", "Tue PM", "Wed AM", "Thu PM", "Sat AM"],
        "culture_tags": ["fun", "high-energy", "community", "body-positive"],
        "specialty_pool": ["Group Fitness", "HIIT", "Dance Fitness", "Cycling", "Boot Camp", "Cardio", "Circuit Training", "Barre"],
        "lifestyle_pool": ["fun", "high-energy", "community", "body-positive", "wellness"],
        "movement_pool": ["rhythm-based", "dynamic-flow", "endurance-focused"],
        "instruction_pool": ["motivational", "music-driven", "voice-led", "high-intensity-cueing"],
        "count": 18,
    },
    {
        # Crunch LA — Personal Trainer
        "city": "Los Angeles", "state": "CA",
        "required_certs": ["NASM-CPT"],
        "preferred_certs": ["ACE-CPT", "NSCA-CSCS", "Precision Nutrition L1"],
        "bonus_certs": ["NASM-PES", "NASM-CES", "TRX-STC", "CPR/AED", "First Aid", "ISSA-SFN"],
        "min_exp": 2,
        "required_avail": ["Mon AM", "Mon PM", "Tue AM", "Wed PM", "Thu AM", "Fri AM"],
        "culture_tags": ["results-driven", "fun", "high-energy", "community"],
        "specialty_pool": ["Personal Training", "Strength Training", "HIIT", "Weight Loss", "Nutrition Coaching", "Functional Training", "Bodybuilding"],
        "lifestyle_pool": ["results-driven", "fun", "high-energy", "community", "wellness", "boutique"],
        "movement_pool": ["strength-focused", "functional-movement", "technical-precision"],
        "instruction_pool": ["motivational", "hands-on", "educational", "data-informed"],
        "count": 18,
    },
    {
        # Crunch NY — Yoga Instructor
        "city": "New York", "state": "NY",
        "required_certs": ["RYT-200"],
        "preferred_certs": ["RYT-500", "NASM-CPT"],
        "bonus_certs": ["Yoga Alliance E-RYT", "ACE-GFI", "Pilates Mat", "CPR/AED", "First Aid", "Meditation Cert"],
        "min_exp": 2,
        "required_avail": ["Mon AM", "Wed AM", "Thu PM", "Sat AM", "Sun AM"],
        "culture_tags": ["wellness", "mindfulness", "community", "holistic"],
        "specialty_pool": ["Yoga", "Meditation", "Breathwork", "Flexibility", "Mobility", "Pilates", "Barre"],
        "lifestyle_pool": ["wellness", "mindfulness", "community", "holistic", "body-positive", "eco-conscious"],
        "movement_pool": ["mind-body-connection", "flexibility-oriented", "dynamic-flow"],
        "instruction_pool": ["calm-and-grounding", "intuitive", "compassionate", "voice-led"],
        "count": 18,
    },
    {
        # Life Time Scottsdale — Certified Personal Trainer
        "city": "Scottsdale", "state": "AZ",
        "required_certs": ["NASM-CPT", "ACE-CPT"],
        "preferred_certs": ["NSCA-CSCS", "Precision Nutrition L1"],
        "bonus_certs": ["NASM-PES", "NASM-CES", "TRX-STC", "ISSA-SFN", "CPR/AED", "First Aid"],
        "min_exp": 3,
        "required_avail": ["Mon AM", "Mon PM", "Tue AM", "Wed AM", "Wed PM", "Thu AM", "Fri AM"],
        "culture_tags": ["premium", "results-driven", "wellness", "community"],
        "specialty_pool": ["Personal Training", "Strength Training", "Weight Loss", "Nutrition Coaching", "Functional Training", "Sports Performance", "HIIT"],
        "lifestyle_pool": ["premium", "results-driven", "wellness", "luxury", "community"],
        "movement_pool": ["strength-focused", "functional-movement", "technical-precision"],
        "instruction_pool": ["educational", "hands-on", "data-informed", "motivational"],
        "count": 15,
    },
    {
        # Life Time Chicago — Pilates Instructor
        "city": "Chicago", "state": "IL",
        "required_certs": ["NCPT"],
        "preferred_certs": ["BASI Pilates", "Pilates Reformer"],
        "bonus_certs": ["Pilates Mat", "Stott Pilates", "ACE-GFI", "Corrective Exercise Specialist", "CPR/AED", "Pre/Postnatal Cert"],
        "min_exp": 3,
        "required_avail": ["Mon AM", "Tue AM", "Tue PM", "Wed AM", "Thu PM", "Fri AM", "Sat AM"],
        "culture_tags": ["wellness", "mindfulness", "premium", "community"],
        "specialty_pool": ["Pilates", "Barre", "Core Training", "Flexibility", "Rehabilitation", "Mobility", "Prenatal Fitness"],
        "lifestyle_pool": ["wellness", "boutique", "premium", "mindfulness", "body-positive"],
        "movement_pool": ["technical-precision", "mind-body-connection", "flexibility-oriented"],
        "instruction_pool": ["educational", "hands-on", "demo-heavy", "compassionate"],
        "count": 15,
    },
    {
        # Life Time Houston — Group Fitness HIIT & Cycle
        "city": "Houston", "state": "TX",
        "required_certs": ["ACE-GFI"],
        "preferred_certs": ["NASM-CPT", "AFAA-GFI", "Spinning Cert"],
        "bonus_certs": ["Les Mills Certified", "ACE-CPT", "Zumba Certified", "CPR/AED", "First Aid"],
        "min_exp": 2,
        "required_avail": ["Mon AM", "Tue PM", "Wed AM", "Thu PM", "Fri AM", "Sat AM"],
        "culture_tags": ["high-energy", "community", "premium", "fun"],
        "specialty_pool": ["Group Fitness", "HIIT", "Cycling", "Cardio", "Circuit Training", "Boot Camp", "Dance Fitness"],
        "lifestyle_pool": ["high-energy", "community", "premium", "fun", "wellness"],
        "movement_pool": ["rhythm-based", "endurance-focused", "dynamic-flow", "explosive-power"],
        "instruction_pool": ["motivational", "music-driven", "voice-led", "high-intensity-cueing"],
        "count": 17,
    },
]

# Remaining coaches go to non-job cities
TARGETED_COUNT = sum(t["count"] for t in JOB_TEMPLATES)  # ~170
RANDOM_COUNT = NUM_COACHES - TARGETED_COUNT  # ~80

# ── Bios ─────────────────────────────────────────────────────────────────────
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
    "Mom of three who found her calling in prenatal and postnatal fitness. I understand the journey firsthand.",
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
    "Boot camp-style trainer who builds teams, not just bodies. Accountability and camaraderie are my superpowers.",
    "Data-driven personal trainer. I use wearables, body composition analysis, and progress tracking to optimize results.",
    "Inclusive fitness advocate. I create spaces where everyone — regardless of size, ability, or background — can thrive.",
    "Former Marine turned fitness professional. Discipline, structure, and mental toughness are core to my coaching philosophy.",
    "HIIT specialist who keeps sessions under 45 minutes — efficient, effective, and intense.",
    "Barre instructor bringing ballet-inspired conditioning to fitness enthusiasts of all backgrounds.",
    "I focus on the mind-muscle connection. Slow, controlled movements build better bodies.",
    "Passionate about creating welcoming, energizing group fitness experiences for every level.",
    "Dedicated to helping clients discover their strength — both physical and mental.",
]


def make_cert_objects(cert_names: list[str]) -> list[dict]:
    """Turn a list of cert name strings into cert objects with metadata."""
    result = []
    for name in cert_names:
        exp_date = datetime.now() + timedelta(days=random.randint(120, 1400))
        result.append({
            "name": name,
            "verified": random.random() < 0.75,
            "expiration": exp_date.strftime("%Y-%m-%d"),
        })
    return result


def generate_targeted_coach(index: int, template: dict) -> dict:
    """Generate a coach that targets a specific job's requirements.

    All coaches get the required certs and are in the right city.
    Quality varies: some are stellar, some borderline.
    """
    is_female = random.random() < 0.55
    first = random.choice(FIRST_NAMES_F if is_female else FIRST_NAMES_M)
    last = random.choice(LAST_NAMES)

    city = template["city"]
    state = template["state"]

    # ── Experience: always meet minimum, but vary how much above ────────────
    min_exp = template["min_exp"]
    # 30% barely meet it, 40% comfortably above, 30% very experienced
    tier = random.choices(["borderline", "solid", "veteran"], weights=[30, 40, 30], k=1)[0]
    if tier == "borderline":
        years_exp = min_exp + random.randint(0, 1)
    elif tier == "solid":
        years_exp = min_exp + random.randint(2, 5)
    else:
        years_exp = min_exp + random.randint(5, 15)

    # ── Certs: always include all required; vary preferred + bonus ──────────
    certs = list(template["required_certs"])  # always have these

    # Add preferred certs with high probability
    for cert in template["preferred_certs"]:
        if random.random() < 0.55:
            certs.append(cert)

    # Add bonus certs depending on tier
    if tier == "borderline":
        bonus_count = random.randint(0, 1)
    elif tier == "solid":
        bonus_count = random.randint(1, 3)
    else:
        bonus_count = random.randint(2, 5)
    available_bonus = [c for c in template["bonus_certs"] if c not in certs]
    certs.extend(random.sample(available_bonus, min(bonus_count, len(available_bonus))))

    # Always add CPR/AED for experienced coaches
    if years_exp >= 3 and "CPR/AED" not in certs:
        certs.append("CPR/AED")

    # Deduplicate
    certs = list(dict.fromkeys(certs))
    cert_objects = make_cert_objects(certs)

    # ── Specialties ─────────────────────────────────────────────────────────
    num_specs = random.randint(3, 6)
    specialties = random.sample(template["specialty_pool"], min(num_specs, len(template["specialty_pool"])))
    # Add 0-2 random extras
    extras = [s for s in SPECIALTIES if s not in specialties]
    specialties.extend(random.sample(extras, min(random.randint(0, 2), len(extras))))

    # ── Availability: always cover required slots; vary extras ──────────────
    required_slots = list(template["required_avail"])
    extra_pool = [s for s in TIME_SLOTS if s not in required_slots]

    if tier == "borderline":
        extra_count = random.randint(0, 2)
    elif tier == "solid":
        extra_count = random.randint(2, 5)
    else:
        extra_count = random.randint(4, len(extra_pool))

    extra_slots = random.sample(extra_pool, min(extra_count, len(extra_pool)))
    available_times = sorted(required_slots + extra_slots, key=TIME_SLOTS.index)

    # ── Culture/style tags: bias toward matching the job's culture ──────────
    # Pick from template pools (which overlap with job culture_tags)
    lifestyle = random.sample(template["lifestyle_pool"], min(random.randint(2, 4), len(template["lifestyle_pool"])))
    movement = random.sample(template["movement_pool"], min(random.randint(1, 3), len(template["movement_pool"])))
    instruction = random.sample(template["instruction_pool"], min(random.randint(1, 3), len(template["instruction_pool"])))

    # Occasionally add a random tag to keep variety
    if random.random() < 0.3:
        extra = random.choice([t for t in ALL_LIFESTYLE_TAGS if t not in lifestyle])
        lifestyle.append(extra)
    if random.random() < 0.2:
        extra = random.choice([t for t in ALL_MOVEMENT_TAGS if t not in movement])
        movement.append(extra)

    bio = random.choice(BIOS)

    # ── Engagement signals ──────────────────────────────────────────────────
    if tier == "borderline":
        completeness = round(random.uniform(0.60, 0.80), 2)
    elif tier == "solid":
        completeness = round(random.uniform(0.78, 0.95), 2)
    else:
        completeness = round(random.uniform(0.90, 1.0), 2)

    verified_at = None
    if tier != "borderline" or random.random() < 0.3:
        verified_at = datetime.utcnow() - timedelta(days=random.randint(1, 200))

    now = datetime.utcnow()
    created_days_ago = random.randint(5, 400)
    created_at = now - timedelta(days=created_days_ago)
    # Recent last_updated boosts engagement score
    if tier == "veteran":
        last_updated = now - timedelta(days=random.randint(0, 15))
    elif tier == "solid":
        last_updated = now - timedelta(days=random.randint(0, 45))
    else:
        last_updated = now - timedelta(days=random.randint(10, 120))

    return {
        "first_name": first,
        "last_name": last,
        "email": f"{first.lower()}.{last.lower().replace(' ', '')}.t{index}@{EMAIL_DOMAIN}",
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


def generate_random_coach(index: int) -> dict:
    """Generate a coach in a non-job city. These won't match on location
    but still have decent profiles for general realism."""
    is_female = random.random() < 0.55
    first = random.choice(FIRST_NAMES_F if is_female else FIRST_NAMES_M)
    last = random.choice(LAST_NAMES)
    city, state = random.choice(OTHER_CITIES)

    years_exp = random.randint(1, 20)

    # Give them a decent spread of certs (3-6)
    num_certs = random.randint(3, 6)
    certs = random.sample(ALL_CERTS, num_certs)
    cert_objects = make_cert_objects(certs)

    num_specs = random.randint(3, 6)
    specialties = random.sample(SPECIALTIES, num_specs)

    # Broad availability
    num_slots = random.randint(6, 12)
    available_times = sorted(random.sample(TIME_SLOTS, num_slots), key=TIME_SLOTS.index)

    lifestyle = random.sample(ALL_LIFESTYLE_TAGS, random.randint(2, 4))
    movement = random.sample(ALL_MOVEMENT_TAGS, random.randint(1, 3))
    instruction = random.sample(ALL_INSTRUCTION_TAGS, random.randint(1, 3))

    bio = random.choice(BIOS)
    completeness = round(random.uniform(0.65, 1.0), 2)

    verified_at = None
    if random.random() < 0.5:
        verified_at = datetime.utcnow() - timedelta(days=random.randint(1, 300))

    now = datetime.utcnow()
    created_days_ago = random.randint(5, 400)
    created_at = now - timedelta(days=created_days_ago)
    last_updated = now - timedelta(days=random.randint(0, 60))

    return {
        "first_name": first,
        "last_name": last,
        "email": f"{first.lower()}.{last.lower().replace(' ', '')}.r{index}@{EMAIL_DOMAIN}",
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
    print("Connecting to database...")
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

    # ── Generate targeted coaches (match specific jobs) ─────────────────────
    coaches_data = []
    idx = 1
    for template in JOB_TEMPLATES:
        for _ in range(template["count"]):
            coaches_data.append(generate_targeted_coach(idx, template))
            idx += 1
        print(f"  Generated {template['count']} coaches for {template['city']}, {template['state']}")

    # ── Generate random coaches (non-matching cities) ───────────────────────
    for i in range(RANDOM_COUNT):
        coaches_data.append(generate_random_coach(idx))
        idx += 1
    print(f"  Generated {RANDOM_COUNT} coaches in non-job cities")

    # Shuffle so insertion order is mixed
    random.shuffle(coaches_data)

    print(f"\nTotal generated: {len(coaches_data)} coach profiles. Inserting...")

    inserted = 0
    skipped = 0
    for c in coaches_data:
        try:
            cur.execute("SELECT id FROM users WHERE email = %s", (c["email"],))
            if cur.fetchone():
                skipped += 1
                continue

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

    # ── Summary ─────────────────────────────────────────────────────────────
    cur.execute("SELECT COUNT(*) FROM coaches")
    total = cur.fetchone()[0]

    print(f"\nDone! Inserted {inserted}/{NUM_COACHES} coaches ({skipped} skipped as duplicates).")
    print(f"Total coaches in DB: {total}")

    cur.execute("SELECT city, state, COUNT(*) FROM coaches GROUP BY city, state ORDER BY COUNT(*) DESC LIMIT 15")
    print("\nTop 15 cities:")
    for row in cur.fetchall():
        print(f"  {row[0]}, {row[1]}: {row[2]}")

    cur.execute("SELECT AVG(years_experience), MIN(years_experience), MAX(years_experience) FROM coaches")
    avg, mn, mx = cur.fetchone()
    print(f"\nExperience: avg={avg:.1f} yrs, min={mn}, max={mx}")

    cur.execute("""
        SELECT c.name, COUNT(*)
        FROM coaches, jsonb_array_elements(certifications) AS c(cert),
             jsonb_extract_path_text(c.cert, 'name') AS c(name)
        GROUP BY c.name
        ORDER BY COUNT(*) DESC
        LIMIT 15
    """)
    print("\nTop 15 certs:")
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[1]}")

    conn.close()


if __name__ == "__main__":
    print(f"Seeding {NUM_COACHES} demo coach profiles (targeted + random)...\n")
    main()
