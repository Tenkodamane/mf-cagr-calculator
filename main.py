import logging
from statistics import mean
import pandas
import matplotlib.pyplot as plt
import math
import argparse
import os

from src.mf_performance import MFPerformance


parser = argparse.ArgumentParser(description='MF Portfolio Generator')
parser.add_argument('--inputXl', dest='inputXl', required=True,
                    help='input xl file absolute path, Example: --inputXl data.xlsx')
parser.add_argument('--configFile', dest='configFile', required=True,
                    help='configFile absolute path, Example: --configFile config.json')
parser.add_argument('--outputFile', dest='outputFile', required=True,
                    help='output xl file absolute path. Example: --outputFileName output.xlsx')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


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


def drawTimeLineGraph(xSeries, ySeries, title, xlable, ylable, dir, fileName):
    x = xSeries
    y = ySeries
    plt.plot(x, y)
    plt.xlabel("%s" % xlable)
    plt.ylabel("%s" % ylable)
    plt.title("%s" % title)
    plt.savefig(os.path.join(dir, fileName), bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    args = parser.parse_args()
    if not os.path.exists("out"):
        os.mkdir("out")
    mfObj = MFPerformance(xlFile=args.inputXl, cfgFile=args.configFile)
    xlData, sheets = mfObj.getXlDataAndSheetNames()
    if xlData and sheets:
        logging.info('Reading XL File %s:' % args.inputXl + '\u2713')
    else:
        raise Exception('Reading XL File:%s Failed' % args.inputXl)
    cagrDict = {sheet: {} for sheet in sheets}
    summary = {"Portfolio Name": [], "First Invested Date": [], "Last Invested Date": [], "CAGR Percentage": []}
    for sheet in sheets:
        logging.info("Calculating CAGR for %s:" % sheet + '\u2713')
        mfData = mfObj.getDataFromSheet(xlData, sheet)
        cagrData = mfObj.calcuLateCAGR(mfData)
        cagrDict[sheet] = cagrData
        summary["Portfolio Name"].append(sheet)
        summary["First Invested Date"].append(cagrData[mfObj.investedDate][-1])
        summary["Last Invested Date"].append(cagrData[mfObj.investedDate][0])
        summary["CAGR Percentage"].append(mean(cagrData["cagr_perc"]))
    logging.info("Generating Summary:" + '\u2713')
    logging.info("Writing the output file:%s" % args.outputFile + '\u2713')
    writer = pandas.ExcelWriter(os.path.join("out", args.outputFile), engine='xlsxwriter')
    dataFrame = pandas.DataFrame(summary)
    dataFrame.to_excel(writer, sheet_name="Summary")
    for key, _ in cagrDict.items():
        dataFrame = pandas.DataFrame(cagrDict[key])
        dataFrame.to_excel(writer, sheet_name=key)
    writer.save()
    logging.info("Drawing Graphs:" + '\u2713')
    drawSummaryBarGraph(xSeries=summary["Portfolio Name"], ySeries=summary["CAGR Percentage"],
                        title="Portfolio Performance", xlable="CAGR in %", dir="out", fileName="MF_Performance.png")
    for key, value in cagrDict.items():
        drawTimeLineGraph(xSeries=value[mfObj.age], ySeries=value["cagr_perc"], title=key, xlable="Days", dir="out",
                          fileName="%s_Performance.png" % key, ylable="CAGR in %")
