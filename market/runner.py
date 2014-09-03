import sys
import csvparser

if len (sys.argv) != 2:
    print ("Invalid command line args")
else:
    de = csvparser.DataExtractor(sys.argv[1])
    '''
    totalDeposits = de.sumActivityTypeValues(sys.argv[1], "ActivityType", "Deposits", "NetAmount")

    print ("Total deposits:\n%.2f" % totalDeposits)

    cumulativeGainOrLoss = de.sumActivityTypeValues(sys.argv[1], "ActivityType", "Trades", "NetAmount")

    print ("Cumulative Gain (Loss) from trades:")
    
    if (cumulativeGainOrLoss >= 0):
        print ("%.2f" % cumulativeGainOrLoss)
    else:
        print ("(%.2f)" % cumulativeGainOrLoss)
    
    cumulativeGainOrLoss = de.sumActivityTypeValues(sys.argv[1], "SettlementDate", "07/06/2012 12:00:00 AM", "NetAmount")
    print ("%.2f" % cumulativeGainOrLoss)

    de.convertNVP2IVP({"Symbol":"BB.TO"})
    result = de.extractRecords({"Symbol":"BB.TO", "Action":"Buy", "ActivityType":"Trades"})
    '''
    
    de.calculateTradesPerformance({"ActivityType":"Trades"}, "Symbol", "NetAmount")
