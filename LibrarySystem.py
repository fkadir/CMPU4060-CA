# CMPU4060 Final CA
import csv
from datetime import date, datetime


# classes
class Library(object):
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.borrow_info = create_transaction_info('borrowing.csv')
        self.items = create_items('items.csv', parse_file('borrowing.csv'))
        self.members = create_members('members.csv', parse_file('borrowing.csv'))

    def search_items(self, word):
        word = word.lower().strip()
        results = []
        for i in self.items.values():
            title = i.title.lower().split()
            if word in title:
                results.append(i.item_id)

        # display results
        for r in results:
            print(self.items[r])

    # better way?
    def borrow_items(self):
        borrow_input = input("Would you like to borrow an item? \n"
                             "If yes, enter item ID\n"
                             "If no, enter exit\n").strip()
        if borrow_input == 'exit':
            return
        else:
            self.items[borrow_input].borrow_item()
            return

    def return_item(self, item, member):
        # mark item as available in the library
        self.items[item].available = True
        # !! add return date to borrowing.csv

        # check if item is overdue
        today = date.today()
        print(self.borrow_info[member])
        for i in range(0, len(self.borrow_info[member])):
            if self.borrow_info[member][i][1] == item:
                return_date = datetime.strptime(self.borrow_info[member][i][3], '%d/%m/%Y').date()
                if today > return_date:
                    # calculate how many days late the item was returned
                    days_late = int((today - return_date).total_seconds() / 86400)
                    self.members[member].fine += 1.0 * days_late

    def add_item(self):
        item_id= 'I'+str(len(self.items)+1)
        category = input("category: ")
        title = input("title: ")
        l_name = input("last name of author/director: ")
        f_name = input("first name of author/director: ")
        year = input("year of release/publication: ")
        journal = input("Which journal was it published (if not press enter)")
        # add item to items.csv

        # refresh self.items method?

    # def edit_item(self):

    def remove_item(self, id):
        print(id)
        # remove row with id from items.csv
        # refresh self.items method?

    def __str__(self):
        return '{} at {}'.format(self.name, self.address)


class Members(object):
    def __init__(self, ID, l_name, f_name, DOB, address, borrowed_items=None):
        self.member_id = ID
        self.l_name = l_name
        self.f_name = f_name
        self.dob = DOB
        self.address = address
        self.items = borrowed_items
        self.fine = 0.0

    def __str__(self):
        return '{} {} (Member ID: {}) has borrowed {} items' \
            .format(self.f_name, self.l_name, self.member_id, len(self.items))


class Items(object):
    def __init__(self, ID, category, title):
        self.item_id = ID
        self.title = title
        self.type = category
        self.available = True

    def borrow_item(self):
        self.available = False
        # !! add entry to borrowing.csv

    def __str__(self):
        if self.available:
            return '{} (Item ID: {}) is a {} and available to borrow'.format(self.title,
                                                                             self.item_id,
                                                                             self.type)
        else:
            return '{} (Item ID: {}) is a {} and unavailable to borrow'.format(self.title,
                                                                               self.item_id,
                                                                               self.type)


class Book(Items):
    def __init__(self, ID, title, author_l_name, author_f_name, yof=0000):  # publisher better way?
        Items.__init__(self, ID, 'Book', title)
        self.author_l_name = author_l_name
        self.author_f_name = author_f_name
        self.publication_year = yof

    def __str__(self):
        if self.available:
            return 'The Book: {} (Item: {}) was written by {} {} in {} and is available for borrowing' \
                .format(self.title, self.item_id, self.author_f_name, self.author_l_name, self.publication_year)
        else:
            return 'The Book: {} (Item ID: {}) was written by {} {} in {} and is unavailable for borrowing' \
                .format(self.title, self.item_id, self.author_f_name, self.author_l_name, self.publication_year)


class Article(Items):
    def __init__(self, ID, title, author_l_name, author_f_name, journal, yof=0000):
        Items.__init__(self, ID, 'Article', title)
        self.author_l_name = author_l_name
        self.author_f_name = author_f_name
        self.journal = journal
        self.publication_year = yof

    def __str__(self):
        if self.available:
            return 'The Article: {} (Item ID: {}) from {} was written by {} {} in {} and is available for borrowing'.format(
                self.title, self.item_id, self.journal, self.author_f_name, self.author_l_name,
                self.publication_year)
        else:
            return 'The Article: {} (Item ID: {}) from {} was written by {} {} in {} and is unavailable for borrowing'.format(
                self.title, self.item_id, self.journal, self.author_f_name, self.author_l_name,
                self.publication_year)


