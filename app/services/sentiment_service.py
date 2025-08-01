import asyncio
import logging
from typing import Dict, List, Optional
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
import requests
import json
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class SentimentAnalysisService:
    def __init__(self):
        self.model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        self.sentiment_analyzer = None
        self.slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the sentiment analysis model"""
        try:
            logger.info("🤖 Initializing DistilBERT sentiment analysis model...")
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model=self.model_name,
                tokenizer=self.model_name,
                return_all_scores=True
            )
            logger.info("✅ Sentiment analysis model initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize sentiment model: {e}")
            # Fallback to a simpler approach if model loading fails
            self.sentiment_analyzer = None
    
    async def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment of given text"""
        try:
            if not self.sentiment_analyzer:
                # Fallback sentiment analysis
                return self._fallback_sentiment_analysis(text)
            
            # Use DistilBERT for sentiment analysis
            results = self.sentiment_analyzer(text)
            
            # Extract scores
            sentiment_scores = {}
            for result in results[0]:
                sentiment_scores[result['label'].lower()] = result['score']
            
            # Determine primary sentiment
            primary_sentiment = max(sentiment_scores, key=sentiment_scores.get)
            confidence = sentiment_scores[primary_sentiment]
            
            analysis_result = {
                "text": text,
                "sentiment": primary_sentiment,
                "confidence": confidence,
                "scores": sentiment_scores,
                "timestamp": datetime.utcnow().isoformat(),
                "is_negative": primary_sentiment == "negative" and confidence > 0.7
            }
            
            # Trigger alert for negative sentiment
            if analysis_result["is_negative"]:
                await self._send_slack_alert(analysis_result)
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"❌ Sentiment analysis failed: {e}")
            return {
                "text": text,
                "sentiment": "neutral",
                "confidence": 0.5,
                "scores": {"positive": 0.5, "negative": 0.5},
                "timestamp": datetime.utcnow().isoformat(),
                "is_negative": False,
                "error": str(e)
            }
    
    def _fallback_sentiment_analysis(self, text: str) -> Dict:
        """Simple fallback sentiment analysis using keyword matching"""
        positive_keywords = [
            "excellent", "amazing", "wonderful", "great", "fantastic", "love", "perfect",
            "outstanding", "exceptional", "brilliant", "superb", "awesome", "incredible"
        ]
        negative_keywords = [
            "terrible", "awful", "horrible", "hate", "worst", "disappointing", "bad",
            "poor", "unacceptable", "disgusting", "rude", "slow", "dirty", "broken"
        ]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_keywords if word in text_lower)
        negative_count = sum(1 for word in negative_keywords if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = "positive"
            confidence = min(0.9, 0.6 + (positive_count * 0.1))
        elif negative_count > positive_count:
            sentiment = "negative"
            confidence = min(0.9, 0.6 + (negative_count * 0.1))
        else:
            sentiment = "neutral"
            confidence = 0.5
        
        return {
            "text": text,
            "sentiment": sentiment,
            "confidence": confidence,
            "scores": {
                "positive": confidence if sentiment == "positive" else 1 - confidence,
                "negative": confidence if sentiment == "negative" else 1 - confidence
            },
            "timestamp": datetime.utcnow().isoformat(),
            "is_negative": sentiment == "negative" and confidence > 0.7
        }
    
    async def _send_slack_alert(self, analysis_result: Dict):
        """Send alert to Slack when negative sentiment is detected"""
        if not self.slack_webhook_url:
            logger.warning("⚠️ Slack webhook URL not configured")
            return
        
        try:
            message = {
                "text": "🚨 Negative Guest Feedback Alert",
                "attachments": [
                    {
                        "color": "danger",
                        "fields": [
                            {
                                "title": "Feedback Text",
                                "value": analysis_result["text"][:200] + "..." if len(analysis_result["text"]) > 200 else analysis_result["text"],
                                "short": False
                            },
                            {
                                "title": "Sentiment",
                                "value": f"{analysis_result['sentiment'].upper()} ({analysis_result['confidence']:.2%})",
                                "short": True
                            },
                            {
                                "title": "Timestamp",
                                "value": analysis_result["timestamp"],
                                "short": True
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(
                self.slack_webhook_url,
                json=message,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("✅ Slack alert sent successfully")
            else:
                logger.error(f"❌ Failed to send Slack alert: {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Error sending Slack alert: {e}")
    
    async def analyze_batch(self, texts: List[str]) -> List[Dict]:
        """Analyze sentiment for multiple texts"""
        results = []
        for text in texts:
            result = await self.analyze_sentiment(text)
            results.append(result)
        return results

# Global instance
sentiment_service = SentimentAnalysisService()
