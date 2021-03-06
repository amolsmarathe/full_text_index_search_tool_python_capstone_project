
import docx
import glob


def docx_to_plain_text(docx_path, plain_text_path):
    """
    Convert a .docx file into plain text file. This plain text will be further used to build indexes.

    :param docx_path: Full path of the .docx document to be converted to plain text
    :param plain_text_path: Full path of a temporary test.txt file where the converted plain text will be stored for
     later use to build indexes
    :return: None
    """

    f1_doc = docx.opendocx(docx_path)
    f1_para_list = docx.getdocumenttext(f1_doc)

    plain_text = open(plain_text_path, 'w')
    for para in f1_para_list:
        para = remove_punctuations(para)
        plain_text.write('\n' + para)
    plain_text.close()


def remove_punctuations(text):
    """
    Filter and remove all the unwanted punctuations and special characters from the given text.

    :param text: The text (of type string) to be filtered.
    :return: Filtered text (of type string)
    """

    bad_char = ['[', '.', ',', '/', ';', "'",  '[', ']', '-', '=', '(', ')', '<', '>', '?', ':', '"', '{', '}', '_',
                '+', '!', '@', '#', '$', '%', '^', '&', '*', '~', '`', ']', '\\']
    text = list(filter(lambda char: char not in bad_char, text))
    return ''.join([str(elem) for elem in text])


files_text_dict = {}
indexes = {}


def start_indexing(path):
    """
    Build inverted indexes for all docx files in all directories and subdirectories at a given path.
    The indexes built are in-memory, run-time.

    :param path: The path at which all directories and subdirectories will be scanned for existing docx files
    :return: None
    """

    global indexes, files_text_dict
    plain_text_path = 'C:\\Users\\j39\\Desktop\\Python_Learnings\\Capstone_Projects_Udemy\\Data_Structure\\' \
                      'Inverted_Index_Search\\test_file.txt'

    docx_path_list = [f for f in glob.glob(path + "**/*.docx", recursive=True)]

    opened_files = []
    for docx_path in docx_path_list:
        if '~' in docx_path:
            docx_path_list.remove(docx_path)
            opened_files.append(docx_path)
    if len(opened_files) > 0:
        print('WARNING for Indexed data: Some files are currently in Open state. \nSearch tool may not account for the'
              ' latest changes in such files. \nYou can save and close these files to get most up-to-date search'
              'results. \nFollowing files are currently Opened:')
        for file in opened_files:
            print(f'\t{file}')

    for docx_path in docx_path_list:
        docx_to_plain_text(docx_path, plain_text_path)
        f = open(plain_text_path, 'r')
        files_text_dict[docx_path] = f.read()
        f.close()
    # for each_file in files:
    #     file_list.append(each_file)

    for each_file in files_text_dict:
        file_text_list = list(files_text_dict[each_file].lower().split())
        text_set = {''}
        # print(file_text_list)
        for word in file_text_list:
            # print(word)
            # print(indexes)
            if word not in text_set:
                text_set.add(word)
                if word in list(indexes.keys()):
                    indexes[word].append((each_file, file_text_list.count(word)))
                else:
                    indexes[word] = [(each_file, file_text_list.count(word))]


def search():
    """
    Search for a word or a phrase in the files using inverted index. Search results are naive and case-insensitive.
    Search result show: filename (full path) and frequency of occurrence of search item.
    It also throws a warning if some files are already in Open state.

    :return: None
    """

    search_item = input('What would you like to search for? ')
    word_list = search_item.lower().split()

    for i, word in enumerate(word_list):
        word_list[i] = remove_punctuations(word)

    print(f'\nSearch results for \'{search_item}\': ')
    for word in word_list:
        if word in indexes:
            word_index_tuple_list = indexes[word]
            for i, tpl in enumerate(word_index_tuple_list):
                if len(word_index_tuple_list) >= 2:
                    while i < len(word_index_tuple_list) - 1:
                        a1, a2 = word_index_tuple_list[i], word_index_tuple_list[i+1]
                        if a2[1] > a1[1]:
                            word_index_tuple_list[i] = a2
                            word_index_tuple_list[i+1] = a1
                        i += 1
            print(f'Occurrences of \'{word}\': ')
            for i in range(len(word_index_tuple_list)):
                print(f'In {word_index_tuple_list[i][0]}: {word_index_tuple_list[i][1]} times')
        else:
            print(f'Zero occurrences of \'{word}\': ')


def main():
    """
    Execute full text search (based on inverted index) and provide search results for user's search query.
    """

    path = 'C:\\Users\\j39\\Desktop\\localTEMP'
    start_indexing(path)

    search()


if __name__ == '__main__':
    main()
