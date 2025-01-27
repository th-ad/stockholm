from decimal import Decimal

import pytest

import stockholm
from stockholm import BaseCurrency, Currency, DefaultCurrency, Money
from stockholm.currency import CLF, DOGE, IQD, JPY, USD, XBT, Bitcoin, DogeCoin, Ethereum, get_currency


def test_currency():
    EUR = Currency("EUR")
    assert str(EUR) == "EUR"
    assert EUR.as_string() == "EUR"
    assert EUR.as_str() == "EUR"
    assert repr(EUR) == '<stockholm.Currency: "EUR">'

    assert repr(type(EUR)) == "<class 'stockholm.currency.Currency'>"
    assert str(type(EUR)) == "<class 'stockholm.currency.Currency'>"
    assert repr(Currency) == "<class 'stockholm.currency.Currency'>"
    assert str(Currency) == "<class 'stockholm.currency.Currency'>"

    m = Money(100, EUR)
    assert str(m) == "100.00 EUR"
    assert isinstance(m.currency, BaseCurrency)
    assert str(m.currency) == "EUR"
    assert str(m.currency.ticker) == "EUR"
    assert m.currency_code == "EUR"
    assert EUR.decimal_digits == 2


def test_default_currency():
    with pytest.raises(TypeError):
        DefaultCurrency()

    m1 = Money(4711)
    m2 = Money(4711, DefaultCurrency)
    m3 = Money(4711, currency=DefaultCurrency)

    assert m1 == m2 == m3

    assert m1.currency is None
    assert m2.currency is None
    assert m3.currency is None

    assert m1.currency_code is None
    assert m2.currency_code is None
    assert m3.currency_code is None


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
    class EUR(BaseCurrency):
        pass

    class SEK(BaseCurrency):
        pass

    class DogeCoin(BaseCurrency):
        ticker = "DOGE"

    class AppleStock(BaseCurrency):
        ticker = "APPL"

    EUR2 = Currency("EUR")

    assert f"{AppleStock:c}" == "APPL"
    assert f"{EUR2:c}" == "EUR"

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

    class CurrencyConcept(BaseCurrency):
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
    class EUR(BaseCurrency):
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
    class EUR(BaseCurrency):
        pass

    c1 = Currency("EUR")
    assert c1 != Money(0, EUR)
    assert c1.decimal_digits == 2

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

    CARLOS = Currency("CarlosCoin", decimal_digits=0)
    assert CARLOS.ticker == "CarlosCoin"
    m = Money(100, CARLOS)
    assert str(m) == "100 CarlosCoin"


def test_currency_hashable() -> None:
    EUR = Currency("EUR")

    class SEK(BaseCurrency):
        pass

    assert hash(EUR)
    assert hash(SEK)


