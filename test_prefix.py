import pytest
from prefix import PrefixSearcher

max_results = 10
prefix_searcher = PrefixSearcher('words_alpha.txt', max_results)
test_set = PrefixSearcher('test_words.txt')

@pytest.fixture
def prod_input() -> PrefixSearcher:
    return prefix_searcher
    
@pytest.fixture
def poor_input() -> PrefixSearcher:
    return test_set

def test_empty_query(prod_input):
    assert prod_input.get_words_for_prefix('') == []

def test_prod_input_miss(prod_input: PrefixSearcher):
    assert prod_input.get_words_for_prefix('chrufheskf') == []

def test_upper_lower(prod_input: PrefixSearcher):
    assert prod_input.get_words_for_prefix('AlPhabeTIC') == ['alphabetic', 'alphabetical', 'alphabetically', 'alphabetics']

def test_prefix_dict(poor_input: PrefixSearcher):
    for key, word_list in poor_input.prefix_map.items():
        assert key == key.lower()
        for word in word_list:
            assert word == word.lower()

def test_special_characters(prod_input: PrefixSearcher):
    with pytest.raises(Exception) as e:
        prod_input.get_words_for_prefix('£6345(*$!)(£')
    assert e.type == ValueError

def test_result_cap(prod_input: PrefixSearcher, poor_input: PrefixSearcher):
    # test max of {max_results}
    assert len(prod_input.get_words_for_prefix('a')) == max_results
    assert len(prod_input.get_words_for_prefix('alphabetic')) == 4

    # test no max
    assert len(poor_input.get_words_for_prefix('a')) == len(poor_input.prefix_map['a'])

def test_prefix_map_mem_leak(prod_input: PrefixSearcher):
    assert prod_input.get_words_for_prefix('chrufheskf') == []
    # ensure key wasn't added to prefix map
    assert 'chrufheskf' not in prod_input.prefix_map
