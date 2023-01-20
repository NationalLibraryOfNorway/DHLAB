from urllib.parse import urlparse

import requests
from IPython.display import HTML, display


def code_toggle(button_text="Klikk for å vise/skjule kodeceller"):
    display(
        HTML(
            '''<div>
                <style>
                 .mybutton {
                    background-color: lightgrey;
                    border: none;
                    color: white;
                    padding: 10px 16px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    margin: 4px 2px;
                    cursor: pointer;
                }
            </style>
            <script>
                code_show=true;
                function code_toggle() {
                 if (code_show){
                 $('div.input').hide();
                 } else {
                 $('div.input').show();
                 }
                 code_show = !code_show
                }
                $( document ).ready(code_toggle);
            </script>
            <form  action="javascript:code_toggle()">
                <input class='mybutton' type="submit" value=''' + '"' + button_text + '"' + '''>
            </form>
        </div>'''
        ))


def css(url="https://raw.githubusercontent.com/Yoonsen/Modules/master/css_style_sheets/nb_notebook.css"):
    """Associate a css stylesheet with the notebook,
    just specify a file or web reference, default is a custom css"""

    uri = urlparse(url)
    css_file = ""

    if uri.scheme.startswith('http'):
        query = requests.get(url)
        if query.status_code == 200:
            css_file = query.text

    elif uri.scheme == "file":
        # assume on form "file:/// on windows there is drive letter on unix not"
        file_path = url[7:]
        if file_path[2] == ':':  # then windows drive reference
            file_path = file_path[1:]
        with open(file_path, encoding='utf-8') as file:
            css_file = file.read()
    else:
        # assume string is a file locator
        with open(url, encoding='utf-8') as file:
            css_file = file.read()

    return HTML(f"<style>{css_file}</style>")
