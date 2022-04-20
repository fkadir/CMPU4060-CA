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

    # item methods
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
            self.items[borrow_input].available = False
            # !! add entry to borrowing.csv
            return

    def return_item(self, item, member):
        # mark item as available in the library
        self.items[item].available = True
        with open('borrowing.csv') as borrow_csv:
            print(borrow_csv)
            # add return date to borrowing_csv

        # check if item is overdue
        today = date.today()
        for i in range(0, len(self.borrow_info[member])):
            if self.borrow_info[member][i][1] == item:
                return_date = datetime.strptime(self.borrow_info[member][i][3], '%d/%m/%Y').date()
                if today > return_date:
                    # calculate how many days late the item was returned
                    days_late = int((today - return_date).total_seconds() / 86400)
                    self.members[member].fine += 1.0 * days_late

    def add_item(self):
        item_id = 'I' + str(len(self.items) + 1)
        category = input("category: \n"
                         "a. Book \n"
                         "b. Article \n"
                         "c. Digital Media\n")
        title = input("title: ")
        l_name = input("last name of author/director: ")
        f_name = input("first name of author/director: ")
        year = int(input("year of release/publication: "))
        journal = input("Which journal was it published (if not press enter): ")
        if category == 'a':
            self.items[item_id] = Book(item_id, title, l_name, f_name, year)
        elif category == 'b':
            self.items[item_id] = Article(item_id, title, l_name, f_name, journal, year)
        elif category == 'c':
            self.items[item_id] = DigitalMedia(item_id, title, l_name, f_name, year)
        else:
            print('error')
            # !! error handling

        self.update_items_csv()

    def edit_item(self, id):
        item_input = input("Would you like to edit the following item: {} by {} {} (press enter to confirm or enter "
                          "exit) ".format(self.items[id].title, self.items[id].f_name, self.items[id].l_name))
        if item_input.strip() == 'exit':
            return
        type_edit = input('What would you like to edit? \n'
                          'a. Item ID \n'
                          'b. Category \n'
                          'c. Title \n'
                          'd. Last Name \n'
                          'e. First Name \n'
                          'f. Publication/Release Year \n'
                          'g. Journal \n')
        if type_edit == 'a':
            i = input("Enter Item ID: ")
            self.items[id].item_id = i 
        elif type_edit == 'b':
            i = input("Enter Category: ")
            self.items[id].type = i
        elif type_edit == 'c':
            i = input("Enter Title: ")
            self.items[id].title = i
        elif type_edit == 'd':
            i = input("Enter Last Name: ")
            self.items[id].l_name = i
        elif type_edit == 'e':
            i = input("Enter First Name: ")
            self.items[id].f_name = i
        elif type_edit == 'f':
            i = int(input("Enter Publication/Release year: "))
            self.items[id].year = i
        elif type_edit == 'g':
            i = input("Enter Journal: ")
            self.items[id].journal = i
            # !! error handling if book or article
        else: 
            print("error bitch")
            # !! error handling
        self.update_items_csv()

    def delete_item(self, id):
        removed_item = self.items.pop(id)
        self.update_items_csv()

    def update_items_csv(self):
        fields = ['Item ID', 'Category', 'Title', 'Last name', 'First name', 'publication year', 'journal']
        rows = []
        for i in self.items.values():
            if i.type == 'Book':
                a = [i.item_id, i.type, i.title, i.l_name, i.f_name, i.year]
                rows.append(a)
            elif i.type == 'Article':
                a = [i.item_id, i.type, i.title, i.l_name, i.f_name, i.year, i.journal]
                rows.append(a)
            else:
                a = [i.item_id, i.type, i.title, i.l_name, i.f_name, i.year]
                rows.append(a)
        with open('items.csv', 'w+') as items_csv:
            csv_writer = csv.writer(items_csv, lineterminator='\n')
            csv_writer.writerow(fields)
            csv_writer.writerows(rows)

    # member methods
    def add_member(self):
        member_id = 'M' + str(len(self.members) + 1)
        l_name = input("Enter last name: ")
        f_name = input("Enter first name: ")
        dob = input("Enter Date of Birth: ")
        street = input("Enter street and number: ")
        city = input("Enter city: ")
        self.members[member_id] = Members(member_id, l_name, f_name, dob, street, city)
        self.update_members_csv()

    def edit_member(self, id):
        item_input = input("Would you like to edit the following member: {} {} (Member ID: {}) (press enter to "
                           "confirm or enter exit) ".format(self.members[id].f_name, self.members[id].l_name,
                                                            self.members[id].member_id))
        if item_input.strip() == 'exit':
            return
        type_edit = input('What would you like to edit? \n'
                          'a. Member ID \n'
                          'b. Last Name \n'
                          'c. First Name \n'
                          'd. Date of Birth \n'
                          'e. Street and number \n'
                          'f. City \n')
        if type_edit == 'a':
            i = input("Enter Member ID: ")
            self.members[id].member_id = i
        elif type_edit == 'b':
            i = input("Enter Last Name: ")
            self.members[id].l_name = i
        elif type_edit == 'c':
            i = input("Enter First Name: ")
            self.members[id].f_name = i
        elif type_edit == 'd':
            i = input("Enter Date of Birth: ")
            self.members[id].dob = i
        elif type_edit == 'e':
            i = input("Enter Street and number: ")
            self.members[id].street = i
        elif type_edit == 'f':
            i = input("Enter City: ")
            self.members[id].city = i
        else:
            print("error bitch")
            # !! error handling
        self.update_members_csv()

    def delete_member(self, id):
        removed_member = self.members.pop(id)
        self.update_members_csv()

    def update_members_csv(self):
        fields = ['Member ID', 'Last name', 'First name', 'Date of Birth', 'Street', 'City']
        rows = []
        for i in self.members.values():
            a = [i.member_id, i.l_name, i.f_name, i.dob, i.street, i.city]
            rows.append(a)
        with open('members.csv', 'w+') as members_csv:
            csv_writer = csv.writer(members_csv, lineterminator='\n')
            csv_writer.writerow(fields)
            csv_writer.writerows(rows)

    def __str__(self):
        return '{} at {}'.format(self.name, self.address)


