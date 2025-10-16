"""
Non-Tourism Question Handler for Rwanda Tourism QA
Filters out questions not related to Rwanda tourism
"""

from typing import Tuple


class NonTourismQuestionHandler:
    """Handle questions not related to Rwanda tourism"""

    def __init__(self):
        self.tourism_keywords = {
            'national_parks': [
                'park', 'gorilla', 'chimpanzee', 'wildlife', 'safari',
                'akagera', 'volcanoes', 'nyungwe', 'gishwati', 'mukura',
                'trekking', 'hiking', 'animals', 'birds', 'mountain', 'forest'
            ],
            'cultural_heritage': [
                'museum', 'culture', 'dance', 'traditional', 'heritage',
                'palace', 'history', 'intore', 'art', 'monument',
                'ethnographic', 'genocide', 'memorial', 'royal'
            ],
            'general_tourism': [
                'rwanda', 'visit', 'tourism', 'travel', 'tourist',
                'attraction', 'destination', 'kigali', 'vacation',
                'trip', 'holiday', 'guide', 'tour'
            ]
        }

    def is_tourism_related(self, question: str) -> Tuple[bool, str]:
        """Check if question is tourism-related"""
        question_lower = question.lower()

        # Check each category
        for category, keywords in self.tourism_keywords.items():
            if any(keyword in question_lower for keyword in keywords):
                return True, category

        return False, "non_tourism"

    def get_fallback_response(self, question: str) -> str:
        """Generate fallback response for non-tourism questions"""
        return (
            "🌍 I'm specifically designed to help with Rwanda tourism questions! "
            "I can assist you with:\n\n"
            "🦍 **National Parks**: Volcanoes, Akagera, Nyungwe, Gishwati-Mukura\n"
            "🏛️ **Cultural Heritage**: Museums, traditional dances, monuments\n"
            "🎯 **Tourism Planning**: Best times to visit, permits, activities\n\n"
            "Please ask me about Rwanda's amazing tourism attractions!"
        )