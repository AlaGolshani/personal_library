"""
This program is about a personal bookshelf,
that can include books, magazines, podcasts and audiobooks 

author: Ala Golshani

date: April 3, 2021
"""

from tabulate import tabulate
from os import system


class Media:
    my_bookshelf = []

    def __init__(self, title, publish_year, price):   # common attributes
        self.title = title
        self.publish_year = publish_year
        self.price = price
        self.progress = 0
    
    def get_status(self):
        media_type = self.__class__.__name__

        if self.progress == 0:
            return "unread" if media_type in ['Book', 'Magazine'] else "unlistened"
        elif self.progress == 100:
            return "finished"
        else:
            return "reading" if media_type in ['Book', 'Magazine'] else "listening"

    @classmethod
    def add(cls, media_type):
        if media_type == 1:
            Book.get_data()
            
        elif media_type == 2:
            Magazine.get_data()

        elif media_type == 3:
            Podcast.get_data()

        else:  # media_type = 4, Audiobook selected
            Audiobook.get_data()

    @classmethod
    def show(cls):
        if len(Media.my_bookshelf) == 0:
            print('''\n\n
                                    The bookshelf is empty!
                  ''')
            return
        
        data = [[media.__class__.__name__, media.title, str(media.progress)]
                for media in Media.my_bookshelf]
        print(tabulate(data, headers=['media type', 'name', 'progress (%)']))
    
    @classmethod
    def search(cls, title):
        if len(Media.my_bookshelf) == 0:
            print('''\n\n
                                    The bookshelf is empty!
                  ''')
            return -1

        for media in Media.my_bookshelf:
            if media.title == title:
                obj = media
                return obj

    @classmethod
    def sort(cls):
        if len(Media.my_bookshelf) == 0:
            print('''\n\n
                                    The bookshelf is empty!
                  ''')
            return

        Media.my_bookshelf.sort(key=lambda media: media.progress, reverse=True)
        Media.show()

    def __str__(self):
        propertis = [f"{key.replace('_',' ')} : {value}"
                     for key, value in self.__dict__.items()]
        propertis = '\n'.join(propertis)
        return propertis


class Book(Media):

    def __init__(self, title, authors, publish_year,
                 pages, language, price, readen_pages=0):
        super().__init__(title, publish_year, price)
        self.authors = authors
        self.pages = pages
        self.language = language
        self.readen_pages = 0
        self.read(readen_pages)
        self.progress = int(self.readen_pages / self.pages * 100)  # progress percentage

    def read(self, new_pages):
        if self.pages == self.readen_pages:
            print(f'\n\tYou have already finished this book')
            return

        while self.readen_pages + new_pages > self.pages:
            new_pages = int(input('\n\tit is more than the book pages. \
                                   \n\tenter the number of pages that you have read: '))

        self.readen_pages += new_pages

        if self.pages == self.readen_pages:
            print(f'\n\tWell done, you finished the {self.title} book.')
        else:
            print(f'\n\tyou have read {self.readen_pages} pages from {self.title}. \
                    \n\tThere are {self.pages - self.readen_pages} pages left.\n')
        self.progress = int(self.readen_pages / self.pages * 100)

    @classmethod
    def get_data(cls):
        print('\n\nYou are adding a book. Please enter the following information:')
        title = input('\n\tTitle: ')
        authors = input('\tAuthors: ')
        publish_year = input('\tPublish Year: ')
        pages = int(input('\tNumber Of Pages: '))
        language = input('\tLanguage: ')
        price = input('\tPrice: ')
        readen_pages = int(input(f'\tHow many pages of {title} have you read so far? '))

        instance = Book(title, authors, publish_year,
                        pages, language, price, readen_pages)

        Media.my_bookshelf.append(instance)


class Magazine(Book):

    def __init__(self, title, authors, publish_year,
                 pages, language, price, issue, readen_pages=0):
        super().__init__(title, authors, publish_year,
                         pages, language, price, readen_pages)
        self.issue = issue

    @classmethod
    def get_data(cls):
        print('\n\nYou are adding a magazine. Please enter its information:')
        title = input('\tTitle: ')
        authors = input('\tAuthors: ')
        publish_year = input('\tPublish Year: ')
        pages = int(input('\tNumber of pages: '))
        language = input('\tLanguage: ')
        price = input('\tPrice: ')
        issue = input('\tissue: ')
        readen_pages = int(input(f'\tHow many pages of {title} have you read so far? '))

        instance = Magazine(title, authors, publish_year,
                            pages, language, price, issue, readen_pages)
        
        Media.my_bookshelf.append(instance)
        

