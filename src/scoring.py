"""
Scoring functions for user story quality.

This module is generated from notebook 04. Do not edit by hand. If you
need to change the scoring logic, update notebook 04 and re-export.

The scoring framework follows:
  - Cohn (Mountain Goat Software) - the classic As a / I want / so that
    template and the INVEST checklist.
  - Lucassen et al. (2016) - the QUS framework, 13 quality criteria.
  - Mordal et al. (2012), Squale model - aggregation principles.
  - Challa et al. (2011) - interpretation bands.

Each score is in the range 0 to 5, higher is better. scope_risk is
inverted internally so that 5 means low risk, in line with the other
dimensions.
"""

from typing import Dict, List, Any
import math


def clamp(value: float, low: float = 0.0, high: float = 5.0) -> float:
    """Bound a score to the [low, high] range."""
    return max(low, min(high, value))


def clarity_score(story: Dict[str, Any]) -> float:
    """Clarity: how unambiguous and well-formed is the story? 0 to 5."""
    score = 5.0
    if story['is_cohn_full_template']:
        pass
    elif story['is_well_formed']:
        score -= 0.5
    elif story['has_as_a'] or story['has_means']:
        score -= 1.5
    else:
        score -= 2.5
    if story['flag_title_too_short']:
        score -= 1.0
    if story['flag_title_too_long']:
        score -= 0.5
    if story['has_vague_words']:
        vague_penalty = min(1.5, 0.5 + 0.25 * (story['vague_word_count'] - 1))
        score -= vague_penalty
    if story['flag_description_markup_only']:
        score -= 2.0
    return clamp(score)


def completeness_score(story: Dict[str, Any]) -> float:
    """Completeness: are all the parts present? 0 to 5."""
    score = 5.0
    if story['flag_description_missing']:
        score -= 2.5
    elif story['flag_description_too_short']:
        score -= 1.0
    if not story['has_acceptance_criteria']:
        score -= 1.5
    if not story['has_as_a']:
        score -= 0.5
    if not story['has_means']:
        score -= 0.5
    if not story['has_so_that']:
        score -= 0.5
    return clamp(score)


def testability_score(story: Dict[str, Any]) -> float:
    """Testability: can QA write a concrete test? 0 to 5."""
    score = 5.0
    if not story['has_acceptance_criteria']:
        score -= 2.0
    if story['has_vague_words']:
        vague_penalty = min(2.0, 0.75 + 0.5 * (story['vague_word_count'] - 1))
        score -= vague_penalty
    if story['flag_description_missing']:
        score -= 1.5
    if story['flag_description_markup_only']:
        score -= 2.0
    if not story['has_means']:
        score -= 0.5
    return clamp(score)


def business_value_score(story: Dict[str, Any]) -> float:
    """Business value: is the reason explicit? 0 to 5."""
    score = 5.0
    if not story['has_so_that']:
        score -= 2.5
    if not story['has_as_a']:
        score -= 1.0
    if not story['has_means']:
        score -= 0.5
    if story['flag_description_missing']:
        score -= 1.5
    if story['has_implementation_hint']:
        score -= 0.5
    return clamp(score)


def scope_risk_score(story: Dict[str, Any]) -> float:
    """Scope risk: is the story small enough? Higher = lower risk. 0 to 5."""
    score = 5.0
    if story['flag_sp_missing']:
        score -= 1.5
    else:
        if story['flag_sp_extreme_scope_risk']:
            score -= 3.0
        elif story['flag_sp_high_scope_risk']:
            score -= 1.5
        if not story['is_fibonacci_sp']:
            score -= 0.5
    if story['has_multi_feature_signal']:
        atomic_penalty = min(2.0, 0.5 + 0.25 * (story['conjunction_count'] - 3))
        score -= atomic_penalty
    return clamp(score)


def overall_quality_score(story: Dict[str, Any]) -> float:
    """Combine the five dimensions into one score using geometric mean."""
    dimensions = [
        clarity_score(story),
        completeness_score(story),
        testability_score(story),
        business_value_score(story),
        scope_risk_score(story),
    ]
    eps = 0.01
    safe_dims = [max(d, eps) for d in dimensions]
    log_mean = sum(math.log(d) for d in safe_dims) / len(safe_dims)
    geo_mean = math.exp(log_mean)
    return clamp(geo_mean)


def issue_tags(story: Dict[str, Any]) -> List[str]:
    """Return a list of issue tag strings that apply to this story."""
    tags = []
    if story.get('flag_description_missing'):
        tags.append('missing_description')
    if story.get('flag_description_markup_only'):
        tags.append('markup_only')
    if not story.get('has_acceptance_criteria'):
        tags.append('missing_acceptance_criteria')
    if not story.get('has_as_a'):
        tags.append('weak_role')
    if not story.get('has_means'):
        tags.append('weak_means')
    if not story.get('has_so_that'):
        tags.append('missing_reason')
    if story.get('has_vague_words'):
        tags.append('has_vague_words')
    if story.get('has_implementation_hint'):
        tags.append('has_implementation_hint')
    if story.get('has_multi_feature_signal'):
        tags.append('non_atomic')
    if story.get('flag_sp_missing'):
        tags.append('missing_estimate')
    else:
        if not story.get('is_fibonacci_sp'):
            tags.append('non_fibonacci_estimate')
        if story.get('flag_sp_extreme_scope_risk'):
            tags.append('extreme_scope_risk')
        elif story.get('flag_sp_high_scope_risk'):
            tags.append('high_scope_risk')
    if story.get('flag_duplicate_in_project'):
        tags.append('duplicate_in_project')
    return tags


def score_band(score: float) -> str:
    """Convert a numeric quality score (0 to 5) to a readable band."""
    if score >= 4.0:
        return 'Very good'
    if score >= 3.0:
        return 'Good'
    if score >= 2.0:
        return 'Average'
    if score >= 1.0:
        return 'Poor'
    return 'Very poor'
