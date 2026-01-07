# Database Migrations

This directory contains SQL migration scripts for the FitHire database.

## How to Apply Migrations

### Option 1: Using Neon Console (Recommended)

1. Go to [Neon Console](https://console.neon.tech/)
2. Select your FitHire project
3. Click on **SQL Editor** in the left sidebar
4. Copy the contents of `APPLY_MIGRATIONS.sql`
5. Paste into the SQL Editor
6. Click **Run** to execute the migration
7. Verify the migration was successful (you should see "Success" message)

### Option 2: Using psql Command Line

```bash
# Connect to your Neon database
psql "postgresql://[user]:[password]@[host]/[database]?sslmode=require"

# Run the migration file
\i /path/to/APPLY_MIGRATIONS.sql

# Verify columns were added
\d jobs
\d coaches
```

### Option 3: Using Railway CLI

If you have Railway CLI installed:

```bash
# Connect to database
railway connect postgres

# Then paste the SQL from APPLY_MIGRATIONS.sql
```

## Migration History

| File | Date | Description |
|------|------|-------------|
| 001_add_job_image_fields.sql | 2026-01-07 | Add compensation_type, brand_logo_url, brand_banner_url to jobs table |
| 002_add_coach_profile_image.sql | 2026-01-07 | Add profile_image_url to coaches table |

## Verifying Migrations

After running migrations, verify they were applied:

```sql
-- Check jobs table columns
SELECT column_name, data_type, character_maximum_length
FROM information_schema.columns
WHERE table_name = 'jobs'
AND column_name IN ('compensation_type', 'brand_logo_url', 'brand_banner_url');

-- Check coaches table columns
SELECT column_name, data_type, character_maximum_length
FROM information_schema.columns
WHERE table_name = 'coaches'
AND column_name = 'profile_image_url';
```

Expected output:
```
Jobs table should have:
- compensation_type (varchar, 50)
- brand_logo_url (varchar, 500)
- brand_banner_url (varchar, 500)

Coaches table should have:
- profile_image_url (varchar, 500)
```

## Rollback (if needed)

If you need to rollback these migrations:

```sql
BEGIN;

ALTER TABLE jobs DROP COLUMN IF EXISTS compensation_type;
ALTER TABLE jobs DROP COLUMN IF EXISTS brand_logo_url;
ALTER TABLE jobs DROP COLUMN IF EXISTS brand_banner_url;

ALTER TABLE coaches DROP COLUMN IF EXISTS profile_image_url;

COMMIT;
```

**Note:** Only rollback if absolutely necessary. This will delete all existing image URLs from the database.

## Important Notes

- ✅ These migrations use `IF NOT EXISTS` to prevent errors if run multiple times
- ✅ All migrations are wrapped in transactions (BEGIN/COMMIT)
- ✅ Safe to run on production database
- ⚠️ Backup your database before running migrations (Neon has automatic backups)
- ⚠️ The compensation_type column is nullable (existing jobs won't have this data)
- ⚠️ Image URL columns are nullable (existing profiles/jobs won't have images)
