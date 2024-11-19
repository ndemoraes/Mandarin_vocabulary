
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from collections import namedtuple
from typing import List, Dict, NamedTuple

# Define the named tuples for word and character information

class WordInfo(NamedTuple):
    Tocfl: int = -1
    Definition: str = ''
    Chapter: int = 0

class CharacterInfo(NamedTuple):
    Tuttle: int = 0
    Heisig: int = 0
    Top3000: int = 0
    Tocfl: int = -1
    Definition: str = ''
    Words: List[str] = []
    Chapter: int = 0

class WordToLearn(NamedTuple):
    Word: str = ''
    WInfo: WordInfo = WordInfo()

class CharToLearn(NamedTuple):
    Character: str = ''
    CInfo: CharacterInfo = CharacterInfo()


def process_known_words(known_words, known_chars) -> None:

    # process words in simple text file
    file_path: str = './input_data/pre-skritter_known.txt'  # has only one column
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            word: str = line.strip()
            # Add word to known_words dictionary
            known_words[word] = None

            #  Break word into characters and populate known_characters dictionary
            for char in word:
                if char not in known_chars:
                    # Create a new CharacterInfo object with default integer values and the current word in the list
                    known_chars[char] = CharacterInfo(Tuttle=0, Heisig=0, Top3000=0, Tocfl=-1, Definition='',Words=[word], Chapter=0)
                else:
                    # Update the existing CharacterInfo by adding the word to the list of words
                    current_info: CharacterInfo = known_chars[char]
                    updated_words: List[str] = current_info.Words + [word]
                    known_chars[char] = current_info._replace(Words=updated_words)

    # Process words in TSV file - words I already know

    file_path = './input_data/skritter_export.tsv'
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Assuming columns are separated by tabs
            columns = line.strip().split('\t')
            word = columns[1]  # The word is in the second column
            definition: str = columns[3]  # The definition is in the fourth column

            # Step 4: Add the word to known_words dictionary with the Tocfl value as 0 and definition from column 4
            known_words[word] = WordInfo(Tocfl=-1, Definition=definition, Chapter=0)

            # Step 5: Break word into characters and populate known_characters dictionary
            for char in word:
                if char not in known_chars:
                    # Create a new CharacterInfo object with default integer values and the current word in the list
                    known_chars[char] = CharacterInfo(Tuttle=0, Heisig=0, Top3000=0, Tocfl=-1, Definition=columns[3], Words=[word], Chapter=0)
                else:
                    # Update the existing CharacterInfo by adding the word to the list of words
                    current_info = known_chars[char]
                    updated_words = current_info.Words + [word]
                    known_chars[char] = current_info._replace(Words=updated_words)

