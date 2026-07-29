import unittest

from generatepage import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extract_title_strips_whitespace(self):
        self.assertEqual(extract_title("#   Hello World   "), "Hello World")

    def test_extract_title_not_first_line(self):
        md = "Some intro text\n\n# The Title\n\nMore content here"
        self.assertEqual(extract_title(md), "The Title")

    def test_extract_title_ignores_h2(self):
        md = "## Not an h1\n\n# Actual Title"
        self.assertEqual(extract_title(md), "Actual Title")

    def test_extract_title_no_h1_raises(self):
        md = "## Just an h2\n\nSome paragraph text"
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_extract_title_no_heading_at_all_raises(self):
        with self.assertRaises(ValueError):
            extract_title("Just a plain paragraph, no headings here")

    def test_extract_title_requires_space_after_hash(self):
        with self.assertRaises(ValueError):
            extract_title("#NoSpace")

    def test_extract_title_first_of_multiple_h1s(self):
        md = "# First Title\n\n# Second Title"
        self.assertEqual(extract_title(md), "First Title")


if __name__ == "__main__":
    unittest.main()
