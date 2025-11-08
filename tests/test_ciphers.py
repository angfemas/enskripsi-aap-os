import unittest
from enkripsi_app_gui_os import (
    caesar_encrypt,
    caesar_decrypt,
    vigenere_encrypt,
    vigenere_decrypt,
    transposition_encrypt,
    transposition_decrypt,
)


class TestCiphers(unittest.TestCase):
    def test_caesar(self):
        self.assertEqual(caesar_encrypt("ABC", 3), "DEF")
        self.assertEqual(caesar_decrypt("DEF", 3), "ABC")

    def test_vigenere(self):
        # verify round-trip: encrypt then decrypt returns original
        encrypted = vigenere_encrypt("ATTACK", "KEY")
        self.assertEqual(vigenere_decrypt(encrypted, "KEY"), "ATTACK")

    def test_transposition(self):
        pt = "WEAREDISCOVEREDFLEEATONCE"
        ct = transposition_encrypt(pt, 5)
        self.assertIsInstance(ct, str)
        self.assertEqual(transposition_decrypt(ct, 5), pt)


if __name__ == "__main__":
    unittest.main()
