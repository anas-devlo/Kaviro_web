# Python Standard Libraries
import secrets
import hashlib
import hmac
import time
import logging
import re
import ipaddress

from datetime import datetime, timedelta, timezone
from collections import defaultdict, deque

# External Libraries
from pwdlib import PasswordHash

# FastAPI
from fastapi import Request, HTTPException


# Password Security
class PasswordSecurity:
        password_hash = PasswordHash.recommended()
        @staticmethod
        def hash_password(password):
                return PasswordSecurity.password_hash.hash(password)
        @staticmethod
        def verify_password(password, hashed_password):
                        return PasswordSecurity.password_hash.verify(
            password,
            hashed_password
        )

class BruteForceProtection:

    MAX_ACCOUNT_ATTEMPTS = 5
    MAX_IP_ATTEMPTS = 10
    LOCK_TIME = 60

    def __init__(self):
        self.account_attempts = defaultdict(int)
        self.ip_attempts = defaultdict(int)

        self.account_blocked_until = {}
        self.ip_blocked_until = {}

    @staticmethod
    def validate_ip(ip_address):
        try:
            ipaddress.ip_address(ip_address)
            return True
        except ValueError:
            return False

    @staticmethod
    def get_client_ip(request: Request):
        if request.client is None:
            return None

        ip = request.client.host

        if not BruteForceProtection.validate_ip(ip):
            return None

        return str(ipaddress.ip_address(ip))

    def check_attempts(self, account, ip_address):

        current_time = time.monotonic()

        account_block = self.account_blocked_until.get(account)
        ip_block = self.ip_blocked_until.get(ip_address)

        if account_block is not None and current_time >= account_block:
            self.account_blocked_until.pop(account, None)
            self.account_attempts.pop(account, None)

        if ip_block is not None and current_time >= ip_block:
            self.ip_blocked_until.pop(ip_address, None)
            self.ip_attempts.pop(ip_address, None)

        account_blocked = account in self.account_blocked_until
        ip_blocked = ip_address in self.ip_blocked_until

        return not (account_blocked or ip_blocked)

    def record_failure(self, account, ip_address):

        if not self.check_attempts(account, ip_address):
            return

        self.account_attempts[account] += 1
        self.ip_attempts[ip_address] += 1

        current_time = time.monotonic()

        if self.account_attempts[account] >= self.MAX_ACCOUNT_ATTEMPTS:
            self.account_blocked_until[account] = current_time + self.LOCK_TIME

        if self.ip_attempts[ip_address] >= self.MAX_IP_ATTEMPTS:
            self.ip_blocked_until[ip_address] = current_time + self.LOCK_TIME

    def reset_attempts(self, account):
        self.account_attempts.pop(account, None)
        self.account_blocked_until.pop(account, None)