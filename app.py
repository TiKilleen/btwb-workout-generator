<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <meta http-equiv="Content-Style-Type" content="text/css">
  <title></title>
  <meta name="Generator" content="Cocoa HTML Writer">
  <meta name="CocoaVersion" content="2575.6">
  <style type="text/css">
    p.p1 {margin: 0.0px 0.0px 0.0px 0.0px; font: 12.0px Helvetica}
    p.p2 {margin: 0.0px 0.0px 0.0px 0.0px; font: 12.0px Helvetica; min-height: 14.0px}
  </style>
</head>
<body>
<p class="p1">from flask import Flask, render_template_string, send_file</p>
<p class="p1">from PIL import Image, ImageDraw, ImageFont</p>
<p class="p1">import io</p>
<p class="p1">import requests</p>
<p class="p2"><br></p>
<p class="p1">app = Flask(__name__)</p>
<p class="p2"><br></p>
<p class="p1">BTWB_API_KEY = "apry1ewoh2ssxeanwyne8lldq"</p>
<p class="p1">TRACK_ID = 310497<span class="Apple-converted-space">  </span># Replace with your actual BTWB track ID</p>
<p class="p2"><br></p>
<p class="p1"># Fetch live workout data from BTWB</p>
<p class="p2"><br></p>
<p class="p1">def get_btwb_workout():</p>
<p class="p1"><span class="Apple-converted-space">    </span>headers = {</p>
<p class="p1"><span class="Apple-converted-space">        </span>"Authorization": f"Bearer {BTWB_API_KEY}",</p>
<p class="p1"><span class="Apple-converted-space">        </span>"Accept": "application/json"</p>
<p class="p1"><span class="Apple-converted-space">    </span>}</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">    </span>url = f"https://api.beyondthewhiteboard.com/api/v1/tracks/{TRACK_ID}/wods"</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">    </span>try:</p>
<p class="p1"><span class="Apple-converted-space">        </span>response = requests.get(url, headers=headers)</p>
<p class="p1"><span class="Apple-converted-space">        </span>response.raise_for_status()</p>
<p class="p1"><span class="Apple-converted-space">        </span>data = response.json()</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">        </span>latest_wod = data["wods"][0]</p>
<p class="p1"><span class="Apple-converted-space">        </span>title = latest_wod.get("name", "WOD")</p>
<p class="p1"><span class="Apple-converted-space">        </span>movements = [m.get("name", "Unknown Movement") for m in latest_wod.get("movements", [])]</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">        </span>return {</p>
<p class="p1"><span class="Apple-converted-space">            </span>"date": latest_wod.get("date", "Unknown Date"),</p>
<p class="p1"><span class="Apple-converted-space">            </span>"title": title,</p>
<p class="p1"><span class="Apple-converted-space">            </span>"movements": movements if movements else ["Movement details not available"]</p>
<p class="p1"><span class="Apple-converted-space">        </span>}</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">    </span>except Exception as e:</p>
<p class="p1"><span class="Apple-converted-space">        </span>print(f"BTWB API error: {e}")</p>
<p class="p1"><span class="Apple-converted-space">        </span>return {</p>
<p class="p1"><span class="Apple-converted-space">            </span>"date": "N/A",</p>
<p class="p1"><span class="Apple-converted-space">            </span>"title": "BTWB API Unavailable",</p>
<p class="p1"><span class="Apple-converted-space">            </span>"movements": ["Check your API key or network."]</p>
<p class="p1"><span class="Apple-converted-space">        </span>}</p>
<p class="p2"><br></p>
<p class="p1">@app.route("/")</p>
<p class="p1">def home():</p>
<p class="p1"><span class="Apple-converted-space">    </span>return render_template_string('''</p>
<p class="p1"><span class="Apple-converted-space">        </span>&lt;h1&gt;Generate BTWB Workout Graphic&lt;/h1&gt;</p>
<p class="p1"><span class="Apple-converted-space">        </span>&lt;form action="/generate"&gt;</p>
<p class="p1"><span class="Apple-converted-space">            </span>&lt;button type="submit"&gt;Generate Image&lt;/button&gt;</p>
<p class="p1"><span class="Apple-converted-space">        </span>&lt;/form&gt;</p>
<p class="p1"><span class="Apple-converted-space">    </span>''')</p>
<p class="p2"><br></p>
<p class="p1">@app.route("/generate")</p>
<p class="p1">def generate():</p>
<p class="p1"><span class="Apple-converted-space">    </span>data = get_btwb_workout()</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">    </span># Create a blank image</p>
<p class="p1"><span class="Apple-converted-space">    </span>img = Image.new('RGB', (1080, 1080), color='white')</p>
<p class="p1"><span class="Apple-converted-space">    </span>draw = ImageDraw.Draw(img)</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">    </span># Load fonts (macOS system fonts)</p>
<p class="p1"><span class="Apple-converted-space">    </span>try:</p>
<p class="p1"><span class="Apple-converted-space">        </span>title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Helvetica Bold.ttf", 60)</p>
<p class="p1"><span class="Apple-converted-space">        </span>text_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Helvetica.ttf", 45)</p>
<p class="p1"><span class="Apple-converted-space">    </span>except:</p>
<p class="p1"><span class="Apple-converted-space">        </span>title_font = text_font = ImageFont.load_default()</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">    </span># Add text</p>
<p class="p1"><span class="Apple-converted-space">    </span>draw.text((100, 50), "CSC", fill='red', font=title_font)</p>
<p class="p1"><span class="Apple-converted-space">    </span>draw.text((100, 150), "6AM // 9:30AM // 5:30PM", fill='black', font=text_font)</p>
<p class="p1"><span class="Apple-converted-space">    </span>draw.text((100, 300), data["title"], fill='black', font=title_font)</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">    </span>y = 400</p>
<p class="p1"><span class="Apple-converted-space">    </span>for move in data["movements"]:</p>
<p class="p1"><span class="Apple-converted-space">        </span>draw.text((100, y), move, fill='red', font=text_font)</p>
<p class="p1"><span class="Apple-converted-space">        </span>y += 80</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">    </span>draw.text((100, 1000), f"Workout of the Day {data['date']}", fill='black', font=text_font)</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">    </span># Save to BytesIO</p>
<p class="p1"><span class="Apple-converted-space">    </span>img_io = io.BytesIO()</p>
<p class="p1"><span class="Apple-converted-space">    </span>img.save(img_io, 'PNG')</p>
<p class="p1"><span class="Apple-converted-space">    </span>img_io.seek(0)</p>
<p class="p2"><br></p>
<p class="p1"><span class="Apple-converted-space">    </span>return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='btwb_workout.png')</p>
<p class="p2"><br></p>
<p class="p1">if __name__ == '__main__':</p>
<p class="p1"><span class="Apple-converted-space">    </span>app.run(debug=True)</p>
</body>
</html>
