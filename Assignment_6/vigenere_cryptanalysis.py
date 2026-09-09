from collections import Counter


# ============================================================
# 1. CLEAN CIPHERTEXT
# ============================================================

def clean_ciphertext(ciphertext):
    """
    Remove spaces, newlines and special characters.
    Convert everything to uppercase.
    """

    return ''.join(
        ch for ch in ciphertext.upper()
        if 'A' <= ch <= 'Z'
    )


# ============================================================
# 2. FIND REPEATED PATTERNS
# ============================================================

def find_repeated_patterns(ciphertext, pattern_length=3):
    """
    Find repeated sequences of the given length.

    Example:
        ABCXYZABC

    ABC occurs at positions 0 and 6.
    """

    patterns = {}

    for i in range(len(ciphertext) - pattern_length + 1):

        pattern = ciphertext[i:i + pattern_length]

        if pattern not in patterns:
            patterns[pattern] = []

        patterns[pattern].append(i)

    repeated = {}

    for pattern, positions in patterns.items():

        if len(positions) > 1:
            repeated[pattern] = positions

    return repeated


# ============================================================
# 3. CALCULATE DISTANCES
# ============================================================

def calculate_distances(patterns):
    """
    Calculate distances between repeated patterns.
    """

    distances = []

    for pattern, positions in patterns.items():

        for i in range(len(positions)):

            for j in range(i + 1, len(positions)):

                distance = positions[j] - positions[i]

                distances.append(
                    (pattern, distance)
                )

    return distances


# ============================================================
# 4. FIND FACTORS
# ============================================================

def find_factors(number, max_key_length=20):
    """
    Find possible key-length factors of a distance.
    """

    factors = []

    for i in range(2, min(number, max_key_length) + 1):

        if number % i == 0:

            factors.append(i)

    return factors


# ============================================================
# 5. KASISKI ANALYSIS
# ============================================================

def kasiski_analysis(ciphertext):
    """
    Perform Kasiski examination.

    Returns candidate key lengths and their frequencies.
    """

    patterns = find_repeated_patterns(ciphertext)

    distances = calculate_distances(patterns)

    factor_counts = Counter()

    for pattern, distance in distances:

        factors = find_factors(distance)

        for factor in factors:

            factor_counts[factor] += 1

    return patterns, distances, factor_counts


# ============================================================
# 6. INDEX OF COINCIDENCE
# ============================================================

def calculate_ic(text):
    """
    Calculate Index of Coincidence.
    """

    n = len(text)

    if n <= 1:
        return 0.0

    frequencies = Counter(text)

    numerator = sum(
        count * (count - 1)
        for count in frequencies.values()
    )

    denominator = n * (n - 1)

    return numerator / denominator


# ============================================================
# 7. SPLIT INTO GROUPS
# ============================================================

def split_into_groups(ciphertext, key_length):
    """
    Divide ciphertext according to key length.

    For key length 5:

    Group 1 = positions 0,5,10,...
    Group 2 = positions 1,6,11,...
    etc.
    """

    groups = []

    for i in range(key_length):

        group = ciphertext[i::key_length]

        groups.append(group)

    return groups


# ============================================================
# 8. FREQUENCY ANALYSIS
# ============================================================

def frequency_analysis(group):
    """
    Calculate A-Z frequency for a group.
    """

    frequencies = Counter(group)

    table = {}

    for i in range(26):

        letter = chr(ord('A') + i)

        table[letter] = frequencies.get(letter, 0)

    return table


# ============================================================
# ENGLISH LETTER FREQUENCIES
# ============================================================

ENGLISH_FREQ = [
    0.08167,  # A
    0.01492,  # B
    0.02782,  # C
    0.04253,  # D
    0.12702,  # E
    0.02228,  # F
    0.02015,  # G
    0.06094,  # H
    0.06966,  # I
    0.00153,  # J
    0.00772,  # K
    0.04025,  # L
    0.02406,  # M
    0.06749,  # N
    0.07507,  # O
    0.01929,  # P
    0.00095,  # Q
    0.05987,  # R
    0.06327,  # S
    0.09056,  # T
    0.02758,  # U
    0.00978,  # V
    0.02360,  # W
    0.00150,  # X
    0.01974,  # Y
    0.00074   # Z
]


