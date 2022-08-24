import pandas
import os
import json
import matplotlib.pyplot as plt
import math
import logging
from statistics import mean

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class MFPerformance:

    def __init__(self, xlFile, cfgFile):
        self.xlFile = xlFile
        self.stdKeys = self.parseCfgFile(cfgFile)["column_headings"]
        self.sheets = []
        self.xlData = None
        self.setXlDataAndSheetNames()

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

    def setXlDataAndSheetNames(self):
        """Returns xlData of all sheets and sheet names"""
        self.xlData = pandas.ExcelFile(self.xlFile)
        self.sheets = self.xlData.sheet_names
        if self.xlData and self.sheets:
            logging.info('Reading XL File %s:' % self.xlFile + '\u2713')
        else:
            raise Exception('Reading XL File:%s Failed' % self.xlFile)

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

    @staticmethod
    def drawSummaryBarGraph(xSeries, ySeries, title, xlable, dir, fileName):
        x = xSeries
        y = ySeries
        plt.barh(x, y)
        for index, value in enumerate(y):
            plt.text(value, index,
                     str(math.floor(value)))
        plt.title("%s" % title, fontsize=20)
        plt.xlabel('%s' % xlable, fontsize=16)
        plt.savefig(os.path.join(dir, fileName), bbox_inches='tight')
        plt.close()

    @staticmethod
    def drawTimeLineGraph(xSeries, ySeries, title, xlable, ylable, dir, fileName):
        x = xSeries
        y = ySeries
        plt.plot(x, y)
        plt.xlabel("%s" % xlable)
        plt.ylabel("%s" % ylable)
        plt.title("%s" % title)
        plt.savefig(os.path.join(dir, fileName), bbox_inches='tight')
        plt.close()

    def prepareCAGRSummary(self, outputFile, outDir):
        """Prepares the CAGR summary of all the sheets"""
        cagrDict = {sheet: {} for sheet in self.sheets}
        summary = {"Portfolio Name": [], "First Invested Date": [], "Last Invested Date": [], "CAGR Percentage": []}
        for sheet in self.sheets:
            logging.info("Calculating CAGR for %s:" % sheet + '\u2713')
            mfData = self.getDataFromSheet(self.xlData, sheet)
            cagrData = self.calcuLateCAGR(mfData)
            cagrDict[sheet] = cagrData
            summary["Portfolio Name"].append(sheet)
            summary["First Invested Date"].append(cagrData[self.investedDate][-1])
            summary["Last Invested Date"].append(cagrData[self.investedDate][0])
            summary["CAGR Percentage"].append(mean(cagrData["cagr_perc"]))
        logging.info("Generating Summary:" + '\u2713')
        logging.info("Writing the output file:%s:" % os.path.join(outDir, outputFile) + '\u2713')
        writer = pandas.ExcelWriter(os.path.join(outDir, outputFile), engine='xlsxwriter')
        dataFrame = pandas.DataFrame(summary)
        dataFrame.to_excel(writer, sheet_name="Summary")
        for key, _ in cagrDict.items():
            dataFrame = pandas.DataFrame(cagrDict[key])
            dataFrame.to_excel(writer, sheet_name=key)
        writer.save()
        logging.info("Drawing Graphs:" + '\u2713')
        self.drawSummaryBarGraph(xSeries=summary["Portfolio Name"], ySeries=summary["CAGR Percentage"],
                            title="Portfolio Performance", xlable="CAGR in %", dir=outDir, fileName="MF_Performance.png")
        for key, value in cagrDict.items():
            self.drawTimeLineGraph(xSeries=value[self.age], ySeries=value["cagr_perc"], title=key, xlable="Days", dir=outDir,
                              fileName="%s_Performance.png" % key, ylable="CAGR in %")
