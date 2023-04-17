from customtex import parse, is_text, Part, Text, Switch
from pathlib import Path

TEMPLATES_PATH = Path(__file__).parent / "templates"

def load_template(name: str) -> str:
    with open(TEMPLATES_PATH / name) as f:
        return f.read()
    
def test_parse():
    template = load_template("parse.txt")
    parsed = parse(template)

    assert parsed == [
"""Quis mollit nostrud ea <var:var1=opt1> laborum 
do eu nostrud deserunt <multi:var2=1|2> est do ad.

""",
"""<switch:blocks1=block1|block2|block3>
<block:blocks1=block1>
Deserunt commodo labore est labore 
dolore duis voluptate nostrud nulla.
<block:blocks1=block2>
Est mollit reprehenderit officia 
incididunt cupidatat culpa occaecat anim.
<block:blocks1=block3>
Est mollit reprehenderit officia 
incididunt cupidatat culpa occaecat anim.
<endswitch:blocks1>""",
"""
Duis est cupidatat deserunt labore in sint 
enim veniam ipsum aliquip in proident commodo et.

""",
"""<include:blocks2>
Esse in et exercitation aute eiusmod labore sit non.
<switch:blocks3=block1|block2>
<block:blocks3=block1>
Deserunt commodo labore est labore 
dolore duis voluptate nostrud nulla.
<block:blocks3=block2>
Est mollit reprehenderit officia 
incididunt cupidatat culpa occaecat anim.
<endinclude:blocks2>""",
"""<switch:blocks1>
<block:blocks1=block1>
Deserunt commodo labore est labore 
dolore duis voluptate nostrud nulla.
<block:blocks1=block2>
Est mollit reprehenderit officia 
incididunt cupidatat culpa occaecat anim.
<block:blocks1=block3>
Est mollit reprehenderit officia 
incididunt cupidatat culpa occaecat anim.
<endswitch:blocks1>""",
"""
"""
    ]

def test_is_text():
    assert is_text("Lorem ipsum <var:var1> sit amet <multi:var2=1|2>.")
    assert not is_text("<switch:blocks1=block1|block2|block3>")
    assert not is_text("<include:blocks2>")

def test_text_init():
    template = load_template("text_init.txt")
    text = Text(template)

    assert text.text == template
    assert text.variables == {
        "var1": "deserunt",
        "var2": "",
    }
    assert text.multi == {
        "multi1": (["opt1", "opt2"], False),
        "multi2": (["1", "", "3"], True),
    }
