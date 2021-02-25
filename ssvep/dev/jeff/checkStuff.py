from psychopy.hardware import keyboard
from psychopy import core

kb = keyboard.Keyboard()

# during your trial
kb.clock.reset()  # when you want to start the timer from
keys = kb.getKeys()
if 'q' in keys:
    core.quit()
for key in keys:
    print(key.name, key.rt, key.duration)
    
