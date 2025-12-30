"""Unit tests for FitScore calculation engine"""

from datetime import datetime, timedelta
import pytest

from app.core.fitscore.engine import FitScoreEngine, MatchScore
from app.core.fitscore.presets import WEIGHTING_PRESETS, validate_preset, get_preset


class TestWeightingPresets:
    """Test weighting preset validation"""

    def test_all_presets_sum_to_one(self):
        """All presets should have weights that sum to 1.0"""
        for preset_name, weights in WEIGHTING_PRESETS.items():
            total = sum(weights.values())
            assert abs(total - 1.0) < 0.001, f"Preset '{preset_name}' weights sum to {total}"

    def test_validate_preset_valid(self):
        """validate_preset should return True for valid presets"""
        assert validate_preset("balanced") is True
        assert validate_preset("experience_heavy") is True

    def test_validate_preset_invalid(self):
        """validate_preset should return False for invalid presets"""
        assert validate_preset("nonexistent") is False

    def test_get_preset_valid(self):
        """get_preset should return weights for valid preset"""
        weights = get_preset("balanced")
        assert isinstance(weights, dict)
        assert "certifications" in weights

    def test_get_preset_invalid(self):
        """get_preset should raise ValueError for invalid preset"""
        with pytest.raises(ValueError):
            get_preset("invalid_preset_name")


class TestCertificationScoring:
    """Test certification matching logic"""

    def setup_method(self):
        self.engine = FitScoreEngine()

    def test_missing_required_certification(self):
        """Missing required certification should return 0.0"""
        coach = {"certifications": [{"name": "ACE"}]}
        job = {"required_certifications": ["NASM-CPT", "ACE"]}

        score = self.engine._score_certifications(coach, job)
        assert score == 0.0

    def test_all_required_certifications_met(self):
        """Meeting all required certifications should score ≥ 0.7"""
        coach = {"certifications": [{"name": "NASM-CPT"}, {"name": "ACE"}]}
        job = {"required_certifications": ["NASM-CPT", "ACE"]}

        score = self.engine._score_certifications(coach, job)
        assert score >= 0.7

    def test_preferred_certifications_bonus(self):
        """Having preferred certifications should add bonus"""
        coach = {
            "certifications": [{"name": "NASM-CPT"}, {"name": "RYT-200"}]
        }
        job = {
            "required_certifications": ["NASM-CPT"],
            "preferred_certifications": ["RYT-200"],
        }

        score = self.engine._score_certifications(coach, job)
        assert score == 1.0  # 0.7 base + 0.3 bonus for 100% preferred match


class TestExperienceScoring:
    """Test experience matching logic"""

    def setup_method(self):
        self.engine = FitScoreEngine()

    def test_below_minimum_experience(self):
        """Experience below minimum should return 0.0"""
        coach = {"years_experience": 2}
        job = {"min_experience": 5}

        score = self.engine._score_experience(coach, job)
        assert score == 0.0

    def test_exact_minimum_experience(self):
        """Exact minimum experience should score 0.7"""
        coach = {"years_experience": 3}
        job = {"min_experience": 3}

        score = self.engine._score_experience(coach, job)
        assert score == 0.7

    def test_experience_bonus_diminishing_returns(self):
        """Extra experience should add bonus with diminishing returns"""
        coach = {"years_experience": 13}
        job = {"min_experience": 3}

        score = self.engine._score_experience(coach, job)
        # 10 years over = 0.3 bonus, total = 1.0
        assert score == 1.0


