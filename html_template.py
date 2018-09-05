from string import Template
from html_parser import get_div_tag_attributes




class ProductTableAsCompletePage:

    html = Template('''
    <!DOCTYPE HTML>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>${Page_Title}</title>
    </head>
    <body>
    <style>${Style}</style>
    <h3>${Table_Title}</h3>
    <div class="hideable" data-activate-on="${View_Name}" data-category="${Category}"
        data-subcategory="${Subcategory}"
        data-view="${View_Name}"
        data-menu-rank="product_table">
    <table>
        <tr>
        ${Table_Headers}
        </tr>
        <tr>
        ${Table_Content}
        </tr>
    </table>
    </div>
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
    
    var x = document.getElementsByClassName('product_status');
    for (var i = 0; i < x.length; i++){
        if (x[i].innerHTML=='not for new design' || x[i].innerHTML=='discontinued'){
            x[i].style.cssText= "color: red; font-weight: bold;";
        }
        else{
            x[i].style.cssText= "color: green; font-weight: bold;";
        }
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
            }
            
            span.package, span.housing {
                font-weight: bold;
                color: black;
            }
            
            span.technology {
                font-weight: bold;
                color: green;
            }
            
            span.configuration {
                font-weight: bold;
                color: brown;
            }
            
            span.features {
                font-weight: bold;
                color: darkblue;
            }
            
            span.qualification, span.applications, span.topology {
                font-weight: bold;
                color: darkblue;
            }
            
            
            span.product {
                font-weight: bold;
                color: darkviolet;
            }
            span.measure_value {
                font-weight: bold;
                color: darkblue;
            }
            
            span.measure_unit {
                font-weight: bold;
                color: orangered;
            }
            
            td.nowrap{
                white-space: nowrap;
            }
    '''

    def make(self, **f):
        return self.html.substitute(
            Category=f['Category'],
            Subcategory=f['Subcategory'],
            View_Name=f['View_Name'],
            Page_Title=f['Page_Title'],
            Table_Title=f['Table_Title'],
            Table_Headers=f['Table_Headers'],
            Table_Content=f['Table_Content'],
            Script=self.script,
            Style=self.style,
        )


class ProductTableOnly:

    html = Template('''
    <div class="hideable" data-activate-on="${Category}-${Subcategory}-${View_Name}"
        data-button-name="${View_Name}"
        data-category="${Category}"
        data-subcategory="${Subcategory}"
        data-view="${View_Name}"
        data-menu-rank="product_table">
     <table>
        <tr>
        ${Table_Headers}
        </tr>
        <tr>
        ${Table_Content}
        </tr>
    </table>
    </div>
    ''')

    def make(self, **f):
        return self.html.substitute(
            Category=f['Category'],
            Subcategory=f['Subcategory'],
            View_Name=f['View_Name'],
            Page_Title=f['Page_Title'],
            Table_Title=f['Table_Title'],
            Table_Headers=f['Table_Headers'],
            Table_Content=f['Table_Content'],
        )


class CompeleteToolTemplate:

    html = Template('''
    <!DOCTYPE HTML>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>${Page_Title}</title>
    </head>
    <style>${Style}</style>
        ${ButtonsSections}
        ${TableSections}       
    <script>${Script}</script>
    <body>
    </body>
    </html>
    ''')

    script = '''
            function HideAllTables(){
                var product_tables=document.getElementsByClassName("hideable")
                for(var i = 0; i < product_tables.length; i++){
                    product_tables[i].style.display="none"
                }
            }

            HideAllTables();

            function ShowOneHideOthers(elem){

                var hideable_elements = document.getElementsByClassName("hideable")
                var cur_level = MenuLevelInt(elem.getAttribute("data-menu-rank"))

                for(var i = 0; i < hideable_elements.length; i++){
                    if( MenuLevelInt(hideable_elements[i].getAttribute("data-menu-rank")) >= cur_level ){
                        hideable_elements[i].style.display="none"
                    }
                        
                }
                elem.style.display="block"

            }

            function HideLevelsBelow(div_obj){

                cur_level = MenuLevelInt(div_obj.getAttribute("data-menu-rank"))
 
                var all_hideable=document.getElementsByClassName("hideable")
                for(var i = 0; i < all_hideable.length; i++){
                    if( MenuLevelInt(all_hideable[i].getAttribute("data-menu-rank")) > cur_level){
                        all_hideable[i].style.display="none"
                    }
                }                

            }
 
            function ShowNextLevel(obj){

                HideLevelsBelow(obj.parentNode)

                var hideableElems=document.getElementsByClassName("hideable")


                for(i = 0; i < hideableElems.length; i++){
                    if( hideableElems[i].getAttribute("data-activate-on") == obj.getAttribute("data-id")){
        
                        ShowOneHideOthers( hideableElems[i] )
                    }
                }
            }

            function MenuLevelInt(rank_name){
                var levels = {
                        "category_buttons": 0,
                        "sub_category_buttons": 1,
                        "view_select_buttons": 2,
                        "product_table":3

                    }
                return levels[rank_name]
            }
    
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
                
                var x = document.getElementsByClassName('product_status');
                for (var i = 0; i < x.length; i++){
                    if (x[i].innerHTML=='not for new design' || x[i].innerHTML=='discontinued'){
                        x[i].style.cssText= "color: red; font-weight: bold;";
                    }
                    else{
                        x[i].style.cssText= "color: green; font-weight: bold;";
                    }
                }
            '''

    style = '''
        div.product_table {
                        display: "none";
                    }
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
                            }
                            
                            span.package, span.housing {
                                font-weight: bold;
                                color: black;
                            }
                            
                            span.technology {
                                font-weight: bold;
                                color: green;
                            }
                            
                            span.configuration {
                                font-weight: bold;
                                color: brown;
                            }
                            
                            span.features {
                                font-weight: bold;
                                color: darkblue;
                            }
                            
                            span.qualification, span.applications {
                                font-weight: bold;
                                color: darkblue;
                            }
                            
                            
                            span.product {
                                font-weight: bold;
                                color: darkviolet;
                            }
                            span.measure_value {
                                font-weight: bold;
                                color: darkblue;
                            }
                            
                            span.measure_unit {
                                font-weight: bold;
                                color: orangered;
                            }
                            
                            td.nowrap{
                                white-space: nowrap;
                            }
                            
                            hideable {
                                display: none
                            }
    '''

    def __init__(self):
        self.buttons_and_data_section = ButtonsAndDataSection()

    def add_table(self, html):
        self.buttons_and_data_section.add_table(html)

    def make(self):
        return self.html.substitute(
            Page_Title="Product Selection Tool",
            ButtonsSections=self.buttons_and_data_section.make_buttons(),
            TableSections=self.buttons_and_data_section.make_tables(),
            Script=self.script,
            Style=self.style,
        )

class ButtonsAndDataSection:

    category_button_section_templ = Template('''
        <div data-menu-rank="category_buttons">${Buttons_Html}</div>''')

    subcategory_button_section_templ = Template('''
        <div class="hideable"
        data-activate-on="${ActivateOn}"
        data-menu-rank="sub_category_buttons">${Buttons_Html}</div>''')

    view_select_button_section_templ = Template('''
        <div class="hideable"
        data-activate-on="${ActivateOn}"
        data-menu-rank="view_select_buttons">${Buttons_Html}</div>''')

    button_templ = Template('''
    <button type="button" data-id="${Name}" onclick=ShowNextLevel(this)>${Caption}</button>
    ''')

    templ_by_level = [category_button_section_templ, subcategory_button_section_templ, view_select_button_section_templ]

    def __init__(self):
        self.buttons = list()
        self.sections = list()
        self.tables = list()

    def is_section_new(self, level, name):
        for s in self.sections:
            if s['level'] == level and s['name'] == name:
                return False
        return True

    def is_button_new(self, name, in_section):
        for b in self.buttons:
            if b['name'] == name and b['section'] == in_section:
                return False
        return True

    def add_section(self, level, name):
        if self.is_section_new(level, name):
            self.sections.append({"name": name, "level": level})

    def add_button(self, name, in_section, caption):
        if self.is_button_new(name, in_section):
            self.buttons.append({"name": name, "section": in_section, "caption": caption})

    def add_table(self, table_html):
        attrs = get_div_tag_attributes(table_html)
        self.add_section(0, "main-category")
        self.add_button(attrs["data-category"], "main-category", attrs["data-category"])

        self.add_section(1, attrs["data-category"])
        self.add_button(attrs["data-subcategory"], attrs["data-category"], attrs["data-subcategory"])

        self.add_section(2, attrs["data-subcategory"])

        self.add_button(attrs["data-activate-on"], attrs["data-subcategory"], attrs['data-button-name'])

        self.tables.append(table_html)

    def button_html(self, name, caption):
        return self.button_templ.substitute(Name=name, Caption=caption)

    def section_html(self, activate_on, level, buttons_html):
        return self.templ_by_level[level].substitute(ActivateOn=activate_on, Buttons_Html=buttons_html)

    def make_buttons(self):
        out_html = ''
        for section in self.sections:
            but_html = ''
            for button in self.buttons:
                if button['section'] == section['name']:
                    but_html += self.button_html(button['name'], button['caption'])
            out_html += self.section_html(section['name'], section['level'], but_html)

        return out_html

    def make_tables(self):
        return ''.join(self.tables)
