# FitHire v1 MVP Definition

**Purpose:** Define the smallest functional system delivering value for coaches and hiring managers.

---

## Core V1 Functionality
1. Coach → Job matching
   - Single role type
   - Deterministic FitScore
   - Threshold applied
   - Top N results displayed
   - Explanation snippet visible
2. Job → Coach ranking
   - Mirror logic
   - Threshold and top N enforced

---

## Included
- Coach profile (certifications, experience, availability, location)
- Job listing (requirements, schedule, culture, location)
- Admin-assigned tags for movement, style, lifestyle
- Engagement signals (manual verification only)
- Multi-level access (Brand / Regional / Location / National)

---

## Excluded (V1)
- Automated hiring recommendations
- Predictive performance or retention
- Automated social media ingestion or analysis
- Unlimited match lists
- ML-based or dynamic scoring

---

## Success Criteria
- FitScore logic deterministic and explainable
- Top matches align with explicit criteria
- Users can filter and view results effectively
- Logs captured for future evaluation

---

## First Milestone (Day 1–7)
- FitScore engine implemented as pure function
- Unit tests for scoring logic
- Single role, single preset
- Coach and Job entities created
- API + minimal React UI to display top matches
- Threshold enforced
