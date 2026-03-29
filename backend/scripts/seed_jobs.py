"""
Seed script: Create 10 official job listings from partnered brands.

Brands: MADabolic, Crunch Fitness, Life Time

Usage:
    cd backend
    pip install psycopg2-binary
    python scripts/seed_jobs.py

Requires DATABASE_URL env var or uses the hardcoded default below.
"""

import json
import os
from datetime import datetime

import psycopg2

# ── Config ───────────────────────────────────────────────────────────────────
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://neondb_owner:npg_5iQSl1JqIsTK@ep-orange-hall-afkktrid-pooler.c-2.us-west-2.aws.neon.tech/neondb?sslmode=require",
)

OWNER_EMAIL = "reidsmendoza12@gmail.com"

# Logo paths served from the frontend public directory
BRANDS = [
    {"name": "MADabolic", "slug": "madabolic", "logo": "/logos/madabolic.jpeg"},
    {"name": "Crunch Fitness", "slug": "crunch-fitness", "logo": "/logos/crunch.jpeg"},
    {"name": "Life Time", "slug": "life-time", "logo": "/logos/lifetime.jpeg"},
]

# ── Job listings (10 total) ──────────────────────────────────────────────────
JOB_LISTINGS = [
    # --- MADabolic (4 listings) ---
    {
        "brand_slug": "madabolic",
        "title": "Part-Time Strength & Conditioning Trainer",
        "role_type": "Group Fitness Instructor",
        "city": "Charlotte",
        "state": "NC",
        "location_name": "MADabolic Charlotte - South End",
        "region_name": "Southeast",
        "description": (
            "MADabolic is the industry's top strength & conditioning franchise. "
            "No fads or gimmicks — we execute what works.\n\n"
            "As a MADabolic trainer, you provide 1:1 movement corrections on the floor. "
            "No mics, no high-fives — just world-class coaching. You aim to be the best "
            "part of your client's day by greeting them in the lobby, taking a genuine "
            "interest in their lives, and delivering a world-class experience.\n\n"
            "Responsibilities:\n"
            "• Coach 2-4 classes per week\n"
            "• Prepare for class by studying key points of performance\n"
            "• Deliver professional class instructions, demos, warmups, and 1:1 movement cues\n"
            "• Maintain a clean, organized training floor\n"
            "• Train at MAD 2-4x/week — practice what you preach"
        ),
        "required_certifications": ["NASM-CPT", "ACE-CPT"],
        "preferred_certifications": ["StrongFirst Kettlebell Level 1", "USA Weightlifting"],
        "min_experience": 2,
        "required_availability": ["Mon AM", "Wed AM", "Fri AM", "Sat AM"],
        "culture_tags": ["high-energy", "discipline", "strength-focused", "community"],
        "compensation_type": "per_class",
        "compensation_min": 30,
        "compensation_max": 50,
        "weighting_preset": "experience_heavy",
        "fitscore_threshold": 0.55,
    },
    {
        "brand_slug": "madabolic",
        "title": "Full-Time Head Trainer",
        "role_type": "Personal Trainer",
        "city": "Nashville",
        "state": "TN",
        "location_name": "MADabolic Nashville - The Gulch",
        "region_name": "Southeast",
        "description": (
            "We're looking for a Head Trainer to lead our Nashville location. "
            "You'll set the standard for coaching excellence on the floor, mentor "
            "junior trainers, and help shape the member experience.\n\n"
            "This role goes beyond coaching classes — you'll be a culture carrier "
            "for the MADabolic brand and a key leader in our studio.\n\n"
            "Responsibilities:\n"
            "• Coach 15-20 classes per week\n"
            "• Mentor and develop part-time trainers\n"
            "• Lead new member onboarding sessions\n"
            "• Collaborate with studio manager on programming and events\n"
            "• Maintain equipment and training floor standards"
        ),
        "required_certifications": ["NASM-CPT"],
        "preferred_certifications": ["CSCS", "StrongFirst Kettlebell Level 1"],
        "min_experience": 4,
        "required_availability": ["Mon AM", "Mon PM", "Tue AM", "Wed AM", "Wed PM", "Thu AM", "Fri AM"],
        "culture_tags": ["leadership", "high-energy", "discipline", "mentorship"],
        "compensation_type": "salary",
        "compensation_min": 45000,
        "compensation_max": 60000,
        "weighting_preset": "experience_heavy",
        "fitscore_threshold": 0.65,
    },
    {
        "brand_slug": "madabolic",
        "title": "Part-Time Trainer — Weekend Specialist",
        "role_type": "Group Fitness Instructor",
        "city": "Austin",
        "state": "TX",
        "location_name": "MADabolic Austin - South Lamar",
        "region_name": "South Central",
        "description": (
            "Join the MADabolic Austin team as a Weekend Specialist. Our Saturday "
            "and Sunday classes are the highest-energy sessions of the week, and we "
            "need a trainer who can match that intensity.\n\n"
            "You'll coach weekend warrior members through structured strength & "
            "conditioning workouts with an emphasis on movement quality.\n\n"
            "Responsibilities:\n"
            "• Coach 4-6 weekend classes (Saturday & Sunday)\n"
            "• Deliver 1:1 movement corrections throughout class\n"
            "• Build strong relationships with the weekend member community\n"
            "• Attend monthly team training sessions"
        ),
        "required_certifications": ["NASM-CPT"],
        "preferred_certifications": ["ACE-CPT", "BioForce Conditioning"],
        "min_experience": 1,
        "required_availability": ["Sat AM", "Sat PM", "Sun AM"],
        "culture_tags": ["high-energy", "community", "weekend-warrior", "strength-focused"],
        "compensation_type": "per_class",
        "compensation_min": 25,
        "compensation_max": 40,
        "weighting_preset": "availability_focused",
        "fitscore_threshold": 0.50,
    },
    {
        "brand_slug": "madabolic",
        "title": "Strength Coach — Evening Classes",
        "role_type": "Group Fitness Instructor",
        "city": "Denver",
        "state": "CO",
        "location_name": "MADabolic Denver - RiNo",
        "region_name": "Mountain West",
        "description": (
            "MADabolic Denver is growing and we need an evening Strength Coach to "
            "cover our 5:30 PM and 6:30 PM time slots. These are our most popular "
            "classes with a loyal after-work crowd.\n\n"
            "If you bring energy, precision coaching, and a passion for strength "
            "training, we want to hear from you.\n\n"
            "Responsibilities:\n"
            "• Coach 3-4 evening classes per week\n"
            "• Provide detailed movement corrections and scaling options\n"
            "• Create a motivating yet focused training environment\n"
            "• Participate in quarterly programming reviews"
        ),
        "required_certifications": ["ACE-CPT"],
        "preferred_certifications": ["NASM-CPT", "CSCS"],
        "min_experience": 2,
        "required_availability": ["Mon PM", "Tue PM", "Wed PM", "Thu PM"],
        "culture_tags": ["high-energy", "discipline", "evening-crew", "strength-focused"],
        "compensation_type": "per_class",
        "compensation_min": 30,
        "compensation_max": 45,
        "weighting_preset": "balanced",
        "fitscore_threshold": 0.55,
    },
    # --- Crunch Fitness (3 listings) ---
    {
        "brand_slug": "crunch-fitness",
        "title": "Group Fitness Instructor — All Formats",
        "role_type": "Group Fitness Instructor",
        "city": "Miami",
        "state": "FL",
        "location_name": "Crunch Fitness Miami - Brickell",
        "region_name": "Florida",
        "description": (
            "Crunch Fitness believes in making serious fitness fun! We're hiring "
            "a Group Fitness Instructor for our Brickell location who can teach "
            "across multiple formats — HIIT, strength, dance cardio, and more.\n\n"
            "We want instructors who bring personality to the stage, connect with "
            "members, and keep classes packed.\n\n"
            "Responsibilities:\n"
            "• Teach 5-8 group fitness classes per week across multiple formats\n"
            "• Create engaging playlists and class programming\n"
            "• Build a loyal following through exceptional member experience\n"
            "• Participate in club events and member challenges\n"
            "• Maintain certifications and attend continuing education"
        ),
        "required_certifications": ["ACE-GFI"],
        "preferred_certifications": ["NASM-CPT", "AFAA"],
        "min_experience": 1,
        "required_availability": ["Mon AM", "Tue PM", "Wed AM", "Thu PM", "Sat AM"],
        "culture_tags": ["fun", "high-energy", "inclusive", "community"],
        "compensation_type": "per_class",
        "compensation_min": 25,
        "compensation_max": 45,
        "weighting_preset": "culture_heavy",
        "fitscore_threshold": 0.50,
    },
    {
        "brand_slug": "crunch-fitness",
        "title": "Personal Trainer — Build Your Book",
        "role_type": "Personal Trainer",
        "city": "Los Angeles",
        "state": "CA",
        "location_name": "Crunch Fitness Los Angeles - Hollywood",
        "region_name": "Southern California",
        "description": (
            "Join Crunch Hollywood as a Personal Trainer and build your client base "
            "in one of LA's most vibrant fitness communities. We provide the leads, "
            "the facility, and the brand — you bring the expertise.\n\n"
            "Ideal for trainers who are entrepreneurial, client-focused, and ready "
            "to grow their career.\n\n"
            "Responsibilities:\n"
            "• Conduct initial fitness assessments for new members\n"
            "• Design and deliver personalized training programs\n"
            "• Maintain a minimum of 20 sessions per week\n"
            "• Participate in floor hours to generate new client leads\n"
            "• Track client progress and adjust programs accordingly"
        ),
        "required_certifications": ["NASM-CPT"],
        "preferred_certifications": ["ACE-CPT", "CSCS", "Precision Nutrition Level 1"],
        "min_experience": 2,
        "required_availability": ["Mon AM", "Mon PM", "Tue AM", "Wed PM", "Thu AM", "Fri AM"],
        "culture_tags": ["client-focused", "entrepreneurial", "results-driven", "fun"],
        "compensation_type": "hourly",
        "compensation_min": 20,
        "compensation_max": 40,
        "weighting_preset": "balanced",
        "fitscore_threshold": 0.55,
    },
    {
        "brand_slug": "crunch-fitness",
        "title": "Yoga Instructor — Vinyasa & Power Flow",
        "role_type": "Yoga Instructor",
        "city": "New York",
        "state": "NY",
        "location_name": "Crunch Fitness New York - Union Square",
        "region_name": "Northeast",
        "description": (
            "Crunch Union Square is looking for a Yoga Instructor to lead our "
            "Vinyasa and Power Flow classes. We want someone who can make yoga "
            "accessible to all fitness levels while keeping it challenging.\n\n"
            "Our yoga program is growing fast — this is a chance to build something "
            "special in a high-traffic NYC location.\n\n"
            "Responsibilities:\n"
            "• Teach 4-6 yoga classes per week (Vinyasa, Power Flow)\n"
            "• Offer modifications for beginners and advanced practitioners\n"
            "• Create a welcoming, inclusive class atmosphere\n"
            "• Collaborate with the group fitness team on scheduling\n"
            "• Maintain RYT certification and attend workshops"
        ),
        "required_certifications": ["RYT-200"],
        "preferred_certifications": ["RYT-500", "NASM-CPT"],
        "min_experience": 2,
        "required_availability": ["Mon AM", "Wed AM", "Thu PM", "Sat AM", "Sun AM"],
        "culture_tags": ["wellness", "inclusive", "mindfulness", "community"],
        "compensation_type": "per_class",
        "compensation_min": 35,
        "compensation_max": 60,
        "weighting_preset": "culture_heavy",
        "fitscore_threshold": 0.50,
    },
    # --- Life Time (3 listings) ---
    {
        "brand_slug": "life-time",
        "title": "Certified Personal Trainer",
        "role_type": "Personal Trainer",
        "city": "Scottsdale",
        "state": "AZ",
        "location_name": "Life Time Scottsdale",
        "region_name": "Arizona",
        "description": (
            "Life Time is more than a gym — it's a luxury athletic resort. We're "
            "seeking a Certified Personal Trainer for our Scottsdale location who "
            "embodies our commitment to healthy living.\n\n"
            "You'll work with motivated members in a world-class facility with "
            "top-of-the-line equipment and resources.\n\n"
            "Responsibilities:\n"
            "• Deliver personalized 1-on-1 and small group training sessions\n"
            "• Conduct comprehensive fitness assessments\n"
            "• Develop progressive training programs based on member goals\n"
            "• Maintain a professional appearance and uphold Life Time standards\n"
            "• Attend team meetings and continuing education opportunities"
        ),
        "required_certifications": ["NASM-CPT", "ACE-CPT"],
        "preferred_certifications": ["CSCS", "Precision Nutrition Level 1"],
        "min_experience": 3,
        "required_availability": ["Mon AM", "Mon PM", "Tue AM", "Wed AM", "Wed PM", "Thu AM", "Fri AM"],
        "culture_tags": ["premium", "results-driven", "wellness", "professional"],
        "compensation_type": "hourly",
        "compensation_min": 25,
        "compensation_max": 55,
        "weighting_preset": "experience_heavy",
        "fitscore_threshold": 0.60,
    },
    {
        "brand_slug": "life-time",
        "title": "Pilates Instructor — Reformer & Mat",
        "role_type": "Pilates Instructor",
        "city": "Chicago",
        "state": "IL",
        "location_name": "Life Time Chicago - Lincoln Park",
        "region_name": "Midwest",
        "description": (
            "Life Time Lincoln Park is expanding our Pilates program and seeking "
            "an experienced instructor for both Reformer and Mat classes. Our "
            "state-of-the-art Pilates studio is a member favorite.\n\n"
            "We're looking for someone with deep knowledge of Pilates methodology "
            "who can serve clients from rehab to athletic performance.\n\n"
            "Responsibilities:\n"
            "• Teach 6-10 Reformer and Mat Pilates classes per week\n"
            "• Offer private and semi-private Pilates sessions\n"
            "• Assess member movement patterns and recommend appropriate class levels\n"
            "• Maintain studio equipment and cleanliness standards\n"
            "• Contribute to program development and special workshops"
        ),
        "required_certifications": ["NCPT"],
        "preferred_certifications": ["PMA-CPT", "BASI Pilates"],
        "min_experience": 3,
        "required_availability": ["Mon AM", "Tue AM", "Tue PM", "Wed AM", "Thu PM", "Fri AM", "Sat AM"],
        "culture_tags": ["wellness", "precision", "premium", "mindfulness"],
        "compensation_type": "hourly",
        "compensation_min": 30,
        "compensation_max": 60,
        "weighting_preset": "experience_heavy",
        "fitscore_threshold": 0.60,
    },
    {
        "brand_slug": "life-time",
        "title": "Group Fitness Instructor — HIIT & Cycle",
        "role_type": "Group Fitness Instructor",
        "city": "Houston",
        "state": "TX",
        "location_name": "Life Time Houston - Town & Country",
        "region_name": "Texas",
        "description": (
            "Life Time Houston is hiring a high-energy Group Fitness Instructor "
            "to lead our HIIT and indoor cycling classes. If you can command a room "
            "and leave members feeling accomplished, we want you on our team.\n\n"
            "This is a great opportunity to teach at a premium facility with a "
            "dedicated member base.\n\n"
            "Responsibilities:\n"
            "• Teach 6-8 group fitness classes per week (HIIT, Cycle)\n"
            "• Design progressive class programming within Life Time formats\n"
            "• Motivate and connect with members before, during, and after class\n"
            "• Maintain certifications and complete Life Time training requirements\n"
            "• Support club events, challenges, and community initiatives"
        ),
        "required_certifications": ["ACE-GFI"],
        "preferred_certifications": ["NASM-CPT", "Schwinn Cycling", "AFAA"],
        "min_experience": 2,
        "required_availability": ["Mon AM", "Tue PM", "Wed AM", "Thu PM", "Fri AM", "Sat AM"],
        "culture_tags": ["high-energy", "community", "premium", "fun"],
        "compensation_type": "per_class",
        "compensation_min": 30,
        "compensation_max": 55,
        "weighting_preset": "culture_heavy",
        "fitscore_threshold": 0.55,
    },
]