class Podcast(Media):
    def __init__(self, title, speaker, publish_year,
                 time, language, price, listend_time=0):
        super().__init__(title, publish_year, price)
        self.speaker = speaker
        self.time = time
        self.language = language
        self.listend_time = 0
        self.listen(listend_time)
        self.progress = (listend_time / time * 100)

    def listen(self, new_time):
        while self.listend_time + new_time > self.time:
            new_time = int(input(f'\n\tit is more than the podcast time. \
                                   \n\tHow many minutes of {self.title} have you listen? '))

        self.listend_time += new_time

        if self.time == self.listend_time:
            print(f'\n\tWell done, you finished the {self.title} podcast.')
        else:
            print(f'\n\tyou have listened {self.listend_time} minutes from {self.title}. \
                    \n\tThere are {self.time - self.listend_time} minutes left.')
        self.progress = (self.listend_time / self.time) * 100

    @classmethod
    def get_data(cls):
        print('\n\nYou are adding a podcast. Please enter its information:')
        title = input('\tTitle: ')
        speaker = input('\tSpeaker: ')
        publish_year = input('\tPublish Year: ')
        time = int(input('\tTotal time: '))
        language = input('\tLanguage: ')
        price = input('\tPrice: ')
        listend_time = int(input(f'\tHow many minutes of {title} have you listen? '))

        instance = Podcast(title, speaker, publish_year,
                           time, language, price, listend_time)

        Media.my_bookshelf.append(instance)


class Audiobook(Podcast):
    def __init__(self, title, speaker, authors, publish_year, pages,
                 book_language, audio_language, time, price, listend_time=0):

        super().__init__(title, speaker, publish_year,
                         time, audio_language, price, listend_time)
        self.authors = authors
        self.pages = pages
        self.book_language = book_language

    @classmethod
    def get_data(cls):
        print('\nYou are adding a audiobook. Please enter its information:')
        title = input('\tTitle: ')
        speaker = input('\tSpeaker: ')
        authors = input('\tAuthors: ')
        publish_year = input('\tPublish Year: ')
        pages = int(input('\tNumber of pages: '))
        book_language = input('\tBook language: ')
        audio_language = input('\tAudio language: ')
        time = int(input('\tTotal time: '))
        price = input('\tPrice: ')
        listend_time = int(input(f'\tHow many minutes of {title} have you listen so far? '))

        instance = Audiobook(title, speaker, authors, publish_year, pages,
                             book_language, audio_language, time, price, listend_time)

        Media.my_bookshelf.append(instance)


def menu():
    choice = int(input(f'''
                                    <<< Welcome to your bookshelf >>>



                            1) Add a Book / Magazine / Podcast episode / Audiobook
                            2)                Show my bookshelf
                            3)          Add read page or time listen
                            4)               Sort my bookshelf
                            5)                     Quit
                            \n
                            >> Please enter the requested action number: '''))
    print()
    while choice not in range(1, 6):
        choice = int(input('\n\t\t\tYou entered an invalid number. Please choose between 1-5: '))

    return choice


if __name__ == "__main__":
    system('cls')
    item = menu()
    system('cls')

    while item != 5:
        
        if item == 1:
            media_type = int(input('''
                                >> What kind of media do you want to add?
                                1) Book      2) Magazine
                                3) Podcast   4) Audiobook

                                >> Enter its number: '''))

            while media_type not in range(1, 5):
                media_type = int(input('\t\t\t\tYou entered an invalid number. Please choose between 1-4: '))     
            system('cls')

            Media.add(media_type)
            print('\n\nAdding the media completed successfully.', end='')
        
        elif item == 2:
            Media.show()

        elif item == 3:
            title = input('\n\n\tPlease enter the title of the media, that you wanna update : ')
            obj = Media.search(title)
            if obj != -1:
                obj_type = obj.__class__.__name__
                if obj_type == 'Book' or obj_type == 'Magazine':
                    new_pages = int(input('\n\n\tenter the number of pages that you have read: '))
                    obj.read(new_pages)
                elif obj_type == 'Podcast' or obj_type == 'Audiobook':
                    new_time = int(input(f'\n\n\tHow many minutes of {title} have you listen? '))
                    obj.listen(new_time)

        else:  # choice = 4, that means Sort my bookshelf
            Media.sort()

        input("\n\nPress Enter to Continue...")
        system('cls')
        item = menu()
        system('cls')
