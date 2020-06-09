"""
Dynamically load in a .ui file to a widget and return it to a parent
"""

from PySide2 import QtUiTools, QtCore


class UILoad(QtUiTools.QUiLoader):

    def __init__(self, base_widget, ):

        QtUiTools.QUiLoader.__init__(self, base_widget)
        self.base_widget = base_widget

    def createWidget(self, class_name, parent=None, name=''):

        if parent is None and self.base_widget:
            # supposed to create the top-level widget, return the base instance instead
            return self.base_widget

        else:
            if class_name in self.availableWidgets():
                # create a widget for child widgets
                widget = QtUiTools.QUiLoader.createWidget(self, class_name, parent, name)

            else:
                # if not in the list of availableWidgets, must be a custom widget
                # this will raise KeyError if the user has not supplied the
                # relevant class_name in the dictionary, or TypeError, if
                # customWidgets is None
                try:
                    widget = self.customWidgets[class_name](parent)

                except (TypeError, KeyError):
                    raise Exception(
                        'No custom widget ' + class_name + ' found in customWidgets param of UiLoader __init__.')

            if self.base_widget:
                # set an attribute for the new child widget on the base
                # instance, just like PyQt4.uic.loadUi does.
                setattr(self.base_widget, name, widget)

                # this outputs the various widget names, e.g.
                # sampleGraphicsView, dockWidget, samplesTableView etc.

            return widget


def loadUi(uifile, base_widget):
    uiloader = UILoad(base_widget)
    created_widget = uiloader.load(uifile)
    QtCore.QMetaObject.connectSlotsByName(created_widget)
    return created_widget
