from collections import OrderedDict


def remove_duplicates(input_list):
    seen = OrderedDict.fromkeys(input_list)

    result = list(seen.keys())

    return result


def convert_list_to_tuple(func):
    def inner(*args, **kwargs):
        converted_args = tuple(arg if not isinstance(arg, list) else tuple(arg) for arg in args)
        converted_kwargs = {key: value if not isinstance(value, list) else tuple(value) for key, value in
                            kwargs.items()}

        return func(*converted_args, **converted_kwargs)

    return inner


def print_instructions():
    print("Instructions:")
    # print("'m': Switch to the next object")
    # print("'n': Switch to the previous object")
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
    print("'b': Fading Next Texture")
    print("'v': Fading Previous Texture")
    print("'p': Toggle Wireframe Mode")
    print("'m': Rotate Clockwise In Z Axis")
    print("'n': Rotate Counter Clockwise In Z Axis")
    print("'Up Arrow': Rotate Up In X Axis")
    print("'Down Arrow': Rotate Down  In X Axis")
    print("'Right Arrow': Rotate Clockwise In Y Axis")
    print("'Left Arrow': Rotate Counter Clockwise In Y Axis")
    print("'Z': Reset View")
    print("----------------")
    print("IMPORTANT NOTE")
    print("If objects does not include a triangle surface then it can be subdivided otherwise subdivision doesnt work!")
    print("i.e.: Cube can be subdivided but sphere not.")
    print("----------------")
    print("Press 'Esc' to exit the program.")


class BaseSingletonList:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.data = []
            self.data_dict = dict()
            self.initialized = True

    @convert_list_to_tuple
    def check(self, unique):
        if hash(unique) in self.data_dict:
            return True
        return False

    @convert_list_to_tuple
    def add_to_data(self, data, unique):
        if self.check(unique) is False:
            self.data.append(data)
            self.add_to_dict(data, unique)

    @convert_list_to_tuple
    def delete_from_data(self, data, unique):
        if self.check(unique) is True:
            self.data.remove(data)
            del self.data_dict[hash(unique)]

    @convert_list_to_tuple
    def add_to_dict(self, data, unique):
        self.data_dict[hash(unique)] = data

    @convert_list_to_tuple
    def get_from_value(self, key):
        return self.data_dict[hash(key)]
