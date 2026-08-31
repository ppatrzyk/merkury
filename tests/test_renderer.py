from merkury.renderer import *


def test_generate_chunks():
    assert generate_chunks(zip([], [])) == []
    code = zip(
        (
            ["""print("aaa")"""],
            ["a = 5", "b = 6"],
            ["""print("a")""", "#TITLE previous title", "#TITLE last title", ""],
        ),
        (
            "aaa\n",
            "",
            "a\n",
        ),
    )
    joined = [
        {
            "in": """print("aaa")\n""",
            "out": "aaa\n",
            "html": False,
            "markdown": False,
            "number": 1,
            "title": None,
        },
        {
            "in": """a = 5\nb = 6\nprint("a")\n#TITLE previous title\n#TITLE last title\n\n""",
            "out": "a\n",
            "html": False,
            "markdown": False,
            "number": 2,
            "title": "last title",
        },
    ]
    assert generate_chunks(code) == joined
