import random
import time
from pathlib import Path
import logging
from schema import Problem, Transition

# problem: Growth (easy)
# parameter of ease : simple building from the right works 
def puzzles_1(start_string = 'A', iterations = 15) :
    transitions = {
        'A': 'AB', 
        'B': 'BA',
    }

    lhs = ['A', 'B']
    ind = [-1, -1]

    emp_string = start_string
    while (iterations) :
        for i, l in enumerate(lhs) :
            ind[i] = emp_string.find(l)

        sel = random.randint(0, len(lhs) - 1)
        while(ind[sel] == -1) :
            sel = random.randint(0, len(lhs) - 1)
        
        emp_string = emp_string.replace(lhs[sel], transitions[lhs[sel]], 1)
        iterations -= 1
    
    transitions[emp_string] = ""

    transitions_list = [{key: value} for key, value in transitions.items()]
    save_problem("004", start_string, transitions_list)
    return emp_string

# Bow [game]
# medium variant: 1 bow and enemies on the same side [randomize the position]
# hard invariant : 2 bows with enemies on either side
# harder invariant (idea) :: bow cannot be used more than once.. 'P}.' -> 'P#-'
def puzzles_2(easy_level = 1, length_param = 15):
    num_enemies = random.randint(1, length_param / 3)
    test_string = ""

    transitions = {
        '.P': 'P.',
        'P.': '.P',
        '}P': 'P}',
        'P}': '}P',
        '{P': 'P{',
        'P{' : '{P',
        'P}.': 'P}>',
        '.{P': '<{P',
        '>E' : '..',
        'E<' : '..',
        '>.' : '.>',
        '.<' : '<.',
    }

    if easy_level == 1 :
        bow_pos = random.randint(0, length_param - 1 - num_enemies - 1) # the P and the enemies have to come after
        enemy_pos = []

        mn = length_param + 1
        for i in range(0, num_enemies) :
            sel = random.randint(bow_pos + 2, length_param - 1)
            while(enemy_pos.count(sel) > 0) :
                sel = random.randint(bow_pos + 2, length_param - 1)
            mn = min(mn, sel)
            enemy_pos.append(sel)

        loc_p = random.randint(0, mn - 1)
        while loc_p == bow_pos:
            loc_p = random.randint(0, mn - 1)
        
        for i in range(0, length_param) :
            if i == bow_pos:
                test_string = test_string + '}' 
            elif i in enemy_pos :
                test_string = test_string + 'E' 
            elif i == loc_p:
                test_string = test_string + 'P'
            else :
                test_string = test_string + '.'
    elif easy_level == 2 :
        enemy_pos = []

        en_after = random.randint(1, num_enemies - 1)
        en_before = num_enemies - en_after

        bow_pos = random.randint(en_before + 2, length_param - 1 - en_after - 1)
        
        mn = length_param + 1
        for i in range(0, en_after) :
            sel = random.randint(bow_pos + 2, length_param - 1)
            while(enemy_pos.count(sel) > 0) :
                sel = random.randint(bow_pos + 2, length_param - 1)
            
            mn = min(mn, sel)
            enemy_pos.append(sel)
        
        mx = -1
        for i in range(0, en_before) :
            sel = random.randint(0, bow_pos - 3)
            while(enemy_pos.count(sel) > 0) :
                sel = random.randint(0, bow_pos - 3)
            
            mx = max(mx, sel)
            enemy_pos.append(sel)
        
        loc_p = random.randint(mx + 1, mn - 1)
        while loc_p == bow_pos or loc_p == bow_pos - 1 :
            loc_p = random.randint(mx + 1, mn - 1)

        for i in range(0, length_param) :
            if i == bow_pos:
                test_string = test_string + '}' 
            elif i == bow_pos - 1:
                test_string = test_string + '{'
            elif i in enemy_pos :
                test_string = test_string + 'E' 
            elif i == loc_p:
                test_string = test_string + 'P'
            else :
                test_string = test_string + '.'

    empty_string = ('.'*length_param) + 'P'
    transitions[empty_string] = ""

    transitions_list = [{key: value} for key, value in transitions.items()]
    
    if easy_level == 1 :
        save_problem("005", test_string, transitions_list)
    else :
        save_problem("006", test_string, transitions_list)
    # print(test_string)
    return empty_string


def generate_random_nested_sequence(max_pairs):
    def helper(open_count, close_count, sequence):
        if open_count == max_pairs and close_count == max_pairs:
            return sequence
        
        options = []
        if open_count < max_pairs:
            options.append(("[", open_count + 1, close_count))
        if close_count < open_count:
            options.append(("]", open_count, close_count + 1))
        
        next_bracket, new_open_count, new_close_count = random.choice(options)
        return helper(new_open_count, new_close_count, sequence + next_bracket)
    
    return helper(0, 0, "")


