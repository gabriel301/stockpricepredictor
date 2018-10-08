# -*- coding: utf-8 -*-
from Util import Util
import argparse
import pandas as pd
from TechinalIndicators import TechnicalIndicators
from Util import Util
from StockHistoricalDataDownloader import StockHistoricalDataDownloader
from Model import Model
import os


def main():
    
    epilog = "Sample Usage: --models"
    parser = argparse.ArgumentParser(description='Train a batch of models and outputs benchmarks',
                                     epilog=epilog, add_help=True)

    parser.add_argument('-m','--models', help='List of Model Names separeted by commas.',
                                const='Linear,Ridge,Huber,Lasso,ElasticNet,RandomForests',
                                default='Linear,Ridge,Huber,Lasso,ElasticNet,RandomForests',
                                action='store',
                                nargs='?')
    parser.add_argument('-i','--inputfolder', help='Training Data Folder',
                                const='default',
                                default='default',
                                action='store',
                                nargs='?')
    parser.add_argument('-o','--outputfolder', help='Folder for generated files'
                                ,const='default',
                                default='default',
                                action='store',
                                nargs='?')
    parser.add_argument('-n','--normalization', help='Normalization Method for the price. Type proportion for the first Price start from 1 and future prices be proportional or log for take logarithm from values'
                                ,const='log',
                                default='log',
                                action='store',
                                nargs='?')

    parser.add_argument('-d','--days', help='List of Days Ahead Model will predict after training, separeted by commas')
    

    args=parser.parse_args()

    if args.models == None:
        print "There are no models to train"
        return
    models = str(args.models).split(",")

    availableModels = ['Linear', 'ElasticNet', 'Ridge', 'Huber', 'Lasso','RandomForests']

    unsupportedModels = [x for x in models if x not in availableModels]

    if not len(unsupportedModels) == 0:
        print "Following models are not supported: {} Suppoted models: {}".format(','.join(unsupportedModels),', '.join(models))
        if len(unsupportedModels) == len(availableModels):
            print "Finishing Execution"
            return
    modelsToTrain = [x for x in models if x in availableModels]

    
    rootPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if args.inputfolder == 'default':
        args.inputfolder = os.path.join(rootPath,"Report/")
    if args.outputfolder == 'default':   
        args.outputfolder = os.path.join(rootPath,"Report/")

    if(args.days == None):
         intervals = [1,7,15,30,60,120]
    else:
        intervals = int(str(args.days).split(","))
    
    if not Util().FolderExists(args.inputfolder):
        print "Folder {} does not exist".format(args.inputfolder)
        return
   
    Util().CreateFolder(args.outputfolder)

    quotesFolder = StockHistoricalDataDownloader().GetCleanDataframe(args.inputfolder,args.outputfolder)
    normalizedFolder = StockHistoricalDataDownloader().GetNormalizedDataframe(quotesFolder,args.outputfolder,args.normalization)
    files = Util().GetFilesFromFolder(normalizedFolder,'csv')
    dfs = []
    for file in files:
        df = pd.read_csv(file)
        print "Calculating Techinical Indicators for file {}".format(file)
        dfIndicator  = TechnicalIndicators().GetIndicatorsFromDF(df.copy(),args.outputfolder,True,True)
        dfs.append(dfIndicator.copy())

    for dataframe in dfs:
        for interval in intervals:
            Model().GetBestEstimatorsShiftStrategy(dataframe.copy(),interval,os.path.join(args.outputfolder,'Data/Indicators and Normalized Prices'),True,False,modelsToTrain,args.normalization)
            Model().GetBestEstimatorsShiftStrategy(dataframe.copy(),interval,os.path.join(args.outputfolder,'Data/Only Normalized Indicators'),True,True,modelsToTrain,args.normalization)
    


if  __name__ =='__main__': main() 
