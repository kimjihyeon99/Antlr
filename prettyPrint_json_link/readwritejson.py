import json


result = {}

def loadjson():
    g={}
    f={}
    f1 = {}
    f2 = {}
    with open("./json/json_design.json", "r") as json_file:
        json_data = json.load(json_file)
        print(json.dumps(json_data, indent="\t" ))
        return json_data

        #gfield 를 자료구조에 추가
        # gfield=json_data["g_field"][0]
        #
        # i=0
        # for value in gfield:
        #     g[value] = gfield[value]
        #     i=i+1
        #
        # #function 자료구조에 추가
        # functions =json_data["functions"][0]
        #
        # f_name=['signature','args']
        # f[f_name[0]]= f_name[0]
        #
        # args0 = functions[f_name[1]][0]
        # j=0
        # for value in args0:
        #     f1[value]= args0[value]
        #     j = j+1
        #
        # args1 = functions[f_name[1]][1]
        #
        # j=0
        # for value in args1:
        #     f2[value]= args1[value]
        #     j = j+1
        #
        # flist = []
        #
        # flist.append(f1)
        # flist.append(f2)
        #
        # f[f_name[1]] = flist
        #
        # glist = []
        # f2list = []
        #
        # glist.append(g)
        # f2list.append(f)
        #
        # result["g_field"] = glist
        # result["functions"] = f2list
        #
        # print(result)



def storejson():
    with open('./json/test.json', 'w') as make_file:
        json.dump(result, make_file, indent="\t")