# easy to medium
# probably, the length of the sequence affects the difficulty
# motivated from brackets
def puzzles_3(problem_id) :
    bracks = random.randint(5, 20)
    empty_seq = generate_random_nested_sequence(bracks)
    # print(empty_seq)

    transitions = {
        '?': '[',
        '?': ']',
    }

    missing = random.randint(1, len(empty_seq))
    misses = []
    for i in range(0, missing) :
        sel = random.randint(0, len(empty_seq) - 1)
        while sel in misses :
            sel = random.randint(0, len(empty_seq) - 1)
        misses.append(sel)
    
    test_string = ''
    for i in range(0, len(empty_seq)) :
        if i in misses :
            test_string = test_string + '?'
        else :
            test_string = test_string + empty_seq[i]
        
    transitions[empty_seq] = ""
    transitions_list = [{key: value} for key, value in transitions.items()]
    save_problem(problem_id, test_string, transitions_list)

    return empty_seq;        

#easy 2048 game
def puzzles_4(problem_id) :
    start = '^$'
    transitions = {
        '^':'^1',
    }
    
    i = 1
    for j in range(0, 11):
        transitions[str(i) + "" + str(i)] = "" + str(i * 2)
        i = i * 2
    empty_seq = "^2048$"
    transitions[empty_seq] = ""
    transitions_list = [{key: value} for key, value in transitions.items()]

    save_problem(problem_id, start, transitions_list)
    return empty_seq

# moderate to difficult
# three words
def puzzle_5(problem_id, num_words = 7):
    start = ""

    w1 = "shimmer"
    w2 = "trimmer"
    w3 = "trim"

    transition = {
        "trim" : "",
        "trimmer": "",
        "shimmer": ""
    }

    n1 = random.randint(0, num_words - 3)      # shimmer 
    n2 = random.randint(0, num_words - n1)     # trimmer
    n3 = num_words - n1 - n2        # trim

    lst = []
    for i in range(n1 + n2):
        lst.append(0)

    complete = 0
    n1c = 0
    n2c = 0
    n3c = 0
    while complete < num_words :
        chose = random.randint(0, 3)

        if chose == 0 :
            if n1c == n1 : 
                continue
            ch2 = random.randint(0, n1 - 1)
            while lst[ch2] == 7 :
                ch2 = random.randint(0, n1 - 1)

            step = random.randint(0, 7 - lst[ch2] - 1) + 1
            start = start + w1[lst[ch2]:lst[ch2] + step:1]
            lst[ch2] += step

            if lst[ch2] == 7:
                complete += 1
                n1c += 1
        elif chose == 1 :
            if n2c == n2 : 
                continue
            ch2 = random.randint(0, n2 - 1)
            while lst[n1 + ch2] == 7 :
                ch2 = random.randint(0, n2 - 1)

            step = random.randint(0, 7 - lst[n1 + ch2] - 1) + 1
            start = start + w2[lst[n1 + ch2]:lst[n1 + ch2] + step:1]
            lst[n1 + ch2] += step

            if lst[n1 + ch2] == 7:
                complete += 1
                n2c += 1
        else : 
            if n3c == n3 : 
                continue
            start = start + w3
            complete += 1
            n3c += 1
    # print(start)
    emp_string = ""

    transitions_list = [{key: value} for key, value in transition.items()]
    save_problem(problem_id, start, transitions_list)
    return emp_string


def generate_nested_strings(str, count) :
    iterations = 0
    string_to_return = ""
    while iterations < count :
        pos = random.randint(0, len(string_to_return))
        string_to_return = string_to_return[0:pos] + str + string_to_return[pos:]
        iterations += 1
    return string_to_return

# nested levels (arbitrary) --- medium(12) and long(25) strings (2-tests)
# Omikuji representative [with the initial string given] => 2-examples (puzzle_6)
# Omikuji representative [with 4-options out of which only one is correct] => 1-example (puzzle_7)
def puzzle_6(problem_id, count = 5) :
    transitions =  [
        {"ABC": ""},
    ]
    start_string = generate_nested_strings("ABC", count)
    empty_string = ""
    save_problem(problem_id, start_string, transitions)
    return empty_string

def puzzle_7(problem_id, count = 5) :
    transitions =  [
        {"ABC": ""},
    ]

    starts = []
    starts.append(generate_nested_strings("ABC", count))
    starts.append(generate_nested_strings("ABC", count))
    starts.append(generate_nested_strings("ABC", count))
    starts.append(generate_nested_strings("ABC", count))

    correct = random.randint(0, 3)
    for i in range(4): 
        if i == correct :
            transitions.append({"" : starts[i]})
        else:
            r = random.randint(0, len(starts[i]))
            fake = starts[i][:r] + "AB" + starts[i][r:]
            transitions.append({"" : fake})

    empty_string = ""
    save_problem(problem_id, "", transitions)
    return empty_string


