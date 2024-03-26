from collections import OrderedDict


class LZ78Coding:

    def __init__(self, text):
        self.text = text

    def lz78_compress(self):
        dictionary = {}
        encoded_text = []
        current_phrase = ""

        for symbol in self.text:
            current_phrase += symbol
            if current_phrase not in dictionary:
                if len(current_phrase) == 1:
                    encoded_text.append((0, symbol))
                else:
                    encoded_text.append((dictionary[current_phrase[:-1]], symbol))
                dictionary[current_phrase] = len(dictionary) + 1
                current_phrase = ""

        return encoded_text

    def lz78_decompress(self, compressed_text):
        dictionary = {0: ''}
        decompressed_text = ""

        for index, symbol in compressed_text:
            if index == 0:
                decompressed_text += symbol
                dictionary[len(dictionary)] = symbol
            else:
                phrase = dictionary[index] + symbol
                decompressed_text += phrase
                dictionary[len(dictionary)] = phrase

        return decompressed_text


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
    with open('text.txt', 'r', encoding='utf-8') as file:
        text = file.read()
    my_object_interval = IntervalCoding(text)
    intervals = my_object_interval.create_intervals()
    codes = my_object_interval.assign_codes(intervals)
    encoded_text = my_object_interval.get_encoded_text(codes)

    with open('interval.txt', 'w', encoding='utf-8') as file:
        file.write(encoded_text)

    my_object_lz78 = LZ78Coding(encoded_text)
    compressed_text = my_object_lz78.lz78_compress()

    with open('lz78.txt', 'w', encoding='utf-8') as file:
        file.write(str(compressed_text))

    decompressed_text = my_object_lz78.lz78_decompress(compressed_text)
    decoded_text = my_object_interval.decode(decompressed_text, codes)

    with open('result.txt', 'w', encoding='utf-8') as file:
        file.write(decoded_text)


if __name__ == '__main__':
    main()
