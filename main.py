from collections import OrderedDict


class IntervalCoding:

    def __init__(self, text):
        self.text = text
        self.start = 0
        self.end = 1

    def get_frequency_occurrence(self):
        frequency = {key: self.text.count(key) for key in self.text}
        return OrderedDict(sorted(frequency.items(), key=lambda item: item[1], reverse=True))

    def create_intervals(self):
        intervals = {}
        frequency = self.get_frequency_occurrence()
        for char, freq in frequency.items():
            self.end = self.start + freq / len(self.text)
            intervals[char] = (self.start, self.end)
            self.start = self.end
        return intervals

    def assign_codes(self, intervals):
        intervals = intervals
        codes = {}
        current_code = '0'
        for char, interval in intervals.items():
            code = current_code
            current_code = bin(int(current_code, 2) + 1)[2:]
            codes[char] = code.zfill(24)
        return codes

    def get_encoded_text(self, codes):
        encoded_text = ''
        for char in self.text:
            encoded_text += codes[char]
        return encoded_text

    def decode(self, encoded_text, codes):
        decoded_text = ""
        code = ""

        for bit in encoded_text:
            code += bit
            for char, char_code in codes.items():
                if code == char_code:
                    decoded_text += char
                    code = ""
                    break

        return decoded_text


def main():
    text = 'Привет, как твои дела? У меня все просто замечательно, я написал алгоритм интервального кодирования!'
    my_object = IntervalCoding(text)
    intervals = my_object.create_intervals()
    codes = my_object.assign_codes(intervals)
    encoded_text = my_object.get_encoded_text(codes)
    decoded_text = my_object.decode(encoded_text, codes)
    print(decoded_text)


if __name__ == '__main__':
    main()
