from datetime import datetime
from numpy import nan, zeros
import matplotlib.pyplot as plt
import matplotlib.colors
import argparse

parser = argparse.ArgumentParser(description="Plot SVGS Z position vs time from 'Logcat' data obtained. Lines from Logcat need to be copied to a document. The lines in the document must be in the format: '2022-03-21 16:43:01.373 23512-22667/gov.nasa.svgs D/LoggerPlot: Z-Distance,Mt_mode,TGT_mode,StateResult.status,hueBeingUsed'.")
parser.add_argument("--fileName",required=True,help="Path and name to the file containing the data")
parser.add_argument("--plotTitle",default="SVGS Test",required=False,help="String that will be the title of the plot. For mathematical expressions: https://matplotlib.org/stable/tutorials/text/mathtext.html")
args = parser.parse_args()

class DataSet:
	def __init__(self, filePath):
		self.filePath = filePath
		self.parseData()
		
	def parseData(self):
		with open(self.filePath) as f:
			self.fullDataLines = f.readlines()
		self.length = len(self.fullDataLines)
		self.z = zeros(self.length)
		self.hue = zeros(self.length)
		self.timeStamp = zeros(self.length)
		firstTimeStamp = datetime.strptime(" ".join(self.fullDataLines[0].split(",")[0].split(" ")[0:2]),"%Y-%m-%d %H:%M:%S.%f")
		for i, line in enumerate(self.fullDataLines):
			splitData = line.split(",")
			self.z[i] = abs(float(splitData[-5].split(" ")[-1]))
			self.hue[i] = splitData[-1]
			self.timeStamp[i] = (datetime.strptime(" ".join(splitData[0].split(" ")[0:2]),"%Y-%m-%d %H:%M:%S.%f")-firstTimeStamp).total_seconds()
	
	def plotPositionVsTime(self, plotTitle):
		zeroData = self.z.copy()
		nonZeroData = self.z.copy()
		zeroData[zeroData > 0] = nan
		nonZeroData[nonZeroData == 0] = nan
		plt.figure(1, figsize=[20,11.5], tight_layout=True)
		plt.plot(self.timeStamp, self.z, color='k', linewidth=1.5, label="_Hidden label")
		plt.plot(self.timeStamp, zeroData, color='k', linewidth=1.5, marker='.', markersize=2, label="Zero Data Points")
		plt.plot(self.timeStamp, nonZeroData, color='b', linewidth=2.5, marker='.', label="Non-Zero Data Points")
		for i in range(1,self.length):
			plt.plot(self.timeStamp[i], self.z[i], color=matplotlib.colors.hsv_to_rgb([self.hue[i]/360,1,1]), marker='o', markersize=8, label="_Hidden label")
		plt.title(plotTitle, fontsize=25)
		plt.xlabel("Time (s)", fontsize=17)
		plt.ylabel("Z-Position (m)", fontsize=17)
		plt.legend(loc="best", fontsize=17)
		plt.show()

dataSet = DataSet(args.fileName)
dataSet.plotPositionVsTime(args.plotTitle)
