
import sys
sys.path.append('../../../src')
from saf_reader import SafReader, SafHisto
import pldoc
import argparse

parser = argparse.ArgumentParser(description = '@lemouth Exercise 1c histogram generator')
parser.add_argument('-i',
                    '--input',
                    help = 'The input SAF file',
                    metavar = 'saf_file',
                    required = True)
parser.add_argument('-o',
                    '--output',
                    help = 'The output file. Format is identified by suffix (e.g .png, .pdf, .tiff, etc)',
                    metavar = 'SAF FILE',
                    required = True)

args = parser.parse_args()

reader = SafReader(args.input)

i = 0
xaxis_labels = ('pT', 'pT', r'$\eta$', r'$\eta$')
fig = pldoc.PlFigure(nrows = 2, ncols = 2)
for histo in reader.GetHistos() :
    fig.AddBarChart(histo, xaxis_labels[i])
    i += 1

fig.save(args.output)

