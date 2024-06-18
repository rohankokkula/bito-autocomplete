import streamlit as st

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class AutocompleteSystem:
    def __init__(self):
        self.root = TrieNode()
        self.word_list = set()  # This will store all words for fast lookup

    def insert(self, word):
        current_node = self.root
        for char in word:
            if char not in current_node.children:
                current_node.children[char] = TrieNode()
            current_node = current_node.children[char]
        current_node.is_end_of_word = True
        self.word_list.add(word)

    def search(self, prefix):
        results = []
        current_node = self.root
        for char in prefix:
            if char in current_node.children:
                current_node = current_node.children[char]
            else:
                return results
        self._collect_words(current_node, list(prefix), results)
        return results

    def get_next_letters(self, prefix):
        current_node = self.root
        for char in prefix:
            if char in current_node.children:
                current_node = current_node.children[char]
            else:
                return []
        return list(current_node.children.keys())

    def _collect_words(self, node, prefix, results):
        if node.is_end_of_word:
            results.append(''.join(prefix))
        for char in node.children:
            prefix.append(char)
            self._collect_words(node.children[char], prefix, results)
            prefix.pop()

    def update(self, word):
        if word not in self.word_list:
            self.insert(word)

    def display(self):
        words = []
        self._collect_words(self.root, [], words)
        return words

    def clear(self):
        self.root = TrieNode()
        self.word_list = set()

def main():
    st.title("Bito exercise - Autocompletion")

    if 'autocomplete' not in st.session_state:
        st.session_state.autocomplete = AutocompleteSystem()
        initial_words = ["apple", "app", "application", "banana", "bat", "ball", "cat", "dog", "elephant"]
        for word in initial_words:
            st.session_state.autocomplete.insert(word)

    autocomplete = st.session_state.autocomplete
    words_container = st.empty()
    words_container.write(", ".join(autocomplete.display()))

    new_word = st.text_input("Enter a new word to add:", "")
    if st.button("Add Word") and new_word:
        autocomplete.update(new_word)
        st.success(f"Added '{new_word}' to the dictionary.")
        words_container.empty()
        words_container.write(", ".join(autocomplete.display()))

    prefix = st.text_input("Enter prefix to search:")
    results = autocomplete.search(prefix)
    next_letters = autocomplete.get_next_letters(prefix)

    if next_letters:
        st.text(f"Next possible letters: {', '.join(next_letters)}")
    if results:
        st.header(f"{', '.join(results)}")
    elif prefix:
        st.warning(f"No words found starting with '{prefix}'.")

if __name__ == "__main__":
    main()
