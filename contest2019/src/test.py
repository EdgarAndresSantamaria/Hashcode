from src.FileManager import FileManager
from src.SlideShower import SlideShower


def test1():
    fm = FileManager()
    # data = fm.read_input("c_memorable_moments.txt")
    data = fm.read_input("b_lovely_landscapes.txt")
    minH = 999999999999
    minV = 999999999999
    maxV = -1
    maxH = -1
    for image in data['images']:
        if image['type'] == 'V':
            minV = min(minV, len(image['tags']))
            maxV = max(maxV, len(image['tags']))
        else:
            minH = min(minH, len(image['tags']))
            maxH = max(maxH, len(image['tags']))
    print(minH)
    print(minV)
    print(maxH)
    print(maxV)


def test2():
    fm = FileManager()
    data = fm.read_input("c_memorable_moments.txt")
    # data = fm.read_input("b_lovely_landscapes.txt")
    foo = SlideShower(data)
    foo.main()


if __name__ == "__main__":
    test2()
