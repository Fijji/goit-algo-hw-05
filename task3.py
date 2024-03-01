import urllib.request
import timeit

def load_text(url):
    with urllib.request.urlopen(url) as f:
        text = f.read().decode('latin-1')  
    return text

def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))
    return -1

def kmp_search(text, pattern):
    def generate_prefix_table(pattern):
        prefix_table = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                prefix_table[i] = length
                i += 1
            else:
                if length != 0:
                    length = prefix_table[length - 1]
                else:
                    prefix_table[i] = 0
                    i += 1
        return prefix_table

    prefix_table = generate_prefix_table(pattern)
    i = 0
    j = 0
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
            if j == len(pattern):
                return i - j
        else:
            if j != 0:
                j = prefix_table[j - 1]
            else:
                i += 1
    return -1

def rabin_karp_search(text, pattern):
    def hash_func(string):
        hash_val = 0
        for char in string:
            hash_val = (hash_val * 256 + ord(char)) % 101
        return hash_val

    pattern_hash = hash_func(pattern)
    text_hash = hash_func(text[:len(pattern)])
    for i in range(len(text) - len(pattern) + 1):
        if text_hash == pattern_hash:
            if text[i:i + len(pattern)] == pattern:
                return i
        if i < len(text) - len(pattern):
            text_hash = (256 * (text_hash - ord(text[i]) * (256 ** (len(pattern) - 1))) + ord(text[i + len(pattern)])) % 101
    return -1

# Порівняти ефективність алгоритмів пошуку підрядка: Боєра-Мура, Кнута-Морріса-Пратта та Рабіна-Карпа на основі двох текстових файлів
file1_url = "https://drive.google.com/uc?id=18_R5vEQ3eDuy2VdV3K5Lu-R-B-adxXZh"
file2_url = "https://drive.google.com/uc?id=13hSt4JkJc11nckZZz2yoFHYL89a4XkMZ"
file1_text = load_text(file1_url)
file2_text = load_text(file2_url)

# Використовуючи timeit, треба виміряти час виконання кожного алгоритму для двох видів підрядків: одного, що дійсно існує в тексті, та іншого — вигаданого
existing_pattern = "пошуку"
fake_pattern = "fake_pattern"

# Результати
times = {
    "Боєра-Мура": {
        "file1_existing": timeit.timeit(lambda: boyer_moore_search(file1_text, existing_pattern), number=1),
        "file1_fake": timeit.timeit(lambda: boyer_moore_search(file1_text, fake_pattern), number=1),
        "file2_existing": timeit.timeit(lambda: boyer_moore_search(file2_text, existing_pattern), number=1),
        "file2_fake": timeit.timeit(lambda: boyer_moore_search(file2_text, fake_pattern), number=1)
    },
    "Кнута-Морріса-Пратта": {
        "file1_existing": timeit.timeit(lambda: kmp_search(file1_text, existing_pattern), number=1),
        "file1_fake": timeit.timeit(lambda: kmp_search(file1_text, fake_pattern), number=1),
        "file2_existing": timeit.timeit(lambda: kmp_search(file2_text, existing_pattern), number=1),
        "file2_fake": timeit.timeit(lambda: kmp_search(file2_text, fake_pattern), number=1)
    },
    "Рабіна-Карпа": {
        "file1_existing": timeit.timeit(lambda: rabin_karp_search(file1_text, existing_pattern), number=1),
        "file1_fake": timeit.timeit(lambda: rabin_karp_search(file1_text, fake_pattern), number=1),
        "file2_existing": timeit.timeit(lambda: rabin_karp_search(file2_text, existing_pattern), number=1),
        "file2_fake": timeit.timeit(lambda: rabin_karp_search(file2_text, fake_pattern), number=1)
    }
}

for algorithm, timings in times.items():
    print(f"Алгоритм: {algorithm}")
    for file, timing in timings.items():
        print(f"Файл: {file}, Час: {timing}")
    print()

fastest_algorithms = {
    "file1": min(times, key=lambda x: times[x]["file1_existing"]),
    "file2": min(times, key=lambda x: times[x]["file2_existing"]),
    "overall": min(times, key=lambda x: times[x]["file1_existing"] + times[x]["file2_existing"])
}

print("Найшвидший алгоритм:")
print(f"Для статті 1: {fastest_algorithms['file1']}")
print(f"Для статті 2: {fastest_algorithms['file2']}")
print(f"Загальний: {fastest_algorithms['overall']}")
