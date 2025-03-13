"""
This script checks for the existence of two files: 'token.json' and 'credentials.json'.
If 'token.json' is found, it prints "token found". Otherwise, it raises a FileNotFoundError.
Similarly, if 'credentials.json' is found, it prints "credentials found". Otherwise, it raises a FileNotFoundError.

Raises:
    FileNotFoundError: If 'token.json' or 'credentials.json' is not found in the current directory.
"""
import os
if os.path.exists("token.json"):
    print("token found")
else:
    raise FileNotFoundError("token.json not found")
if os.path.exists("credentials.json"):
    print("credentials found")
else:
    raise FileNotFoundError("credentials.json not found")
