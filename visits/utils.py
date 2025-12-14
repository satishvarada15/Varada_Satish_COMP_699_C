# visits/utils.py
"""
Volunteer suggestion utility (Option B — no distance).

Exports:
    suggest_volunteer(visit) -> VolunteerProfile | None

Behavior:
 - Finds volunteers who declared availability on the visit weekday.
 - Excludes volunteers who reached their service_limit.
 - Scores candidates by:
     * workload (fewer assigned visits => higher score)
     * remaining capacity (more remaining => higher score)
     * risk compatibility (skills give bonus for Medium/High risk)
 - Returns the single best VolunteerProfile or None if no candidate.
"""

from datetime import datetime
from django.db.models import Count
from .models import Availability, Visit
from accounts.models import VolunteerProfile

def _weekday_from_date(d):
    """Return weekday name (e.g., 'Monday') for a date object."""
    return d.strftime('%A')

def _normalize_time_str(t):
    """Return a short time string for comparison like '10:00' from time/time-string."""
    if t is None:
        return ''
    if isinstance(t, str):
        # assume already 'HH:MM' or 'HH:MM:SS'
        return t[:5]
    # assume datetime.time
    return t.strftime('%H:%M')

def suggest_volunteer(visit):
    """
    Suggest the best volunteer for a Visit (no distance).
    Returns: VolunteerProfile instance or None.
    """
    # 1) Determine weekday and time for matching
    weekday = _weekday_from_date(visit.date)
    visit_time_str = _normalize_time_str(visit.time)

    # 2) Find volunteer IDs who have availability for that weekday
    avail_qs = Availability.objects.filter(day__iexact=weekday)
    volunteer_ids = set(avail_qs.values_list('volunteer_id', flat=True))

    if not volunteer_ids:
        return None

    # 3) Load candidate VolunteerProfile objects
    candidates = VolunteerProfile.objects.filter(id__in=volunteer_ids)

    scored_candidates = []

    for v in candidates:
        # 4) Compute current assigned (active) visits count
        # Consider Pending and Scheduled as active load
        active_count = Visit.objects.filter(
            volunteer=v,
            status__in=['Pending', 'Awaiting Approval', 'Scheduled']
        ).count()

        # 5) Skip volunteers at or above their service limit
        service_limit = v.service_limit or 0
        if active_count >= service_limit:
            continue

        # 6) Basic scoring
        score = 0

        # workload: fewer assigned visits => higher score
        score += max(0, 50 - (active_count * 5))

        # remaining capacity bonus
        remaining = service_limit - active_count
        score += remaining * 3

        # risk-level compatibility
        mother_risk = (visit.mother.risk_level or '').lower()
        skills = (v.skills or '').lower()

        # if mother high risk and volunteer has relevant keywords -> boost
        if mother_risk == 'high':
            if any(k in skills for k in ('first aid', 'nurse', 'midwife', 'obgyn')):
                score += 25
            elif 'first aid' in skills:
                score += 12
        elif mother_risk == 'medium':
            if any(k in skills for k in ('first aid', 'midwife', 'nurse')):
                score += 10

        # Optional: match time_slot more precisely if Availability.time_slot used consistently
        # If there's an availability record for this volunteer that includes the visit time_str,
        # give a small bonus.
        vol_avails = avail_qs.filter(volunteer=v)
        time_match = False
        for a in vol_avails:
            ts = (a.time_slot or '').strip().lower()
            if not ts:
                # if volunteer left time_slot empty, treat as available whole day
                time_match = True
                break
            # simple contains match: '10:00' in '9:00-11:00' or '10:00' == '10:00'
            if visit_time_str and (visit_time_str in ts or visit_time_str == ts):
                time_match = True
                break
        if time_match:
            score += 8
        else:
            score -= 5  # small penalty if no precise time match

        # tie-breaker: prefer lower id (stable)
        score += (1000 - (v.id % 100))

        scored_candidates.append((v, score, active_count))

    if not scored_candidates:
        return None

    # 7) Sort by score desc, then active_count asc
    scored_candidates.sort(key=lambda x: (-x[1], x[2]))

    best_volunteer = scored_candidates[0][0]
    return best_volunteer
