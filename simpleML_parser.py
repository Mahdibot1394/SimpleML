import re

class SimpleMLParser:
    def __init__(self, markup):
        self.markup = markup

    def parse(self):
        tag_map = {
            # Headings and text
            'title': lambda x: f"<h1>{x}</h1>",
            'heading': lambda x: f"<h2>{x}</h2>",
            'subheading': lambda x: f"<h3>{x}</h3>",
            'subtitle': lambda x: f"<h4>{x}</h4>",
            'text': lambda x: f"<p>{x}</p>",
            'description': lambda x: f"<p class='description'>{x}</p>",
            'summary': lambda x: f"<summary>{x}</summary>",
            'note': lambda x: f"<div class='note'>{x}</div>",
            'tip': lambda x: f"<div class='tip'>{x}</div>",
            'warning': lambda x: f"<div class='warning'>{x}</div>",
            'info': lambda x: f"<div class='info'>{x}</div>",

            # Formatting
            'bold': lambda x: f"<b>{x}</b>",
            'italic': lambda x: f"<i>{x}</i>",
            'underline': lambda x: f"<u>{x}</u>",
            'strike': lambda x: f"<del>{x}</del>",
            'small': lambda x: f"<small>{x}</small>",
            'big': lambda x: f"<big>{x}</big>",
            'sup': lambda x: f"<sup>{x}</sup>",
            'sub': lambda x: f"<sub>{x}</sub>",
            'mark': lambda x: f"<mark>{x}</mark>",
            'highlight': lambda x: f"<span style='background:yellow;'>{x}</span>",
            'code': lambda x: f"<pre><code>{x}</code></pre>",
            'inlinecode': lambda x: f"<code>{x}</code>",
            'kbd': lambda x: f"<kbd>{x}</kbd>",

            # Lists
            'list': lambda x: f"<ul>{''.join([f'<li>{i.strip()}</li>' for i in x.split('|')])}</ul>",
            'numbered': lambda x: f"<ol>{''.join([f'<li>{i.strip()}</li>' for i in x.split('|')])}</ol>",
            'dl': lambda x: f"<dl>{''.join([f'<dt>{pair.split(';')[0].strip()}</dt><dd>{pair.split(';')[1].strip()}</dd>' for pair in x.split('|') if ';' in pair])}</dl>",
            'menu': lambda x: f"<menu>{''.join([f'<li>{i.strip()}</li>' for i in x.split('|')])}</menu>",

            # Tables
            'table': lambda x: "<table>" + ''.join(["<tr>" + ''.join([f"<td>{cell.strip()}</td>" for cell in row.split(';')]) + "</tr>" for row in x.split('|')]) + "</table>",
            'thead': lambda x: f"<thead>{x}</thead>",
            'tbody': lambda x: f"<tbody>{x}</tbody>",
            'tfoot': lambda x: f"<tfoot>{x}</tfoot>",
            'tr': lambda x: f"<tr>{x}</tr>",
            'th': lambda x: f"<th>{x}</th>",
            'td': lambda x: f"<td>{x}</td>",

            # Media
            'image': lambda x: f"<img src='{x.split('|')[0]}' alt='{x.split('|')[1] if '|' in x else ''}' />",
            'audio': lambda x: f"<audio controls src='{x}'></audio>",
            'video': lambda x: f"<video controls src='{x}'></video>",
            'figure': lambda x: f"<figure>{x}</figure>",
            'figcaption': lambda x: f"<figcaption>{x}</figcaption>",

            # Links and navigation
            'link': lambda x: f"<a href='{x.split('|')[0]}'>{x.split('|')[1]}</a>" if '|' in x else x,
            'email': lambda x: f"<a href='mailto:{x}'>{x}</a>",
            'tel': lambda x: f"<a href='tel:{x}'>{x}</a>",
            'nav': lambda x: f"<nav>{x}</nav>",
            'main': lambda x: f"<main>{x}</main>",
            'aside': lambda x: f"<aside>{x}</aside>",
            'section': lambda x: f"<section>{x}</section>",
            'article': lambda x: f"<article>{x}</article>",
            'footer': lambda x: f"<footer>{x}</footer>",
            'header': lambda x: f"<header>{x}</header>",

            # Structure
            'hr': lambda x: "<hr />",
            'br': lambda x: "<br />",
            'div': lambda x: f"<div>{x}</div>",
            'span': lambda x: f"<span>{x}</span>",
            'center': lambda x: f"<div style='text-align:center'>{x}</div>",
            'right': lambda x: f"<div style='text-align:right'>{x}</div>",
            'left': lambda x: f"<div style='text-align:left'>{x}</div>",

            # Semantic
            'address': lambda x: f"<address>{x}</address>",
            'details': lambda x: f"<details><summary>Details</summary>{x}</details>",
            'summarytag': lambda x: f"<summary>{x}</summary>", # renamed to avoid clash
            'time': lambda x: f"<time>{x}</time>",
            'meter': lambda x: f"<meter value='{x}'></meter>",
            'progress': lambda x: f"<progress value='{x}' max='100'></progress>",
            'abbr': lambda x: f"<abbr title='{x}'>{x}</abbr>",
            'var': lambda x: f"<var>{x}</var>",
            'samp': lambda x: f"<samp>{x}</samp>",

            # Forms
            'form': lambda x: f"<form>{x}</form>",
            'input': lambda x: f"<input placeholder='{x}' />",
            'button': lambda x: f"<button>{x}</button>",
            'label': lambda x: f"<label>{x}</label>",
            'fieldset': lambda x: f"<fieldset>{x}</fieldset>",
            'legend': lambda x: f"<legend>{x}</legend>",
            'select': lambda x: f"<select>{''.join([f'<option>{o.strip()}</option>' for o in x.split('|')])}</select>",
            'option': lambda x: f"<option>{x}</option>",
            'textarea': lambda x: f"<textarea>{x}</textarea>",
            'output': lambda x: f"<output>{x}</output>",

            # Scripts and embeds
            'script': lambda x: f"<script>{x}</script>",
            'noscript': lambda x: f"<noscript>{x}</noscript>",
            'embed': lambda x: f"<embed src='{x}' />",
            'object': lambda x: f"<object data='{x}'></object>",
            'param': lambda x: f"<param value='{x}' />",
            'canvas': lambda x: f"<canvas>{x}</canvas>",

            # Meta/info
            'meta': lambda x: f"<meta content='{x}' />",
            'titlemeta': lambda x: f"<title>{x}</title>",
            'base': lambda x: f"<base href='{x}' />",
            'linkmeta': lambda x: f"<link href='{x}' />",
            'css': lambda x: f"<style>{x}</style>",
            'js': lambda x: f"<script></script>",
            'csslink': lambda x: f'<link rel="stylesheet" href="{x}">',
            'jslink': lambda x: f"<script src={x}>",
            # Miscellaneous
            'blockquote': lambda x: f"<blockquote>{x}</blockquote>",
            'pre': lambda x: f"<pre>{x}</pre>",
            'dfn': lambda x: f"<dfn>{x}</dfn>",
            'bdo': lambda x: f"<bdo dir='rtl'>{x}</bdo>",
            'map': lambda x: f"<map>{x}</map>",
            'area': lambda x: f"<area alt='{x}' />",
            'del': lambda x: f"<del>{x}</del>",
            'ins': lambda x: f"<ins>{x}</ins>",
            'caption': lambda x: f"<caption>{x}</caption>",
            'colgroup': lambda x: f"<colgroup>{x}</colgroup>",
            'col': lambda x: f"<col span='{x}' />",
            'legendtag': lambda x: f"<legend>{x}</legend>", # to avoid clash
            'fieldsettag': lambda x: f"<fieldset>{x}</fieldset>", # to avoid clash
            'template': lambda x: f"<template>{x}</template>",
            'picture': lambda x: f"<picture>{x}</picture>",
            'source': lambda x: f"<source srcset='{x}' />",
            'track': lambda x: f"<track src='{x}' />",
            'svg': lambda x: f"<svg>{x}</svg>",
            'math': lambda x: f"<math>{x}</math>",
            'iframe': lambda x: f"<iframe src='{x}'></iframe>",
            'portal': lambda x: f"<portal src='{x}'></portal>",
            'dialog': lambda x: f"<dialog>{x}</dialog>",
            'marktag': lambda x: f"<mark>{x}</mark>", # to avoid clash
        }

        # Pattern to match (tag)content(end tag)
        pattern = re.compile(r"\((\w+)\)(.*?)\(end \1\)", re.DOTALL)
        html_output = self.markup
        for match in pattern.finditer(self.markup):
            tag, content = match.groups()
            if tag in tag_map:
                html = tag_map[tag](content.strip())
                html_output = html_output.replace(match.group(0), html)
        return html_output

if __name__ == "__main__":
    # Example with all 100 tags
    simpleml_doc = """
()
    """
    parser = SimpleMLParser(simpleml_doc)
    html_result = parser.parse()
    print(html_result)