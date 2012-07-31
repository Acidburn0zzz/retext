import markups
from subprocess import Popen, PIPE
from PyQt4.QtCore import *
from PyQt4.QtGui import *

app_name = "ReText"
app_version = "4.0 (Git)"

settings = QSettings('ReText project', 'ReText')

try:
	import enchant
	enchant.Dict()
except:
	enchant_available = False
else:
	enchant_available = True

icon_path = "icons/"

DOCTYPE_NONE = ''
DOCTYPE_MARKDOWN = markups.MarkdownMarkup.name
DOCTYPE_REST = markups.ReStructuredTextMarkup.name
DOCTYPE_HTML = 'html'

monofont = QFont()
if settings.contains('editorFont'):
	monofont.setFamily(readFromSettings(settings, 'editorFont', str))
else:
	monofont.setFamily('monospace')
if settings.contains('editorFontSize'):
	monofont.setPointSize(readFromSettings(settings, 'editorFontSize', int))

try:
	from PyQt4.QtWebKit import QWebView
except:
	webkit_available = False
else:
	webkit_available = True

def readFromSettings(key, keytype, settings=settings):
	try:
		return settings.value(key, type=keytype)
	except TypeError as error:
		if str(error).startswith('unable to convert'):
			# New PyQt version, but type mismatch
			print('Warning: '+str(error))
			# Return an instance of keytype
			return keytype()
		# For old PyQt versions
		if keytype == str:
			return settings.value(key).toString()
		elif keytype == int:
			result, ok = settings.value(key).toInt()
			if not ok:
				print('Warning: cannot covert settings value to int!')
			return result
		elif keytype == bool:
			return settings.value(key).toBool()

def readListFromSettings(key, settings=settings):
	if not settings.contains(key):
		return []
	value = settings.value(key)
	try:
		return value.toStringList()
	except:
		# For Python 3
		if isinstance(value, str):
			return [value]
		else:
			return value

def writeListToSettings(key, value, settings=settings):
	if len(value) > 1:
		settings.setValue(key, value)
	elif len(value) == 1:
		settings.setValue(key, value[0])
	else:
		settings.remove(key)

def convertToUnicode(string):
	try:
		return unicode(string)
	except:
		# For Python 3
		return string