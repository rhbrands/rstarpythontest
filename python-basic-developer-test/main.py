from collections import Counter
import random
import psycopg2


# DATA

DATA = [
"GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, BLUE, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN",
"ARSH, BROWN, GREEN, BROWN, BLUE, BLUE, BLEW, PINK, PINK, ORANGE, ORANGE, RED, WHITE, BLUE, WHITE, WHITE, BLUE, BLUE, BLUE",
"GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, RED, YELLOW, ORANGE, RED, ORANGE, RED, BLUE, BLUE, WHITE, BLUE, BLUE, WHITE, WHITE",
"BLUE, BLUE, GREEN, WHITE, BLUE, BROWN, PINK, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN",
"GREEN, WHITE, GREEN, BROWN, BLUE, BLUE, BLACK, WHITE, ORANGE, RED, RED, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, WHITE"
]

CORRECTIONS = {"BLEW": "BLUE", "ARSH": "ASH"}


# EXTRACT COLORS

def extract_colors(data):
    result = []
    for row in data:
        for color in row.split(","):
            c = color.strip().upper()
            result.append(CORRECTIONS.get(c, c))
    return result

colors = extract_colors(DATA)


# FREQUENCY / MODE

frequency = Counter(colors)
mode_color = frequency.most_common(1)[0][0]


# MEAN + MEDIAN (numeric mapping)

unique_colors = sorted(frequency.keys())
color_index = {c:i for i,c in enumerate(unique_colors)}

numeric_values = [color_index[c] for c in colors]

mean_value = sum(numeric_values) / len(numeric_values)
mean_color = min(unique_colors, key=lambda c: abs(color_index[c] - mean_value))

sorted_vals = sorted(numeric_values)
median_color = unique_colors[sorted_vals[len(sorted_vals)//2]]


# VARIANCE

variance = sum((x - mean_value) ** 2 for x in numeric_values) / len(numeric_values)


# PROBABILITY OF RED

prob_red = frequency["RED"] / len(colors)


# SAVE TO POSTGRESQL

def save_to_postgres(freq):
    conn = psycopg2.connect(
        host="localhost",
        database="colorsdb",
        user="postgres",
        password="password"
    )

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS dress_colors(
            color TEXT,
            frequency INT
        )
    """)

    for color, count in freq.items():
        cur.execute(
            "INSERT INTO dress_colors(color,frequency) VALUES(%s,%s)",
            (color, count)
        )

    conn.commit()
    cur.close()
    conn.close()

save_to_postgres(frequency)

# RECURSIVE SEARCH

def recursive_search(lst, target, index=0):
    if index >= len(lst):
        return False
    if lst[index] == target:
        return True
    return recursive_search(lst, target, index + 1)


# RANDOM BINARY → BASE10

binary_number = ''.join(random.choice('01') for _ in range(4))
base10_value = int(binary_number, 2)


# SUM FIRST 50 FIBONACCI

def fibonacci_sum(n):
    a, b = 0, 1
    total = 0
    for _ in range(n):
        total += a
        a, b = b, a + b
    return total

fib_sum = fibonacci_sum(50)


# OUTPUT

print("Mean color:", mean_color)
print("Most worn (mode):", mode_color)
print("Median color:", median_color)
print("Variance:", variance)
print("Probability of red:", prob_red)

print("Recursive search:", recursive_search([1,2,3,4,5], 3))

print("Random binary:", binary_number)
print("Base10:", base10_value)

print("Sum first 50 Fibonacci:", fib_sum)
