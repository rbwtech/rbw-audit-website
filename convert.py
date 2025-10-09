from cairosvg import svg2png
from PIL import Image

svg2png(url='icon.svg', write_to='icon.png')
img = Image.open('icon.png')
img.save('icon.ico', format='ICO', sizes=[(256, 256)])