def test_currency_types() -> None:
    assert JPY == Currency("JPY")
    assert JPY.decimal_digits == 0
    assert Currency.JPY.decimal_digits == 0

    JPY2 = get_currency("JPY")
    assert JPY2 == "JPY"
    assert JPY == JPY2
    assert JPY2.decimal_digits == 0

    IQD2 = get_currency("IQD")
    assert IQD2.decimal_digits == 3

    BABA = get_currency("BABA")
    assert BABA.ticker == "BABA"
    assert BABA.decimal_digits == 2

    assert USD.decimal_digits == 2
    assert Currency.USD.decimal_digits == 2

    assert USD is Currency.USD
    assert USD is not Currency.SEK
    assert USD is not Currency("USD")
    assert Currency("USD") is not Currency("USD")
    assert USD == Currency.USD
    assert USD != Currency.SEK
    assert Currency.USD == "USD"
    assert Currency.USD.as_string() == "USD"
    assert Currency.USD.as_str() == "USD"

    m = Money(57167, JPY)
    assert f"{m}" == "57167 JPY"
    assert m.as_string(max_decimals=5) == "57167 JPY"
    assert m.as_string(min_decimals=4, max_decimals=5) == "57167.0000 JPY"

    m = Money(57167, USD)
    assert f"{m}" == "57167.00 USD"
    assert m.as_string(max_decimals=5) == "57167.00 USD"
    assert m.as_string(min_decimals=4, max_decimals=5) == "57167.0000 USD"

    m = Money(57167, IQD)
    assert f"{m}" == "57167.000 IQD"
    assert m.as_string(min_decimals=2) == "57167.00 IQD"
    assert m.as_string(max_decimals=5) == "57167.000 IQD"

    m = Money("0.445", CLF)
    assert f"{m}" == "0.4450 CLF"
    assert m.as_string(min_decimals=2) == "0.445 CLF"
    assert m.as_string(max_decimals=3) == "0.445 CLF"
    assert m.as_string(max_decimals=2) == "0.45 CLF"
    assert m.as_string(max_decimals=5) == "0.4450 CLF"

    m1 = Money("0.30285471", Bitcoin)
    m2 = Money("0.30285471", XBT)
    m3 = Money("0.30285471", Ethereum)
    assert m1 == m2
    assert m1 != m3
    assert f"{m1}" == "0.30285471 BTC"
    assert f"{m2}" == "0.30285471 BTC"

    m = Money(4711, Currency.SEK, from_sub_units=True)
    assert m == "47.11"
    assert m.sub_units == 4711
    m = Money(4711, Currency.SEK, from_sub_units=False)
    assert m == 4711
    assert m.sub_units == 471100
    assert str(Money.from_sub_units(1000, Currency.SEK)) == "10.00 SEK"

    m = Money(1000, Currency.JPY, from_sub_units=True)
    assert m == 1000
    assert m.sub_units == 1000
    m = Money(1000, Currency.JPY, from_sub_units=False)
    assert m == 1000
    assert m.sub_units == 1000
    assert str(Money.from_sub_units(1000, Currency.JPY)) == "1000 JPY"

    m = Money(1000, Currency.IQD, from_sub_units=True)
    assert m == 1
    assert m.sub_units == 1000
    m = Money(1000, Currency.IQD, from_sub_units=False)
    assert m == 1000
    assert m.sub_units == 1000000

    m = Money(1000, Currency.CLF, from_sub_units=True)
    assert m == Money("0.1")
    assert m.sub_units == 1000
    m = Money(1000, Currency.CLF, from_sub_units=False)
    assert m == 1000
    assert m.sub_units == 10000000
    assert str(Money.from_sub_units(4711, Currency.CLF)) == "0.4711 CLF"

    assert str(Money.from_sub_units(471100)) == "4711.00"
    assert str(Money.from_sub_units(4711)) == "47.11"
    assert str(Money.from_sub_units(4711, "XXX")) == "47.11 XXX"
    assert Money.from_sub_units(4711).sub_units == 4711
    assert Money.from_sub_units(4711, "XXX").sub_units == 4711
    assert Money("1").sub_units == 100
    assert Money("0.1").sub_units == 10
    assert Money("0.01").sub_units == 1
    assert Money("0.001").sub_units == Decimal("0.1")

    assert str(Money("0.01").sub_units) == "1"
    assert str(Money("0.01", currency="SEK").sub_units) == "1"
    assert str(Money("100.50", currency="SEK").sub_units) == "10050"
    assert "." in str(Money("100.10", Currency.JPY).sub_units)
    assert str(round(Money("100.10", Currency.JPY).sub_units)) == "100"

    assert Money("1", Currency.JPY).sub_units == 1
    assert Money("0.1", Currency.JPY).sub_units == Decimal("0.1")
    assert Money("0.01", Currency.JPY).sub_units == Decimal("0.01")
    assert Money("0.001", Currency.JPY).sub_units == Decimal("0.001")

    assert Money("1", Currency.SEK, from_sub_units=True).sub_units == 1
    assert Money("133742", Currency.SEK, from_sub_units=True).sub_units == 133742

    assert str(Money.from_sub_units(Money("133742", Currency.SEK, from_sub_units=True).to_sub_units())) == "1337.42 SEK"


def test_currency_to_money():
    currency = Currency("NEW")

    assert str(currency.money(100)) == "100.00 NEW"
    assert str(Currency.SEK.money(100)) == "100.00 SEK"
    assert str(Currency.JPY.money(100)) == "100 JPY"
    assert str(JPY.money(100)) == "100 JPY"
    assert str(stockholm.currency.Bitcoin.money("1.523")) == "1.523 BTC"


def test_currency_constructors():
    currency = Currency("NEW")
    assert currency
    assert currency.ticker == "NEW"

    with pytest.raises(TypeError):
        currency("NEW")

    with pytest.raises(TypeError):
        Currency.SEK("NEW")

    with pytest.raises(TypeError):
        JPY("NEW")


def test_dogecoin():
    class CustomDoge(BaseCurrency):
        ticker = "DOGE"

    assert Money("1 DOGE") == Money("1 DOGE")

    assert Money(1, DogeCoin) == Money(1, DogeCoin)
    assert Money(1, DOGE) == Money(1, DOGE)
    assert Money(1, "DOGE") == Money(1, "DOGE")
    assert Money(1, DOGE) == Money(1, "DOGE")
    assert Money(1, DogeCoin) == Money(1, DOGE)
    assert Money(1, DogeCoin) == Money(1, CustomDoge)
    assert Money(1, "DOGE") == Money(1, CustomDoge)
    assert Money(1, CustomDoge) == Money(1, DOGE)
