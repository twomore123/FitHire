# FitHire v1 Scope Clarifications

**Purpose:** Remove ambiguity and define functional limits before development.

---

## 1. Social Media & External Content
- **V1 Decision:** Manual / Declared Only
  - Coaches provide links; admins optionally verify
  - No automated scraping or NLP/ML
- **Movement / Lifestyle / Style:** manually categorized as tags
- **FitScore Contribution:** additive factor separate from core scoring
- **Compliance:** only user-consented public content

---

## 2. Cultural Fit & Weighting
- Weighting **required** for each job listing
- **Preset options**: e.g., “Experience-heavy”, “Culture-heavy”
- **Visibility:** partially visible (high-level explanation only)
- **Validation:** sum to 100%, UI warnings for invalid configs

---

## 3. Engagement Signals
- Moderate influence on FitScore
- Can reduce score if data decays
- Only user-submitted/admin-verified
- Decay over time for certifications, profile updates, uploaded videos

---

## 4. Multi-Unit Access
- **V1:** Full multi-level hierarchical access implemented
- Roles: Brand Admin, Regional Director, Location Manager, National Scout
- Scoped queries enforced per hierarchy
- Advanced analytics deferred to future releases

---

## 5. Score Thresholds & Visibility
- Threshold **role-specific** and **adjustable by hiring managers**
- Coaches cannot see the threshold number
- Only above-threshold matches displayed

---

## 6. Role-Specific Scoring Logic
- Certain roles may have **customized scoring logic**
- All other roles use standard FitScore

---

## 7. Version-1 Exclusions
- No automated hiring decisions
- No predictive performance or retention modeling
- No continuous external data ingestion
- No automated interpretation of unstructured media
- Limited result sets

---

## 8. Decision Lock
- Together with the questionnaire, defines **v1 functional scope**
- Anything outside this requires explicit review
