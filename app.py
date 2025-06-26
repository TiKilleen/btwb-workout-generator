from flask import Flask, render_template_string, send_file
from PIL import Image, ImageDraw, ImageFont
import io
import requests

app = Flask(__name__)

BTWB_API_KEY = "apry1ewoh2ssxeanwyne8lldq"
TRACK_ID = 310497  # Replace with your actual BTWB track ID

def get_btwb_workout():
    headers = {
        "Authorization": f"Bearer {BTWB_API_KEY}",
        "Accept": "application/json"
    }

    url = f"https://api.beyondthewhiteboard.com/api/v1/tracks/{TRACK_ID}/wods"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        latest_wod = data["wods"][0]
        title = latest_wod.get("name", "WOD")
        movements = [m.get("name", "Unknown Movement") for m in latest_wod.get("movements", [])]

        return {
            "date": latest_wod.get("date", "Unknown Date"),
            "title": title,
            "movements": movements if movements else ["Movement details not available"]
        }

    except Exception as e:
        print(f"BTWB API error: {e}")
        return {
            "date": "N/A",
            "title": "BTWB API Unavailable",
            "movements": ["Check your API key or network."]
        }

@app.route("/")
def home():
    return render_template_string('''
        <h1>Generate BTWB Workout Graphic</h1>
        <form action="/generate">
            <button type="submit">Generate Image</button>
        </form>
    ''')

@app.route("/generate")
def generate():
    data = get_btwb_workout()

    img = Image.new('RGB', (1080, 1080), color='white')
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Helvetica Bold.ttf", 60)
        text_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Helvetica.ttf", 45)
    except:
        title_font = text_font = ImageFont.load_default()

    draw.text((100, 50), "CSC", fill='red', font=title_font)
    draw.text((100, 150), "6AM // 9:30AM // 5:30PM", fill='black', font=text_font)
    draw.text((100, 300), data["title"], fill='black', font=title_font)

    y = 400
    for move in data["movements"]:
        draw.text((100, y), move, fill='red', font=text_font)
        y += 80

    draw.text((100, 1000), f"Workout of the Day {data['date']}", fill='black', font=text_font)

    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='btwb_workout.p_
