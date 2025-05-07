from datetime import datetime

from DatabaseManager import DropoffTable, PickupTable, Connection
from Menu.Menu import Menu
from Menu.QueryMenu import QueryMenu
from Menu.DeleteMenu import DeleteMenu
from Menu.UpdateMenu import UpdateMenu

class MainMenu(Menu):

    def __init__(self):
        # self.connection =
        super().__init__(Connection("tests.db").connect())
        self.connection.close()

    def display_menu(self):
        self.menu("Main Menu",
                  (
                  "1: Query\n"
                  "2: Pickup Form\n"
                  "3: Drop-off Form\n"
                  "4: Delete Form\n"
                  "5: Update Form\n"
                  "0: Exit"
                  ),
                  {
                      '0': self.back,
                      '1': QueryMenu,
                      '2': self.pickup_form,
                      '3': self.dropoff_form,
                      '4': DeleteMenu,
                      '5': UpdateMenu
                  }
                  )

    def pickup_form(self):
        # we select from the dropoff table to create a pickup form

        test_referral = self.get_item_from_table(is_pickup=False, need_item=True, check_if_referral_usable=True)

        if test_referral is None: # just in case they went back on previous input
            return

        # fill out the test referral
        raw_input = self.get_str_lst_input("Pickup Form",
                                           "question: is this form being filled in advance? (Does it need to be resolved?)",
                                           ['Y', 'N'])
        if raw_input == 'Y':
            is_resolved = False
        elif raw_input == 'N':
            is_resolved = True
        else:
            return

        CE = self.get_str_lst_input(self.get_table(test_referral, is_pickup=False), "Completed or Expired.", ['C', 'E'])
        if CE is None:
            return

        student_name = self.get_str_input(self.get_table(test_referral, is_pickup=False),"Student Name")
        if student_name is None:
            return

        HN = self.get_str_lst_input(self.get_table(test_referral, is_pickup=False), "Homework or Note-card.", ['H', 'N', ''])
        if HN is None:
            return

        if is_resolved:
            staff_initial = self.get_str_input(self.get_table(test_referral, is_pickup=False),"Staff Initials")
            if staff_initial is None:
                return

            SFMP = self.get_str_lst_input(self.get_table(test_referral, is_pickup=False), "Sent, Filed, Mailed, or Pickup.", ['S', 'F', 'M', 'P'])
            if SFMP is None:
                return
            elif SFMP == 'F':
                test_referral.current_amount = test_referral.current_amount + 1 #because we are returning the pickup to file

            date_out = datetime.today()
        else:
            staff_initial = ""
            SFMP = ""
            date_out = datetime.min

        self.connection.add(PickupTable(CE=CE, student_name=student_name, test_name=test_referral.test_name,
                                        HN=HN, date_in=test_referral.date_in, date_out=date_out,
                                        staff_initial=staff_initial, SFMP=SFMP, instructor_name=test_referral.instructor_name,
                                        dropoff_id=test_referral.id, is_resolved=is_resolved))

        test_referral.current_amount = test_referral.current_amount - 1
        self.connection.commit()

    def dropoff_form(self):
        self.clear_screen()
        print("Drop-off Form")

        # fill out test referral
        test_name = self.get_str_input("Drop-off Form", "Test Name")
        if test_name is None:
            return

        instructor_name = self.get_str_input("Drop-off Form", "Instructor Name")
        if instructor_name is None:
            return

        amount = self.get_int_input("Drop-off Form", "Amount")
        if amount is None:
            return

        self.connection.add(DropoffTable(test_name=test_name, date_in=datetime.today(), instructor_name=instructor_name,
                                         initial_amount=amount, current_amount=amount))
        self.connection.commit()
