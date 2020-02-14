import os


class FileManager:

    def __init__(self, folder=None):
        if not folder:
            folder = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
        self._input_path = os.path.join(folder, "input")
        self._output_path = os.path.join(folder, "output")

    def read_input(self, filename):
        path = os.path.join(self._input_path, filename)
        with open(path, 'r') as file:
            first_line = file.readline()
            data = {
                'amount': int(first_line),
                'images': {}
            }
            i = 0
            for line in file:
                d = line.split(" ")
                image = {}
                image['type'] = d[0]
                image['n_tags'] = int(d[1])
                image['tags'] = d[2:]
                image['tags'][-1] = image['tags'][-1][:-1]
                data['images'][i] = image
                i += 1
        return data

    def write_file(self, filename, data):
        path = os.path.join(self._output_path, filename)
        with open(path, 'r') as file:
            file.write(data)
