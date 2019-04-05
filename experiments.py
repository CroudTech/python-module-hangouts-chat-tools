import json
from collections import OrderedDict


class CardSection(OrderedDict):
    def __init__(self, dict={}):
        self.__dict__ = dict
        self.widgets = {}

    def addWidget(self, name, widget, before=None, after=None):
        if before != None and before in self.widgets:
            keys = list(self.widgets.keys())
            index = keys.index(before)
            k1 = keys[index:]
            k2 = keys[:index]
            d1 = OrderedDict((key, self.widgets[key]) for key in self.widgets if key in k1)
            d2 = OrderedDict((key, self.widgets[key]) for key in self.widgets if key in k2)
            d2[name] = widget
            self.widgets = {**d2, **d1}
        elif after != None and after in self.widgets:
            keys = list(self.widgets.keys())
            index = keys.index(after)
            k1 = keys[index+1:]
            k2 = keys[:index+1]
            d1 = OrderedDict((key, self.widgets[key]) for key in self.widgets if key in k1)
            d2 = OrderedDict((key, self.widgets[key]) for key in self.widgets if key in k2)
            d2[name] = widget
            self.widgets = {**d2, **d1}
        else:
            self.widgets[name] = widget


testdict = CardSection()

for i in range(20):
    testdict.widgets['testkey' + str(i)] = 'testval' + str(i)

#print(testdict)


testdict.addWidget('testwidget444', 'inserted', after='sdfsdf')




print(json.dumps(testdict.widgets))

