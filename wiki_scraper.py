import requests
from bs4 import BeautifulSoup
import re

url = "https://en.wikipedia.org/wiki/Athens"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    infobox = soup.find('table', {'class': 'infobox'})
    if infobox:
        text_content = infobox.get_text(separator=' | ', strip=True)
        clean_text = re.sub(r"\[\s*\|*\s*\d+\s*\|*\s*\]", "", text_content)
        clean_text = re.sub(r"\[\d+\]", "", clean_text)

        print("--- Infobox Extraction (1-7) ---")
        name_match = re.search(r"^(.*?)\s*\|", clean_text)
        if name_match: print(f"1. City: {name_match.group(1).strip()}")

        pop_match = re.search(r"Population.*?\|\s*(\d{1,3}(?:,\d{3})+)", clean_text)
        if pop_match: print(f"2. Population: {pop_match.group(1).strip()}")

        area_match = re.search(r"Area.*?\|\s*([\d,.]+)", clean_text)
        if area_match: print(f"3. Area: {area_match.group(1).strip()} km2")

        country_match = re.search(r"Country\s*\|\s*([^|]+)", clean_text)
        if country_match: print(f"4. Country: {country_match.group(1).strip()}")

        coord_match = re.search(r"Coordinates:\s*\|\s*([^|]+)\s*\|\s*([^|]+)", clean_text)
        if not coord_match:
            coord_match = re.search(r"Coordinates:\s*([^|]+)", clean_text)
            if coord_match: print(f"5. Coordinates: {coord_match.group(1).strip()}")
        else:
            print(f"5. Coordinates: {coord_match.group(1).strip()} {coord_match.group(2).strip()}")

        elev_match = re.search(r"Elevation\s*\|\s*([^|]+)", clean_text)
        if elev_match: print(f"6. Elevation: {elev_match.group(1).strip()}")

        tz_match = re.search(r"Time zone\s*\|\s*([^|]+)", clean_text)
        if tz_match: print(f"7. Time Zone: {tz_match.group(1).strip()}")

    print("\n--- Climate Extraction (8) ---")
    tables = soup.find_all('table', {'class': 'wikitable'})
    climate_found = False

    for table in tables:
        table_text = table.get_text(separator=' | ', strip=True)
        if "Climate" in table_text or "°C" in table_text:
            climate_found = True

            high_match = re.search(r"(?:Mean daily maximum|Average high|Record high).*?\|\s*([-]?\d+(?:\.\d+)?)",
                                   table_text)
            if high_match: print(f"8a. Max Temp (Jan): {high_match.group(1)} °C")

            mean_match = re.search(r"(?:Daily mean|Mean).*?\|\s*([-]?\d+(?:\.\d+)?)", table_text)
            if mean_match: print(f"8b. Mean Temp (Jan): {mean_match.group(1)} °C")

            low_match = re.search(r"(?:Mean daily minimum|Average low|Record low).*?\|\s*([-]?\d+(?:\.\d+)?)",
                                  table_text)
            if low_match: print(f"8c. Min Temp (Jan): {low_match.group(1)} °C")

            break

    if not climate_found:
        print("Climate table not found.")

else:
    print(f"Error. Status code: {response.status_code}")