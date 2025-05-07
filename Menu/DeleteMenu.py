from DatabaseManager import PickupTable, DropoffTable
from Menu.Menu import Menu

class DeleteMenu(Menu):
    def display_menu(self):
        self.menu("Delete Menu",
                  "1: Pickup Table\n"
                            "2: Drop-off Table\n"
                            "0: Back",
                  {
                      '0': self.back,
                      '1': self.delete_from_pickup,
                      '2': self.delete_from_dropoff
                  })

    def delete_from_pickup(self):
        test_referral = self.get_item_from_table(is_pickup=True, need_item=True, check_if_referral_usable=False)
        if test_referral is None:
            return

        answer = self.get_str_lst_input("Delete Form",
                                        "whether you wish to add the amount back to the dropoff referral?",
                                        ['Y', 'N'])
        if answer == 'Y':
            add_amount_back = True
        elif answer == 'N':
            add_amount_back = False
        elif answer == '0':
            return

        if add_amount_back:
            dropoff_item = self.connection.query(DropoffTable).filter(test_referral.dropoff_id == DropoffTable.id)
            for item in dropoff_item:
                item.current_amount = item.current_amount + 1  # should be the only item in the list
            self.connection.commit() # TODO: this line may or may not be needed
        self.connection.delete(test_referral)

        input("Deleted, press enter to continue...")
        self.connection.commit()

    def delete_from_dropoff(self):
        test_referral = self.get_item_from_table(is_pickup=False, need_item=True, check_if_referral_usable=False)
        if test_referral is None:
            return

        answer = self.get_str_lst_input("Delete Form",
                                        "whether you wish to delete the related pickup referrals",
                                        ['Y', 'N'])
        if answer == 'Y':
            delete_related_pickup = True
        elif answer == 'N':
            delete_related_pickup = False
        elif answer == '0':
            return

        if delete_related_pickup:
            self.connection.query(PickupTable).filter(PickupTable.dropoff_id == test_referral.id).delete()
        self.connection.delete(test_referral)

        input("Deleted, press enter to continue...")
        self.connection.commit()