# ============================================================
# 9. FIND CAESAR SHIFT
# ============================================================

def find_shift(group):
    """
    Estimate Caesar shift using chi-square analysis.
    """

    n = len(group)

    if n == 0:
        return 0

    observed = [
        group.count(chr(ord('A') + i))
        for i in range(26)
    ]

    best_shift = 0
    best_score = float('inf')

    for shift in range(26):

        score = 0.0

        for plain_index in range(26):

            expected = ENGLISH_FREQ[plain_index] * n

            cipher_index = (
                plain_index + shift
            ) % 26

            observed_value = observed[cipher_index]

            if expected > 0:

                score += (
                    (observed_value - expected) ** 2
                ) / expected

        if score < best_score:

            best_score = score

            best_shift = shift

    return best_shift


# ============================================================
# 10. FIND KEY
# ============================================================

def find_key(groups):
    """
    Combine Caesar shifts to obtain
    the probable Vigenere key.
    """

    key = ""

    for group in groups:

        shift = find_shift(group)

        key += chr(
            ord('A') + shift
        )

    return key


# ============================================================
# 11. VIGENERE DECRYPTION
# ============================================================

def vigenere_decrypt(ciphertext, key):
    """
    Decrypt ciphertext using Vigenere key.
    """

    plaintext = ""

    for i, ch in enumerate(ciphertext):

        c = ord(ch) - ord('A')

        k = (
            ord(key[i % len(key)])
            - ord('A')
        )

        p = (c - k) % 26

        plaintext += chr(
            p + ord('A')
        )

    return plaintext


# ============================================================
# 12. VIGENERE ENCRYPTION
# ============================================================

def vigenere_encrypt(plaintext, key):
    """
    Encrypt plaintext using Vigenere key.
    """

    ciphertext = ""

    for i, ch in enumerate(plaintext):

        p = ord(ch) - ord('A')

        k = (
            ord(key[i % len(key)])
            - ord('A')
        )

        c = (p + k) % 26

        ciphertext += chr(
            c + ord('A')
        )

    return ciphertext


# ============================================================
# 13. VERIFY
# ============================================================

def verify(ciphertext, plaintext, key):
    """
    Re-encrypt plaintext and compare
    with original ciphertext.
    """

    encrypted = vigenere_encrypt(
        plaintext,
        key
    )

    return encrypted == ciphertext


# ============================================================
# 14. DISPLAY FREQUENCY TABLE
# ============================================================

