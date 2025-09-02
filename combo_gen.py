# input.txt ফাইলে থাকবে:
# url | username | password

credentials = set()  # ডুপ্লিকেট রিমুভ করার জন্য set()

with open("creds.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split("|")
        if len(parts) == 3:
            username = parts[1].strip()
            password = parts[2].strip()
            credentials.add(f"{username}:{password}")

# combo.txt ফাইলে লিখে দেওয়া
with open("combo.txt", "w", encoding="utf-8") as f:
    for cred in credentials:
        f.write(f"{cred}\n")

print("[INFO] combo.txt ফাইল তৈরি হয়ে গেছে ✅")
