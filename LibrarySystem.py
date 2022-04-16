# CMPU4060 Final CA
import csv


# classes
class Library(object):
    def __init__(self, name, address):
        self.name = name
        self.address = address

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
    def __init__(self, ID, category, title, yof):
        self.item_id = ID
        self.title = title
        self.year_of_publication = yof
        self.type = category
        self.available = True

    def __str__(self):
        if self.available:
            return '{} (Item ID: {}) is a {} and was published in {} and available to borrow'.format(self.title,
                                                                                                     self.item_id,
                                                                                                     self.type,
                                                                                                     self.year_of_publication)
        else:
            return '{} (Item ID: {}) is a {} and was published in {} and unavailable to borrow'.format(self.title,
                                                                                                       self.item_id,
                                                                                                       self.type,
                                                                                                       self.year_of_publication)


# class Book(Items):
#     def __init__(self, ID, title, author_l_name, author_f_name, yof):
#         Items.__init__(self, ID, title, yof)
#         self.author_l_name = author_l_name
#         self.author_f_name = author_f_name
#
# def __str__(self): return '{} (Book ID: {}) was written by {} {} in {}'.format(self.title, self.item_id,
# self.author_f_name, self.author_l_name, self.year_of_publication)

# class Article(Items):
#
# class DigitalMedia(Items):

# methods
def system_startup():
    # A create library
    library = Library('The University Library', 'Park House, 191 N Circular Rd, Co. Dublin, D07 EWV4, Ireland')
    # create nested list with borrowed items
    # (who borrowed them, at what date and when they need to be returned)
    borrow_info = parse_file('borrowing.csv')
    # create items
    items = create_items('items.csv', borrow_info)
    # create members
    members = create_members('members.csv', borrow_info)

    # return library    better way? aggregation my friend
    return items, members


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
    members_dic = {}
    for m in member_info:
        borrowed_dict = {}
        for i in items_info:
            if i[1] == m[0]:
                borrowed_dict[i[0]] = (i[2], i[3])
        members_dic[m[0]] = Members(m[0], m[1], m[2], m[3], '{}, {}, {}'.format(m[4], m[5], m[6]), borrowed_dict)
    return members_dic


def create_items(file, borrow_info):
    item_info = parse_file(file)
    items_dic = {}
    for i in item_info:
        items_dic[i[0]] = Items(i[0], i[1], i[2], i[5])
    for j in borrow_info:
        items_dic[j[0]].available = False
    return items_dic


def search_items(items, word):
    word = word.lower().strip()
    results = []
    for i in items.values():
        title = i.title.lower().split()
        if word in title:
            results.append(i.item_id)

    # display results
    for r in results:
        print(items[r])


def borrow_items(items):
    borrow_input = input("Would you like to borrow any of these items? \n"
                         "If yes, enter item ID\n"
                         "If no, enter exit\n").strip()
    if borrow_input == 'exit':
        return
    else:
        items[borrow_input].available = False
        # !! add entry to borrowing.csv
        return


# main
def main():
    items, members = system_startup()
    while True:
        try:
            # create menu
            i = int(input("What would you like to do?\n"
                          "1. Browse Items?\n"
                          "2. Add, edit or remove a member?\n"
                          "3. Add, edit or remove an item?\n"
                          "4. Return Item(s)?\n"
                          "5. Quit program\n"))
            # call correct function depending on user input
            if i == 1:
                search_input = input("Enter your keyword: ")
                search_items(items, search_input)
                borrow_items(items)

            # elif i == 2:
            #
            # elif i == 3:
            #
            elif i == 4:
                return_input = input("Please enter item_ID: ")
                items[return_input].available = True
                # !! remove entry from borrowing.csv
            elif i == 5:
                exit()
        except ValueError:
            print("Invalid input, please try again: ", '\n')
        except KeyError:
            print("Invalid input, please try again: ", '\n')

    # !! update external files


main()
# items, members = system_startup()
