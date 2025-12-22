# FitScore v1 Behavior Specification (Non-Technical)

**Purpose:** Define deterministic system behavior for v1 matching and scoring engine.

---

## 1. Product Overview
**Function:** Matches coaches with relevant job opportunities and ranks by FitScore (alignment).

**Main Task:** 
- Coaches: find roles that fit their profile
- Clubs: find candidates aligned with requirements and culture

---

## 2. Users & Roles
- **Primary:** Coaches, Hiring Managers
- **Optional / Secondary:** Platform Admins
- **Notes:** Multi-unit organizations require hierarchical access (regional, national)

---

## 3. Data Inputs
**Coach Profile:**
- Certifications, experience, specialties, availability, location
- Verified credentials, social links
- Engagement signals (applications, profile views, achievements)

**Job Listing:**
- Role requirements, schedule, responsibilities, culture indicators
- Location and compensation

**Input Method:**
- Users fill structured forms
- Admins verify critical fields
- No external scraping

---

## 4. Core System Actions
- Compare coach profiles to job listings
- Calculate FitScore
- Rank results by FitScore
- Track engagement and outcome signals

**Trigger Points:**
- Profile updates
- Job listing updates
- Login to view matches

---

## 5. Matching Logic
- “Good match” = alignment across:
  - Certifications, experience, specialties
  - Availability and location
  - Cultural values and work style
  - Engagement signals

- One coach → many jobs
- One job → many coaches

---

## 6. Score Generation
**FitScore:**
- Relative score within role context
- Factors: certifications, experience, specialties, availability, culture, engagement
- Updates when data changes

---

## 7. Querying & Results
**Exploration:**
- Sort by FitScore
- Filter by location, availability, experience, specialty, cultural fit

**Display per Result:**
- Name
- FitScore
- Key criteria / explanation snippet

---

## 8. Rules, Limits, Simplifications
- Only top 10–20 matches shown
- Incomplete profiles do not score
- FitScore role-specific
- Users cannot artificially influence score beyond truthful updates
- No predictive hiring or automatic decisions

---

## 9. Functional Success Criteria
- Top-ranked matches align with explicit criteria
- Scores meaningfully differentiate candidates
- Users can filter/sort and retrieve relevant results
- Updates correctly recalc scores

---

## 10. Open Questions
- Weighting of criteria
- Handling partial matches
- Engagement influence thresholds
- Role-specific scoring nuances

---

## Addendum A — Data & Scoring Clarification
- Unequal input importance: certifications/experience/availability > secondary fields
- Missing required data reduces/prevents score
- Users can only influence score via truthful profile updates
- Only matches above FitScore threshold shown

---

## Addendum B — Worked Example
1. Coach submits profile
2. System compares against jobs
3. Each job receives FitScore
4. Results sorted high → low
5. Coach sees top 10–20 with explanations

---

## Addendum C — Internal Notes (Technical)
- Entities: Coach, JobListing, EngagementSignals
- Matching: 1→many (coach→jobs), 1→many (job→coaches)
- Score triggers: profile/job update, engagement update, login
- Score stable and context-specific
- Queries: top N, filterable by criteria