def display_frequency_table(table):

    print()

    for letter, count in table.items():

        print(
            f"{letter}: {count:3d}",
            end="    "
        )

        if letter == 'M':

            print()


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    # ========================================================
    # GROUP 15 = ODD GROUP
    # Therefore use Ciphertext 1
    # ========================================================

    ciphertext = """
    DAZFI SFSPA VQLSN PXYSZ WXALC DAFGQ UISMT PHZGA
    MKTTF TCCFX

    KFCRG GLPFE TZMMM ZOZDE ADWVZ WMWKV GQSOH QSVHP
    WFKLS LEASE

    PWHMJ EGKPU RVSXJ XVBWV POSDE TEQTX OBZIK WCXLW
    NUOVJ MJCLL

    OEOFA ZENVM JILOW ZEKAZ EJAQD ILSWW ESGUG KTZGQ
    ZVRMN WTQSE

    OTKTK PBSTA MQVER MJEGL JQRTL GFJYG SPTZP GTACM
    OECBX SESCI

    YGUFP KVILL TWDKS ZODFW FWEAA PQTFS TQIRG MPMEL
    RYELH QSVWB

    AWMOS DELHM UZGPG YEKZU KWTAM ZJMLS EVJQT GLAWV
    OVVXH KWQIL

    IEUYS ZWXAH HUSZO GMUZQ CIMVZ UVWIF JJHPW VXFSE
    TZEDF
    """

    # ========================================================
    # STEP 1: CLEAN
    # ========================================================

    ciphertext = clean_ciphertext(
        ciphertext
    )

    print("=" * 70)
    print("VIGENERE CIPHER CRYPTANALYSIS")
    print("GROUP NUMBER: 15")
    print("=" * 70)

    print("\nCleaned ciphertext:")
    print(ciphertext)

    print("\nCiphertext length:")
    print(len(ciphertext))

    # ========================================================
    # STEP 2: KASISKI
    # ========================================================

    patterns, distances, factor_counts = (
        kasiski_analysis(ciphertext)
    )

    print("\n" + "=" * 70)
    print("KASISKI EXAMINATION")
    print("=" * 70)

    print("\nRepeated patterns:")

    for pattern, positions in patterns.items():

        print(
            f"{pattern} -> {positions}"
        )

    print("\nDistances:")

    for pattern, distance in distances:

        print(
            f"{pattern} -> {distance}"
        )

    print("\nCandidate key lengths:")

    for length, count in factor_counts.most_common():

        print(
            f"Key length {length}: "
            f"{count} occurrence(s)"
        )

    # ========================================================
    # STEP 3: TEST CANDIDATE KEY LENGTHS USING IC
    # ========================================================

    print("\n" + "=" * 70)
    print("INDEX OF COINCIDENCE ANALYSIS")
    print("=" * 70)

    candidate_lengths = [
        length
        for length, count
        in factor_counts.most_common(10)
        if length <= 20
    ]

    ic_results = []

    for key_length in candidate_lengths:

        groups = split_into_groups(
            ciphertext,
            key_length
        )

        ic_values = [
            calculate_ic(group)
            for group in groups
        ]

        average_ic = (
            sum(ic_values) /
            len(ic_values)
        )

        ic_results.append(
            (key_length, average_ic)
        )

        print(
            f"Key length {key_length:2d} "
            f"| Average IC = {average_ic:.4f}"
        )

    # ========================================================
    # SELECT KEY LENGTH
    # ========================================================

    if ic_results:

        # Prefer IC closest to typical English IC
        target_ic = 0.066

        key_length, _ = min(
            ic_results,
            key=lambda x: abs(
                x[1] - target_ic
            )
        )

    elif factor_counts:

        key_length = (
            factor_counts
            .most_common(1)[0][0]
        )

    else:

        key_length = 1

    print(
        f"\nEstimated key length: "
        f"{key_length}"
    )

    # ========================================================
    # STEP 4: SPLIT INTO GROUPS
    # ========================================================

    groups = split_into_groups(
        ciphertext,
        key_length
    )

    print("\n" + "=" * 70)
    print("CIPHERTEXT GROUPS")
    print("=" * 70)

    for i, group in enumerate(groups):

        print(
            f"Group {i + 1}: {group}"
        )

    # ========================================================
    # STEP 5: FREQUENCY ANALYSIS
    # ========================================================

    print("\n" + "=" * 70)
    print("FREQUENCY ANALYSIS")
    print("=" * 70)

    for i, group in enumerate(groups):

        print(
            f"\nGroup {i + 1}"
        )

        print(
            f"Index of Coincidence: "
            f"{calculate_ic(group):.4f}"
        )

        table = frequency_analysis(
            group
        )

        display_frequency_table(
            table
        )

    # ========================================================
    # STEP 6: FIND KEY
    # ========================================================

    key = find_key(groups)

    print("\n" + "=" * 70)
    print("RECOVERED KEY")
    print("=" * 70)

    print(
        f"Probable Vigenere Key: {key}"
    )

    # ========================================================
    # STEP 7: DECRYPT
    # ========================================================

    plaintext = vigenere_decrypt(
        ciphertext,
        key
    )

    print("\n" + "=" * 70)
    print("RECOVERED PLAINTEXT")
    print("=" * 70)

    print(plaintext)

    # ========================================================
    # STEP 8: RE-ENCRYPT
    # ========================================================

    encrypted_again = vigenere_encrypt(
        plaintext,
        key
    )

    print("\n" + "=" * 70)
    print("RE-ENCRYPTED CIPHERTEXT")
    print("=" * 70)

    print(encrypted_again)

    # ========================================================
    # STEP 9: VERIFY
    # ========================================================

    result = verify(
        ciphertext,
        plaintext,
        key
    )

    print("\n" + "=" * 70)
    print("VERIFICATION")
    print("=" * 70)

    if result:

        print(
            "SUCCESS: Re-encryption matches "
            "the original ciphertext."
        )

    else:

        print(
            "FAILED: Re-encryption does not "
            "match the original ciphertext."
        )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()