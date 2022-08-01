import csv
import tkinter as tk
import os.path
import pickle


def word_from_list(event):
    if synonym_list_box.curselection() == ():
        return
    word = synonym_list_box.get(synonym_list_box.curselection()).lower()
    search_word.delete(0, tk.END)
    search_word.insert(tk.END, string=word)
    search_for_word()


def search_for_word():
    word = search_word.get().lower()
    word_list = thesaurus.get(word)
    synonym_list_box.delete(0, tk.END)
    if word_list is not None:
        word_list = sorted(list(word_list))
        for i, word in enumerate(word_list):
            synonym_list_box.insert(i, word)
    else:
        synonym_list_box.insert(0, 'Not found')


def build_thesaurus():
    d = {}
    if os.path.exists('synonyms.pickle'):
        with open('synonyms.pickle', 'rb') as pck:
            data = pck.read()
        d = pickle.loads(data)
    else:
        with open('synonyms.txt', 'rt') as file:
            all_words_list = list(csv.reader(file))[:-1]

            for words in all_words_list:
                for word_key in words:
                    word_key = word_key.lower()
                    if word_key.lower() not in d:
                        d[word_key] = set()

                    for synonym in words:
                        if word_key != synonym:
                            d[word_key].add(synonym)

    with open('synonyms.pickle', 'wb') as pck:
        pickle.dump(d, pck, protocol=pickle.HIGHEST_PROTOCOL)

    return d


window = tk.Tk()
window.title('Thesaurus')
window.minsize(width=300, height=600)

thesaurus = build_thesaurus()

title_label = tk.Label(text='Thesaurus', font='Arial 24 bold italic')
title_label.pack(pady=(5, 15))

search_word = tk.Entry(width=30)
search_word.focus()
search_word.pack(pady=5)

search_button = tk.Button(text='Find Synonyms', command=search_for_word)
search_button.pack(pady=(5, 25))

synonym_list_box = tk.Listbox(height=25, width=40)
synonym_list_box.bind(sequence='<<ListboxSelect>>', func=word_from_list)
synonym_list_box.pack(pady=5)


window.mainloop()