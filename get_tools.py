import urllib.request
import os

url = "https://gist.githubusercontent.com/the-stark/d9e034b7fbf7c3275712e0802c6104be/raw/stadium_tools.py"
target_path = os.path.expanduser("~/sovereign_grid/tools/stadium_tools.py")

print(f"Fetching tools from Gist...")
try:
    # Set a common user-agent to bypass basic bot-blocking filters if present
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        code_content = response.read().decode('utf-8')
    
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "w") as f:
        f.write(code_content)
    print(f"Success! Saved tool matrix directly to {target_path}")
except Exception as e:
    print(f"Download failed: {e}")
