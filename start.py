from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog
from ui import Ui_MainWindow
import json


class Widget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # записуємо першу замітку
        self.notes = {}

        self.ui.list_notes.itemClicked.connect(self.show_note)
        self.ui.button_note_create.clicked.connect(self.add_note)
        self.ui.button_note_save.clicked.connect(self.save_notes)
        self.ui.button_note_save.clicked.connect(self.del_note)

        with open ("notes_data.json", "r") as file:
            self.notes = json.load(file)
        self.ui.list_notes.addItems(self.notes)

    def show_note(self):
        key = self.ui.list_notes.selectedItems()[0].text()
        self.ui.textEdit.setText(self.notes[key]["Текст"])
        self.ui.list_tags.clear()
        self.ui.list_tags.addItems(self.notes[key]["теги"])


    def add_note(self):
        note_name, ok = QInputDialog.getText(notes_win, "Додати замітку", "Назва замітки:")
        if ok and note_name != "":
            self.notes[note_name] = {"Текст": "", "теги": []}
            self.ui.list_notes.addItem(note_name)
            self.ui.list_tags.addItems(self.notes[note_name]["теги"])
            print(self.notes)

    def del_note(self):
        if self.ui.list_notes.selectedItems():
            key=self.ui.list_notes.selectedItems()[0].text()
            del self.notes[key]
            self.ui.list_notes.clear()
            self.ui.list_tags.clear()
            self.ui.textEdit.clear()
            self.ui.list_notes.addItems(self.notes)
            self.ui.butto_note_del.clicked.connect(self.del_note)
            with open("notes_data.json", "w") as file:
                json.dump(self.notes, file, sort_keys=True, ensure_ascii=False)
            print(self.notes)
        else:
            print("Замітка для вилучення не обрана!")
        
    def save_notes(self):
        if self.ui.list_notes.selectedItems():
            key = self.ui.list_notes.selectedItems()[0].text()
            self.notes[key]["Текст"] = self.ui.textEdit.toPlainText()
            with open("notes_data.json", "w") as file:
                json.dump(self.notes, file, sort_keys=True, ensure_ascii=False)
            print(self.notes)
    
    def add_tag(self):
        if self.ui.list_notes.selectedItems():
            key = self.ui.list_notes.selectedItems()[0].text()
            tag = self.ui.textEdit.text()
            if not tag in self.notes[key]["теги"]:
                self.notes[key]["теги"].append(tag)
                self.ui.list_tags.addItem(tag)
                self.ui.textEdit.clear()
            with open("notes_data.json", "w") as file:
                json.dump(self.notes, file, sort_keys=True, ensure_ascil=False)
            print(self.notes)
        else:
            print("Замітка для додавання тега не обрана.")

    def del_tag(self):
        if self.ui.list_notes.selectedItems:
            key = self.ui.list_notes.selectedItems()[0].text()
            tag = self.ui.list_tags.selectedItems()[0].text()
            self.notes[key]["теги"].remove(tag)
            self.ui.list_tags.clear()
            self.ui.list_tags.addItems(self.notes[key]["теги"])
            with open("notes_data.json", "w") as file:
                json.dump(self.notes, file, sort_keys=True, ensure_ascil=False)
            print(self.notes)
        else:
            print("Тег для вилученя не обраний.")

    def seach_tag(self):
        tag = self.ui.textEdit.text()
        if self.ui.button_tag_seach.text() == "Шукати замітки по тегу" and tag:
            notes_filtered = {}
            for note in self.notes:
                if tag in self.notes[note]["теги"]:
                    notes_filtered[note] = self.notes[note]
            self.ui.button_tag_seach.setText("Скинути пошук")
            self.ui.list_notes.clear()
            self.ui.list_tags.clear()
            self.ui.list_notes.addItems(notes_filtered)
        elif self.ui.button_tag_seach.text == "Скинути пошук":
            self.ui.textEdit.clear()
            self.ui.list_tags.clear()
            self.ui.list_tags.clear()
            self.ui.list_notes.addItems(self.notes)
            self.ui.button_tag_seach.setText("Шукати амітки по тегу")
        else:
            pass


app = QApplication([])
notes_win = Widget()
notes_win.show()
app.exec_()