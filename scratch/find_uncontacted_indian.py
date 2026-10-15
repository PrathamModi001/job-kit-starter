import csv

with open('job-kit-starter/output/job-search/outreach/startups_outreach.csv', encoding='utf-8', errors='ignore') as f:
    existing = {row['Company'].strip().lower() for row in csv.DictReader(f) if row.get('Company')}

candidates = [
    ("Plum", "Abhishek Poddar", "abhishek@plumhq.com"),
    ("Pocket FM", "Rohan Nayak", "rohan@pocketfm.com"),
    ("Zepto", "Aadit Palicha", "aadit@zeptonow.com"),
    ("Licious", "Abhay Hanjura", "abhay@licious.com"),
    ("Rebel Foods", "Jaydeep Barman", "jaydeep@rebelfoods.com"),
    ("Curefoods", "Ankit Nagori", "ankit@curefoods.in"),
    ("Captain Fresh", "Utham Gowda", "utham@captainfresh.com"),
    ("Euler Motors", "Saurav Kumar", "saurav@eulermotors.com"),
    ("Chargeup", "Varun Goenka", "varun@chargeup.co.in"),
    ("Ultrahuman", "Mohit Kumar", "mohit@ultrahuman.com"),
    ("Park+", "Amit Lakhotia", "amit@myparkplus.com"),
    ("Boba", "Saurabh", "saurabh@boba.in"),
    ("Jar", "Nishchay", "nishchay@jar.com"),
    ("Kite", "Nithin", "nithin@zerodha.com"),
    ("Gupshup", "Beerud Sheth", "beerud@gupshup.io"),
    ("Yellow.ai", "Raghu Ravinutala", "raghu@yellow.ai"),
    ("Haptik", "Aakrit Vaish", "aakrit@haptik.ai"),
    ("Loco", "Anirudh Pandita", "anirudh@loco.gg"),
    ("WinZO", "Paavan Nanda", "paavan@winzogames.com"),
    ("MPL", "Sai Srinivas", "sai@mplgaming.com"),
    ("CoinSwitch", "Ashish Singhal", "ashish@coinswitch.co"),
    ("Mudrex", "Edul Patel", "edul@mudrex.com"),
    ("Wint Wealth", "Ajinkya Kulkarni", "ajinkya@wintwealth.com"),
    ("StrideOne", "Ishpreet Gandhi", "ishpreet@strideone.in"),
    ("Volt Money", "Lalit Bihani", "lalit@voltmoney.in"),
    ("Betterhalf", "Pawan Gupta", "pawan@betterhalf.ai")
]

available = []
for co, founder, email in candidates:
    if co.lower() not in existing:
        available.append((co, founder, email))

print(f"Available Indian startups: {len(available)}")
for co, founder, email in available[:15]:
    print(f"- {co} | {founder} | {email}")
