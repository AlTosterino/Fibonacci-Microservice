import asyncio


class FibonacciGenerator:
    def __init__(self, settings: "GeneratorSettings"):
        # TODO: Check for the last two numbers in DB
        self.settings = settings
        self.first_number, self.second_number = 0, 1

    def __aiter__(self):
        return self

    async def __anext__(self):
        await asyncio.sleep(self.settings.delay)
        temp_number = self.first_number
        self.first_number, self.second_number = (
            self.second_number,
            self.first_number + self.second_number,
        )
        return temp_number
