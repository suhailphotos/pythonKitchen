import fontforge
import os
import re

# Define the directory containing the fonts (update as needed)
FONT_DIR = "/Users/suhail/Downloads/Demo_Fonts"

# Mapping from numeric weight to (style name, OS/2 weight value)
weight_map = {
    "15": ("Thin", 200),
    "25": ("Light", 300),
    "35": ("Book", 350),
    "45": ("Regular", 400),
    "55": ("Medium", 500),
    "65": ("SemiBold", 600),
    "75": ("Bold", 700),
    "85": ("ExtraBold", 800),
    "95": ("Black", 900)
}

# Function to process each font file
def process_font(file_path):
    # Extract base filename
    filename = os.path.basename(file_path)
    
    # Use regex to extract the weight and whether it's italic.
    # Expected filename format: coresanscXX.otf or coresanscXXit.otf
    match = re.search(r'^coresansc(\d+)(it)?\.otf$', filename, re.IGNORECASE)
    if not match:
        print(f"Skipping file (pattern not matched): {filename}")
        return
    
    weight_digits = match.group(1)
    italic_flag = match.group(2) is not None

    if weight_digits not in weight_map:
        print(f"Weight {weight_digits} not in mapping for file: {filename}")
        return

    style_name, os2_weight = weight_map[weight_digits]
    # Append 'Italic' to style name if needed
    style_name_full = style_name + (" Italic" if italic_flag else "")
    
    # Open the font
    font = fontforge.open(file_path)
    
    # Update metadata: all fonts share the same family
    family = "Core Sans C"
    
    # Create a font internal name, typically without spaces
    internal_name = family.replace(" ", "") + "-" + style_name_full.replace(" ", "")
    full_name = f"{family} {style_name_full}"
    
    # Set the core naming properties
    font.familyname = family
    font.fontname = internal_name
    font.fullname = full_name
    
    # Update OS/2 weight if needed
    font.os2_weight = os2_weight
    
    # Optionally update the TTF names table (Name IDs)
    # Note: This helps applications like Font Book or Photoshop correctly group your fonts.
    font.sfnt_names = (
        ("English (US)", "Family", family),
        ("English (US)", "SubFamily", style_name_full),
        ("English (US)", "Fullname", full_name)
    )
    
    # Save the modified font (you can choose to overwrite or write to a new filename)
    # This example overwrites the original file.
    font.generate(file_path)
    font.close()
    print(f"Processed: {filename} → {full_name}")

def main():
    # List all .otf files in the directory
    for entry in os.listdir(FONT_DIR):
        if entry.lower().endswith(".otf"):
            file_path = os.path.join(FONT_DIR, entry)
            process_font(file_path)

if __name__ == '__main__':
    main()
