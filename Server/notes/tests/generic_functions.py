import random
import string


def random_string(length=16, text=string.ascii_letters + string.digits):
    """
    Lazy way to create random strings, such as usernames or notes.
    """
    return "".join(random.choice(text) for _ in range(length)).strip()


def random_bell_curve_int(low=1, high=12):
    """
    Random integer generator. Numbers are skewed along a bell curve.
    """
    return int(round(random.triangular(low, high), 0))


def random_length_string(low=1, high=12, allow_digits=True):
    """
    Creates a string of random length
    """
    text = string.ascii_letters
    if allow_digits:
        text += string.digits
    return random_string(
        length=random_bell_curve_int(low=low, high=high), text=text
    ).strip()


def random_sentence(total_len=128, allow_numbers=True):
    """
    Create sentences consisting of random letters (and numbers). Used as quick filler.
    """
    # Base variables
    count = 0
    words_to_punctuation = random.randint(5, 16)
    punctuation = [".", "?", "!", ",", ";"]
    text_choices = string.ascii_letters

    # If numbers are allowed, add them
    if allow_numbers:
        text_choices += string.digits

    # Set the first word of the sentence
    sentence = random_string(length=random_bell_curve_int(), text=text_choices)

    # Add words until the total_len of the sentence is reached
    while len(sentence) < total_len:
        count += 1

        # If the count length is reached, add a random punctuation
        if count >= words_to_punctuation:
            sentence += random.choice(punctuation) + " "

            # Reset base variables
            count = 0
            words_to_punctuation = random.randint(5, 16)

        else:
            # Otherwise, keep adding words
            sentence += " " + random_string(
                length=random_bell_curve_int(), text=text_choices
            )

    return sentence[:total_len]
