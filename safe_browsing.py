# safe_browsing.py (tambahan)

import requests
import json
import socket

class SafeBrowsingChecker:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"
    
    def validate_domain(self, url):
        try:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            socket.gethostbyname(domain)
            return True
        except:
            return False
    
    def check_url(self, url):
        if not self.validate_domain(url):
            return None, ["Domain tidak valid atau tidak dapat diakses"]
        
        payload = {
            "client": {
                "clientId": "radipta-safebrowsing",
                "clientVersion": "1.0.0"
            },
            "threatInfo": {
                "threatTypes": [
                    "MALWARE",
                    "SOCIAL_ENGINEERING",
                    "UNWANTED_SOFTWARE",
                    "POTENTIALLY_HARMFUL_APPLICATION"
                ],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": url}]
            }
        }
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            
            if "matches" in result:
                threat_types = [match["threatType"] for match in result["matches"]]
                return False, threat_types
            else:
                return True, []
                
        except requests.exceptions.RequestException as e:
            return None, [f"Error: {str(e)}"]
    
    def check_urls(self, urls):
        results = []
        for url in urls:
            is_safe, threats = self.check_url(url)
            results.append((url, is_safe, threats))
        return results