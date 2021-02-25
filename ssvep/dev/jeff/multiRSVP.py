import string

import numpy as np

import psychopy.visual
import psychopy.event
import psychopy.misc


letters = string.letters[:26]

win = psychopy.visual.Window(
    size=(800, 800),
    units="pix",
    fullscr=False
)

n_text = 26
text_cap_size = 34

text_strip_height = n_text * text_cap_size

text_strip = np.full((text_strip_height, text_cap_size), np.nan)

text = psychopy.visual.TextStim(win=win, height=32, font="Courier")

cap_rect_norm = [
    -(text_cap_size / 2.0) / (win.size[0] / 2.0),  # left
    +(text_cap_size / 2.0) / (win.size[1] / 2.0),  # top
    +(text_cap_size / 2.0) / (win.size[0] / 2.0),  # right
    -(text_cap_size / 2.0) / (win.size[1] / 2.0)   # bottom
]

# capture the rendering of each letter
for (i_letter, letter) in enumerate(letters):

    text.text = letter.upper()

    buff = psychopy.visual.BufferImageStim(
        win=win,
        stim=[text],
        rect=cap_rect_norm
    )

    i_rows = slice(
        i_letter * text_cap_size,
        i_letter * text_cap_size + text_cap_size
    )

    text_strip[i_rows, :] = (
        np.flipud(np.array(buff.image)[..., 0]) / 255.0 * 2.0 - 1.0
    )

# need to pad 'text_strip' to pow2 to use as a texture
new_size = max(
    [
        int(np.power(2, np.ceil(np.log(dim_size) / np.log(2))))
        for dim_size in text_strip.shape
    ]
)

pad_amounts = []

for i_dim in range(2):

    first_offset = int((new_size - text_strip.shape[i_dim]) / 2.0)
    second_offset = new_size - text_strip.shape[i_dim] - first_offset

    pad_amounts.append([first_offset, second_offset])

text_strip = np.pad(
    array=text_strip,
    pad_width=pad_amounts,
    mode="constant",
    constant_values=0.0
)

# position the elements on a circle
el_thetas = np.linspace(0, 360, n_text, endpoint=False)
el_rs = 300
el_xys = np.array(psychopy.misc.pol2cart(el_thetas, el_rs)).T

# make a central mask to show just one letter
el_mask = np.ones(text_strip.shape) * -1.0

# start by putting the visible section in the corner
el_mask[:text_cap_size, :text_cap_size] = 1.0

# then roll to the middle
el_mask = np.roll(
    el_mask,
    (new_size / 2 - text_cap_size / 2, ) * 2,
    axis=(0, 1)
)

# work out the phase offsets for the different letters
base_phase = (
    (text_cap_size * (n_text / 2.0)) - (text_cap_size / 2.0)
) / new_size

phase_inc = (text_cap_size) / float(new_size)

phases = np.array(
    [
        (0.0, base_phase - i_letter * phase_inc)
        for i_letter in range(n_text)
    ]
)

# random colours
colours = np.random.uniform(low=-1.0, high=1.0, size=(n_text, 3))

els = psychopy.visual.ElementArrayStim(
    win=win,
    units="pix",
    nElements=n_text,
    sizes=text_strip.shape,
    xys=el_xys,
    phases=phases,
    colors=colours,
    elementTex=text_strip,
    elementMask=el_mask
)

win.recordFrameIntervals = True

keep_going = True

i_frame = 0

while keep_going:

    if np.mod(i_frame, 5) == 0:
        els.phases = phases[np.random.choice(n_text, size=n_text), :]
        els.colors = colours[np.random.choice(n_text, size=n_text), :]

    els.draw()

    win.flip()

    keys = psychopy.event.getKeys()

    keep_going = not "q" in keys

    i_frame += 1

win.close()

