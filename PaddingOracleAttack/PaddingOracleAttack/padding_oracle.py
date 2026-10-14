from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

BLOCK_SIZE = 16


def create_oracle(secret_key):
    def padding_oracle(iv, ciphertext):
        try:
            cipher = AES.new(secret_key, AES.MODE_CBC, iv)
            decrypted = cipher.decrypt(ciphertext)
            unpad(decrypted, BLOCK_SIZE)
            return True
        except ValueError:
            return False

    return padding_oracle


def padding_oracle_attack(ciphertext, iv, oracle):
    if len(ciphertext) == 0 or len(ciphertext) % BLOCK_SIZE != 0:
        raise ValueError("Ciphertext must contain complete AES blocks.")

    blocks = [
        ciphertext[i:i + BLOCK_SIZE]
        for i in range(0, len(ciphertext), BLOCK_SIZE)
    ]

    recovered = bytearray()
    query_count = 0

    for block_index, target in enumerate(blocks):
        original_previous = iv if block_index == 0 else blocks[block_index - 1]
        intermediate = bytearray(BLOCK_SIZE)

        for padding_value in range(1, BLOCK_SIZE + 1):
            position = BLOCK_SIZE - padding_value
            found = False

            crafted = bytearray(original_previous)

            for j in range(position + 1, BLOCK_SIZE):
                crafted[j] = intermediate[j] ^ padding_value

            for guess in range(256):
                crafted[position] = guess
                query_count += 1

                valid = oracle(bytes(crafted), target)

                if not valid:
                    continue

                if padding_value == 1 and position > 0:
                    confirmation = bytearray(crafted)
                    confirmation[position - 1] ^= 1
                    query_count += 1

                    if not oracle(bytes(confirmation), target):
                        continue

                intermediate[position] = guess ^ padding_value
                found = True
                break

            if not found:
                raise RuntimeError(
                    f"Unable to recover byte at block {block_index}, "
                    f"position {position}."
                )

        plaintext_block = bytes(
            intermediate[i] ^ original_previous[i]
            for i in range(BLOCK_SIZE)
        )

        recovered.extend(plaintext_block)

    return unpad(bytes(recovered), BLOCK_SIZE), query_count


def main():
    secret_key = get_random_bytes(32)
    iv = get_random_bytes(BLOCK_SIZE)

    original_plaintext = (
        b"This is a padding oracle attack demonstration."
    )

    cipher = AES.new(secret_key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(original_plaintext, BLOCK_SIZE))

    oracle = create_oracle(secret_key)

    print("Ciphertext:", ciphertext.hex())
    print("IV:", iv.hex())
    print("Starting padding oracle attack...")

    recovered_plaintext, queries = padding_oracle_attack(
        ciphertext, iv, oracle
    )

    print("Recovered plaintext:", recovered_plaintext.decode("utf-8"))
    print("Total oracle queries:", queries)
    print("Recovery successful:", recovered_plaintext == original_plaintext)


if __name__ == "__main__":
    main()
