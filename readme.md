# SearchItMKD NVDA Add-on #

## Features

This package gives an explanation about selected words in Macedonian.

## Usage

This tool gives an explanation for words in macedonian language. It has to be only one word that this script will give an explanation for. <br><t>
    NVDA + shit + x for activation. <br><t>
    First layer of commands: <br><t><t>
        q : for info about selected text. (proceed to second layer of commands) <br></t></t>
        w : for clipboard text. (proceed to second layer of commands) <br></t></t>
        e : for last saved text. (proceed to second layer of commands) <br></t></t>
        o : show Settings Menu. <br></t></t>
        c : copies last given result to clipboard. <br></t>
    Second layer of commands: <br></t></t>
        s : grammar + all the meanings (basically all the information you can get about a word from this addon) ('s' as 'se'). <br></t></t>
        g : only grammar information ('g' as 'gramatika'). <br></t></t>
        d : only all the meanings information ('d' as 'definicii'). <br></t></t>
        b : info about how many meanings there are in total ('b' za 'broj na definicii'). <br></t></t>
        1 : only first meaning information (if there is one). <br></t></t>
        2 : only second meaning information (if there is one). <br></t></t>
        ... <br></t></t>
        0 : only 10-th meaning information (if there is one). <br></t></t>
        shift + 1 : only first meaning's translations (if there are any). <br></t></t>
        shift + 2 : only second meaning's translations (if therea are any). <br></t></t>
        ... <br></t></t> 
        shift + 0 : only 10-th meaning's translations (if there are any). <br></t>
    Meanings are taken from the Digital Dictionary of the Macedonian Language.

It can be configured whether grammar information about the word itself or some other attributes per every meaning of the word SHOULD be given/printed or not. <br>
Confgigurable categories per every meaning of the word are: <br></t>
	- Translations (if there are any provided by the Digital Dictionary). <br></t>
	- Examples of sentences using the word having that particular meaning (if there are any provided by the Digital Dictionary). <br></t>
	- Some additional meta data, such as synonyms, antonyms etc. (if there are any provided by the Digital Dictionary). These are configured as one single category. <br>
The only attribute that can not be configured is the definition of every meaning. The meanings' definitions are always shown. <br>
These categories can be congifured in nvda menu -> Preferences -> Settings -> SearchIt which can also be opened by the "second layer" 'o' command. <br>

