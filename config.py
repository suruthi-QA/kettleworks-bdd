"""All settings in one place. Override any value with an environment variable."""
import os

BASE_URL = os.getenv("BASE_URL", "https://interview-qa-task.vercel.app").rstrip("/")

# Test accounts (practice site: any password works, emails starting with admin@ get the admin role)
CUSTOMER_EMAIL = os.getenv("CUSTOMER_EMAIL", "test@yopmail.com")
CUSTOMER_PASSWORD = os.getenv("CUSTOMER_PASSWORD", "India1@1")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@yopmail.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "India1@1")

HEADLESS = os.getenv("HEADLESS", "0") == "1"   # set HEADLESS=1 to run without opening a window
TIMEOUT = int(os.getenv("TIMEOUT", "10"))      # seconds to wait for elements
