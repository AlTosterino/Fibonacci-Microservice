import asyncio


class FibonacciGenerator:
    def __init__(self, settings: "GeneratorSettings"):
        self.settings = settings
        try:
            # Try to get last numbers from DB
            (
                self.first_number,
                self.second_number,
            ) = settings.db_repo.get_last_two_numbers()
            self.add_numbers()
            self.add_numbers()
        except ValueError:
            self.first_number, self.second_number = 0, 1

    def __aiter__(self):
        return self

    async def __anext__(self):
        await asyncio.sleep(self.settings.delay)
        temp_number = self.first_number
        self.add_numbers()
        return temp_number

    def add_numbers(self):
        self.first_number, self.second_number = (
            self.second_number,
            self.first_number + self.second_number,
        )