# A8B13C11
# variant1 : easy version with A, B and C (level = 0)
# variant2 : harder version with A, B, C and D (level = 1) ///// --- improve
def puzzle_8(problem_id, level = 0):
    transitions = []
    str = ""
    if level == 0 : 
        str = "ABC"
    else :
        str = "ABCD"
    
    for i in range(len(str) - 1):
        for j in str[i + 1:]:
            src = str[i] + j
            transitions.append({src: ""})
    
    start_string = ""

    r1 = random.randint(7, 50)
    r2 = random.randint(7, 50)

    if level == 0 :
        diff = max(r1, r2) - min(r1, r2)
        mn = min(r1, r2)

        r3 = random.randint(diff, diff + 2 * mn)
        if ( r3 - diff ) % 2 == 1 : 
            r3 += 1
        
        for i in range(r1) :
            start_string += 'A'
        for i in range(r3) :
            start_string += 'B'
        for i in range(r2) :
            start_string += 'C'
    else :
        diff = max(r1, r2) - min(r1, r2)
        mn = min(r1, r2)

        r3 = random.randint(0, 50)
        r4 = random.randint(max(0, diff - r3), 2 * mn)

        if (r3 + r4 - diff) % 2 == 1:
            r4 += 1

        # #keeping r4 > r3
        
        for i in range(r1) :
            start_string += 'A'
        for i in range(r3) :
            start_string += 'B'
        for i in range(r4) :
            start_string += 'C'
        for i in range(r2) :
            start_string += 'D'
    
    empty_string = ""
    save_problem(problem_id, start_string, transitions)
    return empty_string

# A <-> B <-> C (inferred from A <-> B)
# the difference with the actual problem is that C and A are not directly interconvertible but convertible only via B
def puzzle_9(problem_id, length = 10) :
    empty_string = ""

    chars = ['A', 'B', 'C']
    for i in range(length) :
        r = random.randint(0, 2)
        empty_string = empty_string + chars[r]

    start_string = 'A' * length
    transitions = [
        {'A': 'B'},
        {'B': 'C'},
        {'C': 'B'},
        {'B': 'A'},
    ]
    
    transitions.append({empty_string: ""})
    save_problem(problem_id, start_string, transitions)
    return empty_string


# # March (variation in the final puzzle setting)
# def puzzle_10(problem_id, length = 10) :
#     hashes = 5      # because of the unique nature of the problem they have to remain at 5

#     pos = []
#     for i in range(5): 
#         r = random.randint(0, length)
#         while r in pos:
#             r = random.randint(0, length)
#         pos.append(r)
    
#     target_string = ""
#     for i in range(length) :
#         if i in pos :
#             target_string = target_string + '#'
#         else :
#             target_string = target_string + "."
        
#     transitions = [
#         {'#.': '.#'},
#         {'##.': '.##'}
#     ]
#     transitions.append({target_string: ""})
#     save_problem(problem_id, )
#     return target_string


# # 2 tests for Calculate in Any Order (base 5 and 7)
# def generate_transition_list(base = 5):
#     transitions = []
#     rev_transitions = dict()
#     for i in range(0, base):
#         for j in range(0, base): 
#             r1 = (i + j) % base
#             r2 = (i * j) % base
        
#             transitions.append({'{i}+{j}' : '{r1}'})
#             transitions.append({'{i}*{j}' : '{r2}'})

#             rev_transitions[r1].append('{i}+{j}')
#             rev_transitions[r2].append('{i}*{j}')
#     return transitions, rev_transitions

# def puzzle_11(iterations = 10, base = 5) :
#     start_string = '2=2'
#     empty_string = '2=2'

#     (transitions, rev_transitions) = generate_transition_list(base)
#     for i in range(iterations) :
#         r = random.randint(0, i)

#         cnt = 0
#         for j in range(len(start_string)):
#             ch = start_string[j]
#             if ch != '+' and ch != '*' and ch != '=':
#                 if cnt == r :
#                     r2 = random.randint(0, len(rev_transitions[int(ch)]))
#                     start_string = start_string[:j] + rev_transitions[int(ch)][r2] + start_string[j+1:]
#                     break
#                 cnt += 1
    
#     print(start_string)
#     return empty_string

def generate_transition_list(base=5):
    transitions = []
    rev_transitions = {i: [] for i in range(base)}  # Initialize lists for each remainder

    for i in range(base):
        for j in range(base): 
            r1 = (i + j) % base
            r2 = (i * j) % base
        
            transitions.append({f'{i}+{j}': f'{r1}'})
            transitions.append({f'{i}*{j}': f'{r2}'})

            rev_transitions[r1].append(f'{i}+{j}')
            rev_transitions[r2].append(f'{i}*{j}')
    
    return transitions, rev_transitions

