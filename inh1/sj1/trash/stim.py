import numpy
from PIL import Image
import sys
img = Image.open('green.png')


img = img.convert('RGBA')

p = 0.45 
data = numpy.array(img)
data[data>0] = (numpy.random.binomial(1, p, numpy.size(data[data>0]))+250)


red, green, blue, alpha = data.T
black_areas = (red == 0) & (blue == 0) & (green == 0) & (alpha == 250)
data[..., :-1][black_areas.T] = (0, 0, 255)
black_areas = (red == 0) & (blue == 0) & (green == 0) & (alpha == 251)
data[..., :-1][black_areas.T] = (0, 255, 0)


img1 = Image.fromarray(data)
img1.show()


imr = Image.open('red.png')
imb = Image.open('blue.png')
imr = imr.convert('RGBA')
imb = imb.convert('RGBA')

