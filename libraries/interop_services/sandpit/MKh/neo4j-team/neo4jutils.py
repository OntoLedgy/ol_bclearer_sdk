import csv
import threading
import time
import math
import sys
from collections import deque
import pandas as pd

def synchronized(func):

    func.__lock__ = threading.Lock()

    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)

    return synced_func

def showdf(df):
    df.set_index(df.columns[0], inplace=True)
    try:
        display(df)
    except Exception as e:
        print(df)

def makeEmptyNull(aRow):
    for key in aRow.keys():
        if aRow[key] is not None and type(aRow[key]) == str and aRow[key] == "":
            aRow[key] = None
    return aRow

class Neo4jLoader (threading.Thread) :
    
    def __init__(
            self, 
            threadID, 
            name, 
            session, 
            cypherQuery, 
            batchSize, 
            out, 
            debug, 
            maxQueueSize=10000):
        
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.queue = deque()
        self.batchSize = batchSize
        self.rows = []
        self.nodesCreated = 0
        self.labelsCreated = 0
        self.relationshipsCreated = 0
        self.propertiesSet = 0
        self.query = cypherQuery
        self.session = session
        self.pcnt = 0
        self.debug = debug
        self.ListenQueue = True
        self.line_count = 0
        self.out = out
        self.maxQueueSize = maxQueueSize
        self.waited = False
        self.batchKeyName = "batch"
        # print(f".Neo4jLoader __init__  id queue object: {id(queue)}")
    
    def addRow(self, row):
        if row is not None:
            while len(self.queue) >= self.maxQueueSize:
                self.waited = True
                time.sleep(0.001)
                
            self.queue.append(row); 
            
    def run(self):
        print ("starting loader :" + self.name)
        self.line_count = 0
        # loop and check if there are things on the queue
        try:
            while True:
                if (len(self.queue) > 0):
                    row = self.queue.popleft();
                    self.rows.append(row)
                    if self.line_count > 1:
                        if len(self.rows) >= self.batchSize:
                            result = self.session.run(self.query, { self.batchKeyName : self.rows})
                            cntr = result.consume().counters
                            self.out.prt(str(self.threadID), self.waited)
                            self.waited = False;
                            self.labelsCreated += cntr.labels_added
                            self.nodesCreated += cntr.nodes_created
                            self.propertiesSet += cntr.properties_set
                            self.relationshipsCreated += cntr.relationships_created
                            self.pcnt = self.pcnt + len(self.rows)
                            self.rows = []
                    self.line_count += 1
                else:
                    time.sleep(0.5)
                
                
                
                if self.ListenQueue == False and len(self.queue) == 0:
                    # self.out.prtln(f"\n stop listening to queue in loader {self.name}" )
                    break
            if len(self.rows) > 0:         
                result = self.session.run(self.query, {self.batchKeyName: self.rows});
                cntr = result.consume().counters
                self.labelsCreated += cntr.labels_added
                self.nodesCreated += cntr.nodes_created
                self.propertiesSet += cntr.properties_set
                self.relationshipsCreated += cntr.relationships_created
                self.pcnt = self.pcnt + len(self.rows)
                self.rows = []

                
        except KeyboardInterrupt:
            print(f"loader {self.threadID} Cancelled after crtl-c")
            sys.exit()    
        except Exception as e:
            print(f" last batch unexpected error one line {self.line_count}" )
            print(type(e)) 
            print(e.args)
            print(len(self.rows))
            with open('batchrows.txt', 'w') as f:
                for line in self.rows:
                    f.write(f"{line}")
                    f.write('\n')
            raise
        
        
    def finish(self):
        # print ("csv finished signal for loader :" + self.name )
        self.ListenQueue = False

class ProgressOutput():
    def __init__(self, batchSize):
        self.batchSize = batchSize
        self.counter = 0
        self.points = 0
        self.mod = 40
        # print("ProgressOutput created")
    
    @synchronized
    def prt(self, s, waited=False):
        self.counter += self.batchSize
        self.points += 1
        prefix = "+";
        if waited:
            prefix = "|"
        if (self.points == self.mod) :
            print(prefix + s + " (" + str(self.counter) + ")")
            self.points = 0
        else:
            print(prefix + s,end=' ')
            sys.stdout.flush()

    def finished(self, cntr):
        print(" finished (" + str(cntr) + ")") 

