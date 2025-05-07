import os
from prettytable import PrettyTable
from Filter import Filter
from math import ceil

class Menu:
    def __init__(self, connection):
        self.connection = connection
        # self.connection = Connection("tests.db").connect()
        self.go_back = False

        while not self.go_back:
            self.display_menu()

        Menu.clear_screen()
        # self.connection.close()
        print("Logged Out Successfully")

    def display_menu(self):
        pass

    def back(self):
        self.go_back = True

    @staticmethod
    def clear_screen():
        # For Windows
        if os.name == 'nt':
            _ = os.system('cls')
        # For macOS and Linux
        else:
            _ = os.system('clear')

    @staticmethod
    def get_str_input(form_title, input_title):
        Menu.clear_screen()
        print(form_title)
        raw_input = input("Please enter the " + input_title + "[0 to go back]: ")
        return None if raw_input == "0" else raw_input

    @staticmethod
    def get_str_lst_input(form_title, input_title, allowed_list):
        # allowed_list must be in all caps to allow cap insensitivity for user
        raw_input = "-1"

        while raw_input.upper() not in allowed_list:
            Menu.clear_screen()
            print(form_title)
            print("Please enter " + input_title + " Answer in [", end="")
            for i in allowed_list[:-1]:
                print(i, end=", ")
            raw_input = input(allowed_list[-1] + "][0 to go back]: ")
            if raw_input == "0":
                return None

            if raw_input.upper() not in allowed_list:  # duplicate of while loop, but can't find anything better
                input("Invalid input. Press enter to try again...")
        return raw_input.upper()

    @staticmethod
    def get_int_input(form_title, input_title):
        while True:
            Menu.clear_screen()
            print(form_title)
            raw_int = input("Please enter the " + input_title + "[0 to go back]: ")
            try:
                raw_int = int(raw_int)
            except ValueError:
                input("Invalid input, press enter to try again...")
                continue
            if raw_int < 0:
                input("Invalid input, press enter to try again...")
                continue
            return None if raw_int == 0 else raw_int

    def menu(self, title, options_str, options_dict):
        Menu.clear_screen()
        print(title)
        print(options_str)
        pick = input("Select an option: ")

        if pick in options_dict:
            try:
                # If we are using menus
                options_dict.get(pick, lambda: None)(self.connection)
            except TypeError:
                # if we are filling out a form
                options_dict.get(pick, lambda: None)()
        else:
            input("Invalid option, press enter to try again.")

    @staticmethod
    def get_table(query_result, is_pickup, max_amount=5, page_num=0):
        current_count_displayed = 0
        index = 0
        try:
            query_count = len(query_result)
        except TypeError: # just in case we are using the pickup form and are just displaying one item, it just so
                          # happens that that one item is not in a list, so make it a list of one item
            query_count = 1
            query_result = (query_result,)

        if is_pickup:
            table = PrettyTable(['Pickup ID', 'Completed or Expired?', 'Student Name', 'Test Name',
                                 'Homework/Notecard', 'Date in', 'Date out',
                                 'Staff Initial', 'Sent/Filed/Mailed/Pickup', 'Instructor Name', 'Resolved?'])
        else:
            table = PrettyTable(
                ['Dropoff ID', 'Test Name', 'Date in', 'Instructor Name', 'Initial Amount', 'Current Amount'])

        for test_referral in query_result:
            # going from page_num * max_amount to (page_num + 1) * max_amount, so that we can do only one page
            if index >= (page_num + 1) * max_amount:
                break
            if ((current_count_displayed < max_amount)
                    and (index >= (page_num * max_amount))):

                if is_pickup:
                    table.add_row([
                        test_referral.id, test_referral.CE, test_referral.student_name, test_referral.test_name,
                        test_referral.HN, test_referral.date_in, test_referral.date_out,
                        test_referral.staff_initial, test_referral.SFMP, test_referral.instructor_name, test_referral.is_resolved])
                else:
                    table.add_row([
                        test_referral.id, test_referral.test_name, test_referral.date_in,
                        test_referral.instructor_name,
                        test_referral.initial_amount, test_referral.current_amount])

                current_count_displayed += 1
            index += 1

        return (f"Querying {'Pickup' if is_pickup else 'Dropoff'} Form\n" + table.get_string()
                + f"\nShowing {current_count_displayed} out of {query_count}, max {max_amount} per page"
                + f"\nPage {page_num + 1} of {ceil(query_count / max_amount)}")

    def get_item_from_table(self, is_pickup, need_item, check_if_referral_usable):
        query_filter = Filter(self.connection, is_pickup=is_pickup, check_if_referral_usable=check_if_referral_usable)
        should_break = False

        max_amount = 5
        page_num = 0

        while True:
            self.clear_screen()
            query = query_filter.apply_filters()
            query_count = len(query)
            print(self.get_table(query, is_pickup=is_pickup, max_amount=max_amount, page_num=page_num))
            raw_input = input("[0 to go back][f to filter][o to order by][< to go back a page]"
                              "[> to go forward a page][m to change amount per page]: ")

            if raw_input == "0":
                return None
            elif raw_input == "f":
                query_filter.filter_select()
                continue
            elif raw_input == "o":
                query_filter.order_by_select()
                continue
            elif raw_input == "<" and page_num > 0:
                page_num -= 1
                continue
            elif raw_input == ">" and page_num + 1 < ceil(query_count / max_amount):
                page_num += 1
                continue
            elif raw_input == "m":
                raw_input = self.get_int_input("Query Page", "amount per page")
                if raw_input is not None:
                    max_amount = int(raw_input)
                    page_num = 0
                continue

            try:
                raw_input = int(raw_input)
            except ValueError:
                input("Invalid input, press enter to try again...")
                continue

            if need_item:
                for item in query_filter.apply_filters():
                    if item.id == raw_input:
                        return item

            input("Incorrect Selection, press enter to try again...")
