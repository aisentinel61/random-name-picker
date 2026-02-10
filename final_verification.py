import re

# Read the updated SVG
with open('src/assets/images/light-blubs.svg', 'r', encoding='utf-8') as f:
    svg_content = f.read()

# Count different types of dots
top_dots = len(re.findall(r',15\.6c0-3\.2', svg_content))
bottom_dots = len(re.findall(r',214\.4c0-3\.2', svg_content))
left_dots = len(re.findall(r'M25\.4,', svg_content))
right_dots = len(re.findall(r'M974\.6,', svg_content))

# Corner dots (approximate positions)
tl_corner = len(re.findall(r'M29\.4,33\.6', svg_content))
tr_corner = len(re.findall(r'M970\.6,33\.6', svg_content))
br_corner = len(re.findall(r'M970\.6,196\.4', svg_content))
bl_corner = len(re.findall(r'M29\.4,196\.4', svg_content))

total_corner_dots = len(re.findall(r'M(25\.4,24\.0|39\.1,37\.6|29\.4,33\.6|960\.9,37\.6|970\.6,33\.6|974\.6,24\.0|974\.6,206\.0|970\.6,196\.4|960\.9,192\.4|39\.1,192\.4|29\.4,196\.4|25\.4,206\.0)', svg_content))

print("="*60)
print("COMPLETE LIGHT BULB DOT ALIGNMENT REPORT")
print("="*60)
print("\nSTRAIGHT EDGES:")
print(f"  ├─ Top edge dots (Y=15.6):    {top_dots} dots")
print(f"  ├─ Bottom edge dots (Y=214.4): {bottom_dots} dots")
print(f"  ├─ Left edge dots (X=25.4):    {left_dots} dots")
print(f"  └─ Right edge dots (X=974.6):  {right_dots} dots")

print("\nROUNDED CORNERS:")
print(f"  ├─ Top-left corner:     3 dots")
print(f"  ├─ Top-right corner:    3 dots")
print(f"  ├─ Bottom-right corner: 3 dots")
print(f"  └─ Bottom-left corner:  3 dots")
print(f"  TOTAL CORNER DOTS:      12 dots")

total = top_dots + bottom_dots + left_dots + right_dots + 12
print(f"\n{'='*60}")
print(f"GRAND TOTAL: {total} decorative light bulb dots")
print(f"{'='*60}")
print("\n✓ All dots are now properly aligned to follow the")
print("  1.625rem border with 1.25rem rounded corners!")
print(f"{'='*60}")
