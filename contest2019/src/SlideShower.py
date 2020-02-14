class SlideShower:

    def __init__(self, dataset):
        self._dataset = dataset
        self._vertical, self._horizontal = self.separate()
        self._v_sorted = None
        self._h_sorted = None
        self._used = []
        self._slides = []
        self.sort()

    def separate(self):
        vertical = {}
        horizontal = {}
        images = self._dataset['images']
        for key in images:
            image = images[key]
            if image['type'] == 'V':
                vertical[key] = image
            else:
                horizontal[key] = image
        return vertical, horizontal

    def sort(self):
        self._v_sorted = sorted(self._vertical.items(), key=lambda v: len(v[1]['tags']), reverse=True)
        self._h_sorted = sorted(self._horizontal.items(), key=lambda v: len(v[1]['tags']), reverse=True)

    @staticmethod
    def join_tags(tags_a, tags_b):
        return list(set(tags_a) | set(tags_b))

    @staticmethod
    def intersect_tags(tags_a, tags_b):
        return list(set(tags_a) & set(tags_b))

    @staticmethod
    def points(tags_a, tags_b):
        intersect = len(SlideShower.intersect_tags(tags_a, tags_b))
        return min(len(tags_a) - intersect, intersect, len(tags_b) - intersect)

    def get_biggest_slide(self):
        horizontal = self.get_biggest_h_slide()
        vertical = self.get_biggest_v_slide()
        if horizontal[0][1]['n_tags'] > len(SlideShower.join_tags(vertical[0][1]['tags'], vertical[1][1]['tags'])):
            return horizontal
        else:
            return vertical

    def get_biggest_h_slide(self):
        return self._h_sorted[0], None

    def get_biggest_v_slide(self):
        best_0 = None
        best_1 = None
        best_score = -1
        exit = False
        for i in range(0, len(self._v_sorted)):
            if exit:
                break
            else:
                for j in range(i + 1, len(self._v_sorted)):
                    image_0 = self._v_sorted[i][1]
                    image_1 = self._v_sorted[j][1]
                    if image_0['n_tags'] + image_1['n_tags'] < best_score:
                        exit = True
                        break
                    else:
                        joint = SlideShower.join_tags(image_0['tags'], image_1['tags'])
                        # TODO igual >
                        score = len(joint)
                        if score >= best_score:
                            best_score = score
                            best_0 = self._v_sorted[i]
                            best_1 = self._v_sorted[j]

        return best_0, best_1

    # ((id, image), (id, image))
    def get_best_match(self, slide):
        image_v_0 = slide[0][1]
        if slide[1]:
            image_v_1 = slide[1][1]
            tags = SlideShower.join_tags(image_v_0['tags'], image_v_1['tags'])
        else:
            tags = image_v_0['tags']
        best_0 = None
        best_1 = None
        best_score = -1

        for i in range(0, len(self._h_sorted)):
            image_key = self._h_sorted[i][0]
            image_h = self._h_sorted[i][1]
            if image_key not in self._used:
                score = SlideShower.points(tags, image_h['tags'])
                if score >= best_score:
                    best_score = score
                    best_0 = self._h_sorted[i]

        for i in range(0, len(self._v_sorted)):
            image_key_0 = self._v_sorted[i][0]
            image_v_0 = self._v_sorted[i][1]
            if image_key_0 not in self._used:
                for j in range(i + 1, len(self._v_sorted)):
                    image_key_1 = self._v_sorted[j][0]
                    image_v_1 = self._v_sorted[j][1]
                    if image_key_1 not in self._used:
                        joined_tags = SlideShower.join_tags(image_v_0['tags'], image_v_1['tags'])
                        score = SlideShower.points(tags, joined_tags)
                        if score >= best_score:
                            best_score = score
                            best_0 = self._v_sorted[i]
                            best_1 = self._v_sorted[j]

        if best_1:
            result = (best_0, None)
        else:
            result = (best_0, best_1)

        return result

    def use(self, slide):
        index_0 = slide[0][0]
        self._used.append(index_0)
        if slide[1]:
            index_1 = slide[1][0]
            self._used.append(index_1)
        else:
            index_1 = None
        self._slides.append((index_0, index_1))

    def main(self):
        self._used = []
        self._slides = []
        # slide: ((id, image),(id, image))
        initial_slide = self.get_biggest_slide()
        self.use(initial_slide)
        current_slide = initial_slide
        i = 0
        while True:
            print(i)
            i += 1
            next_slide = self.get_best_match(current_slide)
            if next_slide is (None, None):
                break
            else:
                self.use(next_slide)
        for slide in self._slides:
            print(slide)
        print(len(self._used))
