import sys
import os.path
import re
import time
import calendar

def parse_data(line): # extract values
    EXTdata= re.match("(\S+)\s+-\s+-\s+\[(.+)\]\s+\"(.+)\"\s+(\S+)\s+(\S+)" ,line) # extract data
    if EXTdata==None: exit("Error: input info not match the format:\n%s" % line) # check
    (host, timestamp, request, replycode, filebytes)= EXTdata.groups()
    timesecs= calendar.timegm(time.strptime(timestamp, "%d/%b/%Y:%H:%M:%S -0400")) # Epoch time in secs
    try:
        action, resource, *protocol= request.strip().split() # request -> action, resrc
    except:
        print("(Warning) Can\'t parse request:", request)
        action= None; resource= None
    replycode= int(replycode)
    if filebytes=='-':  filebytes= 0 # - means 0
    else:               filebytes= int(filebytes)

    return host, timestamp, timesecs, action, resource, replycode, filebytes

def compute_feature1(NAMEhosts, Naccs_host): # sort Naccs_host and get top 10
    Naccs_host_sorted= sorted(Naccs_host.items(), key= lambda x:(-x[1],x[0]))
    OFILE_HOSTS= open(NAMEhosts, "w")
    for i in range( min(10,len(Naccs_host_sorted)) ):
        key, value= Naccs_host_sorted[i]
        print("%s,%d" % (key, value), file=OFILE_HOSTS)

def compute_feature2(NAMEresrc, Bytes_rsrc): # sort Bytes_rsrc and get top 10
    Bytes_rsrc_sorted= sorted(Bytes_rsrc.items(), key= lambda x:(-x[1],x[0]))
    OFILE_RESRC= open(NAMEresrc, "w")
    for i in range( min(10,len(Bytes_rsrc_sorted)) ):
        key, value= Bytes_rsrc_sorted[i]
        print(key, file=OFILE_RESRC)
    
def compute_feature3(NAMEhours, Naccs_time, tbegin, tend):
    sumhr_Naccs= {} # key: hourly sum of acc. N; value: list of Epoch times
    Ncount= 0       # count N accesses in hr window
    for t in range(tbegin-1, tbegin+3599): # cal Ncount at tbegin-1 sec
        Ncount += Naccs_time.get(t, 0)
    for t in range(tbegin, tend+1): # scan from tbegin to tend
        Nsub= Naccs_time.get(t-1, None) # rolling sum
        Nadd= Naccs_time.get(t+3599, None)
        if Nsub != None: Ncount -= Nsub # sub N at 1sec earlier
        if Nadd != None: Ncount += Nadd # add N at last secs (right bef 3600)
        if sumhr_Naccs.get(Ncount, None)==None:
            sumhr_Naccs[Ncount]= [t]
        else:
            sumhr_Naccs[Ncount].append(t)
    sumhr_Naccs_sorted= sorted(sumhr_Naccs.items(), key= lambda x:x[0], reverse= True)
    Ntop10= 0
    OFILE_HOURS= open(NAMEhours, "w")
    for key, value in sumhr_Naccs_sorted:
        for t in value:
            Ntop10 +=1 
            print(time.strftime("%d/%b/%Y:%H:%M:%S -0400", time.gmtime(t)), key, sep=',', file=OFILE_HOURS)
            if Ntop10==10: return # if same multi secs have same Naccs, choose earlier ones 

def checkNfail_feature4(Nfail_host, host, replycode, timesecs): # change Nfail dict; return if BLOCKED
    if Nfail_host.get(host, None)==None: # if host not in list
        if replycode >=400: Nfail_host[host]= [1,timesecs] # only add it when fail appears
    else:
        nf, ts= Nfail_host[host] # Nfails, timesecs of 1st_fail|begin_blckd
        if nf>3 or nf<0: exit("Error: N fails not in range 0-3: %d" % nf)
        elif nf==3: # 3 fails, if in 5mins, block; else, reset Nfail_host
            if (timesecs-ts)<300:
                return True # BLOCKED; output
