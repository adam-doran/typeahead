from collections import defaultdict

class PrefixSearcher:
    def __init__(self, file_path: str, max_results: int = None):
        self.prefix_map = self.build_prefixes(file_path)

        self.max_results = max_results

    def build_prefixes(self, file_path: str) -> dict:
        # default dict takes care of creating empty lists for prefixes that don't exist yet
        prefix_map = defaultdict(list)
        with open(file_path, 'r') as w:
            for word in w.readlines():
                word = word.lower().rstrip('\n')
                if word.isalpha():
                    for i in range(len(word)):
                        prefix_map[word[0:i+1]].append(word)
        return prefix_map


    def get_words_for_prefix(self, prefix: str) -> list[str]:
        '''Returns first {self.max_results} words alphabetically, assuming input words is alphabetically sorted'''
        # input validation
        prefix = prefix.strip().lower()
        if prefix == '':
            return []
        if not prefix.isalpha():
            raise ValueError("Unsupported characters in input")

        # without this case, we could inadvertantly create infinite dict keys due to default dict behaviour
        if prefix not in self.prefix_map:
            return []

        return self.prefix_map[prefix][:self.max_results]
