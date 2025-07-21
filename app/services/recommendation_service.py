import json
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import random
from app.services.sentiment_service import sentiment_service

logger = logging.getLogger(__name__)

class RecommendationService:
    def __init__(self):
        self.guests_data = self._load_guests_data()
        self.feedback_data = self._load_feedback_data()
        self.recommendations_cache = {}
    
    def _load_guests_data(self) -> List[Dict]:
        """Load guests data from JSON file"""
        try:
            with open('app/data/comprehensive_guests_data.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("Guests data file not found, using empty data")
            return []
    
    def _load_feedback_data(self) -> List[Dict]:
        """Load feedback data from JSON file"""
        try:
            with open('app/data/comprehensive_feedback_data.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("Feedback data file not found, using empty data")
            return []
    
    async def get_personalized_recommendations(self, guest_id: str) -> Dict:
        """Generate personalized recommendations for a guest"""
        try:
            # Find guest data
            guest = self._find_guest(guest_id)
            if not guest:
                return self._get_default_recommendations()
            
            # Analyze guest preferences and feedback
            preferences = await self._analyze_guest_preferences(guest)
            
            # Generate recommendations based on preferences
            recommendations = {
                "guest_id": guest_id,
                "guest_name": f"{guest.get('first_name', '')} {guest.get('last_name', '')}",
                "dining": self._get_dining_recommendations(preferences),
                "amenities": self._get_amenity_recommendations(preferences),
                "activities": self._get_activity_recommendations(preferences),
                "room_services": self._get_room_service_recommendations(preferences),
                "generated_at": datetime.utcnow().isoformat(),
                "personalization_score": preferences.get("personalization_score", 0.5)
            }
            
            # Cache recommendations
            self.recommendations_cache[guest_id] = recommendations
            
            return recommendations
            
        except Exception as e:
            logger.error(f"❌ Error generating recommendations for guest {guest_id}: {e}")
            return self._get_default_recommendations()
    
    def _find_guest(self, guest_id: str) -> Optional[Dict]:
        """Find guest by ID"""
        for guest in self.guests_data:
            if guest.get("guest_id") == guest_id:
                return guest
        return None
    
    async def _analyze_guest_preferences(self, guest: Dict) -> Dict:
        """Advanced analysis of guest preferences, loyalty tier, and feedback sentiment."""
        preferences = {
            "cuisine_preference": guest.get("preferences", {}).get("cuisine", "international"),
            "activity_level": guest.get("preferences", {}).get("activity_level", "moderate"),
            "budget_tier": guest.get("loyalty_tier", "standard").lower(),
            "previous_ratings": [],
            "sentiment_history": [],
            "personalization_score": 0.5,
            "loyalty_tier": guest.get("loyalty_tier", "standard").lower(),
            "recent_sentiment": "neutral"
        }

        guest_feedback = [f for f in self.feedback_data if f.get("guest_id") == guest.get("guest_id")]
        feedback_history = guest_feedback[-5:] if guest_feedback else []

        if feedback_history:
            positive_count = 0
            negative_count = 0
            for feedback in feedback_history:
                sentiment_result = await sentiment_service.analyze_sentiment(feedback.get("feedback_text", ""))
                preferences["sentiment_history"].append(sentiment_result)
                preferences["previous_ratings"].append(feedback.get("rating", 3))
                if sentiment_result["sentiment"] == "positive":
                    positive_count += 1
                elif sentiment_result["sentiment"] == "negative":
                    negative_count += 1

            # Recent sentiment (last feedback)
            if preferences["sentiment_history"]:
                preferences["recent_sentiment"] = preferences["sentiment_history"][-1]["sentiment"]

            avg_rating = sum(preferences["previous_ratings"]) / len(preferences["previous_ratings"])
            avg_sentiment = positive_count / len(feedback_history)
            # Boost score for Gold tier, reduce for negative feedback
            tier_boost = 0.15 if preferences["loyalty_tier"] == "gold" else 0
            sentiment_boost = -0.15 if preferences["recent_sentiment"] == "negative" else 0.05 if preferences["recent_sentiment"] == "positive" else 0
            preferences["personalization_score"] = min(1.0, max(0.0, (avg_rating / 5.0 + avg_sentiment) / 2 + tier_boost + sentiment_boost))

        return preferences
    
    def _get_dining_recommendations(self, preferences: Dict) -> List[Dict]:
        """Generate dining recommendations with loyalty and preference enhancements"""
        all_dining = [
            {
                "name": "Skyline Rooftop Restaurant",
                "cuisine": "international",
                "price_tier": "premium",
                "rating": 4.8,
                "description": "Exquisite fine dining with panoramic city views",
                "image": "/static/images/dining/skyline.jpg",
                "specialties": ["Wagyu Beef", "Fresh Seafood", "Craft Cocktails"],
                "upgrade_offer": "Gold guests get complimentary dessert!" if preferences.get("loyalty_tier") == "gold" else None
            },
            {
                "name": "Garden Bistro",
                "cuisine": "mediterranean",
                "price_tier": "standard",
                "rating": 4.5,
                "description": "Fresh Mediterranean cuisine in a garden setting",
                "image": "/static/images/dining/garden.jpg",
                "specialties": ["Fresh Salads", "Grilled Fish", "Organic Vegetables"]
            },
            {
                "name": "Spice Route",
                "cuisine": "asian",
                "price_tier": "standard",
                "rating": 4.6,
                "description": "Authentic Asian flavors with modern presentation",
                "image": "/static/images/dining/spice.jpg",
                "specialties": ["Dim Sum", "Curry Dishes", "Sushi"]
            },
            {
                "name": "Local Harvest",
                "cuisine": "local",
                "price_tier": "budget",
                "rating": 4.3,
                "description": "Farm-to-table local cuisine with seasonal ingredients",
                "image": "/static/images/dining/harvest.jpg",
                "specialties": ["Seasonal Menu", "Local Ingredients", "Comfort Food"]
            }
        ]

        # Prioritize cuisine preference
        preferred = [r for r in all_dining if r["cuisine"] == preferences.get("cuisine_preference")]
        others = [r for r in all_dining if r["cuisine"] != preferences.get("cuisine_preference")]
        scored_dining = []
        for restaurant in preferred + others:
            score = self._calculate_dining_score(restaurant, preferences)
            # Boost for Gold guests
            if preferences.get("loyalty_tier") == "gold":
                score += 0.1
            restaurant["recommendation_score"] = score
            scored_dining.append(restaurant)

        # If recent feedback is negative, add a suggestion for improvement
        if preferences.get("recent_sentiment") == "negative":
            scored_dining.append({
                "name": "Chef's Special Comfort Meal",
                "cuisine": "international",
                "price_tier": "standard",
                "rating": 4.7,
                "description": "A personalized comfort meal to improve your stay experience.",
                "image": "/static/images/dining/comfort.jpg",
                "specialties": ["Custom Comfort Food"],
                "recommendation_score": 1.0
            })

        scored_dining.sort(key=lambda x: x["recommendation_score"], reverse=True)
        return scored_dining[:3]
    
    def _get_amenity_recommendations(self, preferences: Dict) -> List[Dict]:
        """Generate amenity recommendations"""
        all_amenities = [
            {
                "name": "Luxury Spa & Wellness Center",
                "category": "wellness",
                "price_tier": "premium",
                "rating": 4.9,
                "description": "Full-service spa with massage, facials, and wellness treatments",
                "image": "/static/images/amenities/spa.jpg",
                "services": ["Hot Stone Massage", "Aromatherapy", "Yoga Classes"]
            },
            {
                "name": "Fitness Center & Pool",
                "category": "fitness",
                "price_tier": "standard",
                "rating": 4.4,
                "description": "State-of-the-art gym with Olympic-size pool",
                "image": "/static/images/amenities/fitness.jpg",
                "services": ["24/7 Gym Access", "Personal Training", "Swimming Pool"]
            },
            {
                "name": "Business Center",
                "category": "business",
                "price_tier": "standard",
                "rating": 4.2,
                "description": "Fully equipped business center with meeting rooms",
                "image": "/static/images/amenities/business.jpg",
                "services": ["Meeting Rooms", "High-Speed Internet", "Printing Services"]
            },
            {
                "name": "Kids Club",
                "category": "family",
                "price_tier": "budget",
                "rating": 4.6,
                "description": "Supervised activities and entertainment for children",
                "image": "/static/images/amenities/kids.jpg",
                "services": ["Supervised Play", "Arts & Crafts", "Movie Nights"]
            }
        ]
        
        # Filter and score based on preferences
        scored_amenities = []
        for amenity in all_amenities:
            score = self._calculate_amenity_score(amenity, preferences)
            amenity["recommendation_score"] = score
            scored_amenities.append(amenity)
        
        # Sort by score and return top 3
        scored_amenities.sort(key=lambda x: x["recommendation_score"], reverse=True)
        return scored_amenities[:3]
    
    def _get_activity_recommendations(self, preferences: Dict) -> List[Dict]:
        """Generate activity recommendations"""
        all_activities = [
            {
                "name": "City Walking Tour",
                "category": "cultural",
                "activity_level": "moderate",
                "price_tier": "budget",
                "duration": "3 hours",
                "rating": 4.7,
                "description": "Guided tour of historic city landmarks and hidden gems",
                "image": "/static/images/activities/walking.jpg"
            },
            {
                "name": "Adventure Sports Package",
                "category": "adventure",
                "activity_level": "high",
                "price_tier": "premium",
                "duration": "Full day",
                "rating": 4.8,
                "description": "Thrilling outdoor activities including zip-lining and rock climbing",
                "image": "/static/images/activities/adventure.jpg"
            },
            {
                "name": "Cooking Class Experience",
                "category": "culinary",
                "activity_level": "low",
                "price_tier": "standard",
                "duration": "4 hours",
                "rating": 4.5,
                "description": "Learn to cook local dishes with professional chefs",
                "image": "/static/images/activities/cooking.jpg"
            },
            {
                "name": "Wine Tasting Tour",
                "category": "leisure",
                "activity_level": "low",
                "price_tier": "premium",
                "duration": "5 hours",
                "rating": 4.6,
                "description": "Visit local wineries and taste premium wines",
                "image": "/static/images/activities/wine.jpg"
            }
        ]
        
        # Filter and score based on preferences
        scored_activities = []
        for activity in all_activities:
            score = self._calculate_activity_score(activity, preferences)
            activity["recommendation_score"] = score
            scored_activities.append(activity)
        
        # Sort by score and return top 3
        scored_activities.sort(key=lambda x: x["recommendation_score"], reverse=True)
        return scored_activities[:3]
    
    def _get_room_service_recommendations(self, preferences: Dict) -> List[Dict]:
        """Generate room service recommendations"""
        services = [
            {
                "name": "24/7 Concierge Service",
                "category": "concierge",
                "description": "Personal assistance with reservations, tickets, and local information",
                "available": "24/7"
            },
            {
                "name": "In-Room Dining",
                "category": "dining",
                "description": "Gourmet meals delivered to your room",
                "available": "6:00 AM - 11:00 PM"
            },
            {
                "name": "Laundry & Dry Cleaning",
                "category": "housekeeping",
                "description": "Professional laundry and dry cleaning services",
                "available": "8:00 AM - 6:00 PM"
            }
        ]
        return services
    
    def _calculate_dining_score(self, restaurant: Dict, preferences: Dict) -> float:
        """Calculate recommendation score for dining"""
        score = restaurant["rating"] / 5.0  # Base score from rating
        
        # Adjust based on cuisine preference
        if restaurant["cuisine"] == preferences.get("cuisine_preference", "international"):
            score += 0.3
        
        # Adjust based on budget tier
        if restaurant["price_tier"] == preferences.get("budget_tier", "standard"):
            score += 0.2
        
        # Adjust based on personalization score
        score *= (0.5 + preferences.get("personalization_score", 0.5))
        
        return min(1.0, score)
    
    def _calculate_amenity_score(self, amenity: Dict, preferences: Dict) -> float:
        """Calculate recommendation score for amenities"""
        score = amenity["rating"] / 5.0
        
        # Adjust based on budget tier
        if amenity["price_tier"] == preferences.get("budget_tier", "standard"):
            score += 0.2
        
        # Adjust based on personalization score
        score *= (0.5 + preferences.get("personalization_score", 0.5))
        
        return min(1.0, score)
    
    def _calculate_activity_score(self, activity: Dict, preferences: Dict) -> float:
        """Calculate recommendation score for activities"""
        score = activity["rating"] / 5.0
        
        # Adjust based on activity level preference
        if activity["activity_level"] == preferences.get("activity_level", "moderate"):
            score += 0.3
        
        # Adjust based on budget tier
        if activity["price_tier"] == preferences.get("budget_tier", "standard"):
            score += 0.2
        
        # Adjust based on personalization score
        score *= (0.5 + preferences.get("personalization_score", 0.5))
        
        return min(1.0, score)
    
    def _get_default_recommendations(self) -> Dict:
        """Return default recommendations when guest data is not available"""
        return {
            "guest_id": "unknown",
            "guest_name": "Valued Guest",
            "dining": [
                {
                    "name": "Garden Bistro",
                    "cuisine": "international",
                    "rating": 4.5,
                    "description": "Fresh international cuisine in a garden setting",
                    "image": "/static/images/dining/garden.jpg"
                }
            ],
            "amenities": [
                {
                    "name": "Fitness Center & Pool",
                    "category": "fitness",
                    "rating": 4.4,
                    "description": "State-of-the-art gym with Olympic-size pool",
                    "image": "/static/images/amenities/fitness.jpg"
                }
            ],
            "activities": [
                {
                    "name": "City Walking Tour",
                    "category": "cultural",
                    "rating": 4.7,
                    "description": "Guided tour of historic city landmarks",
                    "image": "/static/images/activities/walking.jpg"
                }
            ],
            "room_services": [
                {
                    "name": "24/7 Concierge Service",
                    "category": "concierge",
                    "description": "Personal assistance with reservations and local information"
                }
            ],
            "generated_at": datetime.utcnow().isoformat(),
            "personalization_score": 0.5
        }

# Global instance
recommendation_service = RecommendationService()
