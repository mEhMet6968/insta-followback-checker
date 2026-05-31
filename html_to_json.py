"""
following.html dosyasını insta_checker.py'nin beklediği
JSON formatına dönüştürür.

Kullanım:
    python html_to_json.py
    # Çıktı: following.json

İsteğe bağlı argümanlar:
    python html_to_json.py input.html output.json
"""

import json
import sys
from datetime import datetime

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("BeautifulSoup bulunamadı. Yükleniyor...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4", "-q"])
    from bs4 import BeautifulSoup


def html_to_json(input_file="following.html", output_file="following.json"):
    print(f"Okunuyor: {input_file}")

    with open(input_file, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    links = soup.find_all("a", href=True)

    entries = []
    for link in links:
        href = link.get("href", "")
        if "instagram.com" not in href:
            continue

        # Kullanıcı adını URL'den çıkar
        username = (
            href.replace("https://www.instagram.com/_u/", "")
                .replace("https://www.instagram.com/", "")
                .strip("/")
        )

        if not username:
            continue

        # insta_checker.py'nin beklediği format:
        # { "title": "kullanıcıadı", "string_list_data": [{ "href": "...", "value": "kullanıcıadı", "timestamp": ... }] }
        entry = {
            "title": username,
            "string_list_data": [
                {
                    "href": f"https://www.instagram.com/{username}/",
                    "value": username,
                    "timestamp": int(datetime.now().timestamp())
                }
            ]
        }
        entries.append(entry)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

    print(f"Dönüştürüldü: {len(entries)} kullanıcı → {output_file}")
    return entries


if __name__ == "__main__":
    input_file  = sys.argv[1] if len(sys.argv) > 1 else "following.html"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "following.json"
    html_to_json(input_file, output_file)