class TestAvailabilityScoring:
    """Test availability matching logic"""

    def setup_method(self):
        self.engine = FitScoreEngine()

    def test_missing_required_slots(self):
        """Missing required time slots should return 0.0"""
        coach = {"available_times": ["Mon AM", "Wed PM"]}
        job = {"required_availability": ["Mon AM", "Fri AM", "Sat AM"]}

        score = self.engine._score_availability(coach, job)
        assert score == 0.0

    def test_exact_required_slots(self):
        """Exactly covering required slots should score 0.7"""
        coach = {"available_times": ["Mon AM", "Wed PM", "Fri AM"]}
        job = {"required_availability": ["Mon AM", "Wed PM", "Fri AM"]}

        score = self.engine._score_availability(coach, job)
        assert score == 0.7

    def test_extra_availability_bonus(self):
        """Extra availability should add flexibility bonus"""
        coach = {
            "available_times": [
                "Mon AM",
                "Mon PM",
                "Tue AM",
                "Wed AM",
                "Thu AM",
                "Fri AM",
                "Sat AM",
            ]
        }
        job = {"required_availability": ["Mon AM", "Fri AM"]}

        score = self.engine._score_availability(coach, job)
        # 5 extra slots = 0.15 bonus (5/10 * 0.3), total = 0.85
        assert score == 0.85


class TestLocationScoring:
    """Test location matching logic"""

    def setup_method(self):
        self.engine = FitScoreEngine()

    def test_same_city_and_state(self):
        """Same city and state should return 1.0"""
        coach = {"city": "New York", "state": "NY"}
        job = {"city": "New York", "state": "NY"}

        score = self.engine._score_location(coach, job)
        assert score == 1.0

    def test_different_city(self):
        """Different city should return 0.0"""
        coach = {"city": "Boston", "state": "MA"}
        job = {"city": "New York", "state": "NY"}

        score = self.engine._score_location(coach, job)
        assert score == 0.0

    def test_case_insensitive_city(self):
        """City comparison should be case-insensitive"""
        coach = {"city": "new york", "state": "NY"}
        job = {"city": "New York", "state": "NY"}

        score = self.engine._score_location(coach, job)
        assert score == 1.0


class TestCultureScoring:
    """Test cultural fit matching logic"""

    def setup_method(self):
        self.engine = FitScoreEngine()

    def test_no_culture_requirements(self):
        """No culture requirements should return 1.0"""
        coach = {"lifestyle_tags": ["wellness", "community"]}
        job = {"culture_tags": []}

        score = self.engine._score_culture(coach, job)
        assert score == 1.0

    def test_perfect_culture_match(self):
        """All culture tags matching should return 1.0"""
        coach = {"lifestyle_tags": ["wellness", "community", "high-energy"]}
        job = {"culture_tags": ["wellness", "community"]}

        score = self.engine._score_culture(coach, job)
        assert score == 1.0

    def test_partial_culture_match(self):
        """Partial culture match should return proportional score"""
        coach = {"lifestyle_tags": ["wellness"]}
        job = {"culture_tags": ["wellness", "community", "high-energy"]}

        score = self.engine._score_culture(coach, job)
        assert score == pytest.approx(1 / 3, 0.01)

    def test_no_culture_match(self):
        """No culture match should return 0.0"""
        coach = {"lifestyle_tags": ["technical-precision"]}
        job = {"culture_tags": ["high-energy", "motivational"]}

        score = self.engine._score_culture(coach, job)
        assert score == 0.0


class TestEngagementScoring:
    """Test engagement signal scoring logic"""

    def setup_method(self):
        self.engine = FitScoreEngine()

    def test_minimum_engagement(self):
        """Minimal profile should score 0.5"""
        coach = {
            "profile_completeness": 0.5,
            "last_updated": (datetime.now() - timedelta(days=60)).isoformat(),
            "verified_video_url": None,
        }

        score = self.engine._score_engagement(coach)
        assert score == 0.5

    def test_complete_profile_bonus(self):
        """Complete profile (≥90%) should add 0.2"""
        coach = {"profile_completeness": 0.95}

        score = self.engine._score_engagement(coach)
        assert score >= 0.7  # 0.5 base + 0.2 completeness

    def test_recent_update_bonus(self):
        """Recent update (<30 days) should add 0.2"""
        coach = {"last_updated": (datetime.now() - timedelta(days=15)).isoformat()}

        score = self.engine._score_engagement(coach)
        assert score >= 0.7  # 0.5 base + 0.2 recent

    def test_verified_video_bonus(self):
        """Verified video should add 0.1"""
        coach = {"verified_video_url": "https://example.com/video.mp4"}

        score = self.engine._score_engagement(coach)
        assert score >= 0.6  # 0.5 base + 0.1 video

    def test_maximum_engagement(self):
        """Perfect engagement should score 1.0"""
        coach = {
            "profile_completeness": 1.0,
            "last_updated": datetime.now().isoformat(),
            "verified_video_url": "https://example.com/video.mp4",
        }

        score = self.engine._score_engagement(coach)
        assert score == 1.0


