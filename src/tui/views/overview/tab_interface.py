class TabInterface:
    async def process_input(self, input_key: int):
        raise NotImplementedError("This is an Interface")

    def refresh(self):
        raise NotImplementedError("This is an Interface")

    def show(self):
        raise NotImplementedError("This is an Interface")

    def hide(self):
        raise NotImplementedError("This is an Interface")
