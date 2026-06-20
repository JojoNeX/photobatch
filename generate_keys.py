#!/usr/bin/env python3
"""
PhotoBatch License Key Generator
Format: PB-XXXX-XXXX-XXCC (CC = checksum)
Usage: python generate_keys.py --email client@example.com
       python generate_keys.py --batch emails.txt
"""
import hashlib
import argparse
import sys
from datetime import datetime

SECRET = "photobatch-pro-2026"  # Change this to invalidate all existing keys

def generate_key(email: str) -> str:
    """Generate a license key from an email address.
    
    Format: PB-XXXX-XXXX-XXCC
    - First 10 hex chars from SHA256(email + secret)
    - Last 2 hex chars (CC) = checksum of the first 10 chars
    """
    email = email.strip().lower()
    if not email or '@' not in email:
        raise ValueError(f"Invalid email: {email}")
    
    # Hash the email + secret
    h = hashlib.sha256(f"{email}-{SECRET}".encode()).hexdigest()
    
    # Take first 10 hex chars for the key body
    body = h[:10]
    
    # Checksum: sum of hex values of body chars, mod 256, as 2-char hex
    checksum = sum(ord(c) for c in body) % 256
    cc = f"{checksum:02x}"
    
    # Format: PB-XXXX-XXXX-XXCC
    key = f"PB-{body[:4]}-{body[4:8]}-{body[8:10]}{cc}".upper()
    return key

def generate_batch(input_file: str) -> list:
    """Generate keys for multiple emails from a file."""
    with open(input_file, 'r') as f:
        emails = [line.strip() for line in f if line.strip()]
    
    results = []
    for email in emails:
        try:
            key = generate_key(email)
            results.append((email, key))
        except ValueError as e:
            results.append((email, f"ERROR: {e}"))
    
    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PhotoBatch License Key Generator')
    parser.add_argument('--email', help='Single email address')
    parser.add_argument('--batch', help='File with one email per line')
    parser.add_argument('--output', '-o', help='Output CSV file (default: stdout)')
    
    args = parser.parse_args()
    
    if args.email:
        try:
            key = generate_key(args.email)
            print(f"Email: {args.email}")
            print(f"Key:   {key}")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    
    elif args.batch:
        results = generate_batch(args.batch)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write("email,license_key,generated_at\n")
                timestamp = datetime.now().isoformat()
                for email, key in results:
                    f.write(f"{email},{key},{timestamp}\n")
            print(f"✅ {len(results)} keys written to {args.output}")
        else:
            print("email,license_key")
            for email, key in results:
                print(f"{email},{key}")
    
    else:
        parser.print_help()
        print("\nExample:")
        print("  python generate_keys.py --email client@example.com")
        print("  python generate_keys.py --batch buyers.txt -o keys.csv")
