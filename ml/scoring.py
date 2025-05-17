#scoring.py

rating_map = {
    'Excellent': 3, 'Good': 2, 'Poor': 1,
    'High': 3, 'Moderate': 2, 'Low': 1,
    'Yes': 1, 'No': 0,
    'Monthly': 4, 'Quarterly': 3, 'Bi-Yearly': 2, 'Yearly': 1
}

def calculate_compliance_score(application, ratings, application_weights):
    weight_dict = application_weights.get(application, {})
    if not weight_dict:
        raise ValueError(f"Application weights not defined for: {application}")

    max_score = sum(4 * weight for weight in weight_dict.values())
    score = sum(rating_map.get(rating, 0) * weight_dict.get(feature, 0) for feature, rating in ratings.items())
    return (score / max_score) * 100 if max_score else 0
