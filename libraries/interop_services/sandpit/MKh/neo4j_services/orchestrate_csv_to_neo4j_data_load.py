import csv
import threading
import time
import math
import sys
from collections import deque
import pandas as pd
import configparser

from source.code.services.storage_interop_services.graph_processing_services.neo4j_services.object_models.Neo4jLoader import Neo4jLoader

def synchronized(func):

    func.__lock__ = threading.Lock()

    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)

    return synced_func

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
 
def makeEmptyNull(aRow):
    for key in aRow.keys():
        if aRow[key] is not None and type(aRow[key]) == str and aRow[key] == "":
            aRow[key] = None
    return aRow    


#TODO - method signature too large, move parameters to config file.
def orchestrate_csv_to_neo4j_load(
        csv_file_name_and_path, 
        neo4j_connection, 
        cypher_load_query, 
        batch_size,
        concurrency=1,
        csv_file_delimiter=',', 
        csv_file_quote_character='"',
        csv_file_encoding='utf-8', 
        csv_escape_character='\\', 
        emptyIsNull=True, 
        debug=False):
   
    print("loadCSVToNeo4j started file: " + csv_file_name_and_path);
    print(f"               concurrency: {concurrency}")
    print(f"                 batchSize: {batch_size} ")
    print(f"                 delimiter: {csv_file_delimiter} ")
    print(f"                 quotechar: {csv_file_quote_character} ")
    print(f"                escapechar: {csv_escape_character} ")

    if debug:
        print(f"                     query: {cypher_load_query}")
    
    nodesCreated = 0
    labelsCreated = 0
    relationshipsCreated = 0
    propertiesSet = 0
    pcnt = 0
    tStart = time.perf_counter_ns()
    neo4jLoadThreads = []
    out = ProgressOutput(batch_size)
    maxQueueSize = 10 * batch_size

    with open(
        csv_file_name_and_path, 
        mode='r', 
        encoding=csv_file_encoding) as csv_file:
        
        csv_reader = csv.DictReader(
            csv_file, 
            delimiter=csv_file_delimiter, 
            quotechar=csv_file_quote_character, 
            escapechar=csv_escape_character)
        
        line_count = 0
        
        # initiate the concurrent Threads
        for thread_index in range(concurrency):
  
            neo4j_loader_thread = Neo4jLoader(
                threadID=thread_index,
                name="neo4j loader " + str(thread_index), 
                neo4j_connection=neo4j_connection,
                cypher_query=cypher_load_query,
                batchSize=batch_size, 
                out=out, 
                debug=debug,
                maxQueueSize=maxQueueSize)
            
            
            neo4jLoadThreads.append(neo4j_loader_thread)
            neo4j_loader_thread.start()

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
        
        return nodesCreated



