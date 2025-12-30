"""FitScore calculation engine

Deterministic scoring algorithm that ranks coach-job matches based on:
1. Certifications (required + preferred)
2. Experience (years, with diminishing returns)
3. Availability (time slot overlap)
4. Location (city match)
5. Cultural fit (tag overlap)
6. Engagement (profile quality and recency)
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass

from app.core.fitscore.presets import get_preset


@dataclass
class MatchScore:
    """
    Complete FitScore breakdown for a coach-job match
    """

    fitscore: float  # Overall score (0.0 to 1.0)
    cert_score: float
    experience_score: float
    availability_score: float
    location_score: float
    culture_score: float
    engagement_score: float

    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary for API responses"""
        return {
            "fitscore": self.fitscore,
            "cert_score": self.cert_score,
            "experience_score": self.experience_score,
            "availability_score": self.availability_score,
            "location_score": self.location_score,
            "culture_score": self.culture_score,
            "engagement_score": self.engagement_score,
        }


class FitScoreEngine:
    """
    Calculates FitScore for coach-job matches using deterministic algorithms
    """

    def calculate_match(
        self, coach_data: Dict, job_data: Dict, preset: str = "balanced"
    ) -> MatchScore:
        """
        Calculate complete FitScore for a coach-job pair

        Args:
            coach_data: Coach profile data
            job_data: Job listing data
            preset: Weighting preset name

        Returns:
            MatchScore: Complete score breakdown
        """
        # Get weighting values for this preset
        weights = get_preset(preset)

        # Calculate all sub-scores
        cert_score = self._score_certifications(coach_data, job_data)
        exp_score = self._score_experience(coach_data, job_data)
        avail_score = self._score_availability(coach_data, job_data)
        loc_score = self._score_location(coach_data, job_data)
        culture_score = self._score_culture(coach_data, job_data)
        engage_score = self._score_engagement(coach_data)

        # Calculate weighted final score
        fitscore = (
            weights["certifications"] * cert_score
            + weights["experience"] * exp_score
            + weights["availability"] * avail_score
            + weights["location"] * loc_score
            + weights["cultural_fit"] * culture_score
            + weights["engagement"] * engage_score
        )

        return MatchScore(
            fitscore=round(fitscore, 3),
            cert_score=round(cert_score, 3),
            experience_score=round(exp_score, 3),
            availability_score=round(avail_score, 3),
            location_score=round(loc_score, 3),
            culture_score=round(culture_score, 3),
            engagement_score=round(engage_score, 3),
        )

    def _score_certifications(self, coach_data: Dict, job_data: Dict) -> float:
        """
        Score certification match (0.0 to 1.0)

        Logic:
        - Must have ALL required certifications (else return 0.0)
        - Base score: 0.7 for meeting requirements
        - Bonus: Up to 0.3 for having preferred certifications

        Args:
            coach_data: Dict with 'certifications' list
            job_data: Dict with 'required_certifications' and 'preferred_certifications'

        Returns:
            float: Score from 0.0 to 1.0
        """
        # Extract certification names from coach data
        coach_certs = set()
        for cert in coach_data.get("certifications", []):
            if isinstance(cert, dict):
                coach_certs.add(cert.get("name", ""))
            else:
                coach_certs.add(str(cert))

        # Get required and preferred certifications from job
        required = set(job_data.get("required_certifications", []))
        preferred = set(job_data.get("preferred_certifications", []))

        # Must have all required certifications
        if not required.issubset(coach_certs):
            return 0.0

        # Base score for meeting requirements
        base_score = 0.7

        # Bonus for preferred certifications
        if preferred:
            preferred_match_count = len(coach_certs & preferred)
            preferred_bonus = (preferred_match_count / len(preferred)) * 0.3
        else:
            preferred_bonus = 0.0

        return base_score + preferred_bonus

    def _score_experience(self, coach_data: Dict, job_data: Dict) -> float:
        """
        Score experience match (0.0 to 1.0)

        Logic:
        - Must meet minimum experience requirement (else return 0.0)
        - Base score: 0.7 for meeting minimum
        - Bonus: Up to 0.3 for years beyond minimum (diminishing returns)

        Args:
            coach_data: Dict with 'years_experience'
            job_data: Dict with 'min_experience'

        Returns:
            float: Score from 0.0 to 1.0
        """
        coach_years = coach_data.get("years_experience", 0)
        min_years = job_data.get("min_experience", 0)

        # Must meet minimum experience
        if coach_years < min_years:
            return 0.0

        # Base score for meeting minimum
        base_score = 0.7

        # Bonus for additional experience (diminishing returns)
        years_over = coach_years - min_years
        # Max bonus of 0.3 for 10+ years over minimum
        bonus = min(years_over / 10.0, 0.3)

        return base_score + bonus

    def _score_availability(self, coach_data: Dict, job_data: Dict) -> float:
        """
        Score availability overlap (0.0 to 1.0)

        Logic:
        - Must cover ALL required time slots (else return 0.0)
        - Base score: 0.7 for covering all required slots
        - Bonus: Up to 0.3 for additional flexibility

        Args:
            coach_data: Dict with 'available_times' list
            job_data: Dict with 'required_availability' list

        Returns:
            float: Score from 0.0 to 1.0
        """
        coach_slots = set(coach_data.get("available_times", []))
        required_slots = set(job_data.get("required_availability", []))

        # Must cover all required slots
        if not required_slots.issubset(coach_slots):
            return 0.0

        # Base score for covering requirements
        base_score = 0.7

        # Bonus for additional availability (flexibility)
        extra_slots = len(coach_slots - required_slots)
        # Max bonus of 0.3 for 10+ extra slots
        flexibility_bonus = min(extra_slots / 10.0, 1.0) * 0.3

        return base_score + flexibility_bonus

    def _score_location(self, coach_data: Dict, job_data: Dict) -> float:
        """
        Score location match (0.0 to 1.0)

        Phase 1 Logic: Simple city match
        - Same city = 1.0
        - Different city = 0.0

        Phase 2+: Add distance-based scoring with graduated tiers

        Args:
            coach_data: Dict with 'city' and 'state'
            job_data: Dict with 'city' and 'state'

        Returns:
            float: Score from 0.0 to 1.0
        """
        coach_city = coach_data.get("city", "").strip().lower()
        coach_state = coach_data.get("state", "").strip().upper()
        job_city = job_data.get("city", "").strip().lower()
        job_state = job_data.get("state", "").strip().upper()

        # Exact city and state match
        if coach_city == job_city and coach_state == job_state:
            return 1.0

        return 0.0

    def _score_culture(self, coach_data: Dict, job_data: Dict) -> float:
        """
        Score cultural alignment (0.0 to 1.0)

        Logic:
        - Compare coach lifestyle/style tags with job culture tags
        - Score = (number of matching tags) / (number of job tags)
        - If no job culture requirements, return 1.0 (perfect match)

        Args:
            coach_data: Dict with 'lifestyle_tags', 'movement_tags', 'instruction_tags'
            job_data: Dict with 'culture_tags'

        Returns:
            float: Score from 0.0 to 1.0
        """
        # Combine all coach tags
        coach_tags = set()
        coach_tags.update(coach_data.get("lifestyle_tags", []))
        coach_tags.update(coach_data.get("movement_tags", []))
        coach_tags.update(coach_data.get("instruction_tags", []))

        # Get job culture tags
        job_tags = set(job_data.get("culture_tags", []))

        # If no culture requirements, perfect match
        if not job_tags:
            return 1.0

        # Calculate overlap percentage
        overlap = coach_tags & job_tags
        score = len(overlap) / len(job_tags)

        return score

    def _score_engagement(self, coach_data: Dict) -> float:
        """
        Score engagement signals (0.0 to 1.0)

        Logic:
        - Base score: 0.5
        - Profile completeness ≥90%: +0.2
        - Updated in last 30 days: +0.2
        - Has verified video: +0.1
        - Maximum: 1.0

        Args:
            coach_data: Dict with 'profile_completeness', 'last_updated', 'verified_video_url'

        Returns:
            float: Score from 0.0 to 1.0
        """
        score = 0.5

        # Profile completeness bonus
        completeness = coach_data.get("profile_completeness", 0.0)
        if completeness >= 0.9:
            score += 0.2

        # Recent activity bonus
        last_updated = coach_data.get("last_updated")
        if last_updated:
            if isinstance(last_updated, str):
                # Parse ISO format datetime string
                try:
                    last_updated = datetime.fromisoformat(
                        last_updated.replace("Z", "+00:00")
                    )
                except (ValueError, AttributeError):
                    last_updated = None

            if last_updated and isinstance(last_updated, datetime):
                days_since_update = (datetime.now() - last_updated.replace(tzinfo=None)).days
                if days_since_update <= 30:
                    score += 0.2

        # Verified video bonus
        if coach_data.get("verified_video_url"):
            score += 0.1

        return min(score, 1.0)