def puzzle_11(problem_id, iterations=10, base=5):
    start_string = '2=2'
    empty_string = '2=2'

    transitions, rev_transitions = generate_transition_list(base)
    for i in range(iterations):
        r = random.randint(0, i)  # Ensure r is not 0 when i is 0

        cnt = 0
        for j in range(len(start_string)):
            ch = start_string[j]
            if ch.isdigit():  # Check for digits only
                if cnt == r:
                    possible_revs = rev_transitions.get(int(ch), [])
                    if possible_revs:  # Check if there's anything to replace
                        r2 = random.randint(0, len(possible_revs) - 1)
                        start_string = start_string[:j] + possible_revs[r2] + start_string[j+1:]
                        break
                cnt += 1
    
    # print(start_string)
    transitions.append({empty_string : ""})
    save_problem(problem_id, start_string, transitions)
    return empty_string

# # Example Tests
# puzzle_11(5, 5)
# puzzle_11(5, 7)


# MISSISSIPPI example for (HELLO WORLD 4) 
def puzzle_12(problem_id, check = "MISSISSIPPI"):
    transitions = []
    for i in range(len(check)) :
        if {check[i]:check[i:i+2]} not in transitions :
            transitions.append({check[i] : check[i:i+2]})
    
    start_string = check[0]
    empty_string = check
    transitions.append({empty_string : ""})

    save_problem(problem_id, start_string, transitions)

    return empty_string


# binary increment
def puzzle_13(problem_id) :
    length = random.randint(10, 50)
    empty_string = "1"
    for i in range(length) :
        r = random.randint(0, 1)
        empty_string = empty_string + str(r)
    
    start_string = '0'
    transitions = [
        {'0': '1'},
        {'1': '10'}
    ]
    transitions.append({empty_string: ""})

    save_problem(problem_id, start_string, transitions)
    return empty_string

# ternary_increment
def puzzle_14(problem_id) :
    length = random.randint(10, 50)
    empty_string = "1"
    for i in range(length) :
        r = random.randint(0, 2)
        empty_string = empty_string + str(r)

    start_string = '0'
    transitions = [
        {"0": "1"},
        {"1": "2"},
        {"2": "10"}
    ]
    
    transitions.append({empty_string: ""})
    save_problem(problem_id, start_string, transitions)
    return empty_string

# based on brackets + smiles (problem name is Pokeball "(-)" )
def puzzle_15(problem_id, iterations = 10):
    start_string = ""
    for _ in range(iterations) :
        r = random.randint(0, len(start_string))
        start_string = start_string[0:r] + "(-)" + start_string[r:]
    empty_string = ""
    transitions = [
        {"(-)": ""}
    ]

    save_problem(problem_id, start_string, transitions)
    return empty_string

# as you like modification
# puzzle_16 ::: easy version
# puzzle_17 ::: with step limit
def puzzle_16(problem_id, iterations = 7):
    start_string = ""
    possibles = ['AA', 'AB', 'BA', 'BB']
    for i in range(iterations) :
        r = random.randint(0, 3)
        start_string = start_string + possibles[r]

    transitions = []
    for i in range(4):
        for j in range(4) :
            transitions.append({possibles[i] : possibles[j]})
    
    # note here 
    empty_string = start_string
    transitions.append({empty_string: ""})

    start_string = "A" * len(empty_string)
    save_problem(problem_id, start_string, transitions)
    return empty_string

def puzzle_17(problem_id, iterations = 5) :
    length = random.randint(7, 12)
    
    end_string = ""
    start_string = ""
    for _ in range(length): 
        r = random.randint(0, 1)
        if r == 0 :
            start_string = start_string + 'A'
        else :
            start_string = start_string + 'B'
    
    end_string = start_string
    possibles = ['AA', 'AB', 'BA', 'BB']
    for _ in range(iterations) :
        r = random.randint(0, len(possibles) - 1)
        indx = end_string.find(possibles[r])

        while indx == -1:
            r = random.randint(0, len(possibles) - 1)
            indx = end_string.find(possibles[r])
        
        r2 = random.randint(0, 3)
        end_string = end_string[0:indx] + possibles[r2] + end_string[indx + 2:]
    
    empty_string = ('z' * iterations) + end_string
    transitions = []
    for i in range(4):
        for j in range(4) :
            transitions.append({possibles[i] : 'z' + possibles[j]})
    transitions.append({'Az' : 'zA'})
    transitions.append({'Bz' : 'zB'})
    transitions.append({empty_string: ""})

    save_problem(problem_id, start_string, transitions)
    return empty_string
        
