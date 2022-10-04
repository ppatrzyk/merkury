from merkury.renderer import *

def test_join_chunks():
    assert list(join_chunks(zip([], []))) == []
    code = zip(
        (["""print("aaa")"""], ["a = 5", "b = 6"], ["""print("a")""", ""], ),
        ("aaa\n", "", "a\n", )
    )
    joined = [
        {"in": """print("aaa")\n""", "out": "aaa\n", "html": False, "markdown": False},
        {"in": """a = 5\nb = 6\nprint("a")\n\n""", "out": "a\n", "html": False, "markdown": False}
    ]
    assert list(join_chunks(code)) == joined