def run_cypher(
        session, 
        query, 
        params={},
        output="all"):

    if not output in ['all','none','summary']:
        print("ERROR: output parameter must have one of the follwing values :'all','none','summary' ")
        return
        
    bShowSummary = True
    bShowData = True
    if output != "all":
        bShowData = False

    if output == 'none':
        bShowSummary = False
        
    qq = query.strip()
    if len(qq) > 50 :
        qq = qq[0:76].replace("\n", "") + "..."

    if bShowSummary:
        print(f"run_cypher : {qq}")
    result = session.run(query.strip(), params)
    df = pd.DataFrame([r.values() for r in result], columns=result.keys())
    summary = result.consume() 
    
    if df.size > 0:
        if bShowSummary:
            print("Results available after " + str(summary.result_available_after) + "ms, finished query after " + str(summary.result_consumed_after) + "ms") 
    
    cntr = summary.counters
    
    df2 = pd.DataFrame(columns=['counter','value'])
    
    show = True
    if cntr.nodes_created > 0:
        df2.loc[len(df2.index)] = ["nodes created",cntr.nodes_created]
    if cntr.nodes_deleted > 0:
        df2.loc[len(df2.index)] = ["nodes deleted", cntr.nodes_deleted ]
    if cntr.relationships_created > 0:
        df2.loc[len(df2.index)] = ["relationships created",cntr.relationships_created ]
    if cntr.relationships_deleted > 0:
        df2.loc[len(df2.index)] = ["relationships deleted", cntr.relationships_deleted ]
    if cntr.properties_set > 0:
        df2.loc[len(df2.index)] = ["properties set", cntr.properties_set ]
    if cntr.labels_added > 0:
        df2.loc[len(df2.index)] = ["labels added", cntr.labels_added ]
    if cntr.labels_removed > 0:
        df2.loc[len(df2.index)] = ["labels removed", cntr.labels_removed ]
    if cntr.indexes_added > 0:
        df2.loc[len(df2.index)] = ["indexes added", cntr.indexes_added ]
    if cntr.indexes_removed > 0:
        df2.loc[len(df2.index)] = ["indexes removed", cntr.indexes_removed ]
    if cntr.constraints_added > 0:
        df2.loc[len(df2.index)] = ["constraints added", cntr.constraints_added ]
    if cntr.constraints_removed > 0:
        df2.loc[len(df2.index)] = ["constraints removed",cntr.constraints_removed ]
    if cntr.system_updates > 0:
        df2.loc[len(df2.index)] = ["system updates", cntr.system_updates ]
    if bShowData:
        if df.size > 0:
            showdf(df)
            show = False

    if bShowSummary:
        if df2.size > 0:
            showdf(df2)
            show = False
            
        if show:
            print("(no changes, no records)")

def loadmysqltoneo4j(
        SQLconnection,
        SQLQuery, 
        aDriver, 
        aDBName, 
        neo4jQuery, 
        aBatchSize,
        concurrency=1, 
        debug=False):
    print(f"                        concurrency: {concurrency}")
    print(f"                         batch size: {aBatchSize}")
    print(f"loadmysqltoneo4j started connection:{SQLconnection}");
    if debug:
        print(f"                           SQLQuery: {SQLQuery}")    
    if debug:
        print(f"                             cypher: {neo4jQuery}")
    print(f"                     neo4j database: {aDBName}")
    print(f"                      neo4j address: {aDriver.get_server_info().address}")
    
    nodesCreated = 0
    labelsCreated = 0
    relationshipsCreated = 0
    propertiesSet = 0
    tStart = time.perf_counter_ns()
    neo4jLoadThreads = []
    out = ProgressOutput(aBatchSize)
    rows = []
    pcnt = 0
    cursor = SQLconnection.cursor(dictionary=True)
    cursor.execute(SQLQuery)
    row_count = 0
    threadIndex = 0
    maxC = concurrency -1;
    maxQueueSize = 10 * aBatchSize;    
    for row in cursor:
        if row_count == 0:
            # initialise loaders
            for i in range(concurrency):
                thr = Neo4jLoader(i,"neo4j loader " + str(i), aDriver.session(database=aDBName),neo4jQuery,aBatchSize, out, debug, maxQueueSize)
                neo4jLoadThreads.append(thr)
                thr.start()
        
        # now adding the rows to the loaders
        if (pcnt == 0):
            if debug:
                print("First rdbms row:")
                print(row)
            print("---------------------------")
        pcnt += 1
        neo4jLoadThreads[threadIndex].addRow(row)
        if (concurrency > 1):
            if (threadIndex < maxC):
                threadIndex += 1
            elif (threadIndex == maxC ):
                threadIndex = 0
        row_count += 1
        
    for loader in neo4jLoadThreads:
        loader.finish()
        loader.join()
        labelsCreated += loader.labelsCreated
        nodesCreated += loader.nodesCreated
        propertiesSet += loader.propertiesSet
        relationshipsCreated += loader.relationshipsCreated

    # reporting duration result is an integer (milliseconds) due to the usage of //
    duration = (time.perf_counter_ns() - tStart) // 1000000
    if duration == 0:
        duration = 1
    nplusr = nodesCreated + relationshipsCreated
    nrPerSecond = math.floor(((nodesCreated + relationshipsCreated) / duration) * 1000)
    out.finished(str(pcnt))
    if debug:
        print(f' labelsCreated: {labelsCreated}, nodesCreated: {nodesCreated}, propertiesSet: {propertiesSet}, relationshipsCreated: {relationshipsCreated}')

    print(f'\n Processed {row_count} data rows in {duration} ms. Created nodes/relationships per second {nrPerSecond}.')

