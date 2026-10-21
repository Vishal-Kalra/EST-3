"""
Builds YOUR individual code zip for Canvas.

Usage (from the project folder):
    python make_submission.py vishal
    python make_submission.py prithvi
    python make_submission.py mihir
    python make_submission.py jasmine
    python make_submission.py mrunal

Creates e.g. 25620699_Mihir_Chauhan_A3_code.zip containing the shared files
plus only your own test folder, so the marker can run it straight away.
"""
import os
import sys
import zipfile

MEMBERS = {
    "vishal": ("25675962", "Vishal_Kalra"),
    "prithvi": ("25966060", "Prithvi_Krishna_Prasad"),
    "mihir": ("25620699", "Mihir_Chauhan"),
    "jasmine": ("25729738", "Jasmine_Joseph"),
    "mrunal": ("25717430", "Mrunal_Ghag"),
}
SHARED = ["conftest.py", "helpers.py", "pytest.ini", "requirements.txt", "README.md",
          "run_tests.sh", "run_tests.bat"]

if len(sys.argv) != 2 or sys.argv[1].lower() not in MEMBERS:
    sys.exit("Usage: python make_submission.py <" + "|".join(MEMBERS) + ">")

who = sys.argv[1].lower()
sid, name = MEMBERS[who]
out = f"{sid}_{name}_A3_code.zip"
root = f"{sid}_{name}_A3_code"

with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for f in SHARED:
        z.write(f, f"{root}/{f}")
    folder = os.path.join("tests", who)
    for f in sorted(os.listdir(folder)):
        if f.endswith(".py"):
            z.write(os.path.join(folder, f), f"{root}/tests/{who}/{f}")
            body = open(os.path.join(folder, f)).read()
            if "pytest.skip(" in body:
                print(f"WARNING: {f} still has unfinished pytest.skip() scenarios")

print("Created", out)
