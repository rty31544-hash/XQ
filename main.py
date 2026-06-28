import random

RU_ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
KB_ROW_RU = "йцукенгшщзхъфывапролджэячсмитьбю"

KEYBOARD_EN = [
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm"
]

DIGITS_ROW = "1234567890"
NUM_MAP = ["^)", "@(", "#*", "$!", "%&", "+-", "=?", "<>", "[ ]", "{}"]
BASE_BIRTHDAYS = [13, 24, 7, 12, 5, 19, 31, 1, 15, 22]

def get_mutated_list(seed_step):
    random.seed(2026 + seed_step)
    mutated = BASE_BIRTHDAYS.copy()
    random.shuffle(mutated)
    return mutated

def find_en_char_coords(char):
    for y_idx, row in enumerate(KEYBOARD_EN):
        if char in row:
            return y_idx, row.index(char)
    return None

def encrypt_author_cipher(text):
    text = text.strip()
    words = text.split(' ')
    encoded_words = []
    
    last_ru_step = -1
    global_char_idx = 0
    
    for word in words:
        if not word:
            continue
        encoded_chars = []
        for char in word:
            lower_char = char.lower()
            
            if char.isdigit():
                global_char_idx += 1
                idx = DIGITS_ROW.index(char)
                dynamic_shift = (idx + global_char_idx) % 10
                encoded_chars.append("2" + NUM_MAP[dynamic_shift])
                
            elif lower_char in RU_ALPHABET:
                global_char_idx += 1
                idx = RU_ALPHABET.index(lower_char) + 1
                current_birthdays = get_mutated_list(global_char_idx)
                birthday_multiplier = current_birthdays[global_char_idx % len(current_birthdays)]
                
                math_val = (idx * birthday_multiplier) + global_char_idx
                current_step = math_val % len(KB_ROW_RU)
                
                if last_ru_step != -1 and (current_step == last_ru_step or abs(current_step - last_ru_step) <= 2):
                    cipher_char = KB_ROW_RU[-(current_step + 1)].lower()
                else:
                    cipher_char = KB_ROW_RU[current_step].upper()
                    
                last_ru_step = current_step
                encoded_chars.append("1" + cipher_char)
                
            elif any(lower_char in row for row in KEYBOARD_EN):
                global_char_idx += 1
                coords = find_en_char_coords(lower_char)
                y, x = coords
                
                if y == 0:
                    target_y = 1
                    marker = "V"
                elif y == 2:
                    target_y = 1
                    marker = "N"
                else:
                    target_y = 0
                    marker = "S"
                    
                if char.isupper():
                    marker = marker.lower()
                    
                row = KEYBOARD_EN[target_y]
                center_char = row[x % len(row)]
                left_char = row[(x - 1) % len(row)]
                right_char = row[(x + 1) % len(row)]
                
                red_cross_block = f"{left_char}{center_char}{right_char}{marker}".upper()
                encoded_chars.append("4" + red_cross_block)
                
            else:
                encoded_chars.append("1" + char)
                
        if encoded_chars:
            encoded_words.append("".join(encoded_chars))
            
    return "0".join(encoded_words)

def decrypt_author_cipher(cipher_text):
    cipher_text = cipher_text.strip()
    words = cipher_text.split('0')
    decoded_words = []
    
    last_ru_step = -1
    global_char_idx = 0
    
    for word in words:
        if not word:
            continue
        decoded_chars = []
        
        i = 0
        while i < len(word):
            length_indicator = word[i]
            i += 1
            
            if length_indicator == '2':
                enc_char = word[i:i+2]
                i += 2
                
                global_char_idx += 1
                map_idx = NUM_MAP.index(enc_char)
                orig_idx = (map_idx - global_char_idx) % 10
                decoded_chars.append(DIGITS_ROW[orig_idx])
                
            elif length_indicator == '1':
                enc_char = word[i]
                i += 1
                
                if enc_char.lower() in KB_ROW_RU:
                    global_char_idx += 1
                    is_reverse = enc_char.islower()
                    lower_enc = enc_char.lower()
                    
                    current_birthdays = get_mutated_list(global_char_idx)
                    birthday_multiplier = current_birthdays[global_char_idx % len(current_birthdays)]
                    
                    idx_found = None
                    for idx in range(1, len(RU_ALPHABET) + 1):
                        math_val = (idx * birthday_multiplier) + global_char_idx
                        current_step = math_val % len(KB_ROW_RU)
                        
                        if last_ru_step != -1 and (current_step == last_ru_step or abs(current_step - last_ru_step) <= 2):
                            expected_char = KB_ROW_RU[-(current_step + 1)]
                        else:
                            expected_char = KB_ROW_RU[current_step]
                            
                        if expected_char == lower_enc and is_reverse == enc_char.islower():
                            idx_found = idx
                            last_ru_step = current_step
                            break
                            
                    if idx_found is not None:
                        decoded_chars.append(RU_ALPHABET[idx_found - 1])
                    else:
                        decoded_chars.append(enc_char)
                else:
                    decoded_chars.append(enc_char)
                    
            elif length_indicator == '4':
                enc_char = word[i:i+4]
                i += 4
                
                global_char_idx += 1
                lower_enc = enc_char.lower()
                center_char = lower_enc[1]
                marker = enc_char[3]
                
                coords = find_en_char_coords(center_char)
                if coords:
                    y, x = coords
                    if marker.lower() == "v":
                        orig_y = 0
                    elif marker.lower() == "n":
                        orig_y = 2
                    else:
                        orig_y = 1
                    
                    result_char = KEYBOARD_EN[orig_y][x]
                    if marker.islower():
                        result_char = result_char.upper()
                    decoded_chars.append(result_char)
                else:
                    decoded_chars.append(enc_char)
            else:
                decoded_chars.append(length_indicator)
                
        decoded_words.append("".join(decoded_chars))
    return " ".join(decoded_words)

def main():
    print("=== Welcome to the Ultimate XQ-Cipher ===")
    print("Algorithm: Red Cross & Birthday Mutation Matrix (No-XQ Edition)")
    print("Developed by rty31544-hash (Omen)\n")
    
    while True:
        print("Menu:")
        print("Press 1 — Encryption")
        print("Press 2 — Decryption")
        print("Press 3 — Exit program")
        
        choice = input("Your choice: ").strip()
        
        if choice == '1':
            user_text = input("\n[Encryption] Enter text: ")
            result = encrypt_author_cipher(user_text)
            print(f"Result: {result}")
        elif choice == '2':
            user_cipher = input("\n[Decryption] Enter cipher code: ")
            result = decrypt_author_cipher(user_cipher)
            print(f"Result: {result}")
        elif choice == '3':
            print("Program terminated. Goodbye!")
            break
        else:
            print("Error: please enter 1, 2, or 3!")

if __name__ == "__main__":
    main()
