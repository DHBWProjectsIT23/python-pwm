INTERFACE_MSG = "This is an Interface"


class TabInterface:
    async def process_input(self, input_key: int) -> None:
        raise NotImplementedError(INTERFACE_MSG)

    def refresh(self) -> None:
        raise NotImplementedError(INTERFACE_MSG)

    def show(self) -> None:
        raise NotImplementedError(INTERFACE_MSG)

    def hide(self) -> None:
        raise NotImplementedError(INTERFACE_MSG)
