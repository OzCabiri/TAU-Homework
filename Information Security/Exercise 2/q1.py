class RepeatedKeyCipher:

    def __init__(self, key: bytes = bytes([0, 0, 0, 0, 0])):
        """Initializes the object with a list of integers between 0 and 255."""
        # WARNING: DON'T EDIT THIS FUNCTION!
        self.key = list(key)

    def encrypt(self, plaintext: str) -> bytes:
        """Encrypts a given plaintext string and returns the ciphertext."""
        bytes_text = plaintext.encode('latin-1') # Convert plaintext to bytes
        n = len(bytes_text)
        m = len(self.key)
        ciphertext = [bytes_text[i] ^ self.key[i%m] for i in range(n)] # Create bytearray and XOR by bytes
        return bytes(ciphertext) # Convert bytearray to bytes

    def decrypt(self, ciphertext: bytes) -> str:
        """Decrypts a given ciphertext string and returns the plaintext."""
        return (self.encrypt(ciphertext.decode('latin-1'))).decode('latin-1')
        # XOR is symmetric, so the process is the same, we only need to decode it from bytes to string.
        # We decode twice - the first so encrypt can receive str, and then again becuase it returns bytes.


class BreakerAssistant:

    def plaintext_score(self, plaintext: str) -> float:
        """Scores a candidate plaintext string, higher means more likely."""
        # Please don't return complex numbers, that would be just annoying.
        # I'LL DO AS I PLEASE!
        score = 0
        for c in plaintext: # There are on average 100 characters in a sentence.
            if ord('a') <= ord(c) <= ord('z'): # 80 of them are lowercase (so 80%)
                score += 0.8
            elif ord('A') <= ord(c) <= ord('Z'): # 2 of them are uppercase (so 2%)
                score += 0.02
            elif ord(c) == ord(' '): # whitespace is kind of a big deal apparently...
                score += 0.1
            elif ord(c) == ord(',') or ord(c) == ord('.'): # commas and periods are also kinda big, but less so
                score += 0.05
            elif ord('!') <= ord(c) <= ord('@'): # the rest are symbols or numbers
                score += 0.03
                # yes, technically this includes ',' and '.'
                # but they will enter the previous statment anyway so I saw no need to separate the range
        
        return score / len(plaintext) # Normalize by length
        # Score distribution was selected by me on the basis of it's my code
        # Thank you asciitable.com for your assistance

    def brute_force(self, cipher_text: bytes, key_length: int) -> str:
        """Breaks a Repeated Key Cipher by brute-forcing all keys."""
        best_score = -1
        correct_text = ""
        
        for i in range(256**key_length): # a byte is 8 bits, so it can represent 256 numbers
            i = i.to_bytes(key_length, byteorder='big')
            rkc = RepeatedKeyCipher(i)
            
            dec_text = rkc.decrypt(cipher_text)
            dec_score = self.plaintext_score(dec_text)
            
            if dec_score > best_score:
                correct_text = dec_text
                best_score = dec_score
        
        return correct_text

    def smarter_break(self, cipher_text: bytes, key_length: int) -> str:
        """Breaks a Repeated Key Cipher any way you like."""
        # TODO: IMPLEMENT THIS FUNCTION
        current_key = bytearray([0 for _ in range(key_length)])
        rkc = RepeatedKeyCipher(current_key)
        correct_text = ""
        best_score = -1
        
        for i in range(key_length):
            for b in range(256):
                candidate_key = current_key.copy()
                candidate_key[i] = b
                rkc = RepeatedKeyCipher(candidate_key)
                
                dec_text = rkc.decrypt(cipher_text)
                dec_score = self.plaintext_score(dec_text)
                
                if dec_score >= best_score:
                    correct_text = dec_text
                    best_score = dec_score
                    current_key = candidate_key
              
        return correct_text       