class Members(object):
    def __init__(self, ID, l_name, f_name, DOB, street, city, borrowed_items=None):
        if borrowed_items is None:
            borrowed_items = {}
        self.member_id = ID
        self.l_name = l_name
        self.f_name = f_name
        self.dob = DOB
        self.street = street
        self.city = city
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
    def __init__(self, ID, title, l_name, f_name, yof=0000):  # publisher better way?
        Items.__init__(self, ID, 'Book', title)
        self.l_name = l_name
        self.f_name = f_name
        self.year = yof

    def __str__(self):
        if self.available:
            return 'The Book: {} (Item: {}) was written by {} {} in {} and is available for borrowing' \
                .format(self.title, self.item_id, self.f_name, self.l_name, self.year)
        else:
            return 'The Book: {} (Item ID: {}) was written by {} {} in {} and is unavailable for borrowing' \
                .format(self.title, self.item_id, self.f_name, self.l_name, self.year)


class Article(Items):
    def __init__(self, ID, title, l_name, f_name, journal, yof=0000):
        Items.__init__(self, ID, 'Article', title)
        self.l_name = l_name
        self.f_name = f_name
        self.journal = journal
        self.year = yof

    def __str__(self):
        if self.available:
            return 'The Article: {} (Item ID: {}) from {} was written by {} {} in {} and is available for borrowing'.format(
                self.title, self.item_id, self.journal, self.f_name, self.l_name,
                self.year)
        else:
            return 'The Article: {} (Item ID: {}) from {} was written by {} {} in {} and is unavailable for borrowing'.format(
                self.title, self.item_id, self.journal, self.f_name, self.l_name,
                self.year)


class DigitalMedia(Items):
    def __init__(self, ID, title, l_name, f_name, year=0000):
        Items.__init__(self, ID, 'Digital Media', title)
        self.year = year
        self.l_name = l_name
        self.f_name = f_name

    def __str__(self):
        if self.available:
            return 'The Digital Media: {} (Item ID: {}) is directed by {} {} in {} and available for borrowing'.format(
                self.title, self.item_id, self.f_name, self.l_name, self.year)
        else:
            return 'The Digital Media: {} (Item ID: {}) is directed by {} {} in {} and unavailable for borrowing'.format(
                self.title, self.item_id, self.f_name, self.l_name, self.year)


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
        members_dict[m[0]] = Members(m[0], m[1], m[2], m[3], m[4], m[5], borrowed_dict)
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
        elif item_type == 'digital media':
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
                          "5. Return Item?\n"
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
            elif i == 3:
                choice_input = input("Would you like to \n"
                                     "a. add a member \n"
                                     "b. edit a member \n"
                                     "c. remove a member \n")
                choice_input.lower().strip()
                if choice_input == 'a':
                    library.add_member()
                elif choice_input == 'b':
                    id_input = input("Enter Member ID: ")
                    library.edit_member(id_input)
                elif choice_input == 'c':
                    id_input = input("Enter member ID: ")
                    library.delete_member(id_input)
                else:
                    print("erro bitch")
                    # !! error handling
            elif i == 4:
                choice_input = input("Would you like to \n"
                                     "a. add an item \n"
                                     "b. edit an item \n"
                                     "c. remove an item \n")
                choice_input.lower().strip()
                if choice_input == 'a':
                    library.add_item()
                elif choice_input == 'b':
                    id_input = input("Enter Item ID: ")
                    library.edit_item(id_input)
                    print(type(library.items['I5'].year))
                    print(type(library.items['I1'].year))
                elif choice_input == 'c':
                    id_input = input("Enter Item ID: ")
                    library.delete_item(id_input)
                else:
                    print("erro bitch")
                    # !! error handling
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


main()
# library = Library('The University Library', 'Park House, 191 N Circular Rd, Co. Dublin, D07 EWV4, Ireland')