class DigitalMedia(Items):
    def __init__(self, ID, title, director_l_name, director_f_name, release_year=0000):
        Items.__init__(self, ID, 'Digital Media', title)
        self.release_year = release_year
        self.director_l_name = director_l_name
        self.director_f_name = director_f_name

    def __str__(self):
        if self.available:
            return 'The Digital Media: {} (Item ID: {}) is directed by {} {} in {} and available for borrowing'.format(
                self.title, self.item_id, self.director_f_name, self.director_l_name, self.release_year)
        else:
            return 'The Digital Media: {} (Item ID: {}) is directed by {} {} in {} and unavailable for borrowing'.format(
                self.title, self.item_id, self.director_f_name, self.director_l_name, self.release_year)


# methods       # better way?

# why did I think this was a better way? unnecessary?
def create_transaction_info(file):
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # better way?
        entries = {}
        for row in reader:
            info = (row[0], row[2], row[3], row[4], row[5])
            if row[1] in entries.keys():
                entries[row[1]].append(info)
            else:
                entries[row[1]] = [info]
    return entries


def parse_file(file):
    entries = []
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # better way?
        for row in reader:
            entries.append(row)
    return entries


def create_members(file, items_info):
    member_info = parse_file(file)
    members_dict = {}
    for m in member_info:
        borrowed_dict = {}
        for i in items_info:
            if i[1] == m[0]:
                borrowed_dict[i[0]] = (i[2], i[3])
        members_dict[m[0]] = Members(m[0], m[1], m[2], m[3], '{}, {}, {}'.format(m[4], m[5], m[6]), borrowed_dict)
    return members_dict


def create_items(file, borrow_info):
    item_info = parse_file(file)
    items_dic = {}
    for i in item_info:
        item_type = i[1].lower().strip()
        if item_type == 'book':
            items_dic[i[0]] = Book(i[0], i[2], i[3], i[4], int(i[5]))
        elif item_type == 'article':
            items_dic[i[0]] = Article(i[0], i[2], i[3], i[4], i[6], int(i[5]))
        elif item_type == 'dm':
            items_dic[i[0]] = DigitalMedia(i[0], i[2], i[3], i[4], int(i[5]))
        else:
            print('unable to create item, unknown item type')
            # error better way?

    # better way?!
    for j in borrow_info:
        if j[5] == '':
            items_dic[j[2]].available = False

    # for k in items_dic.values():
    #     print(k)
    return items_dic


# main
def main():
    library = Library('The University Library', 'Park House, 191 N Circular Rd, Co. Dublin, D07 EWV4, Ireland')
    while True:
        try:
            # create menu
            i = int(input("What would you like to do?\n"
                          "1. Browse Items?\n"
                          "2. Check availability?\n"
                          "3. Add, edit or remove a member?\n"
                          "4. Add, edit or remove an item?\n"
                          "5. Return Item(s)?\n"
                          "6. Quit program\n"))
            # call correct function depending on user input
            if i == 1:
                search_input = input("Enter your keyword: ")
                library.search_items(search_input)
                library.borrow_items()
            elif i == 2:
                id_input = input("Enter the item ID: ")
                if library.items[id_input].available:
                    print('{} (Item ID: {}) is available for borrowing'.format(library.items[id_input].title,
                                                                               library.items[id_input].item_id))
                else:
                    print('{} (Item ID: {}) is unavailable for borrowing'.format(library.items[id_input].title,
                                                                                 library.items[id_input].item_id))
            # elif i == 3:
            #
            elif i == 4:
                choice_input = input("Would you like to \n"
                                     "a. add an item \n"
                                     "b. edit an item \n"
                                     "c. remove an item \n")
                choice_input.lower().strip()
                if choice_input == 'a':
                    library.add_item()
                # elif choice_input == 'b':
                elif choice_input == 'c':
                    id_input = input("Enter item ID: ")
                    library.remove_item(id_input)
                else:
                    print("erro bitch")
            elif i == 5:
                member_input = input("Please enter member ID: ")
                return_input = input("Please enter item ID: ")
                library.return_item(return_input, member_input)
            elif i == 6:
                exit()
        except ValueError:
            print("Invalid input, please try again: ", '\n')
        except KeyError:
            print("Invalid input, please try again: ", '\n')


# !! update external files
# main()
info = parse_file("borrowing.csv")
# i = create_items("items.csv", info)
# m = create_members('members.csv', info)
library = Library('The University Library', 'Park House, 191 N Circular Rd, Co. Dublin, D07 EWV4, Ireland')
# library.return_item('I0004', 'M0001')
library.add_item()