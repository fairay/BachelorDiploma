colors = {
    'bg': "#edf4fe",
    'bgAlt': "#c1e3ff",
    'text': '#000000',
    'title': '#B4C7D4',
    'button': '#70bdf2',
    'accent1': '#4486B3',
    'accent2': '#4F6675',
    'accent3': '#153f65',
    'add1': '#9C4E05',
    'add2': '#BF7F43'
}

stylesheet = f"""
QMainWindow {{
    background-color: {colors['bg']};
}}

QPushButton {{
    border: 1px solid {colors['accent3']};
    border-radius: 10px;
    height: 35px
}}

QPushButton:hover {{
    background-color: {colors['bgAlt']};
}}

QListWidget {{
    border: 1px solid {colors['add1']};
    border-radius: 10px;
    background-color: {colors['bg']};
}}

QListWidget::item:selected QListWidget::item:hover {{
    background-color: {colors['bgAlt']};
}}

QComboBox {{
    color: {colors['text']};
    padding-left: 10px;
    border: 1px solid {colors['accent3']};
    border-radius: 10px;
    background-color: transparent;
}}

QWidget.list  {{
    background-color: {colors['bgAlt']};
}}

QLabel.wTitle {{
    color: {colors['accent1']};
}}

QLabel.pTitle {{
    color: {colors['accent2']};
}}

QLabel.cTitle {{
    width: 100%;
    color: {colors['accent3']};
}}
"""
