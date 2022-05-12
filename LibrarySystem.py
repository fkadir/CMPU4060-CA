import csv
from datetime import date, datetime, timedelta
# all datetime code is based on the following articles:
# https://www.programiz.com/python-programming/datetime/current-datetime,
# https://www.programiz.com/python-programming/datetime/strptime


# classes
class Library(object):
    """
    A class to represent a library

    Attributes
    ----------
    name: str
    address: str
    borrow_info: dict
    items: dict
    members: dict

    Methods
    -------
    create_transaction_info(file)
        creates dict with all transactions on file of the library
    parse_file(file)
        creates list of entries in csv file
    create_members(file)
        create dict with all members on file of the library
    create_items(file)
        create dict with all items on file of the library
    search_items(word)
        creates a list of items that contain the search word in the title or author
    borrow_item()
        borrow item from the library
    return_item(item, member)
        return item to the library
    update_borrow_csv
        update the borrowing.csv based on the borrowing info dict
    add_item()
        add specific item to the library
    edit_item(item_id)
        edit a specific item from the library
    delete_item(item_id)
        remove an item from the library
    update_items_csv()
        update the items.csv based on items dict
    add_member()
        add a member to the library
    edit_member(member_id)
        edit a specific member from the library
    delete_member(member_id)
        remove a member from the library
    update_members_csv
        update members.csv based on the members dict
     """

    def __init__(self, name: str, address: str):
        """
        Constructs all the necessary attributes for the library object.

        Parameters
        ----------
        name: str
            name of the library
        address: str
            library's address
        """
        self.name = name
        self.address = address
        self.borrow_info = self.create_transaction_info('borrowing.csv')
        self.items = self.create_items('items.csv')
        self.members = self.create_members('members.csv')

    # methods to set up the library
    @staticmethod
    def create_transaction_info(file):
        """
        Create dict with all transactions on file of the library.

        Parameters
        ----------
        file : csv file

        Returns
        ---------
        borrow_info dict
        """
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            entries = {}
            for row in reader:
                # the transaction id is the key, and the rest of the info is the value in the dict
                info = [row[1], row[2], row[3], row[4], row[5]]
                entries[row[0]] = info
        return entries

    @staticmethod
    def parse_file(file):
        """
        Creates list of entries in csv file.

        Parameters
        ----------
        file : csv file

        Returns
        ---------
        list of csv entries
        """
        entries = []
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                entries.append(row)
        return entries

    def create_members(self, file):
        """
        Create dict with all members on file of the library.

        Parameters
        ----------
        file : csv file

        Returns
        ---------
        members dict
        """
        member_info = self.parse_file(file)
        members_dict = {}
        for m in member_info:
            borrowed_dict = {}
            for i in self.borrow_info.items():
                # if the member id is present in the borrowing info, the transaction is added to the borrowed_dict
                if i[1][0] == m[0]:
                    borrowed_dict[i[0]] = (i[1][2], i[1][4])
            members_dict[m[0]] = Members(m[0], m[1], m[2], m[3], m[4], m[5], borrowed_dict)
        return members_dict

    def create_items(self, file):
        """
        Create dict with all items on file of the library.

        Parameters
        ----------
        file : csv file

        Returns
        ---------
        items dict
        """
        item_info = self.parse_file(file)
        items_dic = {}
        for i in item_info:
            item_type = i[1].lower().strip()
            # depending on item type create that instance
            if item_type == 'book':
                items_dic[i[0]] = Book(i[0], i[2], i[3], i[4], int(i[5]))
            elif item_type == 'article':
                items_dic[i[0]] = Article(i[0], i[2], i[3], i[4], i[6], int(i[5]))
            elif item_type == 'digital media':
                items_dic[i[0]] = DigitalMedia(i[0], i[2], i[3], i[4], int(i[5]))
            else:
                print(i)
                print("Unable to create item")

        # label borrowed items as unavailable
        for b in self.borrow_info.values():
            if b[4] == '':
                items_dic[b[1]].available = False
        return items_dic

    # item methods
    def search_items(self, word: str):
        """
        Creates a list of items that contain the search word in the title or author.


        Parameters
        ----------
        word : str

        Returns
        ---------
        list of search results
        """
        item_type = str
        word = word.lower().strip()
        results = []
        category_option = input("Would you like the specify the type of item? (y/n) ")
        if category_option == 'y':
            category_input = input("Are you looking for: \n"
                                   "1. a Book \n"
                                   "2. an Article \n"
                                   "3. Digital Media \n")
            if category_input == '1':
                item_type = 'Book'
            elif category_input == '2':
                item_type = 'Article'
            elif category_input == '3':
                item_type = 'Digital Media'
            else:
                print("invalid input")

            # if the item is of specified type and the search word is present in the title or author name,
            # add the item to the results list
            for i in self.items.values():
                title = i.title.lower().split()
                author_l_name = i.l_name.lower()
                author_f_name = i.f_name.lower()
                if i.type == item_type and word in title or word in author_f_name or word in author_l_name:
                    results.append(i.item_id)
        elif category_option == 'n':
            # if the search word is present in the title, add the item to the results list
            for i in self.items.values():
                title = i.title.lower().split()
                author_l_name = i.l_name.lower()
                author_f_name = i.f_name.lower()
                if word in title or word in author_f_name or word in author_l_name:
                    results.append(i.item_id)
        return results

    def borrow_item(self):
        """
        Borrow item from the library.
        """
        borrow_input = input("Would you like to borrow an item? \n"
                             "If yes, enter item ID\n"
                             "If no, enter exit\n").strip()
        # return to command line menu
        if borrow_input == 'exit':
            return
        else:
            member_id = input('Enter your member ID: ')
            # check if the item is available
            if not self.items[borrow_input].available:
                print('This item is unavailable for borrowing')
                return
            # check how many items the member has borrowed
            elif len(self.members[member_id].items) > 10:
                print("Member has borrowed 10 items already")
                return
            # make the item unavailable
            self.items[borrow_input].available = False
            # create/determine transaction info
            transaction_id = 'T' + str(len(self.borrow_info) + 1)
            today_obj = date.today()
            today = today_obj.strftime('%d/%m/%Y')
            expected_return_obj = today_obj + timedelta(weeks=4.5)  # combination of the following links:
            # https://stackoverflow.com/questions/35066588/is-there-a-simple-way-to-increment-a-datetime-object-one
            # -month-in-python, https://www.geeksforgeeks.org/python-datetime-timedelta-function/
            expected_return = expected_return_obj.strftime('%d/%m/%Y')

            # add the transaction to borrow_info
            self.borrow_info[transaction_id] = [member_id, borrow_input, today, expected_return, '']
            # add the transaction to the member
            self.members[member_id].items[transaction_id] = (today, '')
            print("Happy reading or watching! ")
            # update borrowing.csv
            self.update_borrow_csv()

    def return_item(self, item: str, member: str):
        """
        Return item to the library.

        Parameters
        ----------
        item : str
        member : str

        Returns
        ---------
        None
        """
        # mark item as available in the library
        self.items[item].available = True

        # update borrow_info and member.items
        transaction_id = str
        for i in self.borrow_info.items():
            if i[1][0] == member and i[1][1] == item and i[1][4] == '':
                transaction_id = i[0]
        today_obj = date.today()
        today = today_obj.strftime('%d/%m/%Y')
        # add the return date to library's borrow info and member's borrowed dict
        self.borrow_info[transaction_id][4] = today
        self.members[member].items[transaction_id] = (self.members[member].items[transaction_id][0], today)
        # update borrowing.csv
        self.update_borrow_csv()

        # check if item is overdue and update the member's fine
        latest_return_date = datetime.strptime(self.borrow_info[transaction_id][3], '%d/%m/%Y').date()
        if today_obj > latest_return_date:
            # calculate how many days late the item was returned and the fine
            days_late = int((today_obj - latest_return_date).total_seconds() / 86400)
            self.members[member].fine += 0.25 * days_late
        print("{} is successfully returned, {}'s fine equals {} euros".format(self.items[item].title,
                                                                              self.members[member],
                                                                              self.members[member].fine))

    def add_item(self):
        """
        Add specific item to the library.
        """
        # create item ID
        item_id = 'I' + str(len(self.items) + 1)
        category = input("category: \n"
                         "a. Book \n"
                         "b. Article \n"
                         "c. Digital Media\n")
        category = category.lower().strip()
        # collect all necessary info of the item
        title = input("title: ")
        l_name = input("last name of author/director: ")
        f_name = input("first name of author/director: ")
        year = int(input("year of release/publication: "))
        journal = input("Which journal was it published (if not press enter): ")
        # create specific item                  better way? can you write Items and the correct item will be made?
        if category == 'a':
            self.items[item_id] = Book(item_id, title, l_name, f_name, year)
            print("Book successfully added to the library")
        elif category == 'b':
            self.items[item_id] = Article(item_id, title, l_name, f_name, journal, year)
            print("Article successfully added to the library")
        elif category == 'c':
            self.items[item_id] = DigitalMedia(item_id, title, l_name, f_name, year)
            print("Digital Media successfully added to the library")
        else:
            print("Invalid input: unable to add Item")

        self.update_items_csv()

    def edit_item(self, item_id: str):
        """
        Edit a specific item from the library.

        Parameters
        ----------
        item_id : str

        Returns
        ---------
        None
        """
        item_input = input("Would you like to edit the following item: {} by {} {} (press enter to confirm or enter "
                           "exit) ".format(self.items[item_id].title, self.items[item_id].f_name,
                                           self.items[item_id].l_name))
        # return to command line menu
        if item_input.strip() == 'exit':
            return
        # choose what item info to edit
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
            self.items[item_id].item_id = i
        elif type_edit == 'b':
            i = input("Enter Category: ")
            self.items[item_id].type = i
        elif type_edit == 'c':
            i = input("Enter Title: ")
            self.items[item_id].title = i
        elif type_edit == 'd':
            i = input("Enter Last Name: ")
            self.items[item_id].l_name = i
        elif type_edit == 'e':
            i = input("Enter First Name: ")
            self.items[item_id].f_name = i
        elif type_edit == 'f':
            i = int(input("Enter Publication/Release year: "))
            self.items[item_id].year = i
        elif type_edit == 'g':
            i = input("Enter Journal: ")
            self.items[item_id].journal = i
        else:
            print("Invalid input: unable to edit item")
            return
        print('{} successfully updated!'.format(self.items[item_id].title))
        self.update_items_csv()

    def delete_item(self, item_id: str):
        """
        Remove an item from the library.

        Parameters
        ----------
        item_id : str

        Returns
        ---------
        None
        """
        check = input("Are you sure you want to remove {}? (y/n) \n".format(self.items[item_id]))
        if check == 'y':
            removed_item = self.items.pop(item_id)
            self.update_items_csv()
            print("{} was removed".format(removed_item))
        elif check == 'n':
            print("{} was not removed".format(self.items[item_id]))
        else:
            print('Invalid input: please try again')

    # member methods
    def add_member(self):
        """
            Add a member to the library.
        """
        # create member ID
        member_id = 'M' + str(len(self.members) + 1)
        # collect necessary member info
        l_name = input("Enter last name: ")
        f_name = input("Enter first name: ")
        dob = input("Enter Date of Birth (dd/mm/yyyy): ")
        street = input("Enter street and number: ")
        city = input("Enter city: ")
        self.members[member_id] = Members(member_id, l_name, f_name, dob, street, city)
        print("{} is successfully added as a member".format(self.members[member_id]))
        self.update_members_csv()

    def edit_member(self, member_id: str):
        """
        Edit a specific member from the library.

        Parameters
        ----------
        member_id : str

        Returns
        ---------
        None
        """
        item_input = input("Would you like to edit the following member: {} {} (Member ID: {}) (press enter to "
                           "confirm or enter exit) ".format(self.members[member_id].f_name,
                                                            self.members[member_id].l_name,
                                                            self.members[member_id].member_id))
        # return to command line
        if item_input.strip() == 'exit':
            return
        # choose what member info to edit
        type_edit = input('What would you like to edit? \n'
                          'a. Member ID \n'
                          'b. Last Name \n'
                          'c. First Name \n'
                          'd. Date of Birth \n'
                          'e. Street and number \n'
                          'f. City \n')
        if type_edit == 'a':
            i = input("Enter Member ID: ")
            self.members[member_id].member_id = i
        elif type_edit == 'b':
            i = input("Enter Last Name: ")
            self.members[member_id].l_name = i
        elif type_edit == 'c':
            i = input("Enter First Name: ")
            self.members[member_id].f_name = i
        elif type_edit == 'd':
            i = input("Enter Date of Birth: ")
            self.members[member_id].dob = i
        elif type_edit == 'e':
            i = input("Enter Street and number: ")
            self.members[member_id].street = i
        elif type_edit == 'f':
            i = input("Enter City: ")
            self.members[member_id].city = i
        else:
            print("Invalid input: unable to edit member")
            return
        print("{}'s information is successfully updated".format(self.members[member_id]))
        self.update_members_csv()

    def delete_member(self, member_id: str):
        """
        Remove a member from the library.

        Parameters
        ----------
        member_id : str

        Returns
        ---------
        None
        """
        check = input("Are you sure you want to remove {}? (y/n) \n".format(self.members[member_id]))
        if check == 'y':
            removed_member = self.members.pop(member_id)
            self.update_members_csv()
            print("{} was removed".format(removed_member))
        elif check == 'n':
            print("{} was not removed".format(self.members[member_id]))
        else:
            print("Invalid input: please try again")

    # methods to update external files
    def update_members_csv(self):
        """
            Update members.csv based on the dict containing the members
        """
        labels = ['Member ID', 'Last name', 'First name', 'Date of Birth', 'Street', 'City']
        rows = []
        for i in self.members.values():
            # append the updated information to a list
            a = [i.member_id, i.l_name, i.f_name, i.dob, i.street, i.city]
            rows.append(a)
        # write the updated information to members.csv
        with open('members.csv', 'w+') as members_csv:
            csv_writer = csv.writer(members_csv, lineterminator='\n')
            csv_writer.writerow(labels)
            csv_writer.writerows(rows)

    def update_items_csv(self):
        """
        Update the items.csv based on the dict containing items.
        """
        labels = ['Item ID', 'Category', 'Title', 'Last name', 'First name', 'publication year', 'journal']
        rows = []
        for i in self.items.values():
            # append the updated information to a list (only article has journal attribute)
            if i.type == 'Article':
                a = [i.item_id, i.type, i.title, i.l_name, i.f_name, i.year, i.journal]
                rows.append(a)
            else:
                a = [i.item_id, i.type, i.title, i.l_name, i.f_name, i.year]
                rows.append(a)

        # write the updated information to items.csv
        with open('items.csv', 'w+') as items_csv:
            csv_writer = csv.writer(items_csv, lineterminator='\n')
            csv_writer.writerow(labels)
            csv_writer.writerows(rows)

    def update_borrow_csv(self):
        """
        Update the borrowing.csv based on the borrowing info dict.
        """
        labels = ['Transaction ID', 'Member ID', 'Item ID', 'Borrow date', 'Last expected return', 'Return date']
        rows = []
        for i in self.borrow_info.items():
            # append the updated information to a list
            a = [i[0], i[1][0], i[1][1], i[1][2], i[1][3], i[1][4]]
            rows.append(a)
        # write the updated information to borrowing.csv
        with open('borrowing.csv', 'w+') as borrowing_csv:
            csv_writer = csv.writer(borrowing_csv, lineterminator='\n')
            csv_writer.writerow(labels)
            csv_writer.writerows(rows)

    def __str__(self):
        return '{} at {} has {} items and {} members'.format(self.name, self.address, len(self.items),
                                                             len(self.members))


