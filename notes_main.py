# начни тут создавать приложение с умными заметками
from PyQt5.Qt import (QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QTextEdit, QWidget,
QListWidget, QLineEdit, QInputDialog)
from PyQt5.QtCore import Qt
import json


class SmartNotes(QMainWindow):
    def __init__(self):
        super().__init__()
        # Главный экран
        self.setWindowTitle('Умные заметки')
        self.resize(900, 600)
        self.main_widget = QWidget()
        # Список лэйаутов
        self.main_layout = QHBoxLayout()
        self.right_layout = QVBoxLayout()
        self.left_layout = QVBoxLayout()

        self.notesButtons_layout = QHBoxLayout()
        self.tagsButtons_layout = QHBoxLayout()
        # Поле ввода текста
        self.field_text = QTextEdit()
        # Список заметок и кнопки для него
        self.some_notes = QLabel('Список заметок')
        self.field_notes = QListWidget()

        self.MakeNote_button = QPushButton('Cоздать заметку')
        self.DeleteNote_button = QPushButton('Удалить заметку')
        self.SaveNote_button = QPushButton('Сохранить заметку')
        # Список тэгов, поле поиска и кнопки для него
        self.some_tags = QLabel('Список тегов')
        self.field_tag = QListWidget()

        self.findTag_field = QLineEdit()
        self.findTag_field.setPlaceholderText('Введите тег...')

        self.MakeTag_button = QPushButton('Добавить к заметке')
        self.DeleteTag_button = QPushButton('Открепить от заметки')
        self.findNote_button = QPushButton('Искать заметки по тегу')

        # Создание словаря для хранения заметок, тегов и текста
        self.notes = {
            'Добро пожаловать': {
                'текст': 'В этом приложении можно создавать заметки с тегами...',
                'теги': ['Инструкция', 'Умные заметки']
            },
            'Привет': {
                'текст': 'В этой заметке я здороваюсь',
                'теги': ['Приветствие', 'Прощание']
            }
        }

        # Вызов функций для работы приложения
        self.setup_ui()
        try:
            self.read_json()
        except:
            self.write_json()
            for self.note in self.notes:
                self.field_notes.addItem(self.note)

        # Когда нажат элемент в списке заметок - вывести его элементы в виджеты
        self.field_notes.itemClicked.connect(self.show_result)

        # Обработка событий с полем заметок
        self.MakeNote_button.clicked.connect(self.add_note)
        self.DeleteNote_button.clicked.connect(self.del_note)
        self.SaveNote_button.clicked.connect(self.save_note)

        # Обработка событий с полем тегов и строкой поиска
        self.MakeTag_button.clicked.connect(self.add_tag)
        self.DeleteTag_button.clicked.connect(self.del_tag)
        self.findNote_button.clicked.connect(self.search_tag)

        # Функция для установки виджетов по направляющим линиям
    def setup_ui(self):
        # Набор для левого лэйаута
        self.left_layout.addWidget(self.field_text)

        # Добавление кнопок под заметками и тегами в горизонтальные лэйауты, чтобы находились на одном уровне

        # Кнопки под заметками
        self.notesButtons_layout.addWidget(self.MakeNote_button)
        self.notesButtons_layout.addWidget(self.DeleteNote_button)

        # Кнопки под тегами
        self.tagsButtons_layout.addWidget(self.MakeTag_button)
        self.tagsButtons_layout.addWidget(self.DeleteTag_button)

        # Набор для правого лэйаута
        self.right_layout.addWidget(self.some_notes)
        self.right_layout.addWidget(self.field_notes)
        self.right_layout.addLayout(self.notesButtons_layout)
        self.right_layout.addWidget(self.SaveNote_button)
        self.right_layout.addWidget(self.some_tags)
        self.right_layout.addWidget(self.field_tag)
        self.right_layout.addWidget(self.findTag_field)
        self.right_layout.addLayout(self.tagsButtons_layout)
        self.right_layout.addWidget(self.findNote_button)

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

    def read_json(self):
        with open('notes_main.json', 'r', encoding='utf-8') as file:
            self.notes = json.load(file)

        for self.note in self.notes:
            self.field_notes.addItem(self.note)

    def write_json(self):
        with open('notes_main.json', 'w', encoding='utf-8') as file:
            json.dump(self.notes, file, sort_keys=True)

    def show_result(self):
        self.name = self.field_notes.selectedItems()[0].text()
        self.field_tag.clear()
        self.field_text.setText(self.notes[self.name]['текст'])
        self.field_tag.addItems(self.notes[self.name]['теги'])

    def add_note(self):
        self.note_name, self.result = QInputDialog.getText(self, 'Добавить заметку', 'Название заметки:')
        if self.result and self.note_name != '':
            self.notes[self.note_name] = {'текст': '', 'теги': []}
            self.field_notes.addItem(self.note_name)
            self.write_json()

    def del_note(self):
        if self.field_notes.selectedItems():
            self.note_name = self.field_notes.selectedItems()[0].text()
            self.note_indx = self.field_notes.selectedItems()[0]

            del self.notes[self.note_name]

            self.field_notes.takeItem(self.field_notes.row(self.note_indx))
            self.field_tag.clear()
            self.field_text.clear()
            self.write_json()
        else:
            self.field_text.setText('!ЭЛЕМЕНТ ДЛЯ УДАЛЕНИЯ НЕ ВЫБРАН!')

    def save_note(self):
        if self.field_notes.selectedItems():
            self.note_name = self.field_notes.selectedItems()[0].text()
            self.notes[self.note_name]['текст'] = self.field_text.toPlainText()
            self.write_json()
        else:
            self.field_text.setText('!ЭЛЕМЕНТ ДЛЯ СОХРАНЕНИЯ НЕ ВЫБРАН!')

    def add_tag(self):
        if self.field_notes.selectedItems():
            self.note_name = self.field_notes.selectedItems()[0].text()
            self.tag_name = self.findTag_field.text()
            if self.tag_name not in self.notes[self.note_name]['теги']:
                self.notes[self.note_name]['теги'].append(self.tag_name)
                self.field_tag.addItem(self.notes[self.note_name]['теги'][-1])
                self.write_json()

    def del_tag(self):
        if self.field_tag.selectedItems():
            self.note_name = self.field_notes.selectedItems()[0].text()
            self.tag_indx = self.field_tag.selectedItems()[0]
            self.field_tag.takeItem(self.field_tag.row(self.tag_indx))

            del self.notes[self.note_name]['теги'][self.field_tag.row(self.tag_indx)]

            self.write_json()

    def search_tag(self):
        self.tag_name = self.findTag_field.text()
        if self.findNote_button.text() == 'Искать заметки по тегу' and self.tag_name:
            self.notes_filtered = {}

            self.findNote_button.setText('Сбросить поиск')

            for self.note in self.notes:
                if self.tag_name in self.notes[self.note]['теги']:
                    self.notes_filtered[self.note] = self.notes[self.note]

                    self.field_notes.clear()
                    self.field_tag.clear()
                    self.field_text.clear()
                    self.field_notes.addItems(self.notes_filtered)
        elif self.findNote_button.text() == 'Сбросить поиск':
            self.findTag_field.clear()
            self.field_notes.clear()
            self.field_tag.clear()
            self.field_text.clear()

            self.field_notes.addItems(self.notes)
            self.findNote_button.setText('Искать заметки по тегу')
        else:
            pass


app = QApplication([])
main_win = SmartNotes()
main_win.show()
app.exec_()