# problem is MISSISSIPPI
def puzzle_18(problem_id, iterations = 6) :
    word = "MISSISSIPPI"
    for i in range(iterations) :
        r = random.randint(0, len(word))
        word = word[:r] + "SS" + word[r:]
    
    transitions = [
        {"SS" : "$$"},
        {"SS" : ""}
    ]
    empty_string = "MISSISSIPPI"
    transitions.append({
        empty_string : ""
    })

    save_problem(problem_id, word, transitions)

    return word

def generate_string(symbol, transitions, min_length):
    # Create a dictionary for quick lookup of production rules
    production_rules = {}
    for rule in transitions:
        for key, value in rule.items():
            if key not in production_rules:
                production_rules[key] = []
            production_rules[key].append(value)
    
    # Recursive function to expand the symbol
    def expand(symbol):
        if symbol not in production_rules:
            return symbol  # Terminal symbol
        production = random.choice(production_rules[symbol])
        return ''.join(expand(char) for char in production)

    # Keep generating until the string meets the minimum length
    result = ""
    while len(result) < min_length:
        result = expand(symbol)

    return result

def puzzle_19(problem_id):
    transitions = [
        {"S": "XY"},
        {"S": "YX"},
        {"S": "B"},
        {"X": "0"},
        {"Y": "1"},
        {"X": "XTX"},
        {"Y": "YTY"},
        {"T": "0"},
        {"T": "1"},
        {"B": "0A"},
        {"B": "1A"},
        {"A": "0B"},
        {"A": "1B"},
        {"A": ""}
    ]
    min_length = 10
    # print(generate_string("S", transitions, min_length))
    end_string = generate_string("S", transitions, min_length)
    transitions.append({end_string : ""})

    save_problem(problem_id, "S", transitions)

# not AB
def puzzle_20(problem_id, iterations=8) :
    transitions = [
        {"BB": ""},
        {"AA": ""},
        {"BA": ""},
    ]

    lst = ["AA", "BB", "BA"]
    test_string = ""
    for _ in range(iterations) :
        r = random.randint(0, len(test_string))
        r2 = random.randint(0, 2)

        test_string = test_string[:r] + lst[r2] + test_string[r:]

    start_string  = test_string
    save_problem(problem_id, start_string, transitions)

# hard coded (swap)
def puzzle_21(problem_id) :
    transitions = [
        {">.": ".>"},
        {"><.": ".<>"},
        {".><": "<>."},
        {".<": ">."},
        {"<<<.>>>": ""}
    ]

    start_string = ">>>.<<<"
    save_problem(problem_id, start_string, transitions)

# april
# could use 2-3 cases
def puzzle_22(problem_id, num_of_hashes = 5) :
    pos = []
    prev = 0
    for i in range(0, num_of_hashes) :
        r = random.randint(prev, prev + 6)
        pos.append(r)
        prev = r + 1
    
    length = prev + random.randint(0,5)

    final_string = ""
    for i in range(0, length) :
        if i in pos :
            final_string += "#"
        else :
            final_string += "."
    
    transitions = [
        {'.#' : '#.'},
        {'.##': '##.'},
        {final_string : ""}
    ]
    start_string = ("." * (length - 5)) + ("#" * 5) 

    save_problem(problem_id, start_string, transitions)


# 19-stars
# 2-3 cases (with different numbers) :: all we do is writing in binary
def puzzle_23(problem_id) :
    transitions = {
        "?" : "?0",
        "?" : "?1",
        "?" : "!",
        "*0" : "0**",
        "*1" : "1**",
        "!1" : "!*",
        "!0" : "!"
    }

    r = random.randint(15,40);
    final_string = "!" + ("*" * r)


    transitions_list = [{key: value} for key, value in transitions.items()]
    transitions_list.append({
        final_string : ""
    })
    start_string = "?"
    save_problem(problem_id, start_string, transitions_list)


# easy task (non-overlapping random 5-7 letter words) 
# 2-3 tasks 
def puzzles_24(problem_id) :
    lst = []
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for _ in range(4):
        word = ""
        if _ % 2 == 0 :
            for i in range(5) :
                r = random.randint(0, len(letters) - 1)
                word += letters[r]
        else :
            for i in range(7) :
                r = random.randint(0, len(letters) - 1)
                word += letters[r]
    
        lst.append(word)

    r2 = random.randint(6, 15)
    start_string = ""
    for _ in range(r2) :
        start_string = start_string + lst[random.randint(0, len(lst) - 1)]
    
    transitions = []
    for _ in lst :
        transitions.append({_ : ""})
    
    save_problem(problem_id, start_string, transitions)


