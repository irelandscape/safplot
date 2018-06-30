import xml_as_dict.xml_as_dict as xml_as_dict
import xml.etree.ElementTree as ET

# A class to hold information about a single Histogram stored
# in SAF file.
class SafHisto :
    # histo is a dictionary conversion of the SAF XML
    def __init__ (self, histo) :
        self.histo = histo

    def Title (self) :
        description = self.histo['Description']
        # Parse the description to retrieve title
        elems = description.split('"')
        if len(elems) > 1 :
            return elems[1]
        else :
            return ''

    # Return xmin, xmax
    def Range (self) :
        description = self.histo['Description']
        # Parse the description to retrieve xmin and xmax
        pos = description.find('nbins')
        pos += description[pos:].find('\n') + 1
        fields = description[pos:].split()
        return float(fields[1]), float(fields[2])


    # Return all bin data
    def Bins (self) :
        underflow = 0.0
        overflow = 0.0
        data = self.histo['Data']
        bins = []

        for row in data.split('\n') :
            if len(row.strip()) == 0 :
                continue
            cols = [ float(x) for x in row.split()[:2] ]
            bins.append(cols[0] - cols[1])

        return bins

class SafReader () :

    def __init__ (self, file) :
        with open(file) as f :
            # Store all histograms in a list
            self.histos = [ SafHisto(x) for x in self._GetHistos(f.read()) ]
        f.close()

    # Extract all histograms from the SAF XML
    # Each histogram is stored as a Python dictionary corresponding to 
    # The <Histo></Histo> section of the XML.
    def _GetHistos (self, string) :
        histos = []

        start = 0
        while True :
            start = string.find('<Histo>', start)
            if start == -1 :
                break
            end = string.find('</Histo>', start + 1)
            if end == -1 :
                break

            end += len('</Histo>')

            root = ET.fromstring(string[start : end])
            histos.append(xml_as_dict.XmlDictConfig(root))

            start = end + 1

        return histos


    def GetHistos (self) :
        return self.histos

