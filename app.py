from flask import Flask, render_template, request, send_file, jsonify
from PIL import Image, ImageDraw, ImageFont
import os
from io import BytesIO

app = Flask(__name__)

def hex_to_rgb(hex_color):
    # Convert hex color code to RGB tuple
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_image():
    text = request.form.get('text')
    font_name = request.form.get('font')
    color= request.form.get('favcolor')
    color_tuple= hex_to_rgb(color)
    # Fetch the selected font path
    font_path = f"static/fonts/{font_name}.ttf"

    # Check if the font file exists
    if not os.path.exists(font_path):
        error_message = f"Error: Font file '{font_name}.ttf' not found."
        return jsonify({'error': error_message})

    try:
        # Use the selected font with a fixed size of 36
        font_size = 76
        font = ImageFont.truetype(font_path, font_size)

        # Create an image with a transparent background
        image = Image.new('RGBA', (1000, 250), color=(255, 255, 255, 0))
        draw = ImageDraw.Draw(image)

        # Set a fixed center position
        x = 100
        y = 50  # Assuming the height is half of the image height

        # Draw the text on the image
        draw.text((x, y), text, font=font, fill=color_tuple)  # Setting fill color with full opacity

        # Save the image to a BytesIO object
        image_stream = BytesIO()
        image.save(image_stream, format='PNG')
        image_stream.seek(0)

        return send_file(image_stream, mimetype='image/png', download_name='output.png')
    except Exception as e:
        error_message = f"Error: {str(e)}"
        return jsonify({'error': error_message})

if __name__ == '__main__':
    app.run(debug=True)
