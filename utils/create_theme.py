from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR

prs = Presentation()

# We want to modify the master slide backgrounds
# But python-pptx doesn't easily modify the slide master background.
# Instead, we can add a simple solid background to all layouts.

for layout in prs.slide_layouts:
    background = layout.background
    fill = background.fill
    fill.solid()
    # Dark blue background
    fill.fore_color.rgb = RGBColor(0x1a, 0x2b, 0x4c)

# Save the stylized file as our template
prs.save("template.pptx")
print("Successfully generated template.pptx with a Dark Blue theme!")
