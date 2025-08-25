import re

class SimpleMLParser:
    def __init__(self, markup):
        self.markup = markup

    def parse(self):
        # Tag to HTML mapping
        tag_map = {
            'title': lambda x: f"<h1>{x}</h1>",
            'heading': lambda x: f"<h2>{x}</h2>",
            'text': lambda x: f"<p>{x}</p>",
            'code': lambda x: f"<pre><code>{x}</code></pre>"
        }
        # Pattern to match (tag)content(end tag)
        pattern = re.compile(r"\((\w+)\)(.*?)\(end \1\)", re.DOTALL)
        html_output = self.markup
        # Replace each tag with HTML
        for match in pattern.finditer(self.markup):
            tag, content = match.groups()
            if tag in tag_map:
                html = tag_map[tag](content.strip())
                html_output = html_output.replace(match.group(0), html)
        return html_output

if __name__ == "__main__":
    simpleml_doc = """
    (title)My Document(end title)
    (heading)Introduction(end heading)
    (text)This is the first paragraph of my document.(end text)
    (code)print("Hello, World!")(end code)
    """
    parser = SimpleMLParser(simpleml_doc)
    html_result = parser.parse()
    print(html_result)