# src/services/token_manager.py
import time
import requests
from config import FEISHU_REFRESH_TOKEN_URL

class FeishuTokenManager:
    def __init__(self, app_id: str, app_secret: str, refresh_token: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.refresh_token = refresh_token
        self.access_token = None
        self.expires_at = 0

    def refresh_access_token(self):
        """
        Refreshes the access token using the refresh token.
        """
        headers = {
            "Content-Type": "application/json; charset=utf-8"
        }
        payload = {
            "grant_type": "refresh_token",
            "client_id": self.app_id,
            "client_secret": self.app_secret,
            "refresh_token": self.refresh_token
        }
        
        try:
            response = requests.post(FEISHU_REFRESH_TOKEN_URL, headers=headers, json=payload)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            data = response.json()
            if data.get("code") == 0:
                token_data = data.get("data", {})
                self.access_token = token_data.get("access_token")
                self.refresh_token = token_data.get("refresh_token")
                # Set expiration time with a 5-minute buffer
                self.expires_at = time.time() + token_data.get("expires_in", 0) - 300
                return True, None
            else:
                return False, data.get("msg", "Unknown error")
        except requests.exceptions.RequestException as e:
            return False, str(e)

    def get_token_info(self):
        """
        Returns the current token information. If the token is expired or about to expire,
        it refreshes it first.
        """
        if time.time() >= self.expires_at:
            success, error_msg = self.refresh_access_token()
            if not success:
                # If refresh fails, we should return an error.
                # The caller can then decide how to handle it.
                return None, error_msg

        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_at": self.expires_at
        }, None

# A simple in-memory cache for token managers
# For a production environment, consider a more robust solution like Redis.
token_manager_cache = {}

def get_token_manager(app_id: str, app_secret: str, refresh_token: str) -> FeishuTokenManager:
    """
    Factory function to get or create a FeishuTokenManager instance.
    This ensures that for a given app_id, we reuse the same token manager.
    """
    if app_id not in token_manager_cache:
        token_manager_cache[app_id] = FeishuTokenManager(app_id, app_secret, refresh_token)
    
    # Always update with the latest tokens if provided, in case they were refreshed elsewhere
    manager = token_manager_cache[app_id]
    manager.app_secret = app_secret
    if refresh_token:
        manager.refresh_token = refresh_token
        
    return manager
