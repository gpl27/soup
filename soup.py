from kiwi.defaults import JSONReporter
from soupsolver.soupreporter import SoupReporter

report = JSONReporter.load("report-1721558169268958112.json")
SoupReporter.generate(report)

