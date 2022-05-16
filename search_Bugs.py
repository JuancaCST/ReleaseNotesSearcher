# Name: Juan Cabrera
# Date Created: 05/14/2022
# Purpose: To search the release notes for known bugs through keywords


#This version has the core functionality completed. Need to add support for the transform class of the missing versions.
#If no bugs are found, display a message saying so.
#Test and add error handling.

import json,re,os

urls = {
    "6.5.0" : "https://docs.fortinet.com/document/fortisiem/6.5.0/release-notes/482665/whats-new-in-6-5-0",
    "6.4.0" : "https://docs.fortinet.com/document/fortisiem/6.4.0/release-notes/456886/whats-new-in-6-4-0",
    "6.3.2" : "https://docs.fortinet.com/document/fortisiem/6.3.2/release-notes/803208/whats-new-in-6-3-2"
    #"6.3.1" : "https://docs.fortinet.com/document/fortisiem/6.3.1/release-notes/330225/whats-new-in-6-3-1",
    #"6.3.0" : "https://docs.fortinet.com/document/fortisiem/6.3.0/release-notes/498610/whats-new-in-6-3-0",
    #"6.2.1" : "https://docs.fortinet.com/document/fortisiem/6.2.1/release-notes/498610/whats-new-in-6-2-1",
    #"6.2.0" : "https://docs.fortinet.com/document/fortisiem/6.2.0/release-notes/498610/new-features",
    #"6.1.1" : "https://docs.fortinet.com/document/fortisiem/6.1.1/release-notes/965243/whats-new-in-6-1-1#What's_New_in_6.1.1",
    #"6.1.0" : "https://docs.fortinet.com/document/fortisiem/6.1.0/release-notes/441737/whats-new-in-6-1-0#What's_New_in_6.1.0"
}


# Step 1: Fetch the html page, assign to object, and return it
class extract:
    @staticmethod
    #Gets html page and returns as a string.
    def get_page(url):
        import urllib.request
        fp = urllib.request.urlopen(url)
        mystr = fp.read().decode("utf8")
        fp.close()
        return mystr

    @staticmethod
    #Open cache file and return current dictionary
    def get_cache(data_file):
        with open(data_file) as f:
            data = json.load(f)
        return data

    @staticmethod
    #When version is not in cache file. Get html page, clean data,
    def get_data(data, version):
        html_data = extract.get_page(urls[version])
        parsed_Data = transform.clean_data(html_data, version)
        data.update(parsed_Data)
        return transform.get_bugs(data, keyword, version)



# Takes string as input and returns a list
class transform:
    #Takes the html str as input and returns a list of the bugs as dictionaries.
    @staticmethod
    def clean_data(data, version):
        index_start = re.search("<p>\d{6}</p>|\">\d{6}</td>", data).start()
        index_end = re.search("</tr>\r\n.*<\/tbody>", data).start()
        short_data = data[index_start:index_end-1]
        values = re.findall("<p>.*\n.*</p>\n.*<p><b>.*</b>.*\n.*</p>|<p>.*</p>|<p>.*\n.*</p>|<p>.*\n.*\n.*</p>|<p>.*\n.*\n.*\n.*</p>|<p>.*\n.*\n.*\n.*\n.*</p>|AD.Server.</td>\n.*</tr>", short_data)
        #print(len(values))
        cleaned_values = list()
        columns = ["Bug ID", "Severity", "Module", "Description"]
        for x in range(0, len(values), 4):
            bug_list = list()
            for i in range(x, x+4):
                left_cleaned = values[i].replace("<p>", "")
                right_cleaned = left_cleaned.replace("</p>", "")
                spaces_cleaned = right_cleaned.replace("\r\n", "")
                bug_list.append(spaces_cleaned)
            bug_dict = {columns[i]: bug_list[i] for i in range(len(columns))}
            #print(bug_dict)
            cleaned_values.append(bug_dict)
        final_values = { version : cleaned_values}
        return final_values

    
     #This searches the cache file, and returns found bugs.
    @staticmethod
    def get_bugs(data, keyword, version):
        found = list()
        for bug in data[version]:
            if keyword in str(bug).lower():
                found.append(bug)
        return found
    


class load():
    @staticmethod
    #This is the class that will write the list of bugs (dictionaries) into the local cache file
    def write_file(parsed_data):
        with open("cache.txt", "w") as json_Cache:
            json_Cache.write(json.dumps(parsed_data, indent=4))
        


while True:
    keyword = input("Enter keyword to search for [Type quit to exit]: ").lower()
    if keyword.lower() == "quit" or keyword.lower() == "q" or keyword.lower() == "exit":
        break
    version = input("Enter the lowest version you would like to include in the search [Please use format 6.x.x]")
    if keyword.lower() == "quit" or keyword.lower() == "q" or keyword.lower() == "exit":
        break
    if version not in urls.keys():
        raise Exception("The version you entered is not valid. Only versions 6.1.0 and higher are supported.")

    #Get the list of relevant versions.
    versions_list = list(urls.keys())
    version_index = versions_list.index(version)
    relevant_versions = versions_list[0:version_index+1]

    

    #cache file already exists
    if os.path.exists("cache.txt") == True:
        file_data = extract.get_cache("cache.txt")
        for version in relevant_versions:
            print(f"=== BUGs found in Version {version}===")
            #If version in cache file, search cache and display results.
            if version in file_data.keys():
                results = transform.get_bugs(file_data, keyword, version)
                for bug in results:
                    print(bug)
            
            #If version not in cache file, get the bugs, display results, append new version to cache.
            else:
                results = extract.get_data(file_data, version)
                for bug in results:
                    print(bug)
        load.write_file(file_data)

    #if cache file does not exist.
    else:
        file_data = dict()
        for version in relevant_versions:
            print(f"=== BUGs found in Version {version}===")
            results = extract.get_data(file_data, version)
            for bug in results:
                print(bug)
        load.write_file(file_data)