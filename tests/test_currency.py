import pytest

from stockholm import Currency, Money


def test_currency():
    EUR = Currency("EUR")
    assert str(EUR) == "EUR"
    assert repr(EUR) == '<stockholm.Currency: "EUR">'

    m = Money(100, EUR)
    assert str(m) == "100.00 EUR"
    assert isinstance(m.currency, Currency)
    assert str(m.currency) == "EUR"
    assert str(m.currency.ticker) == "EUR"


def test_currency_arithmetics():
    EUR = Currency("EUR")
    SEK = Currency("SEK")
    assert EUR
    assert EUR == "EUR"
    assert EUR != "SEK"
    assert EUR != SEK
    assert EUR != ""
    assert EUR != 0
    assert EUR is not False

    m1 = Money(100, EUR)
    m2 = Money(100, "EUR")
    assert m1 == m2

    m3 = Money(100, "SEK")
    assert m1 != m3

    m4 = Money(100, SEK)
    assert m1 != m4
    assert m3 == m4


def test_metacurrency():
    class EUR(Currency):
        pass

    class SEK(Currency):
        pass

    class DogeCoin(Currency):
        ticker = "DOGE"

    class AppleStock(Currency):
        ticker = "APPL"

    EUR2 = Currency("EUR")

    assert EUR
    assert EUR == "EUR"
    assert EUR != "EUR2"
    assert EUR == EUR2
    assert EUR != SEK

    m1 = Money(100, EUR)
    m2 = Money(100, "EUR")
    m3 = Money(100, EUR2)
    assert m1 == m2
    assert m1 == m3

    stock = Money(5, AppleStock)
    assert stock == "5.00 APPL"
    assert stock > 0
    assert stock < 10
    assert str(stock) == "5.00 APPL"
    assert f"{stock:c}" == "APPL"

    assert str(EUR) == "EUR"
    assert str(SEK) == "SEK"
    assert str(AppleStock) == "APPL"

    assert repr(EUR) == '<stockholm.Currency: "EUR">'
    assert repr(AppleStock) == '<stockholm.Currency: "APPL">'

    assert EUR is not None
    assert EUR != ""
    assert EUR != 0
    assert EUR != Money(0, EUR)

    class CurrencyConcept(Currency):
        ticker = None

    assert not bool(CurrencyConcept)
    assert CurrencyConcept != EUR
    assert CurrencyConcept == CurrencyConcept
    assert not CurrencyConcept
    assert CurrencyConcept is not None
    assert CurrencyConcept is not False
    assert CurrencyConcept is not True
    assert CurrencyConcept == ""
    assert CurrencyConcept != 0
    assert CurrencyConcept != Money(0, EUR)


def test_immutability():
    class EUR(Currency):
        pass

    BTC = Currency("BTC")

    with pytest.raises(AttributeError):
        EUR.ticker = "USD"

    with pytest.raises(AttributeError):
        BTC.ticker = "ETH"

    with pytest.raises(AttributeError):
        del EUR.ticker

    with pytest.raises(AttributeError):
        del BTC.ticker


def test_custom_currency():
    class EUR(Currency):
        pass

    c1 = Currency("EUR")
    assert c1 != Money(0, EUR)

    c2 = Currency(c1)
    assert c2.ticker == "EUR"
    assert c2 == c1
    assert str(c2) == "EUR"
    assert c2 == "EUR"

    c3 = Currency()
    assert c3.ticker == ""
    assert c3 != c1
    assert c3 == ""
    assert str(c3) == ""
    assert c3 != Money(0, EUR)

    c4 = Currency(EUR)
    assert c4.ticker == "EUR"
    assert c4 == c1
    assert c4 == "EUR"


def test_currency_hashable() -> None:
    EUR = Currency("EUR")

    class SEK(Currency):
        pass

    assert hash(EUR)
    assert hash(SEK)


def test_dogecoin():
    class DogeCoin(Currency):
        ticker = "DOGE"

    assert Money(1, DogeCoin) == Money(1, DogeCoin)