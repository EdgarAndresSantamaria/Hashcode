

class Scanner:
    def __init__(self, book_num, library_num, days, books):
        self.book_num = book_num
        self.library_num = library_num
        self.days = days
        self.books = books
        self.libraries = []

    def __repr__(self):
        return '''<Scanner>: There are %d books, %d libraries, and %d days for scanning. The scores of the books are %s (in order).''' % (self.book_num, self.library_num, self.days, str(self.books))

    __str__ = __repr__

    def baseline(self):
        remaining_days = self.days
        results = []
        for library in self.libraries:
            remaining_days -= library.signin_days
            if remaining_days <= 0:
                break
            books = list(filter(lambda x: x in self.books, library.books))
            scanned = []
            for idx in range(0, len(books), library.capacity):
                if remaining_days <= 0:
                    break
                if idx + library.capacity <= len(books):
                    scanned.extend(books[idx:idx+library.capacity])
                else:
                    scanned.extend(books[idx:])
                remaining_days -= 1
            if len(scanned) > 0:
                results.append((library.index, scanned))

        return results

    def heuristic(self):
        remaining_days = self.days
        results = []
        ordered_libraries = self.Merry()
        prev = set([])
        used_days = 0
        for score, library in ordered_libraries:
            print(remaining_days)
            remaining_days += min(used_days, library.signin_days)
            remaining_days -= library.signin_days
            if remaining_days <= 0:
                break
            books = list(filter(lambda x: x in self.books and x not in prev, library.books))
            scanned = []
            used_days = 0
            for idx in range(0, len(books), library.capacity):
                if remaining_days <= 0:
                    break
                if idx + library.capacity <= len(books):
                    scanned.extend(books[idx:idx+library.capacity])
                else:
                    scanned.extend(books[idx:])
                remaining_days -= 1
                used_days += 1
            if len(scanned) > 0:
                results.append((library.index, scanned))
                prev.update(scanned)

        return results

    def Merry(self):
        scores = []
        for library in self.libraries:
            intersect = set(self.books) & set(library.books)
            scores.append(sum(intersect) / (library.signin_days + len(intersect) / library.capacity))
        scored_libraries = zip(scores, self.libraries)
        ordered_libraries = sorted(scored_libraries, key=lambda x: x[0])
        print(ordered_libraries)
        return ordered_libraries


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
        index = 0
        while True:
            line = f.readline()
            if not line.strip():
                break
            book_num, signin_days, capacity = tuple(map(int, line.split()))
            books = list(map(int, f.readline().split()))
            library = Library(index, book_num, signin_days, capacity, books)
            scanner.libraries.append(library)
            index += 1
    return scanner


def main(filename):
    scanner = read_data('data/'+filename)
    results = scanner.heuristic()
    with open('output/'+filename, 'w') as f:
        f.write(str(len(results)))
        f.write('\n')
        for r in results:
            f.write(' '.join((str(r[0]), str(len(r[1])))))
            f.write('\n')
            f.write(' '.join(map(str, r[1])))
            f.write('\n')


if __name__ == '__main__':
    # filename = 'a_example.txt'
    # main(filename)
    # filename = 'b_read_on.txt'
    # main(filename)
    filename = 'c_incunabula.txt'
    main(filename)
    # filename = 'd_tough_choices.txt'
    # main(filename)
    # filename = 'e_so_many_books.txt'
    # main(filename)
    # filename = 'f_libraries_of_the_world.txt'
    # main(filename)
