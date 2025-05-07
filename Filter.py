from prettytable import PrettyTable
from DatabaseManager import PickupTable, DropoffTable

class Filter:
    def __init__(self, connection, is_pickup, check_if_referral_usable):
        self.connection = connection
        self.is_pickup = is_pickup
        self.check_if_referral_usable = check_if_referral_usable

        self.instructor_filter = ""
        self.test_name_filter = ""
        self.date_in_filter = ""

        self.order_with = DropoffTable.id

        if is_pickup:
            self.order_with = PickupTable.id

            self.student_name_filter = ""
            self.date_out_filter = ""
            self.staff_initial = ""

    def display_filter(self):
        # display pickup filter
        if self.is_pickup:
            print("Pickup Filters")
            table = PrettyTable(["Instructor Name", "Test Name", "Student Name", "Date in", "Date out", "Staff Initial"])
            table.add_row([self.instructor_filter, self.test_name_filter, self.student_name_filter, self.date_in_filter,
                           self.date_out_filter, self.staff_initial])
        else:
            print("Dropoff Filters")
            table = PrettyTable(["Instructor Name", "Test Name", "Date in"])
            table.add_row([self.instructor_filter, self.test_name_filter, self.date_in_filter])

        print(table)

    def apply_filters(self):
        if self.is_pickup:
            return  self.connection.query(PickupTable).filter(
                PickupTable.instructor_name.contains(self.instructor_filter), PickupTable.test_name.contains(self.test_name_filter),
                PickupTable.student_name.contains(self.student_name_filter), PickupTable.date_in.contains(self.date_in_filter),
                PickupTable.date_out.contains(self.date_out_filter), PickupTable.staff_initial.contains(self.staff_initial)).order_by(self.order_with).all()
        else:
            if not self.check_if_referral_usable:
                return self.connection.query(DropoffTable).filter(
                    DropoffTable.instructor_name.contains(self.instructor_filter),
                    DropoffTable.test_name.contains(self.test_name_filter),
                    DropoffTable.date_in.contains(self.date_in_filter)).order_by(self.order_with).all()
            else:
                return self.connection.query(DropoffTable).filter(
                    DropoffTable.instructor_name.contains(self.instructor_filter),
                    DropoffTable.test_name.contains(self.test_name_filter),
                    DropoffTable.date_in.contains(self.date_in_filter), DropoffTable.current_amount > 0).order_by(self.order_with).all()

    def filter_select(self):
        # Selects a filter to change, then returns the applied filter to the connection of the proper table

        # Selection of filter or quit
        self.display_filter()
        print("1: Filter with Instructor Name\n"
              "2: Filter with Test Name\n"
              "3: Filter with Date In\n" +

              ("4: Filter with Student Name\n"
              "5: Filter with Date Out\n"
              "6: Filter with Staff Initial\n"
               if self.is_pickup else "") +

              "0: Back")

        #TODO make a function for entering in options like menu
        user_input = input("Make your selection: ")
        if user_input == "1":
            self.instructor_filter = input("Enter filter for the instructor name: ")
        elif user_input == "2":
            self.test_name_filter = input("Enter filter for the test name: ")
        elif user_input == "3":
            self.date_in_filter = input("Enter filter for the date in: ")
        elif user_input == "4" and self.is_pickup:
            self.student_name_filter = input("Enter filter for the student name: ")
        elif user_input == "5" and self.is_pickup:
            self.date_out_filter = input("Enter filter for the date out: ")
        elif user_input == "6" and self.is_pickup:
            self.staff_initial = input("Enter filter for the staff initial: ")
        elif user_input == "0":
            return -1
        else:
            input("Invalid input, press enter to try again...")

        return self.apply_filters()

    def order_by_select(self):
        print("Select the number to filter by it\n"
              "1: Instructor Name\n"
              "2: Test Name\n"
              "3: Date In\n" +

              ("4: Student Name\n"
              "5: Date Out\n"
              "6: Staff Initial\n"
               if self.is_pickup else "") +

              "0: Back")

        user_input = input("Make your selection: ")
        table = PickupTable if self.is_pickup else DropoffTable
        if user_input == "1":
            self.order_with = table.instructor_name
        elif user_input == "2":
            self.order_with = table.test_name
        elif user_input == "3":
            self.order_with = table.date_in

        elif user_input == "4" and self.is_pickup:
            self.order_with = table.student_name
        elif user_input == "5" and self.is_pickup:
            self.order_with = table.date_out
        elif user_input == "6" and self.is_pickup:
            self.order_with = table.staff_initial

        elif user_input == "0":
            return -1