# _____________________________________________________________________________________________________________
# Create dictionary of important words and characters
def create_reference_dictionaries(word_ref, char_ref)-> None:
    # ADD characters from the Tuttle book
    file_path = './input_data/export-Tuttle.tsv'
    counter: int = 1  # Initialize a counter to keep track of character numbers in Tuttle book
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            columns: list[str] = line.strip().split('\t')
            word:str = columns[1] # the second column has the word
            # Check if it's a single character
            if len(word) == 1:
                # Add the character to the dictionary with the counter as the Tuttle entry number
                char_ref[word] = CharacterInfo(Tuttle=counter, Heisig=0, Top3000=0, Tocfl=-1, Definition=columns[3], Words=[], Chapter=0)
                counter += 1  # Increment the counter for the next character - does not match very well!

    # ADD characters from the Far East top 3000 characters book
    file_path2 = './input_data/export-Far_East_3000.tsv'
    counter2: int = 1  # Initialize a counter to keep track of character numbers in Top 3000 characters book
    with open(file_path2, 'r', encoding='utf-8') as file:
        for line in file:
            columns = line.strip().split('\t')
            char:str = columns[1] # the second column has the character
            if char not in char_ref:  # make sure not already added from Tuttle file
                char_ref[char] = CharacterInfo(Tuttle=0, Heisig=0, Top3000=counter2, Tocfl=-1, Definition=columns[3], Words=[], Chapter=0)
            else:
                new_char_info = char_ref[char]
                char_ref[char] = CharacterInfo(Tuttle=new_char_info.Tuttle, Heisig=new_char_info.Heisig, Top3000=counter2, Tocfl=new_char_info.Tocfl, Definition=columns[3], Words=new_char_info.Words, Chapter=0)
            counter2 += 1

        # ADD characters from the Heisig characters books
        file_path3 = './input_data/export-Heisig.tsv'
        counter3: int = 1  # Initialize a counter to keep track of character numbers in Top 3000 characters book
        #new_char_info = None
        with open(file_path3, 'r', encoding='utf-8') as file:
            for line in file:
                columns = line.strip().split('\t')
                char = columns[1]  # the second column has the character
                if char not in char_ref:  # make sure not already added from Tuttle file
                    char_ref[char] = CharacterInfo(Tuttle=0, Heisig=counter3, Top3000=0, Tocfl=-1, Definition=columns[3],
                                                   Words=[], Chapter=0)
                else:
                    new_char_info = char_ref[char]
                    char_ref[char] = CharacterInfo(Tuttle=new_char_info.Tuttle, Heisig=counter3,
                                                   Top3000=new_char_info.Top3000, Tocfl=new_char_info.Tocfl, Definition=columns[3],
                                                   Words=new_char_info.Words, Chapter=0)
                counter3 += 1

        # Add characters and words from the TOCFL exam list
        file_path4 = './input_data/Tocfl-new-2col.csv'
        with open(file_path4, 'r', encoding='utf-8') as file:
            for line in file:
                # Assuming columns are separated by commas
                # column 0 = word
                # column 1 = TOCFL level
                columns = line.strip().split(',')
                word = columns[0]  # The word is in the first column
                print("word:")
                print(word)
                if word not in word_ref:
                    word_ref[word] = WordInfo(Tocfl=int(columns[1]), Definition=' ', Chapter=0)
                else:
                    # Create copy of current entry
                    current_word_info: WordInfo = word_ref[word]   ####
                    # I want the lowest TOCFL level
                    if current_word_info.Tocfl < 0:  #  the default -1 value
                        word_ref[word] = current_word_info._replace(Tocfl=int(columns[1]))
                    elif current_word_info.Tocfl > int(columns[1]):  # if current value is higher, update
                        word_ref[word] = current_word_info._replace(Tocfl=int(columns[1]))
                    #else do not update, current tocfl value is lower

                #Break word into characters and update char_ref dictionary
                for char in word:
                    if char not in char_ref:
                        # Create a new CharacterInfo object with default integer values and the current word in the list
                        char_ref[char] = CharacterInfo(Tuttle=0, Heisig=0, Top3000=0, Tocfl=int(columns[1]), Definition='',
                                                          Words=[word], Chapter=0)
                    else:
                        # Update the existing CharacterInfo by adding the word to the list of words
                        current_char_info: CharacterInfo = char_ref[char]
                        updated_words: List[str] = current_char_info.Words + [word]
                        char_ref[char] = current_char_info._replace(Words=updated_words)
                        # I want the lowest TOCFL level
                        if current_char_info.Tocfl < 0:  # the default -1 value
                            char_ref[char] = current_char_info._replace(Tocfl=int(columns[1]))
                        elif current_char_info.Tocfl > int(columns[1]):  # if current value is higher, update
                            char_ref[char] = current_char_info._replace(Tocfl=int(columns[1]))
                        # else do not update, current tocfl value is lower




