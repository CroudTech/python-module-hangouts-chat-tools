import sys
import os
import json

from .card import Card
from .card import CardSection
from .card import CardImageWidget
from .card import TextParagraphWidget
from .card import CardButtonWidget
from .card import KeyValueWidget

def test_card_name():
    card_name = 'testcard'
    card = Card(card_name)
    assert card.name == card_name


def test_to_json():
    card_name = 'testcard'
    card = Card(card_name)
    section = CardSection('testsection')
    card.addSection(section)
    widget = CardImageWidget('testimagewidget', 'https://picsum.photos/200', link="https://google.com")
    section.addWidget(widget)

    widget = TextParagraphWidget('testtextwidget', "Here is some text")
    section.addWidget(widget)
    expected = json.loads("""
    {
    "card": {
        "sections": [
            {
                "widgets": [
                    {
                        "image": {
                            "imageUrl": "https://picsum.photos/200",
                            "onClick": {
                                "openLink": {
                                    "url": "https://google.com"
                                }
                            }
                        }
                    },
                    {
                        "textParagraph": {
                            "text": "Here is some text"
                        }
                    }
                ]
            }
        ]
    }
}
""")
    assert expected == json.loads(card.toJson())

    section.getWidgetByName('testtextwidget').updateText('Updated')
    section.getWidgetByName('testimagewidget').updateImage('https://picsum.photos/300')
    expected = json.loads("""
{
    "card": {
        "sections": [
            {
                "widgets": [
                    {
                        "image": {
                            "imageUrl": "https://picsum.photos/300",
                            "onClick": {
                                "openLink": {
                                    "url": "https://google.com"
                                }
                            }
                        }
                    },
                    {
                        "textParagraph": {
                            "text": "Updated"
                        }
                    }
                ]
            }
        ]
    }
}
""")
    assert expected == json.loads(card.toJson())

    widget = TextParagraphWidget('anothertextwidget', "Here is some text to be inserted")
    section.addWidget(widget, after='testimagewidget')
    expected = json.loads("""
{
    "card": {
        "sections": [
            {
                "widgets": [
                    {
                        "image": {
                            "imageUrl": "https://picsum.photos/300",
                            "onClick": {
                                "openLink": {
                                    "url": "https://google.com"
                                }
                            }
                        }
                    },
                    {
                        "textParagraph": {
                            "text": "Here is some text to be inserted"
                        }
                    },
                    {
                        "textParagraph": {
                            "text": "Updated"
                        }
                    }
                ]
            }
        ]
    }
}
""")
    assert expected == json.loads(card.toJson())

    widget = TextParagraphWidget('anothertextwidget2', "Here is some more text to be inserted")
    section.addWidget(widget, before='testimagewidget')
    expected = json.loads("""
{
    "card": {
        "sections": [
            {
                "widgets": [
                    {
                        "textParagraph": {
                            "text": "Here is some more text to be inserted"
                        }
                    },
                    {
                        "image": {
                            "imageUrl": "https://picsum.photos/300",
                            "onClick": {
                                "openLink": {
                                    "url": "https://google.com"
                                }
                            }
                        }
                    },
                    {
                        "textParagraph": {
                            "text": "Here is some text to be inserted"
                        }
                    },
                    {
                        "textParagraph": {
                            "text": "Updated"
                        }
                    }
                ]
            }
        ]
    }
}
""")
    assert expected == json.loads(card.toJson())

def test_button_widget():
    card_name = 'testcard'
    card = Card(card_name)
    section = CardSection('testsection')
    card.addSection(section)
    widget = CardButtonWidget('testimagewidget', link='https://picsum.photos/200', content="some content", button_type="textButton")
    section.addWidget(widget)
    expected = json.loads("""
{
    "card": {
        "sections": [
            {
                "widgets": [
                    {
                        "textButton": {
                            "onClick": {
                                "openLink": {
                                    "url": "https://picsum.photos/200"
                                }
                            },
                            "text": "some content"
                        }
                    }
                ]
            }
        ]
    }
}
""")
    assert expected == json.loads(card.toJson())

def test_key_value_widget():
    card_name = 'testcard'
    card = Card(card_name)
    section = CardSection('testsection')
    card.addSection(section)
    widget = KeyValueWidget(name="testkvwidget", top_label="Some top label", content="Some content", content_multiline=False, bottom_label="A bottom label", link="https://test.com", icon="TRAIN", button="")
    section.addWidget(widget)

    expected = json.loads("""
{
    "card": {
        "sections": [
            {
                "widgets": [
                    {
                        "keyValue": {
                            "topLabel": "Some top label",
                            "content": "Some content",
                            "bottomLabel": "A bottom label",
                            "onClick": {
                                "openLink": {
                                    "url": "https://test.com"
                                }
                            },
                            "icon": "TRAIN"
                        }
                    }
                ]
            }
        ]
    }
}""")

    assert expected == json.loads(card.toJson())

def test_key_value_with_button_widget():
    card_name = 'testcard'
    card = Card(card_name)
    section = CardSection('testsection')
    card.addSection(section)
    button = CardButtonWidget('testimagewidget', link='https://picsum.photos/200', content="some content", button_type="textButton")
    widget = KeyValueWidget(name="testkvwidget", top_label="Some top label", content="Some content", content_multiline=False, bottom_label="A bottom label", link="https://test.com", icon="TRAIN", button=button)
    section.addWidget(widget)

    expected = json.loads("""
{
    "card": {
        "sections": [
            {
                "widgets": [
                    {
                        "keyValue": {
                            "topLabel": "Some top label",
                            "content": "Some content",
                            "bottomLabel": "A bottom label",
                            "onClick": {
                                "openLink": {
                                    "url": "https://test.com"
                                }
                            },
                            "icon": "TRAIN",
                            "button": {
                                "textButton": {
                                    "onClick": {
                                        "openLink": {
                                            "url": "https://picsum.photos/200"
                                        }
                                    },
                                    "text": "some content"
                                }
                            }
                        }
                    }
                ]
            }
        ]
    }
}""")

    assert expected == json.loads(card.toJson())

def test_add_header():
    card_name = 'testcard'
    card = Card(card_name)
    card.title = "Test Header"
    card.subtitle = "a subtitle"
    card.imageUrl = "https://example.com/image.jpg"

    expected = json.loads("""
{
    "card": {
        "sections": [],
        "header": {
            "title": "Test Header",
            "imageStyle": "IMAGE",
            "subtitle": "a subtitle",
            "imageUrl": "https://example.com/image.jpg"
        }
    }
}""")

    assert expected == json.loads(card.toJson())

def test_add_basic_header():
    card_name = 'testcard'
    card = Card(card_name)
    card.title = "Test Header"
    expected = json.loads("""
{
    "card": {
        "sections": [],
        "header": {
            "title": "Test Header"
        }
    }
}""")

    assert expected == json.loads(card.toJson())