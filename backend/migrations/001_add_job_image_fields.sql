-- Migration: Add image fields and compensation type to jobs table
-- Created: 2026-01-07
-- Description: Adds brand_logo_url, brand_banner_url, and compensation_type columns to jobs table

-- Add compensation_type column
ALTER TABLE jobs
ADD COLUMN compensation_type VARCHAR(50);

-- Add brand_logo_url column
ALTER TABLE jobs
ADD COLUMN brand_logo_url VARCHAR(500);

-- Add brand_banner_url column
ALTER TABLE jobs
ADD COLUMN brand_banner_url VARCHAR(500);

-- Add comment to document the migration
COMMENT ON COLUMN jobs.compensation_type IS 'Type of compensation: hourly, salary, or per_class';
COMMENT ON COLUMN jobs.brand_logo_url IS 'URL to brand logo image (200x200px recommended)';
COMMENT ON COLUMN jobs.brand_banner_url IS 'URL to brand banner image (1200x400px recommended)';
