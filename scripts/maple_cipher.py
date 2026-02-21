"""
Maple cipher encoder – Python 3.11+ implementation.

Mirrors the JavaScript ``encode`` function defined in
``src/main/webapp/elements/neon-encoder.html`` at commit 141cd01.

Cipher definition
-----------------
plaintextKey  = "abcdefghijklmnopqrstuvwxyz "   (a–z then space)
ciphertextKey = "oespaporohpqenhscejaocolrkn mgotqqogoattu acib@@aoak"

For each character of the (lowercased) plaintext:
  * Not in plaintextKey  → pass through unchanged.
  * Space (index 26)     → output a literal space.
  * Letter a–z (index i) → output ciphertextKey[2*i : 2*i+2].strip().

The final result is stripped before returning.
If the input is empty / None, return None.
"""

_PLAINTEXT_KEY = "abcdefghijklmnopqrstuvwxyz "
_CIPHERTEXT_KEY = "oespaporohpqenhscejaocolrkn mgotqqogoattu acib@@aoak"


def maple_letter_map() -> dict[str, str]:
    """Return the a–z substitution map derived from the cipher keys.

    Each letter's ciphertext is ciphertextKey[2*i : 2*i+2].strip(), where
    *i* is the zero-based index of the letter in the alphabet (a=0, z=25).
    """
    return {
        letter: _CIPHERTEXT_KEY[2 * i : 2 * i + 2].strip()
        for i, letter in enumerate(_PLAINTEXT_KEY[:26])  # only a–z, not the trailing space
    }


def maple_encode(
    text: str | None,
    letter_map: dict[str, str] | None = None,
) -> str | None:
    """Encode *text* using the Maple cipher.

    Parameters
    ----------
    text:
        Plaintext to encode.  ``None`` or an empty string returns ``None``.
    letter_map:
        Pre-built substitution map (from :func:`maple_letter_map`).
        If omitted, the map is built on every call – pass a cached map for
        repeated use.

    Returns
    -------
    str | None
        Encoded ciphertext (stripped), or ``None`` when *text* is falsy.
    """
    if not text:
        return None

    if letter_map is None:
        letter_map = maple_letter_map()

    ciphertext: list[str] = []
    for ch in text.lower():
        if ch == " ":
            # Space (index 26 in plaintextKey) always maps to a literal space.
            ciphertext.append(" ")
        elif ch in letter_map:
            ciphertext.append(letter_map[ch])
        else:
            # Characters not in plaintextKey pass through unchanged.
            ciphertext.append(ch)

    return "".join(ciphertext).strip()


if __name__ == "__main__":
    _MAP = maple_letter_map()

    samples = [
        "hello",
        "hello world",
        "Hello, World!",
        "maple",
        "",
        None,
    ]

    for sample in samples:
        result = maple_encode(sample, _MAP)
        print(f"{sample!r:25} -> {result!r}")
