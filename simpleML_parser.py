import re

class SimpleMLParser:
    def __init__(self, markup):
        self.markup = markup
        self.tag_map = {
            # Headings and text
            'title': lambda content, attrs="": f"<h1{attrs}>{content}</h1>",
            'heading': lambda content, attrs="": f"<h2{attrs}>{content}</h2>",
            'subheading': lambda content, attrs="": f"<h3{attrs}>{content}</h3>",
            'subtitle': lambda content, attrs="": f"<h4{attrs}>{content}</h4>",
            'text': lambda content, attrs="": f"<p{attrs}>{content}</p>",
            'description': lambda content, attrs="": f"<p class='description'{attrs}>{content}</p>",
            'summary': lambda content, attrs="": f"<summary{attrs}>{content}</summary>",
            'note': lambda content, attrs="": f"<div class='note'{attrs}>{content}</div>",
            'tip': lambda content, attrs="": f"<div class='tip'{attrs}>{content}</div>",
            'warning': lambda content, attrs="": f"<div class='warning'{attrs}>{content}</div>",
            'info': lambda content, attrs="": f"<div class='info'{attrs}>{content}</div>",

            # Formatting
            'bold': lambda content, attrs="": f"<b{attrs}>{content}</b>",
            'italic': lambda content, attrs="": f"<i{attrs}>{content}</i>",
            'underline': lambda content, attrs="": f"<u{attrs}>{content}</u>",
            'strike': lambda content, attrs="": f"<del{attrs}>{content}</del>",
            'small': lambda content, attrs="": f"<small{attrs}>{content}</small>",
            'big': lambda content, attrs="": f"<big{attrs}>{content}</big>",
            'sup': lambda content, attrs="": f"<sup{attrs}>{content}</sup>",
            'sub': lambda content, attrs="": f"<sub{attrs}>{content}</sub>",
            'mark': lambda content, attrs="": f"<mark{attrs}>{content}</mark>",
            'highlight': lambda content, attrs="": f"<span style='background:yellow'{attrs}>{content}</span>",
            'code': lambda content, attrs="": f"<pre{attrs}><code>{content}</code></pre>",
            'inlinecode': lambda content, attrs="": f"<code{attrs}>{content}</code>",
            'kbd': lambda content, attrs="": f"<kbd{attrs}>{content}</kbd>",

            # Lists
            'list': lambda content, attrs="": f"<ul{attrs}>{''.join([f'<li>{i.strip()}</li>' for i in content.split('|')])}</ul>",
            'numbered': lambda content, attrs="": f"<ol{attrs}>{''.join([f'<li>{i.strip()}</li>' for i in content.split('|')])}</ol>",
            'dl': lambda content, attrs="": f"<dl{attrs}>{''.join([f'<dt>{pair.split(';')[0].strip()}</dt><dd>{pair.split(';')[1].strip()}</dd>' for pair in content.split('|') if ';' in pair])}</dl>",
            'menu': lambda content, attrs="": f"<menu{attrs}>{''.join([f'<li>{i.strip()}</li>' for i in content.split('|')])}</menu>",

            # Tables
            'table': lambda content, attrs="": f"<table{attrs}>" + ''.join(["<tr>" + ''.join([f"<td>{cell.strip()}</td>" for cell in row.split(';')]) + "</tr>" for row in content.split('|')]) + "</table>",
            'thead': lambda content, attrs="": f"<thead{attrs}>{content}</thead>",
            'tbody': lambda content, attrs="": f"<tbody{attrs}>{content}</tbody>",
            'tfoot': lambda content, attrs="": f"<tfoot{attrs}>{content}</tfoot>",
            'tr': lambda content, attrs="": f"<tr{attrs}>{content}</tr>",
            'th': lambda content, attrs="": f"<th{attrs}>{content}</th>",
            'td': lambda content, attrs="": f"<td{attrs}>{content}</td>",

            # Media
            'image': lambda content, attrs="": f"<img{attrs} />",
            'audio': lambda content, attrs="": f"<audio controls{attrs}>{content}</audio>",
            'video': lambda content, attrs="": f"<video controls{attrs}>{content}</video>",
            'figure': lambda content, attrs="": f"<figure{attrs}>{content}</figure>",
            'figcaption': lambda content, attrs="": f"<figcaption{attrs}>{content}</figcaption>",

            # Links and navigation
            'link': lambda content, attrs="": f"<a{attrs}>{content}</a>",
            'email': lambda content, attrs="": f"<a href='mailto:{content}'{attrs}>{content}</a>",
            'tel': lambda content, attrs="": f"<a href='tel:{content}'{attrs}>{content}</a>",
            'nav': lambda content, attrs="": f"<nav{attrs}>{content}</nav>",
            'main': lambda content, attrs="": f"<main{attrs}>{content}</main>",
            'aside': lambda content, attrs="": f"<aside{attrs}>{content}</aside>",
            'section': lambda content, attrs="": f"<section{attrs}>{content}</section>",
            'article': lambda content, attrs="": f"<article{attrs}>{content}</article>",
            'footer': lambda content, attrs="": f"<footer{attrs}>{content}</footer>",
            'header': lambda content, attrs="": f"<header{attrs}>{content}</header>",

            # Structure
            'hr': lambda content, attrs="": f"<hr{attrs} />",
            'br': lambda content, attrs="": f"<br{attrs} />",
            'div': lambda content, attrs="": f"<div{attrs}>{content}</div>",
            'span': lambda content, attrs="": f"<span{attrs}>{content}</span>",
            'center': lambda content, attrs="": f"<div style='text-align:center'{attrs}>{content}</div>",
            'right': lambda content, attrs="": f"<div style='text-align:right'{attrs}>{content}</div>",
            'left': lambda content, attrs="": f"<div style='text-align:left'{attrs}>{content}</div>",

            # Semantic
            'address': lambda content, attrs="": f"<address{attrs}>{content}</address>",
            'details': lambda content, attrs="": f"<details{attrs}><summary>Details</summary>{content}</details>",
            'summarytag': lambda content, attrs="": f"<summary{attrs}>{content}</summary>", # renamed to avoid clash
            'time': lambda content, attrs="": f"<time{attrs}>{content}</time>",
            'meter': lambda content, attrs="": f"<meter value='{content}'{attrs}></meter>",
            'progress': lambda content, attrs="": f"<progress value='{content}' max='100'{attrs}></progress>",
            'abbr': lambda content, attrs="": f"<abbr title='{content}'{attrs}>{content}</abbr>",
            'var': lambda content, attrs="": f"<var{attrs}>{content}</var>",
            'samp': lambda content, attrs="": f"<samp{attrs}>{content}</samp>",

            # Forms
            'form': lambda content, attrs="": f"<form{attrs}>{content}</form>",
            'input': lambda content, attrs="": f"<input placeholder='{content}'{attrs} />",
            'button': lambda content, attrs="": f"<button{attrs}>{content}</button>",
            'label': lambda content, attrs="": f"<label{attrs}>{content}</label>",
            'fieldset': lambda content, attrs="": f"<fieldset{attrs}>{content}</fieldset>",
            'legend': lambda content, attrs="": f"<legend{attrs}>{content}</legend>",
            'select': lambda content, attrs="": f"<select{attrs}>{''.join([f'<option>{o.strip()}</option>' for o in content.split('|')])}</select>",
            'option': lambda content, attrs="": f"<option{attrs}>{content}</option>",
            'textarea': lambda content, attrs="": f"<textarea{attrs}>{content}</textarea>",
            'output': lambda content, attrs="": f"<output{attrs}>{content}</output>",

            # Scripts and embeds
            'script': lambda content, attrs="": f"<script{attrs}>{content}</script>",
            'noscript': lambda content, attrs="": f"<noscript{attrs}>{content}</noscript>",
            'embed': lambda content, attrs="": f"<embed{attrs} />",
            'object': lambda content, attrs="": f"<object{attrs}>{content}</object>",
            'param': lambda content, attrs="": f"<param{attrs} />",
            'canvas': lambda content, attrs="": f"<canvas{attrs}>{content}</canvas>",

            # Meta/info
            'meta': lambda content, attrs="": f"<meta content='{content}'{attrs} />",
            'titlemeta': lambda content, attrs="": f"<title{attrs}>{content}</title>",
            'base': lambda content, attrs="": f"<base href='{content}'{attrs} />",
            'linkmeta': lambda content, attrs="": f"<link href='{content}'{attrs} />",
            'css': lambda content, attrs="": f"<style{attrs}>{content}</style>",
            'js': lambda content, attrs="": f"<script{attrs}>{content}</script>",
            'csslink': lambda content, attrs="": f'<link rel="stylesheet"{attrs}>',
            'jslink': lambda content, attrs="": f"<script{attrs}></script>",
            
            # Miscellaneous
            'blockquote': lambda content, attrs="": f"<blockquote{attrs}>{content}</blockquote>",
            'pre': lambda content, attrs="": f"<pre{attrs}>{content}</pre>",
            'dfn': lambda content, attrs="": f"<dfn{attrs}>{content}</dfn>",
            'bdo': lambda content, attrs="": f"<bdo dir='rtl'{attrs}>{content}</bdo>",
            'map': lambda content, attrs="": f"<map{attrs}>{content}</map>",
            'area': lambda content, attrs="": f"<area alt='{content}'{attrs} />",
            'del': lambda content, attrs="": f"<del{attrs}>{content}</del>",
            'ins': lambda content, attrs="": f"<ins{attrs}>{content}</ins>",
            'caption': lambda content, attrs="": f"<caption{attrs}>{content}</caption>",
            'colgroup': lambda content, attrs="": f"<colgroup{attrs}>{content}</colgroup>",
            'col': lambda content, attrs="": f"<col span='{content}'{attrs} />",
            'legendtag': lambda content, attrs="": f"<legend{attrs}>{content}</legend>", # to avoid clash
            'fieldsettag': lambda content, attrs="": f"<fieldset{attrs}>{content}</fieldset>", # to avoid clash
            'template': lambda content, attrs="": f"<template{attrs}>{content}</template>",
            'picture': lambda content, attrs="": f"<picture{attrs}>{content}</picture>",
            'source': lambda content, attrs="": f"<source{attrs} />",
            'track': lambda content, attrs="": f"<track{attrs} />",
            'svg': lambda content, attrs="": f"<svg{attrs}>{content}</svg>",
            'math': lambda content, attrs="": f"<math{attrs}>{content}</math>",
            'iframe': lambda content, attrs="": f"<iframe{attrs}>{content}</iframe>",
            'portal': lambda content, attrs="": f"<portal{attrs}>{content}</portal>",
            'dialog': lambda content, attrs="": f"<dialog{attrs}>{content}</dialog>",
            'marktag': lambda content, attrs="": f"<mark{attrs}>{content}</mark>", # to avoid clash
        }

    def replace_tag(self, match):
        tag, attrs, content = match.groups()
        if tag in self.tag_map:
            return self.tag_map[tag](content.strip(), attrs)
        return match.group(0)

    def parse(self):
        # Pattern to match (tag attributes)content(/tag)
        pattern = re.compile(r"\((\w+)([^)]*)\)(.*?)\(\/\1\)", re.DOTALL)

        html_output = self.markup
        # Loop to handle nested tags
        while True:
            html_output, n = pattern.subn(self.replace_tag, html_output)
            if n == 0:
                break
        return html_output

if __name__ == "__main__":
    simpleml_doc = """
(title)My Test Document(/title)
(text id="intro" class="main")This is a paragraph with attributes.(/text)
(description id="desc")A description with an ID.(/description)
(div)
    (heading)This is a heading inside a div(/heading)
    (list class="items")item 1|item 2|item 3(/list)
(/div)
(image src="/images/logo.png" alt="logo")(/image)
(hr class="separator")(/hr)
(link href="https://example.com" target="_blank")Click me(/link)
(audio src="sound.mp3" id="player")Your browser does not support the audio element.(/audio)
(csslink href="style.css")(/csslink)
(jslink src="script.js")(/jslink)
"""
    parser = SimpleMLParser(simpleml_doc)
    html_result = parser.parse()
    print(html_result)