import os
if os.path.exists("token.json"):
    print("token found")
else:
    print("token missing")
if os.path.exists("credentials.json"):
    print("credentials found")
else:
    print("credentials missing")
