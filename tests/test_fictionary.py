import fictionary


def test_generate_word():
    assert type(fictionary.word()) is str


def test_num_words():
    random_words = fictionary.words(num_words=42)
    assert len(random_words) == 42
