
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




cdef float _get_weight(char* line, char* pattern, int line_len, int pattern_len):
    cdef char line_char, pattern_char, first_pattern_char = pattern[0]
    cdef int pattern_index, line_start, line_index, last_found_index
    cdef float weight, max_weight = 0
    for line_start in range(line_len):
        pattern_index = 0
        weight = 0
        last_found_index = -1
        pattern_char = pattern[pattern_index]
        if line[line_start] != first_pattern_char:
            continue
        for line_index in range(line_start, line_len):
            line_char = line[line_index]
            if line_char == pattern_char:
                if last_found_index != -1:
                    weight += 1.0 / (line_index - last_found_index)
                last_found_index = line_index
                pattern_index += 1
                if pattern_index == pattern_len:
                    max_weight = max(weight, max_weight)
                    break
                pattern_char = pattern[pattern_index]
        if weight == 0:
            break
    return max_weight


cpdef get_weight(line, pattern):
    line_len = len(line)
    pattern_len = len(pattern)
    line = line.encode('UTF-8')
    pattern = pattern.encode('UTF-8')
    return _get_weight(line, pattern, line_len, pattern_len)

cpdef main():
    # D = 68
    # P = 80
    # e = 101
    # i = 105
    # p = 112
    # w = 119
    line = "pewDiePiepDP"
    # line = "ppDP"
    pattern = "pDP"
    pattern = ""
    w = get_weight(line, pattern)
    print("HELLO", w)
