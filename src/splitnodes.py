from extractmarkdown import extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    """
    Splits a list of TextNode instances into multiple TextNode instances based on a delimiter.

    Args:
        old_nodes (list[TextNode]): The original list of TextNode instances to be split.
        delimiter (str): The delimiter string used to split the text in the TextNode instances.
        text_type (TextType): The TextType to be assigned to the new TextNode instances created after splitting.

    Returns:
        list[TextNode]: A new list of TextNode instances, where each instance contains a portion of the original text,
                        split by the specified delimiter. Each new instance will have the specified text_type.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown, unmatched delimiter: {delimiter}")
        for i, part in enumerate(parts):
            if part == "":
                continue
            part_type = TextType.TEXT if i % 2 == 0 else text_type
            new_nodes.append(TextNode(part, part_type, node.url))
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for alt, url in images:
            before, remaining_text = remaining_text.split(f"![{alt}]({url})", 1)
            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for anchor, url in links:
            before, remaining_text = remaining_text.split(f"[{anchor}]({url})", 1)
            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes