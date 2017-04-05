import process_log_CHHuang as processlog

def test_parse_data():
    test_inputs=( "199.72.81.55 - - [01/Jan/1995:00:00:01 -0400] \"GET /history/apollo/ HTTP/1.0\" 200 6245",  
                  "unicomp6.unicomp.net - - [21/Feb/1995:00:00:06 -0400] \"GET /shuttle/countdown/\" 301 -", 
                  "test.example.com - - [30/Mar/2011:15:11:22 -0400] \"/failattemptexample\" 400 0",
                  "example_of_wrong_format")
    exp_results=( ('199.72.81.55', '01/Jan/1995:00:00:01 -0400', 788918401, 'GET', '/history/apollo/', 200, 6245),
                  ('unicomp6.unicomp.net', '21/Feb/1995:00:00:06 -0400', 793324806, 'GET', '/shuttle/countdown/', 301, 0),
                  ('test.example.com', '30/Mar/2011:15:11:22 -0400', 1301497882, None, None, 400, 0) )

    Npass= 0
    for i in range(len(test_inputs)):
        if i==3:
            iserr= False
            try: test_results= processlog.parse_data(test_inputs[i]) # should gives exception
            except: iserr= True
            if iserr: Npass +=1
            else:
                print("  -- Fail (parse_data) --")
                print("   Test_inputs: ", test_inputs[i])
                print("   Exp_results: exit()")
                print("   test_results: Did not exit()")
        else:
            if i==2: print("Should have a Warning here(case 3): ", end='')
            test_results= processlog.parse_data(test_inputs[i]) # call the function
            if test_results==exp_results[i]: Npass +=1
            else:
                print("  -- Fail@ (parse_data) --")
                print("   Test_inputs: ", test_inputs[i])
                print("   Exp_results: ", exp_results[i])
                print("   test_results:", test_results)
    
    if Npass==len(test_inputs): print("[PASS](parse_data) %d/%d cases" % (Npass, len(test_inputs)))
    else:                       print("[FAIL](parse_data) %d/%d cases" % (Npass, len(test_inputs)))

def test_compute_feature1(): pass
def test_compute_feature2(): pass
def test_compute_feature3(): pass

def test_checkNfail_feature4():
    test_inputs=( (dict(), "140.114.520.520", 200, 22),             # None, sucess
                  (dict(), "ex.net", 400, 22),                      # None, fail
                  (dict({"111.net":[0, 1]}), "222.net", 400, 11),   # None, fail (dict size !=0)
                  (dict({"aaa.com":[0, 3]}), "aaa.com", 200, 55),   # Nf=0, sucess
                  (dict({"aaa.com":[0, 3]}), "aaa.com", 400, 55),   # Nf=0, fail
                  (dict({"bbb.com":[1, 3]}), "bbb.com", 400, 12),   # Nf=1, fail in 20secs
                  (dict({"bbb.com":[1, 3]}), "bbb.com", 400, 66),   # Nf=1, fail out 20secs
                  (dict({"ccc.com":[2, 3]}), "ccc.com", 400, 12),   # Nf=2, fail in 20secs
                  (dict({"ccc.com":[2, 3]}), "ccc.com", 400, 66),   # Nf=2, fail out 20secs
                  (dict({"ddd.com":[3, 3]}), "ddd.com", 200, 66),   # Nf=3, sucess in 5mins
                  (dict({"ddd.com":[3, 3]}), "ddd.com", 200, 66),   # Nf=3, fail in 5mins
                  (dict({"ddd.com":[3, 3]}), "ddd.com", 200, 400),  # Nf=3, sucess out 5mins
                  (dict({"ddd.com":[3, 3]}), "ddd.com", 400, 400),  # Nf=3, fail out 5mins
                  (dict({"eee.com":[4, 3]}), "eee.com", 400, 5),    # Nf=4, error
                  (dict({"eee.com":[-1,3]}), "eee.com", 400, 5) )   # Nf=-1, error
    exp_results=( ({}, False), ({'ex.net': [1, 22]}, False), ({'111.net': [0, 1], '222.net': [1, 11]}, False),
                  ({'aaa.com': [0, 3]}, False), ({'aaa.com': [1, 55]}, False),
                  ({'bbb.com': [2, 3]}, False), ({'bbb.com': [1, 66]}, False),
                  ({'ccc.com': [3, 3]}, False), ({'ccc.com': [1, 66]}, False),
                  ({'ddd.com': [3, 3]}, True),  ({'ddd.com': [3, 3]},  True),
                  ({'ddd.com': [0, 3]}, False), ({'ddd.com': [1, 400]},False) )
    
    Npass= 0
    for i in range(len(test_inputs)):
        test_dict= dict(test_inputs[i][0])
        if i==13 or i==14:
            iserr= False
            try: isblocked= processlog.checkNfail_feature4(test_dict, test_inputs[i][1], test_inputs[i][2], test_inputs[i][3])
            except: iserr= True
            if iserr: Npass +=1
            else:
                print("  -- Fail (checkNfail_feature4) --")
                print("   Test_inputs: ", test_inputs[i])
                print("   Exp_results: exit()")
                print("   test_results: Did not exit()")
        else:
            isblocked= processlog.checkNfail_feature4(test_dict, test_inputs[i][1], test_inputs[i][2], test_inputs[i][3])
            if test_dict==exp_results[i][0] and isblocked==exp_results[i][1]: Npass +=1
            else:
                print("  -- Fail (checkNfail_feature4) --")
                print("   Test_inputs: ", test_inputs[i])
                print("   Exp_results: ", exp_results[i])
                print("   test_results:", (test_dict,isblocked))
    
    if Npass==len(test_inputs): print("[PASS](checkNfail_feature4) %d/%d cases" % (Npass, len(test_inputs)))
    else:                       print("[FAIL](checkNfail_feature4) %d/%d cases" % (Npass, len(test_inputs)))

def test_compute_feature5(): pass

def main():
    test_parse_data()
    test_compute_feature1()
    test_compute_feature2()
    test_compute_feature3()
    test_checkNfail_feature4()
    test_compute_feature5()
    print("*** Test completed. ***\n")


if __name__=="__main__":
    main()
