from subprocess import Popen , PIPE
import requests
import webbrowser

def execute_return(cmd):
    args= cmd.split()
    proc= Popen(args , stdout=PIPE , stderr=PIPE)
    out, err= proc.communicate()
    return out,err

def make_req(error):
    print("searching for: "+error)
    response=requests.get("https://api.stackexchange.com/"+"/2.3/search?order=desc&sort=activity&tagged=python&intitle={}&site=stackoverflow".format(error))
    return response.json()

def get_urls(json_dict):
    url_list=[]
    count=0
    for i in json_dict["items"]:
        if i["is_answered"]:
            url_list.append(i["link"])
        count+=1
        if(count==3 or count==len(i)):
            break

    for i in url_list:
        webbrowser.open(i)


if __name__ == "__main__":
    filepath=input("Drop the file you're wroking on: ")
    op,err=execute_return("Python {}".format(filepath))
    error_message=err.decode("utf-8").strip().split("\r\n")[-1]
    print("ERROR-->",error_message)

    if error_message:
        filter_err=error_message.split(":")
        json1=make_req(filter_err[0])
        json2=make_req(filter_err[1])
        json=make_req(error_message)
        get_urls(json1)
        get_urls(json2)
        get_urls(json)

    else:
        print("No error")