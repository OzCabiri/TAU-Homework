from q2_atm import ATM, ServerResponse


def extract_PIN(encrypted_PIN) -> int:
    """Extracts the original PIN string from an encrypted PIN."""
    atm = ATM()
    for i in range(10**4): # We're just gonna brute force...
        candidate_PIN = atm.encrypt_PIN(i)
        if candidate_PIN == encrypted_PIN:
            return i
    return False


def extract_credit_card(encrypted_credit_card) -> int:
    """Extracts a credit card number string from its ciphertext."""
    return round(encrypted_credit_card ** (1/3)) # n is too big, and e is too small - see q2b.txt


def forge_signature():
    """Forge a server response that passes verification."""
    # Return a ServerResponse instance.
    return ServerResponse(1, 1)
