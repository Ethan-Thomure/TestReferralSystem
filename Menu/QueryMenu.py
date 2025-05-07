from Menu.Menu import Menu

class QueryMenu(Menu):
    def display_menu(self):
        self.menu("Query Menu",
                  "1: Pickup Table\n"
                            "2: Drop-off Table\n"
                            "0: Back",
                  {
                      '0': self.back,
                      '1': self.query_pickup_table,
                      '2': self.query_dropoff_table
                  })

    def query_pickup_table(self):
        self.get_item_from_table(is_pickup=True, need_item=False, check_if_referral_usable=False)

    def query_dropoff_table(self):
        self.get_item_from_table(is_pickup=False, need_item=False, check_if_referral_usable=False)
