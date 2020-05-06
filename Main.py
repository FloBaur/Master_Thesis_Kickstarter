from Filter import Filter
from Algorithm import Algorithm

# Daten holen
DataFilter = Filter()

# Ziehen der gewünschten Daten aus CSV

data = DataFilter.cleanColumns()

# Filtern der Daten anhand von Kriterien

cleanedData = DataFilter.filterCriteria(data)

stop = None

# schreiben der Daten in neue CSV

DataFilter.overViewCleanedData(cleanedData)

#Übergabe der Daten an den Deep Learning Algorithmus für die Auswertung

Algorithm = Algorithm()

Algorithm.computerVision(cleanedData)







