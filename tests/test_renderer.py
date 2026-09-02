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
        (9.9, 20.1, 30.1),
    )
    joined = [
        {
            "in": """print("aaa")\n""",
            "out": "aaa\n",
            "html": False,
            "markdown": False,
            "number": 1,
            "title": "Chunk 1",
            "chunk_duration_ms": 10,
        },
        {
            "in": """a = 5\nb = 6\nprint("a")\n#TITLE previous title\n#TITLE last title\n\n""",
            "out": "a\n",
            "html": False,
            "markdown": False,
            "number": 2,
            "title": "last title",
            "chunk_duration_ms": 50,
        },
    ]
    assert generate_chunks(code) == joined
