import pytest
from fib_microservice.infrastructure.fibonacci_generator.generator import (
    FibonacciGenerator,
)
from fib_microservice.shared.settings import GeneratorSettings
from unittest.mock import patch


@pytest.fixture
@patch("fib_microservice.infrastructure.message_broker.sender.pika")
def settings(pika_mock):
    return GeneratorSettings(delay=0, host="localhost")


@pytest.fixture
def generator(settings):
    return FibonacciGenerator(settings)


def test_should_return_self_from_aiter(generator):
    # Given generator
    # When
    gen = generator.__aiter__()
    # THen
    assert gen == generator


def test_should_have_correct_settings(generator):
    # Given generator
    # When
    correct = isinstance(generator.settings, GeneratorSettings)
    # Then
    assert correct


@pytest.mark.asyncio
async def test_should_return_correct_fib_numbers(generator):
    data = (0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89)
    count = 0
    async for num in generator:
        try:
            assert num == data[count]
            count += 1
        except IndexError:
            break
