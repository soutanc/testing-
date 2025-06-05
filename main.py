from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.lang import Builder
import sqlite3

Builder.load_file("main.kv")

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('expense.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscription
            (name TEXT, amount REAL, date TEXT, purpose TEXT)
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenditure
            (purpose TEXT, amount REAL, date TEXT)
        ''')
        self.conn.commit()

    def insert_subscription(self, name, amount, date, purpose):
        self.cursor.execute('''
            INSERT INTO subscription (name, amount, date, purpose)
            VALUES (?, ?, ?, ?)
        ''', (name, amount, date, purpose))
        self.conn.commit()

    def insert_expenditure(self, purpose, amount, date):
        self.cursor.execute('''
            INSERT INTO expenditure (purpose, amount, date)
            VALUES (?, ?, ?)
        ''', (purpose, amount, date))
        self.conn.commit()

    def get_subscription(self):
        self.cursor.execute('SELECT * FROM subscription')
        return self.cursor.fetchall()

    def get_expenditure(self):
        self.cursor.execute('SELECT * FROM expenditure')
        return self.cursor.fetchall()

db = Database()

class SubscriptionScreen(Screen):
    def add_data(self):
        name = self.ids.name_spinner.text
        amount = self.ids.amount_input.text
        date = self.ids.date_input.text
        purpose = self.ids.purpose_spinner.text
        if name != 'Select Name' and purpose != 'Select Purpose' and amount and date:
            db.insert_subscription(name, float(amount), date, purpose)
            self.clear_inputs()

    def show_total(self):
        data = db.get_subscription()
        total = sum(item[1] for item in data)
        content = '\n'.join([f"{i+1}. {d[0]}, ₹{d[1]}, {d[2]}, {d[3]}" for i, d in enumerate(data)])
        content += f"\n\nTotal Amount: ₹{total}"
        self.show_popup("Subscription Summary", content)

    def clear_inputs(self):
        self.ids.amount_input.text = ''
        self.ids.date_input.text = ''
        self.ids.name_spinner.text = 'Select Name'
        self.ids.purpose_spinner.text = 'Select Purpose'

    def show_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size_hint=(0.8, 0.8))
        popup.open()

class ExpenditureScreen(Screen):
    def add_data(self):
        purpose = self.ids.ex_purpose.text
        amount = self.ids.ex_amount.text
        date = self.ids.ex_date.text
        if purpose and amount and date:
            db.insert_expenditure(purpose, float(amount), date)
            self.clear_inputs()

    def show_total(self):
        data = db.get_expenditure()
        total = sum(item[1] for item in data)
        content = '\n'.join([f"{i+1}. {d[0]}, ₹{d[1]}, {d[2]}" for i, d in enumerate(data)])
        content += f"\n\nTotal Expenditure: ₹{total}"
        self.show_popup("Expenditure Summary", content)

    def clear_inputs(self):
        self.ids.ex_purpose.text = ''
        self.ids.ex_amount.text = ''
        self.ids.ex_date.text = ''

    def show_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size_hint=(0.8, 0.8))
        popup.open()

    def exit_app(self):
        App.get_running_app().stop()

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SubscriptionScreen(name='subscription'))
        sm.add_widget(ExpenditureScreen(name='expenditure'))
        return sm

if __name__ == '__main__':
    MyApp().run()