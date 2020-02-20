

class Scanner:
    def __init__(self, book_num, library_num, days, books):
        self.book_num = book_num
        self.library_num = library_num
        self.days = days
        self.books = books

    def __repr__(self):
        return '''<Scanner>: There are %d books, %d libraries, and %d days for scanning. The scores of the books are %s (in order).''' % (self.book_num, self.library_num, self.days, str(self.books))

    __str__ = __repr__


class Library:
    def __init__(self, index, book_num, signin_days, capacity, books):
        self.index = index
        self.book_num = book_num
        self.signin_days = signin_days
        self.capacity = capacity
        self.books = books

    def __repr__(self):
        return '''<Library %d> has %d books, the signup process takes %d days, and the library can ship %d books per day. The books in library %d are: %s.''' % (self.index, self.book_num, self.signin_days, self.capacity, self.index, str(self.books))

    __str__ = __repr__


def read_data(filename):
    with open(filename) as f:
        book_num, library_num, days = tuple(map(int, f.readline().split()))
        books = list(map(int, f.readline().split()))
        scanner = Scanner(book_num, library_num, days, books)
        libraries = []
        index = 0
        while True:
            line = f.readline()
            if not line:
                break
            book_num, signin_days, capacity = tuple(map(int, line.split()))
            books = list(map(int, f.readline().split()))
            library = Library(index, book_num, signin_days, capacity, books)
            libraries.append(library)
            index += 1
    return scanner, libraries


if __name__ == '__main__':
    print(read_data('data/a_example.txt'))
