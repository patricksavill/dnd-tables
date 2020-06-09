import os
import sys
import loadui
import json
from PySide2 import QtWidgets


class DnDTables(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(DnDTables, self).__init__(parent)

        self.ui = loadui.loadUi('main.ui', self)

        self.load_encounters()

        self.dice_spin_box.setKeyboardTracking(False)
        self.dice_spin_box.valueChanged.connect(self.dice_roll)
        self.dice_spin_box.setMinimum(1)

        self.second_dice_spin_box.setKeyboardTracking(False)
        self.second_dice_spin_box.valueChanged.connect(self.second_dice_roll)
        self.second_dice_spin_box.setMinimum(1)
        self.second_dice_spin_box.setHidden(True)
        self.second_dice_label.setHidden(True)

        self.table_combo_box.currentIndexChanged.connect(self.combo_update)
        self.combo_update()

    def load_encounters(self):

        self.encounters = {}
        for filename in os.listdir(os.getcwd() + '/json-tables'):
            if filename.endswith('.json'):
                self.ui.table_combo_box.addItem(filename.split('.')[0])
                self.encounters[filename.split('.')[0]] = json.load(
                    open('/'.join([os.getcwd(), 'json-tables', filename]), 'r'))

    def combo_update(self):
        range_max = len(self.encounters[self.ui.table_combo_box.currentText()])

        self.dice_spin_box.setMaximum(range_max)

        self.dice_label.setText("Dice roll: 1-{0}".format(str(range_max)))
        self.dice_roll()

    def dice_roll(self):
        dice_number = str(self.dice_spin_box.value())
        current_dict = self.encounters[self.table_combo_box.currentText()]

        entry = current_dict[dice_number]
        if type(entry) == dict:
            if 'encounter' in entry:
                self.second_dice_label.setHidden(False)
                self.second_dice_spin_box.setHidden(False)

                range_max = len(entry) - 1  # -1 because of the first key entry
                self.second_dice_spin_box.setMaximum(range_max)
                self.second_dice_label.setText("Dice roll: 1-{0}".format(str(range_max)))

                self.outcome.setPlainText("[Roll Again]")
        else:
            self.second_dice_label.setHidden(True)
            self.second_dice_spin_box.setHidden(True)
            self.outcome.setPlainText(current_dict[dice_number])

    def second_dice_roll(self):
        dice_number = str(self.dice_spin_box.value())
        second_dice_number = str(self.second_dice_spin_box.value())
        current_dict = self.encounters[self.table_combo_box.currentText()]
        if type(current_dict[dice_number]) == dict:
            entry_pt1 = current_dict[dice_number]['encounter']
            entry_pt2 = current_dict[dice_number][second_dice_number]

            self.outcome.setPlainText('\n\n'.join([entry_pt1, entry_pt2]))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    d = DnDTables()
    d.show()

    sys.exit(app.exec_())
