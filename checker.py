import requests
from config import SESSION_ID

def check_account(username):
    username = username.replace("@", "").strip().lower()
    api_url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
    headers = {
        "User-Agent": "【entity-Instagram¦canonical_name=Instagram】 219.0.0.12.117 Android",
        "X-IG-App-ID": "936619743392459",
    }
    cookies = {"sessionid": SESSION_ID} if SESSION_ID else {}
    try:
        r = requests.get(api_url, headers=headers, cookies=cookies, timeout=10)
        if r.status_code == 404:
            return "❌ DISABLED / NOT FOUND"
        try:
            data = r.json()
        except:
            data = {}
        if data.get("status") == "fail":
            return "❌ DISABLED / NOT FOUND"
        user = data.get("data", {}).get("user")
        if user and user.get("id"):
            return "✅ ACTIVE"
        return "❌ DISABLED / NOT FOUND - No profile data found"
    except Exception as e:
        return f"⚠️ ERROR: {e}"