# multiple 3-4 puzzles
def puzzles_25(problem_id):
    transitions = [
        {"XXXXXXXXXX": "C"},
        {"IIIIIIIIII": "X"},
        {"CX": "XC"},
        {"CI": "IC"},
        {"XI": "IX"},
        {"0": "XXXIIIIIIII"},
        {"1": "XXXXIIII"},
        {"2": "XXXXXII"},
        {"3": "XXXXXXI"},
        {"4": "XXXXXXXII"},
        {"5": "CI"},
        {"6": "CXIII"},
        {"7": "CXXI"},
        {"8": "CXXXIIIIIII"},
        {"9": "CXXXXIIII"},
        {"C|C": ""},
        {"X|X": ""},
        {"I|I": ""},
        {"|": ""}
    ]

    # Initialize the initial string
    initial_string = "9876543210|"

    Cs = 0
    Is = 0
    Xs = 0

    C_lst = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    X_lst = [3, 4, 5, 6, 7, 0, 1, 2, 3, 4]
    I_lst = [8, 4, 2, 1, 2, 1, 3, 1, 7, 4]
    for i in range(7):
        r = random.randint(0, 9)
        Cs += C_lst[r]
        Xs += X_lst[r]
        Is += I_lst[r]
    
    Xs += (Is // 10)
    Cs += (Xs // 10)
    Xs %= Xs
    Is %= Is
    initial_string += ("C" * Cs) + ("X" * Xs) + ("I" * Is) 

    empty_string = ""
    save_problem(problem_id, initial_string, transitions)


def random_path(graph, start, length):
    path = ""
    current = start

    for _ in range(length - 1):  # Subtract 1 since we already have the start node
        next_vertex = random.choice(graph[current])
        # print(next_vertex)
        path += str(next_vertex[1])
        current = next_vertex[0]

    path += current
    return path

# 4 problems on graphs
def puzzle_26(problem_id, length = 12) :
    graph = {
        'A': [('B', 1), ('C', 2)],
        'B': [('C', 2), ('D', 3)],
        'C': [('D', 2), ('E', 2)],
        'D': [('A', 1), ('E', 3)],
        'E': [('A', 4), ('B', 1)]
    }

    tmp_string = random_path(graph, 'A', length)
    print(tmp_string)

    last = tmp_string[len(tmp_string) - 1]
    tmp_string = tmp_string[:-1]

    while tmp_string.find("11") != -1 or tmp_string.find("22") != -1 or tmp_string.find("33") != -1 or tmp_string.find("44") != -1 :
        indx1 = tmp_string.find("11")
        indx2 = tmp_string.find("22")
        indx3 = tmp_string.find("33")
        indx4 = tmp_string.find("44")

        if indx1 != -1:
            tmp_string = tmp_string[:indx1] + "" + tmp_string[indx1+2:]
        elif indx2 != -1:
            tmp_string = tmp_string[:indx2] + "" + tmp_string[indx2+2:]
        elif indx3 != -1:
            tmp_string = tmp_string[:indx3] + "" + tmp_string[indx3+2:]
        else:
            tmp_string = tmp_string[:indx4] + "" + tmp_string[indx4+2:]

    emp_string = tmp_string + last
    start_string = "A"
    transitions = [
        {"A": "1B"},
        {"A": "2C"},
        {"B": "2C"},
        {"B": "3D"},
        {"C": "2D"}, 
        {"C": "2E"},
        {"D": "1A"},
        {"D": "3E"},
        {"E": "4A"},
        {"E": "1B"},
        {"11": ""}, 
        {"22": ""},
        {"33": ""},
        {"44": ""},
        {emp_string: ""}
    ]
    save_problem(problem_id, start_string, transitions)

# puzzle_26("044", 12)

# NFA  (3-problems) ::: ending with C, D, F
# Function to get next state based on the current state and input
def get_next_state(state, input_symbol, nfa_transitions):
    # Try to match a transition with the current state and symbol
    transition_key = f"{state}?{input_symbol}"
    if transition_key in nfa_transitions:
        return nfa_transitions[transition_key]
    elif f"{state}?" in nfa_transitions:  # Epsilon transition
        return nfa_transitions[f"{state}?"]

    # print()
    # print(transition_key in nfa_transitions)
    return state  # If no valid transition, stay in the same state

# Simulate random transitions starting from state "A?"
def simulate_nfa(nfa_transitions, start_state="A", num_steps=10):
    current_state = start_state
    print(f"Starting state: {current_state}")

    # whole_string = start_state
    
    for step in range(num_steps):
        # Randomly choose an input symbol (0 or 1, or epsilon represented as '*')
        input_symbol = random.choice([0, 1, 2, "*"])
        # print(f"Step {step + 1}: Current state: {current_state}, Input: {input_symbol}")
        
        # Get the next state based on the transition
        next_state = get_next_state(current_state, input_symbol, nfa_transitions)
        
        # print(f"Transitioning to: {next_state}")
        # whole_string += next_state.
        current_state = next_state
    return current_state

def puzzle_27(problem_id) :
    nfa_transitions = {
        "A?0": "B",
        "A?1": "A",
        "A?2": "C",      # Added transition from A to C on input '2'
        "A?": "C",        # Epsilon transition from A to C
        "B?0": "B",
        "B?1": "D",
        "B?2": "E",      # Added transition from B to E on input '2'
        "B?*": "F",       # Epsilon transition from B to F
        "C?*": "D",
        "C?0": "D",      # Added transition from C to D on input '0'
        "C?": "E",        # Epsilon transition from C to E
        "D?0": "D",
        "D?1": "D",
        "D?2": "C",      # Added transition from D to C on input '2'
        "D?*": "D",       # Epsilon transition from D to D
        "E?1": "F",
        "E?2": "B",      # Added transition from E to B on input '2'
        "F?0": "F",      # Added transition from F to F on input '0'
        "F?1": "F",      # Added transition from F to F on input '1'
        "F?*": "A",       # Added epsilon transition from F to A
        "?" : "!",
    }


    start_state = "A"
    emp_string = simulate_nfa(nfa_transitions, start_state, random.randint(10, 20))
    nfa_transitions[emp_string + "!"] = ""
    
    transitions_list = [{key: value} for key, value in nfa_transitions.items()]
    print(transitions_list)
    save_problem(problem_id, start_state + "?", transitions_list)

# puzzle_27("004")
# 4-problems with different row numbers.
def puzzle_28(problem_id, l, b=3) :
    # initial_string = "|...|...|"

    pos_init_x = random.randint(0, l-1)
    pos_init_y = random.randint(0, b-1)
    while pos_init_x == l - 1 and pos_init_y == b - 1 :
        pos_init_x = random.randint(0, l-1)
        pos_init_y = random.randint(0, b-1)
    
    initial_string = ""
    for i in range(0, l) :
        initial_string = initial_string + "|"
        for j in range(0, b) :
            if i == pos_init_x and j == pos_init_y:
                initial_string = initial_string + "@"
            else :
                initial_string = initial_string + "."
    initial_string = initial_string + "|"

    transitions = {
        "[RIGHT]" : "",
        "@" : "#>",

        "[LEFT]" : "",
        "@" : "<#",

        "[UP]" : "",
        "@" : "<<<<<<<<#",

        "[DOWN]" : "",
        "@" : "#>>>>>>>>",

        ">>." : ".>",
        ">>#" : "#>",
        ">>|" : "|>",
        ".<<" : "<.",
        "#<<" : "<#",
        "|<<" : "<|",
        ".<" : "@",
        ">." : "@",
    }

    final_string = ""
    for i in range(0, l) :
        final_string = final_string + "|"
        for j in range(0, b) :
            if i == l - 1 and j == b - 1:
                final_string = final_string + "@"
            else :
                final_string = final_string + "#"
    final_string = final_string + "|"

    transitions[final_string] = ""
    transitions_list = [{key: value} for (key, value) in transitions.items()]

    # print(initial_string)
    save_problem(problem_id, initial_string, transitions_list)
    return final_string
# puzzle_28("002", 4)

def caller() :
    puzzles_1()
    puzzles_2()

    lst = []
    for _ in range(6, 54) :
        lst.append(str(_).zfill(3))
    
    random.shuffle(lst)

    puzzles_3(lst[0])
    puzzles_3(lst[1])

    puzzles_4(lst[2])

    puzzle_5(lst[3], 8)
    puzzle_5(lst[4], 15)

    puzzle_6(lst[5], 8)
    puzzle_7(lst[6])

    puzzle_8(lst[7], 0)
    # print(lst[8])
    puzzle_8(lst[8], 1)

    puzzle_9(lst[9], 12)
    
    puzzle_11(lst[10], 10, 5)
    puzzle_11(lst[11], 15, 7)

    puzzle_12(lst[12])

    puzzle_13(lst[13])
    puzzle_13(lst[14])

    puzzle_14(lst[15])
    puzzle_15(lst[16])
    puzzle_16(lst[17])

    puzzle_17(lst[18])
    puzzle_18(lst[19])

    puzzle_19(lst[20])
    puzzle_19(lst[21])
    puzzle_19(lst[22])

    puzzle_20(lst[23], 10)

    puzzle_21(lst[24])
    puzzle_22(lst[25])
    puzzle_22(lst[26])
    puzzle_22(lst[27])

    puzzle_23(lst[28])
    puzzle_23(lst[29])
    puzzle_23(lst[30])

    puzzles_24(lst[31])
    puzzles_24(lst[32])
    puzzles_24(lst[33])

    puzzles_25(lst[34])
    puzzles_25(lst[35])
    puzzles_25(lst[36])

    print(lst[37:])
    puzzle_26(lst[37], 12)
    puzzle_26(lst[38], 14)
    puzzle_26(lst[39], 15)
    puzzle_26(lst[40], 13)

    puzzle_27(lst[41])
    puzzle_27(lst[42])
    puzzle_27(lst[43])

    puzzle_28(lst[44], 2)
    puzzle_28(lst[45], 3)
    puzzle_28(lst[46], 3)
    puzzle_28(lst[47], 2)

    # puzzle_5(lst[3], 8)
# def save_problem(problem_id: str, initial_string: str, transitions: list, folder_path=Path("../sample-data/puzzles")):
#     """
#     Creates and saves a problem to the specified folder.

#     Parameters:
#         problem_id (str): Unique identifier for the problem.
#         initial_string (str): The initial string for the problem.
#         transitions (list): A list of dictionaries with 'src' and 'tgt' keys for transitions.
#         folder_path (Path): Path to the folder where the problem will be saved (default is '../sample-data/puzzles').
#     """
#     # Ensure the folder exists
#     folder_path.mkdir(parents=True, exist_ok=True)

#     try:
#         [print(list(t.values())[0]) for t in transitions]
#         # Create the Problem object using the schema
#         # [print(**t) for t in transitions]

#         problem = Problem(
#             problem_id=problem_id,
#             initial_string=initial_string,
#             transitions=[(Transition(src=list(t.keys())[0], tgt=list(t.values())[0]) for t in transitions)]
#         )
        
#         # Save the problem as JSON
#         file_path = folder_path / f"{problem_id}.json"
#         with open(file_path, 'w') as f:
#             f.write(problem.json(indent=4))
        
#         logging.info(f"Problem {problem_id} saved successfully at {file_path}")
        
#     except Exception as e:
#         logging.error(f"Failed to save problem {problem_id}: {e}")


# def save_problem(problem_id: str, initial_string: str, transitions: list, folder_path=Path("../sample-data/puzzles")):
#     """
#     Creates and saves a problem to the specified folder.

#     Parameters:
#         problem_id (str): Unique identifier for the problem.
#         initial_string (str): The initial string for the problem.
#         transitions (list): A list of dictionaries with 'src' and 'tgt' keys for transitions.
#         folder_path (Path): Path to the folder where the problem will be saved (default is '../sample-data/puzzles').
#     """
#     # Ensure the folder exists
#     folder_path.mkdir(parents=True, exist_ok=True)

#     try:
#         # Create list of Transition objects
#         transition_objects = [
#             Transition(src=list(t.keys())[0], tgt=list(t.values())[0]) 
#             for t in transitions
#         ]
        
#         # Create the Problem object using the schema
#         problem = Problem(
#             problem_id=problem_id,
#             initial_string=initial_string,
#             transitions=transition_objects  # Pass the list directly, not wrapped in another list
#         )
        
#         # Save the problem as JSON
#         file_path = folder_path / f"{problem_id}.json"
#         with open(file_path, 'w') as f:
#             f.write(problem.json(indent=4))
        
#         logging.info(f"Problem {problem_id} saved successfully at {file_path}")
        
#     except Exception as e:
#         logging.error(f"Failed to save problem {problem_id}: {e}")

def save_problem(problem_id: str, initial_string: str, transitions: list, folder_path=Path("../sample-data/puzzles")):
    """
    Creates and saves a problem to the specified folder.

    Parameters:
        problem_id (str): Unique identifier for the problem.
        initial_string (str): The initial string for the problem.
        transitions (list): A list of dictionaries with 'src' and 'tgt' keys for transitions.
        folder_path (Path): Path to the folder where the problem will be saved (default is '../sample-data/puzzles').
    """
    # Ensure the folder exists
    folder_path.mkdir(parents=True, exist_ok=True)

    try:
        # Create list of Transition objects
        transition_objects = [
            Transition(src=list(t.keys())[0], tgt=list(t.values())[0]) 
            for t in transitions
        ]
        
        # Create the Problem object using the schema
        problem = Problem(
            problem_id=problem_id,
            initial_string=initial_string,
            transitions=transition_objects
        )
        
        # Save the problem as JSON using model_dump_json() instead of json()
        file_path = folder_path / f"{problem_id}.json"
        with open(file_path, 'w') as f:
            f.write(problem.model_dump_json(indent=4))
        
        logging.info(f"Problem {problem_id} saved successfully at {file_path}")
        
    except Exception as e:
        print(str(transitions))
        logging.error(f"Failed to save problem {problem_id}: {e}")

caller()