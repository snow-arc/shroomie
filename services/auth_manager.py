from datetime import datetime, timedelta
from typing import Dict, Tuple

class AuthManager:
    def __init__(self):
        self.attempt_counts: Dict[str, int] = {}  # IP -> count
        self.blocked_until: Dict[str, datetime] = {}  # IP -> datetime
        self.max_session_attempts = 4
        self.max_password_attempts = 2
        self.block_duration = timedelta(minutes=10)
    
    def can_attempt(self, ip: str) -> Tuple[bool, str]:
        now = datetime.now()
        
        # Check if blocked
        if ip in self.blocked_until:
            if now < self.blocked_until[ip]:
                remaining = (self.blocked_until[ip] - now).seconds // 60
                return False, f"Try again in {remaining} minutes"
            else:
                # Block duration expired
                del self.blocked_until[ip]
                self.attempt_counts[ip] = 0
        
        # Check attempt count
        if ip in self.attempt_counts and self.attempt_counts[ip] >= self.max_session_attempts:
            self.blocked_until[ip] = now + self.block_duration
            return False, "Too many attempts. Try again later"
            
        return True, ""
    
    def record_attempt(self, ip: str, success: bool):
        if not success:
            self.attempt_counts[ip] = self.attempt_counts.get(ip, 0) + 1
        else:
            # Reset on successful attempt
            self.attempt_counts[ip] = 0
