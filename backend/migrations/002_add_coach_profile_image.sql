-- Migration: Add profile_image_url to coaches table
-- Created: 2026-01-07
-- Description: Adds profile_image_url column to coaches table for profile pictures

-- Add profile_image_url column
ALTER TABLE coaches
ADD COLUMN profile_image_url VARCHAR(500);

-- Add comment to document the migration
COMMENT ON COLUMN coaches.profile_image_url IS 'URL to coach profile picture (square format recommended)';