class Members(object):
    """
    A class to represent library members

    Attributes
    ----------
    member_id : str
    l_name : str
    f_name : str
    dob : str
    street : str
    city : str
    items : dict
    fine : float
     """

    def __init__(self, ID: str, l_name: str, f_name: str, DOB: str, street: str, city: str, borrowed_items: dict):
        """
        Constructs all the necessary attributes for the library object.

        Parameters
        ----------
        ID : str
        l_name : str
        f_name : str
        DOB : str
        street : str
        city : str
        borrowed_items : dict
        """
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
        return '{} {} (Member ID: {})'.format(self.f_name, self.l_name, self.member_id)


class Items(object):
    """
    A class to represent library items. 

    Attributes
    ----------
    item_id : str
    title : str
    type : str
    available : boolean
     """

    def __init__(self, ID: str, category: str, title: str):
        """
        Constructs all the necessary attributes for the library object.

        Parameters
        ----------
        ID : str
        title : str
        category : str
        """
        self.item_id = ID
        self.title = title
        self.type = category
        self.available = True

    def __str__(self):
        if self.available:
            return '{} (Item ID: {}) is a {} and available to borrow'.format(self.title, self.item_id, self.type)
        else:
            return '{} (Item ID: {}) is a {} and unavailable to borrow'.format(self.title, self.item_id, self.type)


