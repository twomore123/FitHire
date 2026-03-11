-- Combined Migration Script
-- Run this on your Neon database to add image upload features
-- Date: 2026-01-07

BEGIN;

-- ========================================
-- Migration 001: Add image fields to jobs
-- ========================================

-- Add compensation_type column
ALTER TABLE jobs
ADD COLUMN IF NOT EXISTS compensation_type VARCHAR(50);

-- Add brand_logo_url column
ALTER TABLE jobs
ADD COLUMN IF NOT EXISTS brand_logo_url VARCHAR(500);

-- Add brand_banner_url column
ALTER TABLE jobs
ADD COLUMN IF NOT EXISTS brand_banner_url VARCHAR(500);

-- Add comments
COMMENT ON COLUMN jobs.compensation_type IS 'Type of compensation: hourly, salary, or per_class';
COMMENT ON COLUMN jobs.brand_logo_url IS 'URL to brand logo image (200x200px recommended)';
COMMENT ON COLUMN jobs.brand_banner_url IS 'URL to brand banner image (1200x400px recommended)';


-- ========================================
-- Migration 002: Add profile image to coaches
-- ========================================

-- Add profile_image_url column
ALTER TABLE coaches
ADD COLUMN IF NOT EXISTS profile_image_url VARCHAR(500);

-- Add comment
COMMENT ON COLUMN coaches.profile_image_url IS 'URL to coach profile picture (square format recommended)';

COMMIT;