#                print("(Warning) Request blocked:", line.strip())
            elif replycode >=400:           Nfail_host[host]= [1,timesecs]
            else:                           Nfail_host[host][0] = 0
        elif replycode >=400: # if within 20 secs, Nfail ++
            if nf!=0 and (timesecs-ts)<20:  Nfail_host[host][0] +=1
            else:                           Nfail_host[host]= [1,timesecs]
    
    return False

def compute_ADDfeature5(NAMEhoursNEW, Naccs_time, tbegin, tend):
    # NEW FEATURE: Calculate top 10 busiest hours with strict hour window from XX:00:00 to XX:59:59
    Naccs= {} # key: strict hrs starting at XX:00:00 (epoch secs); value: N access of a hour
    for t, n in Naccs_time.items():
        t0000= (t//3600)*3600 # int division
        Naccs[t0000]= Naccs.get(t0000, 0) + n
    Naccs_sorted= sorted(Naccs.items(), key= lambda x:(-x[1],x[0]))
    OFILE_HOURSNEW= open(NAMEhoursNEW, "w")
    for i in range( min(10,len(Naccs_sorted)) ):
        key, value= Naccs_sorted[i]
        print(time.strftime("%d/%b/%Y:%H:%M:%S -0400", time.gmtime(key)), value, sep=',', file=OFILE_HOURSNEW)

def main():
    if (len(sys.argv) != 7):
        print("\nPerform analytics on server log file\n")
        exit("Use: %s [log_file(IN)] [hosts.txt(OUT)] [resources.txt(OUT)] [hours.txt(OUT)] [blocked.txt(OUT)] [NEWhours.txt(OUT)]\n" % sys.argv[0])

    t0cal= time.time() # cal time spend for the script
    print("Start analyzing...")

    # FILE NAMES #
    INlog= sys.argv[1]
    OUThosts= sys.argv[2] # f1
    OUTresrc= sys.argv[3] # f2
    OUThours= sys.argv[4] # f3
    OUTblked= sys.argv[5] # f4
    OUThoursNEW= sys.argv[6] # f5

    # VARIABLES #
    Naccs_host= {} # num of access of a host (f1)
    Bytes_rsrc= {} # acc bytes of a resource sent (f2)
    Naccs_time= {} # num of access at an Epoch second (f3)
    Nfail_host= {} # list of [N fails, time (1st_fail|begin_blckd)] (f4)
    tlast= -1.0
    OFILE_BLKED= open(OUTblked, "w") # f4 OFILE

    #####------ READING LOG FILE AND COUNT  ------#####
    if not os.path.isfile(INlog): exit("Error: input file %s does not exist!" % INlog) # check
    with open(INlog, "r", encoding="ISO-8859-1") as IFILE:
        for line in IFILE: # Reading log file
            # Extract variables
            host, timestamp, timesecs, action, resource, replycode, filebytes= parse_data(line) 
            if tlast > timesecs: exit("log file is not in time order: %e %e (epoch time)" % (timesecs, tlast))

            # Count values(f1, f2, f3)
            Naccs_host[host]= Naccs_host.get(host, 0) + 1
            if resource!=None: Bytes_rsrc[resource]= Bytes_rsrc.get(resource, 0) + filebytes
            Naccs_time[timesecs]= Naccs_time.get(timesecs, 0) + 1
            if len(Naccs_time)==1: tbegin= timesecs # get time begin of the log
            
            # check if 3 fails in 20 secs, blocked in 5mins (f4)
            isblocked= checkNfail_feature4(Nfail_host, host, replycode, timesecs)
            if isblocked: print(line, end='', file=OFILE_BLKED)
            
            tlast= timesecs # use to check if chronological
    tend= timesecs # get time end of the log

    #####------ POST PROCESSING (feature 1, 2, 3, 5) ------######
    compute_feature1(OUThosts, Naccs_host)
    compute_feature2(OUTresrc, Bytes_rsrc)
    compute_feature3(OUThours, Naccs_time, tbegin, tend)
    compute_ADDfeature5(OUThoursNEW, Naccs_time, tbegin, tend)

    print ("*** Calculation's done. Total time spent:", time.time()-t0cal, "secs ***\n")

if __name__ == "__main__":
    main()