class Book(Items):
    """
    A subclass to represent book items.

    Attributes
    ----------
    l_name : str
    f_name : str
    year : int
     """

    def __init__(self, ID: str, title: str, l_name: str, f_name: str, yof=0000):
        """
        Constructs all the necessary attributes for the book object.

        Parameters
        ----------
        ID : str
        title : str
        l_name : str
        f_name : str
        yof : int
        """
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
    """
    A class to represent article items.

    Attributes
    ----------
    l_name : str
    f_name: str
    journal : str
    year : int
     """

    def __init__(self, ID: str, title: str, l_name: str, f_name: str, journal: str, yof=0000):
        """
        Constructs all the necessary attributes for the article object.

        Parameters
        ----------
        ID : str
        title : str
        l_name : str
        f_name : str
        journal : str
        yof : int
        """
        Items.__init__(self, ID, 'Article', title)
        self.l_name = l_name
        self.f_name = f_name
        self.journal = journal
        self.year = yof

    def __str__(self):
        if self.available:
            return 'The Article: {} (Item ID: {}) from {} was written by {} {} in {} and is available for borrowing' \
                .format(self.title, self.item_id, self.journal, self.f_name, self.l_name, self.year)
        else:
            return 'The Article: {} (Item ID: {}) from {} was written by {} {} in {} and is unavailable for borrowing' \
                .format(self.title, self.item_id, self.journal, self.f_name, self.l_name, self.year)


