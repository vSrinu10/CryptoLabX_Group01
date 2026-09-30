from collections import Counter


def generate_key_matrix(keyword):
    keyword = ''.join(ch for ch in keyword.upper() if ch.isalpha())
    keyword = keyword.replace('J', 'I')

    sequence = []

    for ch in keyword + 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
        if ch not in sequence:
            sequence.append(ch)

    matrix = [sequence[i:i + 5] for i in range(0, 25, 5)]
    return matrix


def prepare_plaintext(plaintext):
    plaintext = ''.join(ch for ch in plaintext.upper() if ch.isalpha())
    plaintext = plaintext.replace('J', 'I')
    return plaintext


def create_digraphs(plaintext):
    digraphs = []
    i = 0

    while i < len(plaintext):
        first = plaintext[i]

        if i + 1 >= len(plaintext):
            digraphs.append(first + 'X')
            i += 1
        elif plaintext[i] == plaintext[i + 1]:
            digraphs.append(first + 'X')
            i += 1
        else:
            digraphs.append(first + plaintext[i + 1])
            i += 2

    return digraphs


def find_position(matrix, letter):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == letter:
                return row, col

    raise ValueError(f"Letter {letter} not found")


def playfair_encrypt(digraphs, matrix):
    ciphertext = ""

    for pair in digraphs:
        a, b = pair

        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        if row1 == row2:
            ciphertext += matrix[row1][(col1 + 1) % 5]
            ciphertext += matrix[row2][(col2 + 1) % 5]

        elif col1 == col2:
            ciphertext += matrix[(row1 + 1) % 5][col1]
            ciphertext += matrix[(row2 + 1) % 5][col2]

        else:
            ciphertext += matrix[row1][col2]
            ciphertext += matrix[row2][col1]

    return ciphertext


def playfair_decrypt(ciphertext, matrix):
    plaintext = ""

    for i in range(0, len(ciphertext), 2):
        a = ciphertext[i]
        b = ciphertext[i + 1]

        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        if row1 == row2:
            plaintext += matrix[row1][(col1 - 1) % 5]
            plaintext += matrix[row2][(col2 - 1) % 5]

        elif col1 == col2:
            plaintext += matrix[(row1 - 1) % 5][col1]
            plaintext += matrix[(row2 - 1) % 5][col2]

        else:
            plaintext += matrix[row1][col2]
            plaintext += matrix[row2][col1]

    return plaintext


def digraph_frequency(ciphertext):
    digraphs = [
        ciphertext[i:i + 2]
        for i in range(0, len(ciphertext), 2)
    ]

    return Counter(digraphs)


def verify(original_digraphs, ciphertext, matrix):
    decrypted_text = playfair_decrypt(ciphertext, matrix)

    decrypted_digraphs = [
        decrypted_text[i:i + 2]
        for i in range(0, len(decrypted_text), 2)
    ]

    re_encrypted = playfair_encrypt(decrypted_digraphs, matrix)

    return (
        decrypted_digraphs == original_digraphs
        and re_encrypted == ciphertext
    )


def print_matrix(matrix):
    print("\nKey Matrix:")
    for row in matrix:
        print(" ".join(row))


def main():
    keyword = input("Keyword: ")
    plaintext = input("Plaintext: ")

    matrix = generate_key_matrix(keyword)
    prepared = prepare_plaintext(plaintext)
    digraphs = create_digraphs(prepared)

    print_matrix(matrix)

    print("\nPrepared Digraphs:")
    print(" ".join(digraphs))

    ciphertext = playfair_encrypt(digraphs, matrix)

    print("\nCiphertext:")
    print(ciphertext)

    decrypted_text = playfair_decrypt(ciphertext, matrix)

    print("\nDecrypted Text:")
    print(decrypted_text)

    frequencies = digraph_frequency(ciphertext)

    print("\nDigraph Frequency:")
    for digraph, count in frequencies.items():
        print(f"{digraph}: {count}")

    result = verify(digraphs, ciphertext, matrix)

    print("\nVerification:")
    if result:
        print("SUCCESS")
    else:
        print("FAILED")


if __name__ == "__main__":
    main()
