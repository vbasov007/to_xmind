
from string import Template


class SimpleHtmlTemplate:

    html = Template('''
    <!DOCTYPE HTML>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>${Page_Title}</title>
    </head>
    <body>
    <style>${Style}</style>
    <table>
        <tr>
        ${Table_Headers}
        </tr>
        <tr>
        ${Table_Content}
        </tr>
    </table>
    <script>${Script}</script>
    </body>
    </html>
    ''')
    script = '''
    var tree = document.querySelectorAll('ul.tree a:not(:last-child)');
            for(var i = 0; i < tree.length; i++){
                tree[i].addEventListener('click', function(e) {
                    var parent = e.target.parentElement;
                    var classList = parent.classList;
                    if(classList.contains("open")) {
                        classList.remove('open');
                        var opensubs = parent.querySelectorAll(':scope .open');
                        for(var i = 0; i < opensubs.length; i++){
                            opensubs[i].classList.remove('open');
                        }
                    } else {
                        classList.add('open');
                    }
                    e.preventDefault();
                });
            }
    '''

    style = '''
    body {
                font-family: Arial;
            }

            ul.tree li {
                list-style-type: none;
                position: relative;
            }

            ul.tree li ul {
                display: none;
            }

            ul.tree li.open > ul {
                display: block;
            }

            ul.tree li a {
                color: black;
                text-decoration: none;
            }

            ul.tree li a:before {
                height: 1em;
                padding:0 .1em;
                font-size: .8em;
                display: block;
                position: absolute;
                left: -1.3em;
                top: .2em;
            }

            ul.tree li > a:not(:last-child):before {
                content: '+';
            }

            ul.tree li.open > a:not(:last-child):before {
                content: '-';
            }
            td {
                vertical-align: top;
            }
            
            table, th, td {
                border: 3px solid red;
                border-collapse: collapse;
            }
            
            th {
	            background: lightgrey
            }
            
            tr td:first-child {
                background: lightgrey;
                font-weight: bold;
            }
            
            a:hover {
                background: lightgray;
            
            /*table {
                display: block;
                overflow-x: auto;
                white-space: nowrap;
            }*/
    
    '''