class DigitalMedia(Items):
    """
    A class to represent library items. 

    Attributes
    ----------
    year : int
    l_name : str
    f_name : str

     """

    def __init__(self, ID: str, title: str, l_name: str, f_name: str, year=0000):
        """
        Constructs all the necessary attributes for the library object.

        Parameters
        ----------
        ID : str
        title : str
        l_name : str
        f_name : str
        year : int
        """
        Items.__init__(self, ID, 'Digital Media', title)
        self.year = year
        self.l_name = l_name
        self.f_name = f_name

    def __str__(self):
        if self.available:
            return 'The Digital Media: {} (Item ID: {}) is directed by {} {} in {} and available for borrowing'. \
                format(self.title, self.item_id, self.f_name, self.l_name, self.year)
        else:
            return 'The Digital Media: {} (Item ID: {}) is directed by {} {} in {} and unavailable for borrowing' \
                .format(self.title, self.item_id, self.f_name, self.l_name, self.year)


# main
def main():
    library = Library('The University Library', 'Park House, 191 N Circular Rd, Co. Dublin, D07 EWV4, Ireland')
    while True:
        try:
            # create command line menu
            i = int(input("\n What would you like to do?\n"
                          "1. Browse Items?\n"
                          "2. Check availability?\n"
                          "3. Add, edit or remove a member?\n"
                          "4. Add, edit or remove an item?\n"
                          "5. Return an item?\n"
                          "6. Check a member's fine?\n"
                          "7. Quit program\n"))
            # call correct function depending on user input
            # Browse items
            if i == 1:
                search_input = input("Enter your keyword: ")
                results = library.search_items(search_input)

                # display search results
                if len(results) == 0:
                    print("No Items matched your search \n")
                else:
                    for r in results:
                        print(library.items[r])
                    library.borrow_item()
            # Check availability of items
            elif i == 2:
                id_input = input("Enter the item ID: ")
                if library.items[id_input].available:
                    print('{} (Item ID: {}) is available for borrowing \n'.format(library.items[id_input].title,
                                                                                  library.items[id_input].item_id))
                    library.borrow_item()
                else:
                    print('{} (Item ID: {}) is unavailable for borrowing \n'.format(library.items[id_input].title,
                                                                                    library.items[id_input].item_id))
            # Member options menu
            elif i == 3:
                choice_input = input("Would you like to \n"
                                     "a. add a member \n"
                                     "b. edit a member \n"
                                     "c. remove a member \n")
                choice_input = choice_input.lower().strip()
                # add member instance
                if choice_input == 'a':
                    library.add_member()
                # edit member instance
                elif choice_input == 'b':
                    id_input = input("Enter Member ID: ")
                    library.edit_member(id_input)
                # delete member instance
                elif choice_input == 'c':
                    id_input = input("Enter member ID: ")
                    library.delete_member(id_input)
                else:
                    print("Invalid input: please try again")
            # Item options menu
            elif i == 4:
                choice_input = input("Would you like to \n"
                                     "a. add an item \n"
                                     "b. edit an item \n"
                                     "c. remove an item \n")
                choice_input = choice_input.lower().strip()
                # add item instance
                if choice_input == 'a':
                    library.add_item()
                # edit item instance
                elif choice_input == 'b':
                    id_input = input("Enter Item ID: ")
                    library.edit_item(id_input)
                # delete item instance
                elif choice_input == 'c':
                    id_input = input("Enter Item ID: ")
                    library.delete_item(id_input)
                else:
                    print("Invalid input: please try again")
            # return item
            elif i == 5:
                member_input = input("Please enter member ID: ")
                return_input = input("Please enter item ID: ")
                library.return_item(return_input, member_input)
            # exit code
            elif i == 6:
                member_input = input("Please enter member ID: ")
                print("{} owes {} euros in fines".format(library.members[member_input],
                                                         library.members[member_input].fine))
            elif i == 7:
                exit()
        except ValueError:
            print("Invalid input, please try again: ", '\n')
        except KeyError:
            print("Invalid input, please try again: ", '\n')


main()
