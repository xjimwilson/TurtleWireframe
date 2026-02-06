# Beta-0.41

ok so i didnt do anything with deltatime like i said i would, but i managed to HUGELY improve performance (around 20x or smn stupid) to the point where optimisation will not be needed for a long time. I did this by migrating from Turtle to RawTurtle, from the pyautogui module. This communicates at an even lower level, and performs WAAAY faster than regular turtle. This also means I can get to work on a gui for settings, options etc.  in the future.

- migrated from Turtle to RawTurtle
- massively increased performance
- Added pyautogui canvas for future gui updates
- changed from arrow key movement to mouse movement
- cleaned up code a little bit

next update ill polish LODs, because now i have more performance to spare. Also, I would like to eventually make an editor for the .bad3d filetype.




# Beta-0.35

i started to get back into this project again. this is what i changed:
Floorgrid now has 3 different LODs / sizes, depending on zoom from models. Still easily modifiable. I understand this will slow down performance, but looks a lot nicer.

-Fixed linesize function, it wasnt working at all but now it is hooray
-better error handling so less crashes, i learnt it in a college lesson
-streamlined file conversion, will be easier for me to add new features in the future (colour maybe??)

next ill be optimising performance, while still staying true to turtle. i could've used more optimised and modern imports, but it wouldn't be so fun would it? thinking about time.deltatime aswell, because it has a strange slowdown effect rn when lagging. thank you for reading these notes if you did.

ALSO GITHUB PULLED INSTEAD OF PUSHING AND OVERWROTE ALL OF MY BRANCH'S CODE. IT TOOK ME 2 HOURS TO REPROGRAM.
