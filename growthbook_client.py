import os
from growthbook import GrowthBook
from dotenv import load_dotenv
import logging
from datetime import datetime
import json

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_growthbook(user_id):
    """
    Create a new GrowthBook instance for a user.
    """
    # User attributes for targeting and experimentation
    attributes = {
        "id": user_id,
        "loggedIn": True
    }

    # Create GrowthBook instance
    gb = GrowthBook(
        attributes=attributes,
        api_host=os.getenv('GROWTHBOOK_API_HOST', 'http://localhost:3100'),
        client_key=os.getenv('GROWTHBOOK_CLIENT_KEY', 'sdk-abc123')
    )

    # Load features from the GrowthBook API
    try:
        gb.load_features()
    except Exception as e:
        logger.error(f"Error loading features: {str(e)}")

    return gb

def get_variations(gb):
    """
    Get feature flag variations using the GrowthBook instance.
    """
    try:
        variations = {
            'ui_color': gb.get_feature_value('ui_color', 'light'),
            'item_link_behavior': gb.get_feature_value('item_link_behavior', 'same_tab')
        }
        return variations
    except Exception as e:
        logger.error(f"Error getting variations: {str(e)}")
        return {
            'ui_color': 'light',
            'item_link_behavior': 'same_tab'
        }

def log_event(gb, event_name, properties=None):
    """
    Log an event locally.
    """
    if properties is None:
        properties = {}
    
    try:
        # Get current variations
        variations = get_variations(gb)
        
        # Create event log entry
        event_log = {
            'timestamp': datetime.now().isoformat(),
            'user_id': gb.attributes.get('id'),
            'event': event_name,
            'properties': properties,
            'variations': variations
        }
        
        # Print event for debugging
        logger.info(f"Event logged: {json.dumps(event_log, indent=2)}")
        
    except Exception as e:
        logger.error(f"Error logging event: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
    
    # You could also write to a file or database here
    # with open('events.log', 'a') as f:
    #     f.write(json.dumps(event_log) + '\n') 