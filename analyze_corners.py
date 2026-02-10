import math

# Slot dimensions
slot_width = 32  # rem
slot_height = 12  # rem
border_width = 1.625  # rem
border_radius = 1.25  # rem

# SVG viewBox dimensions
svg_width = 1000
svg_height = 230

# Calculate border center line
border_center = border_width / 2  # 0.8125 rem from edge

# Convert to SVG coordinates
def rem_to_svg_x(rem_x):
    return (rem_x / slot_width) * svg_width

def rem_to_svg_y(rem_y):
    return (rem_y / slot_height) * svg_height

# Border center positions
top_y = rem_to_svg_y(border_center)
bottom_y = rem_to_svg_y(slot_height - border_center)
left_x = rem_to_svg_x(border_center)
right_x = rem_to_svg_x(slot_width - border_center)

# Corner centers (where arcs should be centered)
# Top-left corner center
tl_center_x = rem_to_svg_x(border_radius)
tl_center_y = rem_to_svg_y(border_radius)

# Top-right corner center
tr_center_x = rem_to_svg_x(slot_width - border_radius)
tr_center_y = rem_to_svg_y(border_radius)

# Bottom-left corner center
bl_center_x = rem_to_svg_x(border_radius)
bl_center_y = rem_to_svg_y(slot_height - border_radius)

# Bottom-right corner center
br_center_x = rem_to_svg_x(slot_width - border_radius)
br_center_y = rem_to_svg_y(slot_height - border_radius)

print("Slot has rounded corners with radius: 1.25rem")
print(f"\nBorder center line should be at: {border_center:.4f} rem from edges")
print(f"\nSVG Coordinates:")
print(f"  Top edge: Y = {top_y:.1f}")
print(f"  Bottom edge: Y = {bottom_y:.1f}")
print(f"  Left edge: X = {left_x:.1f}")
print(f"  Right edge: X = {right_x:.1f}")
print(f"\nCorner arc centers:")
print(f"  Top-left: ({tl_center_x:.1f}, {tl_center_y:.1f})")
print(f"  Top-right: ({tr_center_x:.1f}, {tr_center_y:.1f})")
print(f"  Bottom-left: ({bl_center_x:.1f}, {bl_center_y:.1f})")
print(f"  Bottom-right: ({br_center_x:.1f}, {br_center_y:.1f})")

# Arc radius for dots (on the border center line)
arc_radius_rem = border_radius - border_center
inner_radius = rem_to_svg_x(border_radius - border_radius + border_center)
outer_radius = rem_to_svg_x(border_radius)

print(f"\nArc radius on border center: {arc_radius_rem:.4f} rem")
print(f"Need to add corner dots following 4 rounded corners!")
print(f"\n⚠️  Current SVG only has straight-edge dots!")
print(f"    Missing: Corner arc dots to follow the border-radius curve")
