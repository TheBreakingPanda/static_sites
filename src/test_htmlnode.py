import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "Click me!",
            props={"href": "https://www.boot.dev", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://www.boot.dev" target="_blank"'
        )

    def test_props_to_html_no_props(self):
        node = HTMLNode("p", "This is a paragraph.")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode("img", props={"src": "image.png"})
        self.assertEqual(node.props_to_html(), ' src="image.png"')

    def test_values(self):
        node = HTMLNode("div", "Hello, world!")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello, world!")

    def test_repr(self):
        node = HTMLNode("p", "This is a paragraph.", None, {"class": "text"})
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(tag=p, value=This is a paragraph., children=None, props={'class': 'text'})",
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just raw text")
        self.assertEqual(node.to_html(), "Just raw text")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_repr(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.__repr__(), "LeafNode(tag=p, value=Hello, world!, props=None)")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(), '<div class="container"><span>child</span></div>'
        )

    def test_to_html_no_tag(self):
        parent_node = ParentNode(None, [LeafNode("span", "child")])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_empty_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_parent_repr(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.__repr__(),
            f"ParentNode(tag=div, children=[{child_node!r}], props=None)",
        )


if __name__ == "__main__":
    unittest.main()
