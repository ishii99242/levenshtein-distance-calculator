import unittest

from levenshtein_distance_calculator import distance, normalized_distance


class TestDistance(unittest.TestCase):
    def test_identical_strings(self):
        self.assertEqual(distance("hello", "hello"), 0)

    def test_one_empty(self):
        self.assertEqual(distance("", "abc"), 3)
        self.assertEqual(distance("abc", ""), 3)

    def test_both_empty(self):
        self.assertEqual(distance("", ""), 0)

    def test_single_substitution(self):
        self.assertEqual(distance("cat", "bat"), 1)

    def test_single_insertion(self):
        self.assertEqual(distance("cat", "cart"), 1)

    def test_single_deletion(self):
        self.assertEqual(distance("cart", "cat"), 1)

    def test_completely_different_same_length(self):
        self.assertEqual(distance("abc", "xyz"), 3)

    def test_kitten_sitting(self):
        # Classic textbook example.
        self.assertEqual(distance("kitten", "sitting"), 3)

    def test_sunday_saturday(self):
        self.assertEqual(distance("sunday", "saturday"), 3)

    def test_unicode_code_points(self):
        # These are two distinct code points, so distance is 1.
        self.assertEqual(distance("caf\u00e9", "cafe"), 1)

    def test_repeated_characters(self):
        self.assertEqual(distance("aaaa", "aa"), 2)
        self.assertEqual(distance("aa", "aaaa"), 2)

    def test_case_sensitive(self):
        # 'A' and 'a' are different code points.
        self.assertEqual(distance("ABC", "abc"), 3)

    def test_type_error_on_non_str(self):
        with self.assertRaises(TypeError):
            distance("abc", 123)
        with self.assertRaises(TypeError):
            distance(None, "abc")


class TestNormalizedDistance(unittest.TestCase):
    def test_identical(self):
        self.assertEqual(normalized_distance("hello", "hello"), 0.0)

    def test_both_empty(self):
        self.assertEqual(normalized_distance("", ""), 0.0)

    def test_one_empty(self):
        self.assertEqual(normalized_distance("", "abcd"), 1.0)
        self.assertEqual(normalized_distance("abcd", ""), 1.0)

    def test_value_range(self):
        # Use integer arithmetic to avoid float equality pitfalls.
        # distance("abc","xyz") = 3, max len = 3, so normalised = 1.0.
        self.assertEqual(normalized_distance("abc", "xyz"), 1.0)
        # distance("kitten","sitting") = 3, max len = 7, so 3/7.
        self.assertEqual(normalized_distance("kitten", "sitting"), 3 / 7)

    def test_type_error_on_non_str(self):
        with self.assertRaises(TypeError):
            normalized_distance("abc", 1)


if __name__ == "__main__":
    unittest.main()
