#__init__.py

from functools import wraps
from .interface import SearchItSettingsPanel
from locale import getdefaultlocale
from time import sleep
from tones import beep
from .interpreter import Interpreter
import addonHandler
addonHandler.initTranslation()
import api
import config
import globalPluginHandler
import globalVars
import gui
import json
import os
import queueHandler
import scriptHandler
import textInfos
import threading
import tones
import ui
import wx
import six
import treeInterceptorHandler


def finally_(func, final):
	"""Calls final after func, even if it fails."""
	def wrap(f):
		@wraps(f)
		def new(*args, **kwargs):
			try:
				func(*args, **kwargs)
			finally:
				final()
		return new
	return wrap(final)

#CONSTANTS
#TEXT_CONSTANTS
TEXT_SELECTED = "q"
TEXT_CLIPBOARD = "w"
TEXT_LAST = "e"
#OPTION_CONSTANTS
OPTION_ALL = "q"
OPTION_GRAMMAR = "w"
OPTION_MEANINGS = "e"
OPTION_N_MEANINGS = "r" #number of meanings in general
OPTION_MEANING1 = "1"
OPTION_MEANING2 = "2"
OPTION_MEANING3 = "3"
OPTION_MEANING4 = "4"
OPTION_MEANING5 = "5"
OPTION_MEANING6 = "6"
OPTION_MEANING7 = "7"
OPTION_MEANING8 = "8"
OPTION_MEANING9 = "9"
OPTION_MEANING0 = "0"
OPTION_MEANING_SHIFT1 = "shift+1"
OPTION_MEANING_SHIFT2 = "shift+2"
OPTION_MEANING_SHIFT3 = "shift+3"
OPTION_MEANING_SHIFT4 = "shift+4"
OPTION_MEANING_SHIFT5 = "shift+5"
OPTION_MEANING_SHIFT6 = "shift+6"
OPTION_MEANING_SHIFT7 = "shift+7"
OPTION_MEANING_SHIFT8 = "shift+8"
OPTION_MEANING_SHIFT9 = "shift+9"
OPTION_MEANING_SHIFT0 = "shift+0"
# WARNING: the order of elements in this array is important. Changing the order of elements or the contents of the array will break the code.
OPTION_MEANING_ARRAY = [OPTION_MEANING1, OPTION_MEANING2, OPTION_MEANING3, OPTION_MEANING4, OPTION_MEANING5, OPTION_MEANING6, OPTION_MEANING7, OPTION_MEANING8, OPTION_MEANING9, OPTION_MEANING0]
# WARNING: the order of elements in this array is important. Changing the order of elements or the contents of the array will break the code.
OPTION_MEANING_SHIFT_ARRAY = [OPTION_MEANING_SHIFT1, OPTION_MEANING_SHIFT2, OPTION_MEANING_SHIFT3, OPTION_MEANING_SHIFT4, OPTION_MEANING_SHIFT5, OPTION_MEANING_SHIFT6, OPTION_MEANING_SHIFT7, OPTION_MEANING_SHIFT8, OPTION_MEANING_SHIFT9, OPTION_MEANING_SHIFT0]
    
index_IT = ""
index_ITIT = ""

last_final = ""

