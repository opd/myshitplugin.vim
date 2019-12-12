#!/usr/bin/env python3
import re
import itertools as it

def create_pattern(pattern, all_occurences=False):
    # TODO filter letters
    pattern = list(pattern)
    result = ".*".join(pattern)
    if not all_occurences:
        result = "^.*%s.*$" % result

    return re.compile(result)


def _find_occurences(line, pattern):
    if not pattern:
        return []
    char = pattern[0]
    result = []
    for i, c in enumerate(line):
        if c == char:
            if len(pattern) == 1:
                result.append([0] * i + [1] + [0] * (len(line) - i - 1))
                continue
            recur_results = _find_occurences(line[(i+1):], pattern[1:])
            if recur_results:
                begin = [0] * i + [1]
                for res in recur_results:
                    result.append(begin + res)
    return result


def find_occurences(line, initial_pattern):
    pattern = r"[%s]" % initial_pattern
    pattern = re.compile(pattern)
    indexes = []
    chars = []
    for match in pattern.finditer(line):
        indexes.append(match.start())
        chars.append(match.group())
    short_line = "".join(chars)
    occurences = _find_occurences(short_line, initial_pattern)
    result = []
    for occurence in occurences:
        o = []
        for i, value in enumerate(occurence):
            if value:
                o.append(indexes[i])
        result.append(o)
    return result


def distance_rate(occurence):
    # data = list(i for i, x in enumerate(occurence) if x)
    data = occurence
    data = (b - a for a, b in zip(data, data[1:]))
    data = (1 / x for x in data)
    return sum(data)


def _get_weight(line, occurence):
    return distance_rate(occurence)


def get_weight(line, pattern):
    occurences = find_occurences(line, pattern)
    return max([_get_weight(line, occurence) for occurence in occurences])


def match_func(lines, str_, count):
    pattern = create_pattern(str_)
    result = []
    for line in lines:
        m = pattern.match(line)
        if m:
            weight = get_weight(line, str_)
            # weight = 0
            result.append((line, weight))
    result = sorted(result, reverse=True, key=lambda x: x[1])
    result = (x[0] for x in result)
    result = list(it.islice(result, 0, count))
    # result = [x + "<x>" for x in result]
    result = [x for x in result]
    return result


if __name__ == "__main__":
    import time
    from private_data import data
    items = data["items"]
    str_ = 'asd'
    count = 20
    start = time.time()
    lines = match_func(items, str_, count)
    print(lines)
    print(time.time() - start)
