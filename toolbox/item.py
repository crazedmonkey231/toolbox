class Item(object):
    def __init__(self, item_id: str, item_name: str, item_description: str, item_icon: str, item_value: float,
                 callback=None, callback_params=None):
        self.item_id = item_id
        self.item_name = item_name
        self.item_description = item_description
        self.item_icon = item_icon
        self.item_value = round(item_value, 2)
        self.callback = callback
        self.callback_params = callback_params

    def use(self):
        if self.callback is not None:
            self.callback(*self.callback_params)
