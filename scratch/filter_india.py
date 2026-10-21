import json, re

with open("scratch/qualifying_ats_leads.json", encoding="utf-8") as f:
    leads = json.load(f)

INDIA_EXACT = re.compile(r"\b(bengaluru|bangalore|hyderabad|pune|gurgaon|gurugram|mumbai|chennai|ahmedabad|india)\b", re.I)
FOREIGN = re.compile(r"\b(us|usa|united states|canada|uk|united kingdom|poland|germany|france|spain|mexico|thailand|singapore|australia|malaysia|ireland|netherlands|romania|sweden|switzerland|remote - us|remote - usa|remote us|remote - canada)\b", re.I)

india_leads = []
for l in leads:
    loc = l["location"]
    if INDIA_EXACT.search(loc) and not (FOREIGN.search(loc) and "india" not in loc.lower()):
        title = l["title"]
        if not re.search(r"\b(sales|support|escalation|manager|director|intern|lead|senior|sr)\b", title, re.I):
            india_leads.append(l)

print(f"True India matches: {len(india_leads)}")
for l in india_leads:
    print(f"[{l['ats']}] {l['company']} - {l['title']} ({l['location']}) -> {l['url']}")
