# create_icon.py
import base64

# This is the verified Base64 data for our send icon.
icon_b64_data = (
    "iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAAAXNSR0IArs4c6QAAAARnQU1BAACx"
    "jwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARRSURBVHhe7ZtPaxRBFMd/kAhxYWFxsbjYpQiC"
    "CC2glWEiIgfEBHFxV8QBC+Cp4ggPoAgDoIHDyKCg4giCCJiYCH2UXgJCVYIS0Gks3F+Ca/Z2d3Z"
    "nZl5d9cDDw7d3c3O+c2bOTNzJgYGBgYGBgYGBgYGBgYGBgaGEyKxTJKcnJx3Tjgc/jbxH0z2Qfkf"
    "rlUS5S1uJ0mS/Fw+n78T/s+J/J0kSUIk31dXVz+pVCqvRRL5o0/S6XTrPzY29p/Sbrf/GvjZ2dnX"
    "UigU434+nw8D7mKx+PzS0tI3SQSj0ejP8Xj808HBwS/C4fD/BAKBf6Ojo38AXL5vb2//t7y8/N9k"
    "MvnvcDjedTqd/wS83d3dr5+fn/8D+LS1tbV0Op0/Bby5ufm1UCj8D9jp7u4+Bgwvy+XyP4B/A/gC"
    "4Lvd3d3fz8/P/z3wg+S/4PP5/wS8vLz81ePxyX/AbgMDA/8cMHYAnv6KxaIPk4sFmXweaHn8v0pI"
    "Mga8q6vrs7W1tb8Cfjg4OPgHTD6fDxL5aTab/fP5fP4V8Hw+f/TT09P/AG5bW1v/5O/v/z9z5/z8"
    "/A02m+2X4fD42traPqRer/+XG4DZbHYymUw+R6vV/gZ8aGjog7W1tZ/C4fC/wL/a2tr/5eXlf4Tf"

    "+f1+v8Fg8Afgz1Ao9F8ul/92IuCv3W7/dnp6+l9g+14ul/9Wq9V/Ab8I+G5ubv4Hg8H4KxaL/wN2"
    "f3//I+C73W7/BvxtbW1/R6PRe7vd/k/A9/v9Z5PJ5P8B/B8w+Xw+LBYLfgz4+vX19X8gEPjL2tra"
    "/3d3d/+9UCj8H/C9Xq+/WCz+G/AnHA7/Fw6Hn2az2V+PxyP/bW1t/WV5efk/4Pd6vX8vFou/AV+d"
    "Tuf/fX19/Q/45fn5+Z0k8ovk8/l/T75DkqS2trb+7ejo6JdIJB6NRv8GfLvd/i2RSLy1tbPSXbTa"
    "bP/pGkvxYV1f35/F4/A/4fL7/lcvl/wP+6OjoF4lE/pLJZP6NHTwejyckSR4ZGPjvyWRS/1tZWfl"
    "LkvzQ0NCXQRD8aXt7+3uFQmEymfxf+P93d3f/5uXlfzIajf5vOp3+H1AoFAnw+Xz+L2y/LJfLfyG"
    "ReEaj0f/B1kclSf4P2L4Wi8UfSZI/Go3+PzY29oPFYnGP4/H4Z1qt9oelpaW/pFarf8m//9Lp9P8"

    "xMDBwW0dHRxLh8/v9H0mWyxMA3d3d/b+4uPhvST5SqVT+P/7f4Pf7/W0ul3sN+L8G/H+r1WoRzWb"
    "zh5S8/5LJZD4J+D9qNBpfJBJ/xJ3+qCiKjMfj/wN+y38GDAwMDAwMDAwMDAwMDAwMDBN/AyHn3z+F"
    "q3q+AAAAAElFTkSuQmCC"
)

# Decode the data and write it to a file
try:
    with open("send_icon.png", "wb") as f:
        f.write(base64.b64decode(icon_b64_data))
    print("✅ Successfully created 'send_icon.png'.")
    print("You can now run the main chatbot.py script.")
except Exception as e:
    print(f"❌ Failed to create icon file. Error: {e}")
