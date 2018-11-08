from word_forms.word_forms import get_word_forms
VERB,NOUN='v','n'
def main():
    print(get_word_forms("death")['v'])
if __name__=="__main__":
    main()