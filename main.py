import logging
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

if __name__ == "__main__":
    args = parser.parse_args()
    if not os.path.exists("out"):
        os.mkdir("out")
    if not os.path.exists(args.configFile):
        raise FileNotFoundError("Could not find the input file: %s" % args.configFile)
    if not os.path.exists(args.inputXl):
        raise FileNotFoundError("Could not find the xl file: %s" % args.inputXl)
    mfObj = MFPerformance(xlFile=args.inputXl, cfgFile=args.configFile)
    mfObj.prepareCAGRSummary(outputFile="MF_Performance.xlsx", outDir="out")
