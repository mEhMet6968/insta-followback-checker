import json
def load_users(filename):
    with open(filename, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        for key in data:
            if isinstance(data[key], list):
                data = data[key]
                break
    users = set()
    for entry in data:
        try:
            sld = entry.get("string_list_data", [{}])[0]
            href = sld.get("href", "")
            username = (
                entry.get("title")
                or sld.get("value")
                or href.replace("https://www.instagram.com/", "")
                .replace("_u/", "")
                .replace("/", "")
                .strip()
            )
            if username:
                users.add(username.lower())
        except Exception:
            continue
    return users
followers = load_users("followers_1.json")
following = load_users("following.json")

print(f"Follower count: {len(followers)}")
print(f"T>Follow count: {len(following)}")

not_following_back = following - followers

print("\nDont follow back :")
print("-" * 40)
for user in sorted(not_following_back):
    print(user)
print(f"\nToplam: {len(not_following_back)} kişi seni takip etmiyor.")
