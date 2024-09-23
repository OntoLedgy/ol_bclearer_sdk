
#TODO fix the dependencies.

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
        
    # finishing up
    # if debug:
    #  print(" finished reading csv rows ")

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