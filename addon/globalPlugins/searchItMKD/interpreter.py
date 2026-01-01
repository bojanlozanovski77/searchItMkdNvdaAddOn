#interpreter.py

#In python 3, urllib has been reorganized
#import urllib
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from urllib.parse import quote                                                                                                                                                                
#it might be nice to provide more log output
#from logHandler import log
import json
import ui
import api
import textInfos
import addonHandler
import treeInterceptorHandler
import scriptHandler
import tones
import threading
import globalPluginHandler
import re
import sys
import os
import queueHandler
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import imp
a, b, c=imp.find_module("bs4")
BeautifulSoup=imp.load_module("bs4", a, b, c).BeautifulSoup
sys.path.remove(sys.path[-1])

def get(addr):
    #translators: error
    error=_("Ерор")
    try:
        #response=urlopen(addr).read()
        req = Request(
            addr, 
            data=None, 
            headers={
                #'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
            }
        )
        f = urlopen(req, timeout=180)
        response = f.read()
    except IOError as i:
        #translators: message spoken when we can't connect (error with connection)
        error_connection=_("Ерор при конекцијата")
        if str(i).find("Errno 11001")>-1:
            tones.beep(150, 200)
            ui.message(error_connection)
            return
        elif str(i).find("Errno 10060")>-1:
            tones.beep(150, 200)
            ui.message(error_connection)
            return
        elif str(i).find("Errno 10061")>-1:
            tones.beep(150, 200)
            #translators: message spoken when the connection is refused by our target
            ui.message(_("Има грешка при конекцијата"))
            return
        else:
            tones.beep(150, 200)
            ui.message(error+": "+str(i))
            return
    except Exception as i:
        tones.beep(150, 200)
        ui.message(error+": "+str(i))
        return
    return response

#definition
    #meaning
    #example
    #categories
    #semem-links
     
def word_count(string):
	if not string: return 0
	return len(string.split())

class Interpreter(threading.Thread):

    def __init__(self, text, *args, **kwargs):
        super(Interpreter, self).__init__(*args, **kwargs)
        self._stopEvent = threading.Event()
        self.text = text
        self.result = {}
        #queueHandler.queueFunction(queueHandler.eventQueue, ui.message, _("__init__(): START & FINISH"))

    def stop(self):
        self._stopEvent.set()

    def run(self):
        self.get_info(self.text)

    def get_info(self, text):
        final=""
        w=word_count(text)
        if w==1:
            #translators: message spoken after selecting text that contains a word (will be defined)
            final+=_("Се бара значењето на зборот...")
            queueHandler.queueFunction(queueHandler.eventQueue, ui.message, _(final))
            self.get_word_info_proba(text)
        else:
            final+=(_("Текстот содржи %s %s.") % (str(w), (_("збор") if w==1 else (_("збора") if w==2 else _("зборови")))))
            queueHandler.queueFunction(queueHandler.eventQueue, ui.message, _(final))
        
    def get_word_info_proba(self, word):
        #parsing logic based on that seen in pydictionary
        response=get("http://www.makedonski.info/search/"+quote(word))
        if not response:
            return
        try:
            #print(str(response))
            response=BeautifulSoup(response)
           
            grammar_temp = response.find("div", class_="grammar")
            meanings_temp = response.findAll("div", class_="definition")
            
            meanings = []
            
            for meaning_temp in meanings_temp:
                
                meaning = {}
            
                #2.1 meaning
                explanation_temp = meaning_temp.find("div", class_="meaning")
                explanation = ""
                if explanation_temp:
                    explanation = str(explanation_temp.text.strip().replace("\n", " ").replace("\t", " "))
                meaning["meaning"] = explanation
                
                #2.2 examples
                examples_temp = meaning_temp.findAll("div", class_="example")
                examples= []
                for example_temp in examples_temp:
                    example = ""
                    if example_temp:
                        example = str(example_temp.text.strip().replace("\n", " ").replace("\t", " "))
                    examples.append(example)
                meaning["example"] = examples
                
                #2.3 categories
                categories_temp = meaning_temp.find("div", id="categories")
                categories = ""
                if categories_temp:
                    categories = str(categories_temp.text.strip().replace("\n", " ").replace("\t", " "))
                meaning["categories"] = categories
                
                #2.4 additional meta data
                additional_meta_data_temp = meaning_temp.find("div", class_="semem-links")
                additional_meta_data = ""
                if additional_meta_data_temp:
                    additional_meta_data = str(additional_meta_data_temp.text.strip().replace("\n", " ").replace("\t", " "))
                meaning["semem-links"] = additional_meta_data
                
                meanings.append(meaning)
           
            grammar = ""
            if grammar_temp:
                grammar = str(grammar_temp.text.strip())

            #queueHandler.queueFunction(queueHandler.eventQueue, ui.message, _("grammar: "+str(grammar)))
            #queueHandler.queueFunction(queueHandler.eventQueue, ui.message, _("meanings: "+str(meanings)))
            self.result["text"] = word
            self.result["grammar"] = grammar
            self.result["meanings"] = meanings
        except IndexError:
            tones.beep(150, 200)
            #translators: message spoken when we're unable to find a definition for the given word
            queueHandler.queueFunction(queueHandler.eventQueue, ui.message, _("Не може да се најде дефиниција за зборот"))
        except Exception as e:
            tones.beep(150, 200)
            queueHandler.queueFunction(queueHandler.eventQueue, ui.message, _(str(e)))
