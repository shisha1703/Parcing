import requests
import asyncio
import xml.etree.ElementTree as ET

class Task9:

    async def Run(self):
        bankApiUri = "https://www.cbr.ru/scripts/XML_daily.asp"

        currencyService = CurrencyService(bankApiUri)

        currencyCode = input("Введите код валюты (например, USD) или нажмите Enter для выхода: ") or ""

        currencyRate = await currencyService.GetCurrencyRateAsync(currencyCode)

        if currencyRate is not None:
            print(f"{currencyRate.Name} : {currencyRate.Nominal} {currencyRate.CharCode} = {currencyRate.Value} RUB")
        else:
            print("Валюта не найдена")


class CurrencyService:
    def __init__(self, bankApiUri):
        self._bankApiUri = bankApiUri

    async def GetCurrencyRateAsync(self, currencyCode):
        xmlData = await self.GetXmlDataAsync()
        return next(
            (currencyRate for currencyRate in xmlData.Valutes if currencyRate.CharCode.lower() == currencyCode.lower()),
            None)

    async def GetXmlDataAsync(self):
        response = requests.get(self._bankApiUri)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        valutes = []
        for valuteElem in root.findall("Valute"):
            valute = Valute()
            valute.ID = valuteElem.get("ID")
            valute.NumCode = valuteElem.find("NumCode").text
            valute.CharCode = valuteElem.find("CharCode").text
            valute.Nominal = valuteElem.find("Nominal").text
            valute.Name = valuteElem.find("Name").text
            valute.Value = valuteElem.find("Value").text
            valute.VunitRate = valuteElem.find("VunitRate").text
            valutes.append(valute)
        return ValCurs(root.get("Date"), root.get("name"), valutes)


class ValCurs:
    def __init__(self, Date, Name, Valutes):
        self.Date = Date
        self.Name = Name
        self.Valutes = Valutes


class Valute:
    def __init__(self):
        self.ID = ""
        self.NumCode = ""
        self.CharCode = ""
        self.Nominal = ""
        self.Name = ""
        self.Value = ""
        self.VunitRate = ""


tsk = Task9()

asyncio.run(tsk.Run())
