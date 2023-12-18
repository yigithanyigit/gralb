from collections import OrderedDict


def remove_duplicates(input_list):
    seen = OrderedDict.fromkeys(input_list)

    result = list(seen.keys())

    return result


def print_instructions():
    print("Instructions:")
    #print("'m': Switch to the next object")
    #print("'n': Switch to the previous object")
    print("'r': Rotate camera clockwise around the y-axis")
    print("'f': Rotate camera counterclockwise around the y-axis")
    print("'e': Rotate camera clockwise around the x-axis")
    print("'q': Rotate camera counterclockwise around the x-axis")
    print("'w': Move camera forward")
    print("'s': Move camera backward")
    print("'a': Move camera left")
    print("'d': Move camera right")
    print("'o': Increase subdivision level for the current object")
    print("'l': Decrease subdivision level for the current object")
    print("'p': Toggle Wireframe Mode")
    print("'m': Rotate Clockwise In Z Axis")
    print("'n': Rotate Counter Clockwise In Z Axis")
    print("'Up Arrow': Rotate Up In X Axis")
    print("'Down Arrow': Rotate Down  In X Axis")
    print("'Right Arrow': Rotate Clockwise In Y Axis")
    print("'Left Arrow': Rotate Counter Clockwise In Y Axis")
    print("'Z': Reset View")
    print("Press 'Esc' to exit the program.")
