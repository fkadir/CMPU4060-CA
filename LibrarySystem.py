# CMPU4060 Final CA
import csv, copy


# classes
class Library(object):
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.borrow_info = create_transaction_info('borrowing.csv')
        self.items = create_items('items.csv', self.borrow_info)
        self.members = create_members('members.csv', self.borrow_info)

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

    def borrow_items(self):  # better way?
        borrow_input = input("Would you like to borrow an item? \n"
                             "If yes, enter item ID\n"
                             "If no, enter exit\n").strip()
        if borrow_input == 'exit':
            return
        else:
            self.items[borrow_input].borrow_item()
            return

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

    def __str__(self):
        return '{} {} (Member ID: {}) has borrowed {} items' \
            .format(self.f_name, self.l_name, self.member_id, len(self.items))


class Items(object):
    def __init__(self, ID, category, title, yop):
        self.item_id = ID
        self.title = title
        self.year_of_publication = yop
        self.type = category
        self.available = True

    def return_item(self):
        self.available = True
        # !! remove entry from borrowing.csv

    def borrow_item(self):
        self.available = False
        # !! add entry to borrowing.csv

    def __str__(self):
        if self.available:
            return '{} (Item ID: {}) is a {}, was published in {} and is available to borrow'.format(self.title,
                                                                                                     self.item_id,
                                                                                                     self.type,
                                                                                                     self.year_of_publication)
        else:
            return '{} (Item ID: {}) is a {}, was published in {} and is unavailable to borrow'.format(self.title,
                                                                                                       self.item_id,
                                                                                                       self.type,
                                                                                                       self.year_of_publication)


class Book(Items):
    def __init__(self, ID, title, author_l_name, author_f_name, yof=0000):
        Items.__init__(self, ID, 'Book', title, yof)
        self.author_l_name = author_l_name
        self.author_f_name = author_f_name

    def __str__(self):
        if self.available:
            return '{} (Book ID: {}) was written by {} {} in {} and is available for borrowing' \
                .format(self.title, self.item_id, self.author_f_name, self.author_l_name, self.year_of_publication)
        else:
            return '{} (Book ID: {}) was written by {} {} in {} and is unavailable for borrowing' \
                .format(self.title, self.item_id, self.author_f_name, self.author_l_name, self.year_of_publication)


class Article(Items):
    def __init__(self, ID, title, author_l_name, author_f_name, journal, yof=0000):
        Items.__init__(self, ID, 'Article', title, yof)
        self.author_l_name = author_l_name
        self.author_f_name = author_f_name
        self.journal = journal

    def __str__(self):
        if self.available:
            return '{} (Article ID: {}) from {} was written by {} {} in {} and is available for borrowing'.format(
                self.title, self.item_id, self.journal, self.author_f_name, self.author_l_name,
                self.year_of_publication)
        else:
            return '{} (Article ID: {}) from {} was written by {} {} in {} and is unavailable for borrowing'.format(
                self.title, self.item_id, self.journal, self.author_f_name, self.author_l_name,
                self.year_of_publication)


# class DigitalMedia(Items):


# methods       # better way?

# why did I think this was a better way?
def create_transaction_info(file):
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # better way?
        entries = {}
        for row in reader:
            info = (row[0], row[2], row[3], row[4])
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
    print(members_dict)
    return members_dict


def create_items(file, borrow_info):
    item_info = parse_file(file)
    items_dic = {}
    for i in item_info:
        items_dic[i[0]] = Items(i[0], i[1], i[2], i[5])
    for j in borrow_info:
        items_dic[j[2]].available = False
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
            # elif i == 2:
            #
            # elif i == 3:
            #
            elif i == 5:
                return_input = input("Please enter item ID: ")
                library.items[return_input].return_item()
            elif i == 6:
                exit()
        except ValueError:
            print("Invalid input, please try again: ", '\n')
        except KeyError:
            print("Invalid input, please try again: ", '\n')


# !! update external files


# main()
info = parse_file("borrowing.csv")
print(info)
create_members("members.csv", info)
