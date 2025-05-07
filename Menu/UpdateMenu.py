from DatabaseManager import DropoffTable, PickupTable
from Menu.Menu import Menu
from datetime import datetime

class UpdateMenu(Menu):
    def display_menu(self):
        self.menu("Update Menu",
                  "1: Pickup Table\n"
                  "2: Drop-off Table\n"
                  "0: Back\n",
                  {
                      '0': self.back,
                      '1': self.update_pickup,
                      '2': self.update_dropoff
                  })

    def update_pickup(self):
        self.clear_screen()
        test_referral = self.get_item_from_table(is_pickup=True, need_item=True, check_if_referral_usable=False)
        if test_referral is None:
            return

        # figure out which field to update
        field = input(self.get_table(test_referral, True) +
                      "\nWhich field do you want to update?\n"
                      "1: Test Name [CASCADING]\n"
                      "2: Instructor Name [CASCADING]\n"
                      "3: Completed / Expired\n"
                      "4: Student Name\n"
                      "5: Homework or Notecard\n"
                      "6: Staff Initial\n"
                      "7: Sent/Filed/Mailed/Pickup\n"
                      "8: Resolved?\n"
                      "0: Back\n")
        # update based on field chosen
        if field == "1":
            new_test_name = self.get_str_input("Update Pickup Form", "Test Name")

            # test_referral.test_name = new_test_name

            pickups = self.connection.query(PickupTable).filter(test_referral.dropoff_id == PickupTable.dropoff_id).all()
            for pickup in pickups:
                pickup.test_name = new_test_name

            dropoff_referral = self.connection.query(DropoffTable).filter(DropoffTable.id == test_referral.dropoff_id).all()
            dropoff_referral = dropoff_referral[0]
            dropoff_referral.test_name = new_test_name

        elif field == "2":
            new_instructor_name = self.get_str_input("Update Dropoff Form", "Instructor Name")

            # test_referral.instructor_name = new_instructor_name

            pickups = self.connection.query(PickupTable).filter(test_referral.dropoff_id == PickupTable.dropoff_id).all()
            for pickup in pickups:
                pickup.instructor_name = new_instructor_name

            dropoff_referral = self.connection.query(DropoffTable).filter(DropoffTable.id == test_referral.dropoff_id).all()
            dropoff_referral = dropoff_referral[0]
            dropoff_referral.instructor_name = new_instructor_name

        elif field == "3":
            new_CE = self.get_str_lst_input("Update Pickup Form", "Completed or Expired.", ['C', 'E'])
            if new_CE is None:
                return
            test_referral.CE = new_CE

        elif field == "4":
            new_student_name = self.get_str_input("Update Pickup Form", "Student Name")
            if new_student_name is None:
                return
            test_referral.student_name = new_student_name

        elif field == "5":
            new_HM = self.get_str_lst_input("Update Pickup Form", "Homework or Notecard.", ['H', 'N', ''])
            if new_HM is None:
                return
            test_referral.HM = new_HM

        elif field == "6":
            new_staff_initial = self.get_str_input("Update Pickup Form", "Staff Initials")
            if new_staff_initial is None:
                return
            test_referral.staff_initial = new_staff_initial

        elif field == "7":
            new_SFMP = self.get_str_lst_input("Update Pickup Form", "Sent/Filed/Mailed/Pickup", ['S', 'F', 'M', 'P'])
            if new_SFMP is None:
                return
            test_referral.SFMP = new_SFMP

        elif field == "8":
            if not test_referral.is_resolved:
                raw_input = self.get_str_lst_input("Update Pickup Form",
                                                   "question: are there multiple of the same pickups that need to be resolved?",
                                                   ['Y', 'N'])
                if raw_input == "Y":
                    test_referrals = self.connection.query(PickupTable).filter(test_referral.dropoff_id == PickupTable.dropoff_id).all()
                    raw_input2 = self.get_str_lst_input(self.get_table(test_referrals, is_pickup=True),
                                                       "question: are you sure you want these resolved?",
                                                       ['Y', 'N'])
                    if raw_input2 == "Y":

                        new_staff_initial = self.get_str_input("Update Pickup Form", "Staff Initials")
                        if new_staff_initial is None:
                            return

                        new_SFMP = self.get_str_lst_input("Update Pickup Form",
                                                          "Sent/Filed/Mailed/Pickup",
                                                          ['S', 'F', 'M', 'P'])
                        amount_to_add_back = 0
                        for referral in test_referrals:
                            referral.is_resolved = True
                            referral.date_out = datetime.today()
                            referral.staff_initial = new_staff_initial
                            referral.SFMP = new_SFMP
                            if new_SFMP == 'F':
                                amount_to_add_back += 1

                        if amount_to_add_back > 0:
                            dropoff_referrals = self.connection.query(DropoffTable).filter(DropoffTable.id == test_referral.dropoff_id).all()
                            for dropoff in dropoff_referrals: #should just be one...
                                dropoff.current_amount = dropoff.current_amount + amount_to_add_back
                    else:
                        input("Canceled, press enter to continue...")
                        return
                elif raw_input == "N":
                    new_staff_initial = self.get_str_input("Update Pickup Form", "Staff Initials")
                    if new_staff_initial is None:
                        return

                    new_SFMP = self.get_str_lst_input("Update Pickup Form",
                                                      "Sent/Filed/Mailed/Pickup",
                                                      ['S', 'F', 'M', 'P'])

                    test_referral.is_resolved = True
                    test_referral.date_out = datetime.today()
                    test_referral.staff_initial = new_staff_initial
                    test_referral.SFMP = new_SFMP
                    if new_SFMP == 'F':
                        dropoff_referrals = self.connection.query(DropoffTable).filter(DropoffTable.id == test_referral.dropoff_id).all()
                        for dropoff in dropoff_referrals: #should just be one...
                            dropoff.current_amount = dropoff.current_amount + 1

                else:
                    return
            else:
                input("Can't unresolve things, press enter to continue...")
                return

        elif field == "0":
            return
        else:
            input("Invalid input, press enter to continue...")

        self.connection.commit()

    def update_dropoff(self):
        self.clear_screen()
        test_referral = self.get_item_from_table(is_pickup=False, need_item=True, check_if_referral_usable=False)
        if test_referral is None:
            return

        # figure out which field to update
        field = input(self.get_table(test_referral, False) +
                      "\nWhich field do you want to update?\n"
                      "1: Test Name [CASCADING]\n"
                      "2: Instructor Name [CASCADING]\n"
                      "3: Current Amount\n"
                      "0: Back\n")
        # update based on field chosen
        if field == "1":
            new_test_name = self.get_str_input("Update Dropoff Form", "Test Name")

            test_referral.test_name = new_test_name

            pickups = self.connection.query(PickupTable).filter(test_referral.id == PickupTable.dropoff_id).all()
            for pickup in pickups:
                pickup.test_name = new_test_name

        elif field == "2":
            new_instructor_name = self.get_str_input("Update Dropoff Form", "Instructor Name")

            test_referral.instructor_name = new_instructor_name

            pickups = self.connection.query(PickupTable).filter(test_referral.id == PickupTable.dropoff_id).all()
            for pickup in pickups:
                pickup.instructor_name = new_instructor_name

        elif field == "3":
            new_current_amount = self.get_int_input("Update Dropoff Form", "Current Amount")
            test_referral.current_amount = new_current_amount
        elif field == "0":
            return
        else:
            input("Invalid input, press enter to continue...")

        self.connection.commit()