if __name__ == '__main__':
    # Initialize dictionaries - these global variables are changed by the function, not a copy
    ## Dictionaries for known words and characters
    known_words: Dict[str, WordInfo] = {}  # Dictionary with words as keys and WordInfo Class as value
    known_characters: Dict[str, CharacterInfo] = {}  # Dictionary with characters as keys and CharacterInfo Class as value
    process_known_words(known_words, known_characters)

    ## Dictionaries for most important words and characters
    reference_words: Dict[str, WordInfo] = {}
    reference_characters: Dict[str, CharacterInfo] = {}
    create_reference_dictionaries(reference_words, reference_characters)

    ## Lists for words and characters to learn
    words_to_learn: List[WordToLearn] = []
    chars_to_learn: List[CharToLearn] = []

    # extract words from the file containing words to learn
    file_path5 = './input_data/wordsToLearn.tsv'
    with open(file_path5, 'r', encoding='utf-8') as file:
        for line in file:
            # Assuming standard skritter output format
            # column 1 = word in traditional characters
            columns = line.strip().split('\t')
            word = columns[1]
            definition: str = columns[3]
            chapter: int = int(columns[4])
            if word not in known_words:
                # look it up in the reference
                if word in reference_words:
                    # add it to the list of words to learn
                    current_wordInfo = reference_words[word]
                    w_to_learn_tp:WordToLearn = WordToLearn(word, WordInfo(Tocfl=current_wordInfo.Tocfl, Definition=definition, Chapter=chapter))
                    words_to_learn.append(w_to_learn_tp)
                    print("word in reference words:", word)
                    print(w_to_learn_tp.WInfo)
                else:
                    w_to_learn_tp = WordToLearn(word, WordInfo(Tocfl=-1, Definition=definition, Chapter=chapter))
                    words_to_learn.append(w_to_learn_tp)
                    print("word NOT in reference words:", word)
                    print(w_to_learn_tp.WInfo)
            else: # word in known words
                print("known word", word)


    output_file_path = './output/words_to_learn.tsv'
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for element in words_to_learn:
            word = element.Word
            tocfl = element.WInfo.Tocfl
            definition = element.WInfo.Definition
            ch = element.WInfo.Chapter
            file.write(f"{word}\t{ch}\t{tocfl}\t{definition}\n")

    # extract characters from the file containing words to learn
    with open(file_path5, 'r', encoding='utf-8') as file:
        for line in file:
            # Assuming standard skritter output format
            # column 1 = word in traditional characters
            columns = line.strip().split('\t')
            word = columns[1]
            chapter = int(columns[4])

            for char in word:
                if char not in known_characters:
                    # skip if known

                    if char not in reference_characters:
                        # create default entry

                        new_char: CharacterInfo = CharacterInfo()
                        new_char = new_char._replace(Chapter=chapter)
                        new_char_to_learn: CharToLearn = CharToLearn(Character = char, CInfo=new_char)
                        chars_to_learn.append(new_char_to_learn)

                    else:
                        # create entry from reference
                        new_char = reference_characters[char]
                        new_char = new_char._replace(Chapter=chapter)
                        new_char_to_learn = CharToLearn(Character = char, CInfo=new_char)
                        chars_to_learn.append(new_char_to_learn)

    output_file_path = './output/chars_to_learn.tsv'
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write("char"+"\t"+"chap"+"\t"+"tocfl"+"\t"+"definition"+"\t"+"tuttle"+"\t"+"heisig"+"\t"+"top3000"+"\t"+"words" + "\n")
        for item in chars_to_learn:
            char = item.Character
            tuttle = item.CInfo.Tuttle
            heisig = item.CInfo.Heisig
            top3000 = item.CInfo.Top3000
            tocfl = item.CInfo.Tocfl
            definition = item.CInfo.Definition
            words = item.CInfo.Words
            ch = item.CInfo.Chapter
            file.write(f"{char}\t{ch}\t{tocfl}\t{definition}\t{tuttle}\t{heisig}\t{top3000}\t{words}\n")
            # todo: the ch variable is not getting updated, always zero
    # Output results (for verification purposes)
    # print("Known words dictionary with definitions:")
    # for word, info in known_words.items():
    #     print(f"Word: {word}, Info: {info}")
    #
    # print("\nKnown characters dictionary:")
    # for char, info in known_characters.items():
    #     print(f"Character: {char}, Info: {info}")

    # print("\nReference characters dictionary:")
    # for char, info in reference_characters.items():
    #     print(f"Character: {char}, Info: {info}")





# next: read in words to learn file - create a new dictionary or maybe list of tuples

# use last three files on new words to learn file
# see which words have zero unknown characters