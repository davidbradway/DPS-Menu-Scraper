import os
# Accessing an environment variable
home = os.environ.get("HOME")
if home:
    if os.path.exists(os.path.join(home, "secrets", "token.json")):
        print("token found")
    else:
        print("token missing")
    if os.path.exists(os.path.join(home, "secrets", "credentials.json")):
        print("credentials found")
    else:
        print("credentials missing")
else:
    print("home env var not found")