def loadcsvtoneo4j(
        aCSV, 
        aDriver, 
        aDBName, 
        aQuery, 
        aBatchSize,
        concurrency=1,
        aDelimiter=',', 
        aQuotechar='"',
        aEncoding='utf-8', 
        escapeChar='\\', 
        emptyIsNull=True, 
        debug=False):
    
    print("loadCSVToNeo4j started file: " + aCSV);
    print(f"            neo4j database: {aDBName}")
    print(f"             neo4j address: {aDriver.get_server_info().address}")
    print(f"               concurrency: {concurrency}")
    print(f"                 batchSize: {aBatchSize} ")
    print(f"                 delimiter: {aDelimiter} ")
    print(f"                 quotechar: {aQuotechar} ")
    print(f"                escapechar: {escapeChar} ")

    if debug:
        print(f"                     query: {aQuery}")
    
    nodesCreated = 0
    labelsCreated = 0
    relationshipsCreated = 0
    propertiesSet = 0
    pcnt = 0
    tStart = time.perf_counter_ns()
    neo4jLoadThreads = []
    out = ProgressOutput(aBatchSize)
    maxQueueSize = 10 * aBatchSize

    with open(aCSV, mode='r', encoding=aEncoding) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=aDelimiter, quotechar=aQuotechar, escapechar=escapeChar)
        line_count = 0
        # initiate the concurrent Threads
        for i in range(concurrency):
            thr = Neo4jLoader(i,"neo4j loader " + str(i), aDriver.session(database=aDBName),aQuery,aBatchSize, out, debug,maxQueueSize)
            # print("ADDED LOADER " + str(id(thr)) )
            neo4jLoadThreads.append(thr)
            thr.start()

        threadIndex = 0
        try:
            for row in csv_reader:
                if (pcnt == 0):
                    if debug:
                        print("First csv row:")
                        print(row)
                    print("---------------------------")
    
                pcnt += 1
                maxC = concurrency -1;
                if emptyIsNull:
                    row = makeEmptyNull(row);
                neo4jLoadThreads[threadIndex].addRow(row)
                if (concurrency > 1):
                    if (threadIndex < maxC):
                        threadIndex += 1
                    elif (threadIndex == maxC ):
                        threadIndex = 0
        except KeyboardInterrupt:
            print("Cancelled after crtl-c")
            sys.exit()    


        for loader in neo4jLoadThreads:
            loader.finish()
            loader.join()
            labelsCreated += loader.labelsCreated
            nodesCreated += loader.nodesCreated
            propertiesSet += loader.propertiesSet
            relationshipsCreated += loader.relationshipsCreated
        # reporting duration result is an interge due to the usage of //
        duration = (time.perf_counter_ns() - tStart) // 1000000
        if duration == 0:
            duration = 1
        nplusr = nodesCreated + relationshipsCreated
        nrPerSecond = math.floor(((nodesCreated + relationshipsCreated) / duration) * 1000)
        out.finished(str(pcnt))
        if debug:
            print(f' labelsCreated: {labelsCreated}, nodesCreated: {nodesCreated}, propertiesSet: {propertiesSet}, relationshipsCreated: {relationshipsCreated}')
        
        
        print(f'\n Processed {pcnt} data rows in {duration} ms. Created nodes/relationships per second {nrPerSecond}.')   
