
# def find_occurences(char* line, char* pattern):
#     if not pattern:
#         return []
#     char = pattern[0]
#     result = []
#     for i, c in enumerate(line):
#         if c == char:
#             if len(pattern) == 1:
#                 result.append([0] * i + [1] + [0] * (len(line) - i - 1))
#                 continue
#             recur_results = find_occurences(line[(i+1):], pattern[1:])
#             if recur_results:
#                 begin = [0] * i + [1]
#                 for res in recur_results:
#                     result.append(begin + res)
#     return result


cpdef find_occurences(char* line, char* pattern):
    cdef char pattern_char
    cdef int pattern_index
    for pattern_index, pattern_char in enumerate(pattern):
        print(pattern_index, pattern_char)

    if not pattern:
        return []
    char = pattern[0]
    result = []
    for i, c in enumerate(line):
        if c == char:
            if len(pattern) == 1:
                result.append([0] * i + [1] + [0] * (len(line) - i - 1))
                continue
            recur_results = find_occurences(line[(i+1):], pattern[1:])
            if recur_results:
                begin = [0] * i + [1]
                for res in recur_results:
                    result.append(begin + res)
    return result


def distance_rate(occurence):
    data = list(i for i, x in enumerate(occurence) if x)
    data = [ b - a for a, b in zip(data, data[1:]) ]
    data = [ 1 / x for x in data ]
    return sum(data)


cpdef get_weight(line, pattern):
    line = line.encode('UTF-8')
    pattern = pattern.encode('UTF-8')
    occurences = find_occurences(line, pattern)
    return max([distance_rate(occurence) for occurence in occurences])

cpdef main():
    line = "pewDiePie"
    pattern = "pDP"
    w = get_weight(line, pattern)
    print("HELLO", w)
