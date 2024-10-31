from datetime import datetime, timedelta
import re

class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    def __init__(self, name):
        if not isinstance(name, str) or not name:
            raise ValueError("Name must be a non-empty string")
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone):
        if not self.validate_phone(phone):
            raise ValueError("Invalid phone number format. Use +380XXXXXXXXX")
        super().__init__(phone)

    @staticmethod
    def validate_phone(phone):
        return bool(re.match(r'^\+380\d{9}$', phone))


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def get_birthday(self):
        return self.birthday.value if self.birthday else None


class AddressBook:
    def __init__(self):
        self.contacts = {}

    def add_record(self, record):
        self.contacts[record.name.value] = record

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.now()
        next_week = today + timedelta(days=7)

        for record in self.contacts.values():
            if record.birthday:
                birthday = record.get_birthday()
                if (birthday.month == today.month and birthday.day >= today.day) or (birthday.month == next_week.month and birthday.day <= next_week.day):
                    upcoming_birthdays.append(record.name.value)

        return upcoming_birthdays


if __name__ == "__main__":
    book = AddressBook()

    record1 = Record("Oleh")
    record1.add_phone("+380504923485")
    record1.add_birthday("05.11.1999")
    book.add_record(record1)

    record2 = Record("Anna")
    record2.add_phone("+380987654321")
    record2.add_birthday("12.11.2003")
    book.add_record(record2)

    record3 = Record("Sophia")
    record3.add_phone("+380634321987")
    book.add_record(record3)

    upcoming_birthdays = book.get_upcoming_birthdays()
    print("Upcoming birthdays:", upcoming_birthdays)