confspec = {
"grammar_info_checkbox": "boolean(default=true)",
"subtitle_checkbox": "boolean(default=true)",
"examples_checkbox": "boolean(default=true)",
"add_meta_data_checkbox": "boolean(default=true)",
"copy_result_to_clipboard_checkbox": "boolean(default=true)",
}
config.conf.spec["search_it"] = confspec

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	#scriptCategory = six.text_type(_addonSummary)

    def __init__(self, *args, **kwargs):
        super(GlobalPlugin, self).__init__(*args, **kwargs)
        self.getUpdatedGlobalVars()
        self.toggling = 0
        self.maxCachedResults = 5
        self.cachedResults = []
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(SearchItSettingsPanel)
        
    def terminate(self):
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(SearchItSettingsPanel)

    def getUpdatedGlobalVars(self):
        global isGrammarInfoChkd, isSubtitleChkd, isExamplesChkd, isAddMetaDataChkd, isCopyResultToClipboardChkd
		# should grammar information about the word in general be printed.
        isGrammarInfoChkd = config.conf['search_it']['grammar_info_checkbox']
		# should subtitle if any about every meaning of the word be printed.
        isSubtitleChkd = config.conf['search_it']['subtitle_checkbox']
		# should examples if any about every meaning of the word be printed.
        isExamplesChkd = config.conf['search_it']['examples_checkbox']
		# should additional meta data if any about every meaning of the word be printed.
        isAddMetaDataChkd = config.conf['search_it']['add_meta_data_checkbox']
        # should what has been printed last be copied to clipboard.
        isCopyResultToClipboardChkd = config.conf['search_it']['copy_result_to_clipboard_checkbox']

    def getScript(self, gesture):
        if self.toggling == 0:
            return globalPluginHandler.GlobalPlugin.getScript(self, gesture)
        else: #self.toggling == 1 OR self.toggling == 2
            script = globalPluginHandler.GlobalPlugin.getScript(self, gesture)
            if not script:
                script = finally_(self.script_error, self.finish_failure)
            else:
                if script == self.script_showSettings or script == self.script_copyLastResult:
                    script = finally_(script, self.finish_failure)
                elif script == self.script_ITLayer or script == self.script_qPressed or script == self.script_wPressed or script == self.script_ePressed:
                    script = finally_(script, self.finish_success)
                #else: do nothing.
        return script

    def finish_success(self):
        self.toggling = (self.toggling + 1)%3
        self.clearGestureBindings()
        #if self.toggling == 1: #This is never going to be the case, so that's why I am commenting it out.
        if self.toggling == 2:
            self.bindGestures(self.__ITITGestures)
        else: # self.toggling == 0
            index_IT = ""
            index_ITIT = ""
            self.bindGestures(self.__gestures)
           
    def finish_failure(self):
        self.toggling = 0
        index_IT = ""
        index_ITIT = ""
        self.clearGestureBindings()
        self.bindGestures(self.__gestures)
               
    def script_error(self, gesture):
        tones.beep(120, 100)
    
    def script_ITLayer(self, gesture):
		# A run-time binding will occur from which we can perform various layered translation commands.
        # First, check if a second press of the script was done.
        if not self.toggling == 0:
            self.script_error(gesture)
            return
        self.bindGestures(self.__ITGestures)
        self.toggling = 1
        tones.beep(100, 10)
    # Translators: message presented in input help mode, when user presses the shortcut keys for this addon.
    script_ITLayer.__doc__=_("Прво ниво на команди од речникот: q дава дефиниции за селектираниот збор, w дава дефиниции за зборот на клипбордот, e дава дефиниции за последниот дефиниран збор, c копира последна дефиниција на клипбордот, o ги отвара поставките за речникот.")
	
    def script_qPressed(self, gesture):
        global index_IT
        index_IT = TEXT_SELECTED
        #ui.message("q button was pressed")
        
    def script_wPressed(self, gesture):
        global index_IT
        index_IT = TEXT_CLIPBOARD
        #ui.message("w button was pressed")
        
    def script_ePressed(self, gesture):
        global index_IT
        index_IT = TEXT_LAST
        #ui.message("e button was pressed")
        
    def script_showSettings(self, gesture):
        wx.CallAfter(gui.mainFrame._popupSettingsDialog, gui.settingsDialogs.NVDASettingsDialog, SearchItSettingsPanel)
        	
    def script_copyLastResult(self, gesture):
        global last_final
        self.getUpdatedGlobalVars()
        if len(self.cachedResults) > 0:
            self.copyResult(last_final, ignoreSetting=True)
			# Translators: message presented to announce a successful copy
            ui.message(_("Резултат од последниот дефиниран збор на клипборд."))
        else:
			# Translators: message presented to announce no previous word definition disponibility
            ui.message(_("Нема последно зачувана дефиниција."))
	# Translators: Presented in input help mode.
    script_copyLastResult.__doc__ = _("Го копира последниот дефиниран збор на клипборд")
               
    def script_qPressedITIT(self, gesture):
        global index_ITIT
        index_ITIT = OPTION_ALL
        #ui.message("q button was pressed in ITIT level.")
        self.central()
     
    def script_wPressedITIT(self, gesture):
        global index_ITIT
        index_ITIT = OPTION_GRAMMAR
        #ui.message("w button was pressed in ITIT level.")
        self.central()
        
    def script_ePressedITIT(self, gesture):
        global index_ITIT
        index_ITIT = OPTION_MEANINGS
        #ui.message("e button was pressed in ITIT level.")
        self.central()
        
    def script_rPressedITIT(self, gesture):
        global index_ITIT
        index_ITIT = OPTION_N_MEANINGS
        #ui.message("r button was pressed in ITIT level.")
        self.central()
                
    def script_shiftNumberPressedITIT(self, gesture):
        global index_ITIT
        
        index = -1
        for gesture_identifier in gesture._get_identifiers():
            if gesture_identifier in list(self.__ITITGestures.keys()):
                index = list(self.__ITITGestures.keys()).index(gesture_identifier)
                break
                
        if not index == -1:
            if index < 10:
                index_ITIT = OPTION_MEANING_ARRAY[index]
                #ui.message(str(index+1)+" button was pressed in ITIT level.")
            else:
                index_ITIT = OPTION_MEANING_SHIFT_ARRAY[index - 10]
                #ui.message("shift "+str(index-10+1)+" button was pressed in ITIT level.")
            self.central()
        else: # THIS SHOULD NOT HAPPEN/CAN not happen
            ui.message(_("ЕРОР!"))
                
    def central(self):
        global index_IT
        global index_ITIT
        #ui.message("index_IT: "+str(index_IT)+", index_ITIT: "+str(index_ITIT))
        if index_IT == TEXT_SELECTED:
            #ui.message("TEXT_SELECTED")
            self.getInfo()
        elif index_IT == TEXT_CLIPBOARD:
            #ui.message("TEXT_CLIPBOARD")
            self.getClipInfo()
        elif index_IT == TEXT_LAST:
            #ui.message("TEXT_LAST")
            self.getLast()
        else: # THIS SHOULD NOT HAPPEN/CAN not happen
            ui.message(_("ЕРОР!"))
            
    def getClipInfo(self):
        try:
            text = api.getClipData()
            #ui.message("getClipInfo(): "+ text)
        except TypeError:
            text = None
        if not text or not isinstance(text, str):
			#translators: message spoken when the clipboard is empty
            ui.message(_("Нема никаков текст на клипбордот"))
            return
        else:
            threading.Thread(target=self.getWordInfoFromInterpreter, args=(text.strip(),)).start()

    def getInfo(self):
        text=""
        obj=api.getFocusObject()
        treeInterceptor=obj.treeInterceptor
        if hasattr(treeInterceptor,'TextInfo') and not treeInterceptor.passThrough:
            obj=treeInterceptor
        try:
            info=obj.makeTextInfo(textInfos.POSITION_SELECTION)
            #ui.message("getInfo()First Try: "+ info.text)
        except (RuntimeError, NotImplementedError):
            info=None
        if not info or info.isCollapsed:
            #No text selected, try grabbing word under review cursor
            info=api.getReviewPosition().copy()
            try:
                info.expand(textInfos.UNIT_WORD)
                #ui.message("getInfo()Second Try: "+ info.text)
            except AttributeError: #Nothing more we can do
                #translators: message spoken when no text is selected or focused
                ui.message(_("Селектирај прво нешто"))
                return
        #TRANSLATE
        threading.Thread(target=self.getWordInfoFromInterpreter, args=(info.text.strip(),)).start()
                    
    def getWordInfoFromInterpreter(self, text):
        #TRANSLATE
        #self.getUpdatedGlobalVars()
        global index_ITIT
        index_ITIT_local = index_ITIT
        #queueHandler.queueFunction(queueHandler.eventQueue, ui.message, _("getWordInfoFromInterpreter(): START"))
        result = {}
		
        if text in [x['text'] for x in self.cachedResults]:
            result = [f for f in self.cachedResults if f['text'] == text][0]
            index = [result_dict['text'] for result_dict in self.cachedResults].index(text)
            self.addResultToCache(result, removeIndex=index)
        #else block
        else:
            myInterpreter = None
            myInterpreter = Interpreter(text)
            myInterpreter.start()
            i=0
            while myInterpreter.is_alive():
                sleep(0.1)
                i+=1
                if i == 10:
                    beep(500, 100)
                    i = 0
            myInterpreter.join()
            result = myInterpreter.result
            if 'grammar' in result and result['grammar'] and 'meanings' in result and result['meanings'] and len(result['meanings'])>0:
                self.addResultToCache(result)
        
        #queueHandler.queueFunction(queueHandler.eventQueue, ui.message, _("getWordInfoFromInterpreter(): FINISH"))
        queueHandler.queueFunction(queueHandler.eventQueue, self.printMessage, {"message" : _(result), "index_ITIT_local":index_ITIT_local})
		#lang = myTranslator.lang_to
		#if translation != '':
		#	self.addResultToCache(text, translation, lang)
		#msgTranslation = {'text': translation, 'lang': lang}
		#queueHandler.queueFunction(queueHandler.eventQueue, messageWithLangDetection, msgTranslation)
		#self.copyResult(translation)
        
    def addResultToCache(self, result, removeIndex=0):
        if removeIndex:
            del self.cachedResults[removeIndex]
        elif len(self.cachedResults) == self.maxCachedResults:
            del self.cachedResults[0]
        self.cachedResults.append(result)
        
    def printMessage(self, packet):
        self.getUpdatedGlobalVars()
        global isGrammarInfoChkd
        global last_final
        final = ""
        
        message = packet['message']
        index_ITIT_local = packet['index_ITIT_local']
        
        if not message:
            return
        
        if index_ITIT_local == OPTION_ALL:
            final += self.getGrammar(message)
            final += self.getAllMeanings(message)
        elif index_ITIT_local == OPTION_GRAMMAR:
            final += self.getGrammar(message, ignoreGrammarSettings = True)
        elif index_ITIT_local == OPTION_MEANINGS:
            final += self.getAllMeanings(message)
        elif index_ITIT_local == OPTION_N_MEANINGS:
            final += self.getNMeanings(message)
        elif index_ITIT_local in OPTION_MEANING_ARRAY:
            final += self.getMeaning(message, OPTION_MEANING_ARRAY.index(index_ITIT_local))
        elif index_ITIT_local in OPTION_MEANING_SHIFT_ARRAY:
            final += self.getSubtitle(message, OPTION_MEANING_SHIFT_ARRAY.index(index_ITIT_local), True)
            
        if final and len(final.strip())>0:
            final = "Порака: "+final
        else:
            final = "Ништо не е најдено за тој збор"
        ui.message(final)
        
        #copy the printed message to clipboard also, but only if the Copy Result Checkbox is checked.
        last_final = final
        self.copyResult(final)
        
    def copyResult(self, final, ignoreSetting=False):
        global isCopyResultToClipboardChkd
        if ignoreSetting:
            api.copyToClip(final)
        elif isCopyResultToClipboardChkd:
            api.copyToClip(final)
            
    def getSubtitle(self, message, index, ignoreSubtitleSettings = False):
        global isSubtitleChkd
        final = ""
        if index < len(message['meanings']):
            if 'categories' in message['meanings'][index] and message['meanings'][index]['categories']:
                if ignoreSubtitleSettings:
                    final += "\t" + str(message['meanings'][index]['categories'])
                elif isSubtitleChkd:
                    final += "\n\t" + str(message['meanings'][index]['categories'])
        else:
            num = len(message['meanings'])
            final += (_("Нема веќе преводи. Овој збор има само %s %s.") % (str(num),(_("значење") if num == 1 else _("значења"))))        
        return final
        
    def getMeaning(self, message, index):
        global isExamplesChkd, isAddMetaDataChkd
        final = ""
        if "meanings" in message:
            messages = message['meanings']
            if index < len(messages):
                #1.1 Get meaning of the meaning
                if 'meaning' in messages[index] and messages[index]['meaning']:
                    final += str(messages[index]['meaning'])
                    
                #1.2 Get subtitle of the meaning if Subtitle checkbox is checked 
                final += self.getSubtitle(message, index)
                    
                #1.3 Get examples of the meaning if Examples checkbox is checked 
                if isExamplesChkd and 'example' in messages[index] and messages[index]['example'] and len(messages[index]['example'])>0:
                    final +=  "\n" + "Примери:   "
                    i = 0
                    for example in messages[index]['example']:
                        final += str(example)
                        if not i == (len(messages[index]['example']) - 1):
                            final += "\n\t"
                        i+=1
                                        
                #1.4 Get addMetaData of the meaning if AddMetaData checkbox is checked 
                if isAddMetaDataChkd and 'semem-links' in messages[index] and messages[index]['semem-links']:
                    final += "\n" + str(messages[index]['semem-links'])
  
            else:
                num = len(messages)
                final += (_("Нема веќе дефиниции. Овој збор има само %s %s.") % (str(num), (_("значење") if num == 1 else _("значења"))))
        return final
        
    def getAllMeanings(self, message):
        final = ""
        if "meanings" in message:
                for meaning in message['meanings']:
                    index = message['meanings'].index(meaning)
                    final += self.getMeaning(message, index)
                    if not index == (len(message['meanings']) - 1):
                        final += "\n"
        return final
        
    def getNMeanings(self, message):
        final = ""
        if "meanings" in message:
            num = len(message['meanings'])
            final += (_("Овој збор има %s %s.") % (str(num), (_("значење") if num == 1 else _("значења"))))
        return final
        
    def getGrammar(self, message, ignoreGrammarSettings = False):
        global isGrammarInfoChkd
        final = ""
        if "grammar" in message:
            if ignoreGrammarSettings:
                final += str(message['grammar'])
            elif isGrammarInfoChkd:
                final += (str(message['grammar']) + '\n')
        return final
                 
    def getLast(self):
        #TRANSLATE
        global index_ITIT
        index_ITIT_local = index_ITIT
        
        if len(self.cachedResults) > 0:
            last = self.cachedResults[len(self.cachedResults)-1]
            self.printMessage({"message" : _(last), "index_ITIT_local":index_ITIT_local})
        else:
            #translators: message spoken when the user tries getting previous information but there is none
            ui.message(_("Уште ја немаш добиено информацијата."))
        
    # changes
    # 'q' to 's'
    # 'w' to 'g'
    # 'e' to 'z'
    # 'r' to 'b'
    
    # WARNING: the order of the first 20 elements in this dictionary is important. Changing their order or the content of the first 20 elements will break the code.
    __ITITGestures={
        "kb:1":"shiftNumberPressedITIT", 
        "kb:2":"shiftNumberPressedITIT",
        "kb:3":"shiftNumberPressedITIT",
        "kb:4":"shiftNumberPressedITIT",
        "kb:5":"shiftNumberPressedITIT",
        "kb:6":"shiftNumberPressedITIT",
        "kb:7":"shiftNumberPressedITIT",
        "kb:8":"shiftNumberPressedITIT",
        "kb:9":"shiftNumberPressedITIT",
        "kb:0":"shiftNumberPressedITIT",
        "kb:shift+1":"shiftNumberPressedITIT",
        "kb:shift+2":"shiftNumberPressedITIT",
        "kb:shift+3":"shiftNumberPressedITIT",
        "kb:shift+4":"shiftNumberPressedITIT",
        "kb:shift+5":"shiftNumberPressedITIT",
        "kb:shift+6":"shiftNumberPressedITIT",
        "kb:shift+7":"shiftNumberPressedITIT",
        "kb:shift+8":"shiftNumberPressedITIT",
        "kb:shift+9":"shiftNumberPressedITIT",
        "kb:shift+0":"shiftNumberPressedITIT",
        "kb:s":"qPressedITIT", # 's' for 'se''
        "kb:g":"wPressedITIT", # 'g' for 'gramatika'
        "kb:d":"ePressedITIT", # 'z' for 'znachenja'
        "kb:b":"rPressedITIT", # 'b' for 'broj na znachenja'
    }
       
    __ITGestures={
        "kb:q":"qPressed",
        "kb:w":"wPressed",
        "kb:e":"ePressed",
        "kb:o":"showSettings",
        "kb:c":"copyLastResult",
    }

    __gestures = {
        "kb:NVDA+shift+x": "ITLayer",
    }
