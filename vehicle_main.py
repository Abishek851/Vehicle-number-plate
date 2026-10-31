import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import easyocr
import csv
from datetime import datetime

reader = easyocr.Reader(['en'])
LOG_FILE = "vehicle_log.csv"

def read_image(image_path):
    results = reader.readtext(image_path)
    return ' '.join([res[1] for res in results])

def check_validity(text, keywords):
    for keyword in keywords:
        if keyword in text:
            return "VALID"
    return "EXPIRED"

def log_vehicle(plate, license_status, rc_status, insurance_status, load, final_status):
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            plate,
            license_status,
            rc_status,
            insurance_status,
            f"{load}kg",
            final_status
        ])

def scan_vehicle(prefix, load, vehicle_type):
    print("=" * 45)
    print(f"   TOLL GATE SYSTEM - {vehicle_type}")
    print("=" * 45)
    print("Scanning documents...")
    print("-" * 45)

    plate = read_image(f"test_images/{prefix}_plate.png")
    license_text = read_image(f"test_images/{prefix}_license.png")
    rc_text = read_image(f"test_images/{prefix}_rc.png")
    insurance_text = read_image(f"test_images/{prefix}_insurance.png")

    license_status = check_validity(license_text, ["2027", "2028", "2029", "2030"])
    rc_status = check_validity(rc_text, ["2027", "2028", "2029", "2030"])
    insurance_status = check_validity(insurance_text, ["2027", "2028", "2029", "2030"])

    print(f"  Number Plate : {plate}")
    print(f"  License      : {license_status}")
    print(f"  RC Book      : {rc_status}")
    print(f"  Insurance    : {insurance_status}")
    print(f"  Load         : {load}kg")
    print("-" * 45)

    if (license_status == "VALID" and rc_status == "VALID" and
            insurance_status == "VALID" and load <= 500):
        final_status = "CLEARED"
        print("  FINAL STATUS : >> CLEARED << GATE OPEN!")
    else:
        final_status = "REJECTED"
        reasons = []
        if license_status == "EXPIRED":
            reasons.append("License Expired")
        if rc_status == "EXPIRED":
            reasons.append("RC Expired")
        if insurance_status == "EXPIRED":
            reasons.append("Insurance Expired")
        if load > 500:
            reasons.append(f"Overloaded ({load}kg)")
        print(f"  FINAL STATUS : !! REJECTED !!")
        print(f"  REASON       : {', '.join(reasons)}")

    print("=" * 45)
    log_vehicle(plate, license_status, rc_status, insurance_status, load, final_status)
    print(f"  Logged to {LOG_FILE}")
    print("=" * 45)

# Vehicle list
vehicles = [
    ("car",   300, "CAR   🚗"),
    ("truck", 800, "TRUCK 🚛"),
    ("bus",   400, "BUS   🚌"),
    ("van",   200, "VAN   🚐"),
    ("bike",  50,  "BIKE  🏍️"),
]

print("\n" + "=" * 45)
print("   TOLL GATE MANAGEMENT SYSTEM")
print("   Powered by Alfred & Bruce 🦇")
print("=" * 45 + "\n")

for prefix, load, vtype in vehicles:
    scan_vehicle(prefix, load, vtype)
    print("\nPress Enter to scan next vehicle...")
    input()

print("\n" + "=" * 45)
print("  All vehicles processed!")
print("  Check vehicle_log.csv for full report.")
print("=" * 45)