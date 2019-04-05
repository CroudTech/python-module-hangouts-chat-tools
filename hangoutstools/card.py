from collections import OrderedDict
import validators
import json

class Card:
    header_elements = [
        'title',
        'subtitle',
        'imageUrl',
        'imageStyle',
    ]
    def __init__(self, name):
        self.name = name
        self.card_object = OrderedDict()
        self.card = OrderedDict()
        self.card_object['cards'] = self.card
        self.card['sections'] = []
        self.sections = {}

    def _updateHeader(self):
        if 'header' not in self.card:
            self.card['header'] = {}
        if 'subtitle' in self.__dict__ and self.subtitle:
            self.card['header']['subtitle'] = self.subtitle
        else:
            self.card['header'].pop('subtitle', None)

        if 'title' in self.__dict__ and self.title:
            self.card['header']['title'] = self.title
        else:
            self.card['header'].pop('title', None)

        if 'imageUrl' in self.__dict__ and self.imageUrl and validators.url(self.imageUrl):
            self.card['header']['imageUrl'] = self.imageUrl
            if 'imageStyle' not in self.__dict__ or not self.imageStyle:
                self.imageStyle = 'IMAGE'
            self.card['header']['imageStyle'] = self.imageStyle
        else:
            self.card['header'].pop('imageStyle', None)
            self.card['header'].pop('imageUrl', None)

    def __setattr__(self, name, value):
        self.__dict__[name] = value

        if name in self.header_elements:
            self._updateHeader()

    def addSection(self, section, before=None, after=None):
        self.sections[section.name] = section

        if before != None and before in self.sections:
            keys = list(self.sections.keys())
            index = keys.index(before)
            k1 = keys[index:]
            k2 = keys[:index]
            d1 = OrderedDict((key, self.sections[key]) for key in self.sections if key in k1)
            d2 = OrderedDict((key, self.sections[key]) for key in self.sections if key in k2)
            d2[section.name] = section
            self.sections = {**d2, **d1}
        elif after != None and after in self.sections:
            keys = list(self.sections.keys())
            index = keys.index(after)
            k1 = keys[index+1:]
            k2 = keys[:index+1]
            d1 = OrderedDict((key, self.sections[key]) for key in self.sections if key in k1)
            d2 = OrderedDict((key, self.sections[key]) for key in self.sections if key in k2)
            d2[section.name] = section
            self.sections = {**d2, **d1}
        else:
            self.sections[section.name] = section
        self._updateSections()

    def getSections(self):
        return self.card['sections']

    def toJson(self):
        self._updateSections()
        return json.dumps(self.card_object, default=lambda o: vars(o)[Config.ODICT], indent=4)

    def _updateSections(self):
        self.card['sections'] = list(self.sections.values())


class CardSection(OrderedDict):
    def __init__(self, name, dict={}):
        self.__dict__ = dict
        self.name = name
        self.widgets = {}
        self['widgets'] = []

    def addWidget(self, widget, before=None, after=None):
        if before != None and before in self.widgets:
            keys = list(self.widgets.keys())
            index = keys.index(before)
            k1 = keys[index:]
            k2 = keys[:index]
            d1 = OrderedDict((key, self.widgets[key]) for key in self.widgets if key in k1)
            d2 = OrderedDict((key, self.widgets[key]) for key in self.widgets if key in k2)
            d2[widget.name] = widget
            self.widgets = {**d2, **d1}
        elif after != None and after in self.widgets:
            keys = list(self.widgets.keys())
            index = keys.index(after)
            k1 = keys[index+1:]
            k2 = keys[:index+1]
            d1 = OrderedDict((key, self.widgets[key]) for key in self.widgets if key in k1)
            d2 = OrderedDict((key, self.widgets[key]) for key in self.widgets if key in k2)
            d2[widget.name] = widget
            self.widgets = {**d2, **d1}
        else:
            self.widgets[widget.name] = widget

        self._updateWidgets()

    def _updateWidgets(self):
        self['widgets'] = list(self.widgets.values())

    def getWidgetByName(self, name):
        return self.widgets[name] if name in self.widgets else None

    def deleteSectionByName(self, name):
        return self.pop(name, None)

class CardWidget(OrderedDict):
    def __init__(self, name, dict={}):
        self.name = name
        self.__dict__ = dict

class CardImageWidget(CardWidget):
    def __init__(self, name, image, link=None):
        self.name = name
        self.link = None
        self['image'] = {
            'imageUrl': image
        }
        if link != None:
            self['image']['onClick'] = {
                'openLink': {
                    'url': link
                }
            }

    def updateImage(self, image):
        self['image']['imageUrl'] = image

class TextParagraphWidget(CardWidget):
    def __init__(self, name, text):
        self.name = name
        self.link = None
        self['textParagraph'] = {
            'text': text
        }

    def updateText(self, text):
        self['textParagraph']['text'] = text

class KeyValueWidget(CardWidget):
    def __init__(self, name, top_label="", content="", content_multiline=False, bottom_label="", link="", icon="", button=""):
        self.name = name
        self.key_value = {}
        self['keyValue'] = self.key_value
        self.topLabel = top_label
        self.content = content
        self.contentMultiline = content_multiline
        self.bottomLabel = bottom_label
        self.link = link
        self.icon = icon
        self.button = button
        self._updateWidget()

    def _updateWidget(self):
        if self.topLabel:
            self.key_value["topLabel"] = self.topLabel

        if self.content:
            self.key_value["content"] = self.content

        if self.contentMultiline:
            self.key_value["contentMultiline"] = self.contentMultiline

        if self.bottomLabel:
            self.key_value["bottomLabel"] = self.bottomLabel

        if self.link:
            self.key_value["onClick"] = {
                "openLink": {
                    "url": self.link
                }
            }

        if self.icon:
            if validators.url(self.icon):
                self.key_value["iconUrl"] = self.icon
            else:
                self.key_value["icon"] = self.icon

        if self.button:
            self.key_value["button"] = self.button

class CardButtonWidget(CardWidget):
    def __init__(self, name, link, content, button_type="imageButton"):
        self.name = name
        self.content = content
        self.link = link

        self.button = {
            'onClick': {
                'openLink': {
                    'url': self.link
                }
            }
        }

        self[button_type] = self.button

        self.button_type = button_type
        self._updateWidget()

    def updateLink(self, link):
        self.link = link
        self._updateWidget()

    def updateContent(self, content):
        self.content = content
        self._updateWidget()

    def _updateWidget(self):
        if self.button_type == "ImageButton":
            if validators.url(self.content):
                self.button['iconUrl'] = self.content
                self.pop('icon', None)
            else:
                self.button['icon'] = self.content
                self.pop('iconUrl', None)
        else:
            self.button['text'] = self.content




