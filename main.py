RU_ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
EN_ALPHABET = "abcdefghijklmnopqrstuvwxyz"

NUM_MAP = {
    "0": "^)", "1": "@(", "2": "#*", "3": "$!", "4": "%&",
    "5": "+-", "6": "=?", "7": "<>", "8": "[ ]", "9": "{}"
}
REV_NUM_MAP = {v: k for k, v in NUM_MAP.items()}

def encrypt_author_cipher(text):
    text = text.strip()
    words = text.split(' ')
    encoded_words = []
    
    for word in words:
        if not word:
            continue
        encoded_chars = []
        for char in word:
            lower_char = char.lower()
            if char.isdigit():
                encoded_chars.append(NUM_MAP[char])
            elif lower_char in RU_ALPHABET:
                idx = RU_ALPHABET.index(lower_char) + 1
                if idx <= 26:
                    en_char = EN_ALPHABET[idx - 1].upper()
                    encoded_chars.append(en_char)
                else:
                    remainder = idx - 26
                    en_char = EN_ALPHABET[remainder - 1].upper()
                    encoded_chars.append(f"J{en_char}")
            elif lower_char in EN_ALPHABET:
                idx = EN_ALPHABET.index(lower_char) + 1
                ru_char = RU_ALPHABET[idx - 1].upper()
                encoded_chars.append(ru_char)
            else:
                encoded_chars.append(char)
        encoded_words.append("XQ".join(encoded_chars))
    return "XQX".join(encoded_words)

def decrypt_author_cipher(cipher_text):
    cipher_text = cipher_text.strip()
    words = cipher_text.split('XQX')
    decoded_words = []
    
    for word in words:
        word = word.strip()
        if not word:
            continue
        encoded_chars = word.split('XQ')
        decoded_chars = []
        
        for enc_char in encoded_chars:
            enc_char = enc_char.strip()
            if not enc_char:
                continue
            
            upper_enc = enc_char.upper()
            lower_enc = enc_char.lower()
            
            if enc_char in REV_NUM_MAP:
                decoded_chars.append(REV_NUM_MAP[enc_char])
            elif upper_enc.startswith('J') and len(upper_enc) > 1:
                next_char = upper_enc[1:].lower()
                if next_char in EN_ALPHABET:
                    idx = EN_ALPHABET.index(next_char) + 1 + 26
                    if idx <= len(RU_ALPHABET):
                        decoded_chars.append(RU_ALPHABET[idx - 1])
            elif lower_enc in EN_ALPHABET:
                idx = EN_ALPHABET.index(lower_enc) + 1
                decoded_chars.append(RU_ALPHABET[idx - 1])
            elif lower_enc in RU_ALPHABET:
                idx = RU_ALPHABET.index(lower_enc) + 1
                if idx <= len(EN_ALPHABET):
                    decoded_chars.append(EN_ALPHABET[idx - 1])
            else:
                decoded_chars.append(enc_char)
        decoded_words.append("".join(decoded_chars))
    return " ".join(decoded_words)

def main():
    print("=== Welcome to the Advanced XQ-Cipher ===")
    
    while True:
        print("\nXQ")
        print("Press 1 — Encryption")
        print("Press 2 — Decryption")
        print("Press 3 — Exit program")
        
        choice = input("Your choice: ").strip()
        
        if choice == '1':
            user_text = input("\n[XQ Encryption] Enter text (letters and/or digits): ")
            result = encrypt_author_cipher(user_text)
            print(f"Result: {result}")
        elif choice == '2':
            user_cipher = input("\n[XQ Decryption] Enter cipher code: ")
            result = decrypt_author_cipher(user_cipher)
            print(f"Result: {result}")
        elif choice == '3':
            print("Program terminated. Goodbye!")
            break
        else:
            print("Error: please enter 1, 2, or 3!")

if __name__ == "__main__":
    main()