def seed_jobs():
    """Seed 10 official job listings from partnered brands."""
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    try:
        # 1. Find the owner user by email
        cur.execute("SELECT id, brand_id FROM users WHERE email = %s", (OWNER_EMAIL,))
        user_row = cur.fetchone()
        if not user_row:
            print(f"User {OWNER_EMAIL} not found. Creating user record...")
            # Look for any existing brand to assign, or we'll create one
            cur.execute("SELECT id FROM brands LIMIT 1")
            brand_row = cur.fetchone()
            brand_id = brand_row[0] if brand_row else None

            cur.execute(
                """INSERT INTO users (clerk_user_id, brand_id, email, first_name, last_name, role, created_at, updated_at)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id""",
                (
                    f"clerk_{OWNER_EMAIL}",
                    brand_id,
                    OWNER_EMAIL,
                    "Reid",
                    "Mendoza",
                    "brand_admin",
                    datetime.utcnow(),
                    datetime.utcnow(),
                ),
            )
            user_id = cur.fetchone()[0]
            conn.commit()
            print(f"   Created user: {OWNER_EMAIL} (id={user_id})")
        else:
            user_id = user_row[0]
            print(f"   Found user: {OWNER_EMAIL} (id={user_id})")

        # 2. Create brands (or find existing)
        brand_map = {}  # slug -> {id, logo}
        for brand_def in BRANDS:
            cur.execute("SELECT id FROM brands WHERE slug = %s", (brand_def["slug"],))
            row = cur.fetchone()
            if row:
                brand_map[brand_def["slug"]] = {"id": row[0], "logo": brand_def["logo"]}
                print(f"   Brand exists: {brand_def['name']} (id={row[0]})")
            else:
                cur.execute(
                    "INSERT INTO brands (name, slug, created_at, updated_at) VALUES (%s, %s, %s, %s) RETURNING id",
                    (brand_def["name"], brand_def["slug"], datetime.utcnow(), datetime.utcnow()),
                )
                brand_id = cur.fetchone()[0]
                brand_map[brand_def["slug"]] = {"id": brand_id, "logo": brand_def["logo"]}
                conn.commit()
                print(f"   Created brand: {brand_def['name']} (id={brand_id})")

        # 3. Create regions, locations, and jobs
        jobs_created = 0
        for job_def in JOB_LISTINGS:
            brand_info = brand_map[job_def["brand_slug"]]
            brand_id = brand_info["id"]
            logo_url = brand_info["logo"]

            # Check if this exact job already exists
            cur.execute(
                "SELECT id FROM jobs WHERE title = %s AND city = %s AND brand_id = %s",
                (job_def["title"], job_def["city"], brand_id),
            )
            if cur.fetchone():
                print(f"   Job already exists: {job_def['title']} in {job_def['city']} — skipping")
                continue

            # Find or create region
            cur.execute(
                "SELECT id FROM regions WHERE brand_id = %s AND name = %s",
                (brand_id, job_def["region_name"]),
            )
            region_row = cur.fetchone()
            if region_row:
                region_id = region_row[0]
            else:
                slug = job_def["region_name"].lower().replace(" ", "-")
                cur.execute(
                    "INSERT INTO regions (brand_id, name, slug, created_at) VALUES (%s, %s, %s, %s) RETURNING id",
                    (brand_id, job_def["region_name"], slug, datetime.utcnow()),
                )
                region_id = cur.fetchone()[0]

            # Find or create location
            cur.execute(
                "SELECT id FROM locations WHERE brand_id = %s AND name = %s",
                (brand_id, job_def["location_name"]),
            )
            location_row = cur.fetchone()
            if location_row:
                location_id = location_row[0]
            else:
                cur.execute(
                    "INSERT INTO locations (region_id, brand_id, name, city, state, created_at) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                    (region_id, brand_id, job_def["location_name"], job_def["city"], job_def["state"], datetime.utcnow()),
                )
                location_id = cur.fetchone()[0]

            # Create job
            cur.execute(
                """INSERT INTO jobs (
                    brand_id, location_id, created_by, title, role_type, description,
                    required_certifications, preferred_certifications, min_experience,
                    required_availability, city, state, culture_tags,
                    weighting_preset, fitscore_threshold,
                    compensation_type, compensation_min, compensation_max,
                    brand_logo_url, is_active, created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s,
                    %s, %s, %s,
                    %s, %s, %s, %s
                ) RETURNING id""",
                (
                    brand_id,
                    location_id,
                    user_id,
                    job_def["title"],
                    job_def["role_type"],
                    job_def["description"],
                    json.dumps(job_def["required_certifications"]),
                    json.dumps(job_def.get("preferred_certifications", [])),
                    job_def["min_experience"],
                    json.dumps(job_def["required_availability"]),
                    job_def["city"],
                    job_def["state"],
                    json.dumps(job_def.get("culture_tags", [])),
                    job_def["weighting_preset"],
                    job_def["fitscore_threshold"],
                    job_def.get("compensation_type"),
                    job_def.get("compensation_min"),
                    job_def.get("compensation_max"),
                    logo_url,
                    True,
                    datetime.utcnow(),
                    datetime.utcnow(),
                ),
            )
            job_id = cur.fetchone()[0]
            jobs_created += 1
            print(f"   Created job #{job_id}: {job_def['title']} — {job_def['city']}, {job_def['state']}")

        # 4. Fix any existing jobs with old absolute logo URLs
        cur.execute(
            "UPDATE jobs SET brand_logo_url = REPLACE(brand_logo_url, 'https://fithire.vercel.app', '') "
            "WHERE brand_logo_url LIKE 'https://fithire.vercel.app%'"
        )
        fixed = cur.rowcount
        if fixed:
            print(f"   Fixed {fixed} existing job(s) with old absolute logo URLs")

        conn.commit()
        print(f"\nDone! Created {jobs_created} job listings.")

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        raise
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    print("Seeding 10 official job listings from partnered brands...\n")
    seed_jobs()
