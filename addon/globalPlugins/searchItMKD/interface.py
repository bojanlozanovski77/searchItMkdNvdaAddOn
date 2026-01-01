#interface.py

import os.path
import wx
import gui
import globalVars
import config
import addonHandler
addonHandler.initTranslation()

class SearchItSettingsPanel(gui.SettingsPanel):
	# Translators: name of the dialog.
    title = _("Дигитален речник")

    def __init__(self, parent):
        super(SearchItSettingsPanel, self).__init__(parent)

    def makeSettings(self, sizer):
		# Translators: Title message for a dialog.
        titleLabel = wx.StaticText(self, label=_("Функции на речникот"))
        titleLabel.Wrap(self.GetSize()[0])
        sizer.Add(titleLabel)
        # Translators: First subtitle message for a dialog.
        fSubtitleLabel = wx.StaticText(self, label=_("Општи податоци за бараниот збор"))
        fSubtitleLabel.Wrap(self.GetSize()[0])
        sizer.Add(fSubtitleLabel)
        # Translators: A setting in addon settings dialog.
        self.grammarInfoChk = wx.CheckBox(self, label=_("Граматички информации"))
        self.grammarInfoChk.SetValue(config.conf['search_it']['grammar_info_checkbox'])
        sizer.Add(self.grammarInfoChk)
        # Translators: Second subtitle message for a dialog.
        sSubtitleLabel = wx.StaticText(self, label=_("Општи информации за бараниот збор"))
        sSubtitleLabel.Wrap(self.GetSize()[0])
        sizer.Add(sSubtitleLabel)
        # Translators: A setting in addon settings dialog.
        self.subtitleChk = wx.CheckBox(self, label=_("Превод"))
        self.subtitleChk.SetValue(config.conf['search_it']['subtitle_checkbox'])
        sizer.Add(self.subtitleChk)
        # Translators: A setting in addon settings dialog.
        self.examplesChk = wx.CheckBox(self, label=_("Примери"))
        self.examplesChk.SetValue(config.conf['search_it']['examples_checkbox'])
        sizer.Add(self.examplesChk)
        # Translators: A setting in addon settings dialog.
        self.addMetaDataChk = wx.CheckBox(self, label=_("Дополнителни општи податоци"))
        self.addMetaDataChk.SetValue(config.conf['search_it']['add_meta_data_checkbox'])
        sizer.Add(self.addMetaDataChk)
        # Translators: A setting in addon settings dialog.
        self.copyResultToClipboardChk = wx.CheckBox(self, label=_("Ископирај ја последната кажана дефиниција од даден збор на клипборд"))
        self.copyResultToClipboardChk.SetValue(config.conf['search_it']['copy_result_to_clipboard_checkbox'])
        sizer.Add(self.copyResultToClipboardChk)

    def postInit(self):
        self.grammarInfoChk.SetFocus()

    def onSave(self):
		# Update Configuration
        config.conf['search_it']['grammar_info_checkbox'] = self.grammarInfoChk.GetValue()
        config.conf['search_it']['subtitle_checkbox'] = self.subtitleChk.GetValue()
        config.conf['search_it']['examples_checkbox'] = self.examplesChk.GetValue()
        config.conf['search_it']['add_meta_data_checkbox'] = self.addMetaDataChk.GetValue()
        config.conf['search_it']['copy_result_to_clipboard_checkbox'] = self.copyResultToClipboardChk.GetValue()


