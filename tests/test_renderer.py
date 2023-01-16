from merkury.renderer import *

def test_join_chunks():
    assert join_chunks(zip([], [])) == []
    code = zip(
        (["""print("aaa")"""], ["a = 5", "b = 6"], ["""print("a")""", "#TITLE test title", ""], ),
        ("aaa\n", "", "a\n", )
    )
    joined = [
        {"in": """print("aaa")\n""", "out": "aaa\n", "html": False, "markdown": False, "number": 1, "title": None},
        {"in": """a = 5\nb = 6\nprint("a")\n#TITLE test title\n\n""", "out": "a\n", "html": False, "markdown": False, "number": 2, "title": "test title"}
    ]
    assert join_chunks(code) == joined
