import json
from fontTools.ttLib import TTFont
from fontTools.unicode import Unicode

def get_glyphs_from_ttf(ttf_file):
    font = TTFont(ttf_file)

    # Mapping to store keyboard keys and their corresponding Unicode characters
    keyboard_mapping = {}

    # Iterate through each glyph in the font
    for glyph_name in font.getGlyphOrder():
        # Extract Unicode value(s) associated with the glyph
        unicode_values = font.getBestCmap().get(glyph_name, [])

        # Convert Unicode value(s) to character(s)
        characters = [Unicode[v] for v in unicode_values]

        # Add the glyph to the keyboard mapping for each associated character
        for char in characters:
            if char in keyboard_mapping:
                keyboard_mapping[char].append(glyph_name)
            else:
                keyboard_mapping[char] = [glyph_name]

    return keyboard_mapping

# Example usage:
if __name__ == "__main__":
    ttf_file_path = "static/fonts/AMS_Aaditya.ttf"  # Replace with the path to your TTF file
    keyboard_mapping = get_glyphs_from_ttf(ttf_file_path)

    # Convert the keyboard mapping to JSON
    keyboard_mapping_json = json.dumps(keyboard_mapping)

    # Print the JSON
    print(keyboard_mapping_json)