class TestFullMatchScore:
    """Test complete FitScore calculation"""

    def setup_method(self):
        self.engine = FitScoreEngine()

    def test_perfect_match(self):
        """Perfect coach-job match should score close to 1.0"""
        coach = {
            "certifications": [{"name": "NASM-CPT"}, {"name": "ACE"}],
            "years_experience": 15,
            "available_times": ["Mon AM", "Wed PM", "Fri AM", "Sat AM", "Sun AM"],
            "city": "New York",
            "state": "NY",
            "lifestyle_tags": ["wellness", "community", "high-energy"],
            "profile_completeness": 1.0,
            "last_updated": datetime.now().isoformat(),
            "verified_video_url": "https://example.com/video.mp4",
        }

        job = {
            "required_certifications": ["NASM-CPT"],
            "preferred_certifications": ["ACE"],
            "min_experience": 5,
            "required_availability": ["Mon AM", "Fri AM"],
            "city": "New York",
            "state": "NY",
            "culture_tags": ["wellness", "community"],
        }

        result = self.engine.calculate_match(coach, job, preset="balanced")

        assert isinstance(result, MatchScore)
        assert result.fitscore >= 0.95
        assert result.cert_score == 1.0
        assert result.experience_score == 1.0
        assert result.location_score == 1.0

    def test_poor_match(self):
        """Poor coach-job match should score low"""
        coach = {
            "certifications": [{"name": "RYT-200"}],  # Wrong certification
            "years_experience": 1,  # Below minimum
            "available_times": ["Tue PM"],  # Doesn't match required
            "city": "Boston",
            "state": "MA",
            "lifestyle_tags": ["technical-precision"],
        }

        job = {
            "required_certifications": ["NASM-CPT"],
            "min_experience": 5,
            "required_availability": ["Mon AM", "Fri AM"],
            "city": "New York",
            "state": "NY",
            "culture_tags": ["high-energy", "community"],
        }

        result = self.engine.calculate_match(coach, job, preset="balanced")

        assert result.fitscore < 0.2  # Should score very low
        assert result.cert_score == 0.0  # Missing required cert
        assert result.experience_score == 0.0  # Below minimum
        assert result.availability_score == 0.0  # No overlap
        assert result.location_score == 0.0  # Different city

    def test_different_presets_produce_different_scores(self):
        """Different weighting presets should produce different scores"""
        coach = {
            "certifications": [{"name": "NASM-CPT"}],
            "years_experience": 10,
            "available_times": ["Mon AM", "Fri AM"],
            "city": "New York",
            "state": "NY",
            "lifestyle_tags": ["wellness", "community"],
        }

        job = {
            "required_certifications": ["NASM-CPT"],
            "min_experience": 3,
            "required_availability": ["Mon AM"],
            "city": "New York",
            "state": "NY",
            "culture_tags": ["wellness"],
        }

        balanced_score = self.engine.calculate_match(coach, job, preset="balanced")
        exp_heavy_score = self.engine.calculate_match(
            coach, job, preset="experience_heavy"
        )
        culture_heavy_score = self.engine.calculate_match(
            coach, job, preset="culture_heavy"
        )

        # Scores should differ based on preset emphasis
        assert balanced_score.fitscore != exp_heavy_score.fitscore
        assert balanced_score.fitscore != culture_heavy_score.fitscore

    def test_match_score_to_dict(self):
        """MatchScore should convert to dictionary"""
        score = MatchScore(
            fitscore=0.85,
            cert_score=1.0,
            experience_score=0.8,
            availability_score=0.9,
            location_score=1.0,
            culture_score=0.75,
            engagement_score=0.7,
        )

        score_dict = score.to_dict()

        assert isinstance(score_dict, dict)
        assert score_dict["fitscore"] == 0.85
        assert score_dict["cert_score"] == 1.0
