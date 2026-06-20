#!/usr/bin/env python3
"""Quick test: generate a key and simulate JS validation."""
import hashlib

SECRET = "photobatch-pro-2026"
email = "test@example.com"

h = hashlib.sha256(f"{email}-{SECRET}".encode()).hexdigest()
body = h[:10]
checksum = sum(ord(c) for c in body) % 256
cc = f"{checksum:02x}"
key = f"PB-{body[:4]}-{body[4:8]}-{body[8:10]}{cc}".upper()

print(f"Generated key: {key}")

# Simulate JS validation
parts = key.split("-")
js_body = (parts[1] + parts[2] + parts[3][:2]).lower()
js_cc = parts[3][2:].lower()
js_sum = sum(ord(c) for c in js_body)
js_expected = f"{js_sum % 256:02x}"

print(f"JS body: {js_body}")
print(f"JS cc: {js_cc}")
print(f"JS expected: {js_expected}")
print(f"MATCH: {'✅' if js_cc == js_expected else '❌'}")

# Also test an invalid key
fake_key = "PB-AAAA-BBBB-CCCC"
parts = fake_key.split("-")
fb = (parts[1] + parts[2] + parts[3][:2]).lower()
fc = parts[3][2:].lower()
fs = sum(ord(c) for c in fb)
fe = f"{fs % 256:02x}"
print(f"\nFake key: {fake_key}")
print(f"JS would say: {'✅' if fc == fe else '❌ invalid'} (cc={fc}, expected={fe})")
