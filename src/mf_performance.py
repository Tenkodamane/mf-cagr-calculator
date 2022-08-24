import pandas
import os
import json


class MFPerformance:

    def __init__(self, xlFile, cfgFile):
        if not os.path.exists(xlFile):
            raise Exception("Could not find the input file: %s" % xlFile)
        self.xlFile = xlFile
        if not os.path.exists(cfgFile):
            raise Exception("Could not find the input file: %s" % cfgFile)
        self.stdKeys = self.parseCfgFile(cfgFile)["column_headings"]

    @property
    def investedDate(self):
        return self.stdKeys["invested_date"]

    @property
    def price(self):
        return self.stdKeys["price"]

    @property
    def qty(self):
        return self.stdKeys["qty"]

    @property
    def age(self):
        return self.stdKeys["age"]

    @property
    def profit(self):
        return self.stdKeys["profit"]

    def parseCfgFile(self, cfgFile):
        with open(cfgFile, "r") as fp:
            cfgData = json.loads(fp.read())
        return cfgData

    def getXlDataAndSheetNames(self):
        """Returns xlData of all sheets and sheet names"""
        xlData = pandas.ExcelFile(self.xlFile)
        return xlData, xlData.sheet_names

    def getDataFromSheet(self, data, sheet):
        """Returns data of a sheet
        Args:
            data: xl data from getXlDataAndSheetNames
            sheet: sheet name
        """
        df = pandas.read_excel(data, [sheet])
        data = df[sheet]
        return data[data['invested_date'].notna()]

    def calcuLateCAGR(self, data):
        """Calculates CAGR for a portfolio
        Args:
            data: Parsed excel data, Ex: return of getDataFromSheet
        Returns: Dictionary with CAGR calculated for each SIP/Investment
        """
        outDict = {key: [] for key in data.keys()}
        outDict["invetsed_amount"] = []
        outDict["current_amount"] = []
        outDict["years_invested"] = []
        outDict["cagr_perc"] = []
        for i in data[self.qty].index:
            investedAmt = float(data[self.qty][i]) * float(data[self.price][i])
            currentAmt = investedAmt + float(data[self.profit][i])
            yearsInvested = int(data[self.age][i]) / 365
            cagrPerc = ((currentAmt / investedAmt) ** (1 / yearsInvested) - 1) * 100
            outDict[self.investedDate].append(data[self.investedDate][i])
            outDict[self.qty].append(data[self.qty][i])
            outDict[self.price].append(data[self.price][i])
            outDict[self.age].append(data[self.age][i])
            outDict[self.profit].append(data[self.profit][i])
            outDict["invetsed_amount"].append(investedAmt)
            outDict["current_amount"].append(currentAmt)
            outDict["years_invested"].append(yearsInvested)
            outDict["cagr_perc"].append(cagrPerc)
        return outDict

