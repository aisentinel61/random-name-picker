import math
import re

# Slot dimensions
slot_width = 32  # rem
slot_height = 12  # rem
border_width = 1.625  # rem
border_radius = 1.25  # rem

# SVG viewBox dimensions
svg_width = 1000
svg_height = 230

# Dot radius (approximately)
dot_radius = 5.9

# Convert rem to SVG coordinates
def rem_to_svg_x(rem_x):
    return (rem_x / slot_width) * svg_width

def rem_to_svg_y(rem_y):
    return (rem_y / slot_height) * svg_height

# Border center line
border_center = border_width / 2  # 0.8125 rem

# Calculate corner arc centers and radius
# The arc should be centered on the border center line
arc_radius_rem = border_radius - border_center  # radius from corner center to border center
arc_radius_svg = rem_to_svg_x(arc_radius_rem)  # Convert to SVG units

# Corner centers
tl_center = (rem_to_svg_x(border_radius), rem_to_svg_y(border_radius))
tr_center = (rem_to_svg_x(slot_width - border_radius), rem_to_svg_y(border_radius))
bl_center = (rem_to_svg_x(border_radius), rem_to_svg_y(slot_height - border_radius))
br_center = (rem_to_svg_x(slot_width - border_radius), rem_to_svg_y(slot_height - border_radius))

# Generate dots along an arc
def generate_arc_dots(center_x, center_y, radius, start_angle, end_angle, num_dots):
    """Generate dot positions along an arc"""
    dots = []
    for i in range(num_dots):
        angle = start_angle + (end_angle - start_angle) * i / (num_dots - 1)
        x = center_x + radius * math.cos(math.radians(angle))
        y = center_y + radius * math.sin(math.radians(angle))
        dots.append((x, y))
    return dots

# Approximate dot spacing on straight edges (about 33 pixels between dots)
straight_dot_spacing = svg_width / 30  # approximately
arc_length = (math.pi / 2) * arc_radius_svg  # Quarter circle
corner_dots = max(3, int(arc_length / straight_dot_spacing))  # Number of dots per corner

print(f"Arc radius: {arc_radius_svg:.1f} SVG units")
print(f"Arc length per corner: {arc_length:.1f} SVG units")
print(f"Adding {corner_dots} dots per corner arc")
print()

# Generate corner dots
# Top-left (180° to 90° - from left edge to top edge)
tl_dots = generate_arc_dots(tl_center[0], tl_center[1], arc_radius_svg, 180, 90, corner_dots)

# Top-right (90° to 0° - from top edge to right edge)
tr_dots = generate_arc_dots(tr_center[0], tr_center[1], arc_radius_svg, 90, 0, corner_dots)

# Bottom-right (0° to -90° - from right edge to bottom edge)
br_dots = generate_arc_dots(br_center[0], br_center[1], arc_radius_svg, 0, -90, corner_dots)

# Bottom-left (-90° to -180° - from bottom edge to left edge)
bl_dots = generate_arc_dots(bl_center[0], bl_center[1], arc_radius_svg, -90, -180, corner_dots)

# Generate SVG path commands for the dots
def create_dot_path(x, y):
    """Create a circular dot path"""
    return (f"M{x:.1f},{y:.1f}c0-3.2,2.6-5.9,5.9-5.9l0,0c3.2,0,5.9,2.6,5.9,5.9l0,0"
            f"c0,3.2-2.6,5.9-5.9,5.9l0,0C{x+2.6:.1f},{y+5.9:.1f},{x:.1f},{y+3.2:.1f},{x:.1f},{y:.1f}z ")

corner_paths = []

print("Top-left corner dots:")
for x, y in tl_dots:
    print(f"  ({x:.1f}, {y:.1f})")
    corner_paths.append(create_dot_path(x, y))

print("\nTop-right corner dots:")
for x, y in tr_dots:
    print(f"  ({x:.1f}, {y:.1f})")
    corner_paths.append(create_dot_path(x, y))

print("\nBottom-right corner dots:")
for x, y in br_dots:
    print(f"  ({x:.1f}, {y:.1f})")
    corner_paths.append(create_dot_path(x, y))

print("\nBottom-left corner dots:")
for x, y in bl_dots:
    print(f"  ({x:.1f}, {y:.1f})")
    corner_paths.append(create_dot_path(x, y))

# Read current SVG
with open('src/assets/images/light-blubs.svg', 'r', encoding='utf-8') as f:
    svg_content = f.read()

# Find the end of the current path and add corner dots before the closing tags
# Look for the last z"/> before </g>
insertion_point = svg_content.rfind('z"/>')

if insertion_point > 0:
    # Insert the corner dot paths
    corner_path_str = ''.join(corner_paths)
    svg_content = svg_content[:insertion_point + 2] + corner_path_str + svg_content[insertion_point + 2:]
    
    # Write updated SVG
    with open('src/assets/images/light-blubs.svg', 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print(f"\n✓ Added {len(corner_paths)} corner dots to the SVG!")
    print(f"  Total: {corner_dots * 4} dots for all 4 rounded corners")
else:
    print("✗ Could not find insertion point in SVG")
