import re

def replace_abbreviations(sentence):
    pattern_aita1 = r'\bada\b'
    pattern_aita2 = r'\bida\b'
    pattern_aita3 = r'\baida\b'
    pattern_aita4 = r'\bada\b'
    pattern_tifu1 = r'\btyphoo\b'
    pattern_tifu2 = r'\bTIF(?:\s*,*\s*)you\b'
    
    modified_sentence = re.sub(pattern_aita1, 'AITA', sentence, flags=re.IGNORECASE)
    modified_sentence = re.sub(pattern_aita2, 'AITA', sentence, flags=re.IGNORECASE)
    modified_sentence = re.sub(pattern_aita3, 'AITA', sentence, flags=re.IGNORECASE)
    modified_sentence = re.sub(pattern_aita4, 'AITA', sentence, flags=re.IGNORECASE)
    modified_sentence = re.sub(pattern_tifu1, 'TIFU', modified_sentence, flags=re.IGNORECASE)
    modified_sentence = re.sub(pattern_tifu2, 'TIFU', modified_sentence, flags=re.IGNORECASE)

    return modified_sentence

def title_to_print(video_title):
    first_5_words = video_title[:-1].split()[:5]
    words_until_10_chars = ""
    for word in first_5_words:
        if len(words_until_10_chars) > 15:
              break
        else:
            words_until_10_chars += word + "_"
    return words_until_10_chars[:-1].replace(':', '').replace('&', '')

def splitTextForWrap(input_str: str, line_length: int):
    words = input_str.split(" ")
    line_count = 0
    split_input = ""
    line = ""
    i = 0
    for word in words:
        # long word case
        if (line_count == 0 and len(word) >= line_length):
            split_input += (word + ("\n" if i < (len(words) - 1) else ""))
        elif (line_count + len(word) + 1) > line_length:
            paddingNeeded = line_length - line_count
            alternatePadding = True
            while (paddingNeeded > 0):
                if alternatePadding:
                    line = "\u00A0" + line
                else:
                    line = line + "\u00A0"
                alternatePadding = not alternatePadding
                paddingNeeded -= 1
            line += "\n"

            split_input += line
            line = word
            line_count = len(word)
        else:
            line += ("\u00A0" + word) 
            line_count += len(word) + 1
        i += 1
    
    paddingNeeded = line_length - line_count
    alternatePadding = True
    while (line_count != 0 and paddingNeeded > 0):
        if alternatePadding:
            line = "\u00A0" + line
        else:
            line = line + "\u00A0"
        alternatePadding = not alternatePadding
        paddingNeeded -= 1
    split_input += line
    return split_input
