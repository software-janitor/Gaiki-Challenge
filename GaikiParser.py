# Matthew Garcia
# This file contains two classes that are used to represent and construct Gaiki Jobs.
# Furthermore, the GaikiParser class handles all the heavy lifting for GET requests
#
#
#

from Parser import Parser
import urllib
import json
from json import JSONEncoder
import collections
import math
# A Class that represents a Giaki job.
class GaikiJob:

    def __init__(self):
        self.title=""
        self.responsibilities=[]
        self.requirements=[]
        self.skills=[]
        self.additionalAttributes=[]

    def __lt__(self,other):
        if isinstance(other,GaikiJob):
            return self.title < other.title

    def __eq__(self,other):
        if isinstance(other,GaikiJob):
            return self.title == other.title

    def titleSubString(self,gaikijob_other):
        
        if gaikijob_other.getTitle().lower() in self.title.lower():
            print self.title
            return True

        return False

    def getTitle(self):
        return self.title

    def getResponsibilities(self):
       return self.responsibilities

    def getRequirements(self):
        return self.requirements

    def getSkills(self):
        return self.skills

    def getAdditionalAttributes(self):
        return self.additionalAttributes

    def setTitle(self,s_title):
        self.title=s_title

    def addResponsibility(self,s_responsibility):
        self.responsibilities.append(s_responsibility)
   
    def addRequirments(self,s_requirement):
        self.requirements.append(s_requirement)
  
    def addSkill(self,s_skill):
        self.skills.append(s_skill)
  
    def addAdditionalAttributes(self,s_additionalAttribute):
        self.additionalAttributes.append(s_additionalAttribute)

# The Class that perfroms all of the heavy lifting when a GET request is made.
# The Class will parse the page when a GET request is made and will CACHE the results so that future requests are faster. The
# career's page will only be re parsed if something on the page has changed.
class GaikiParser(Parser):


    def __init__(self,url):
            self.jobHashTable={}
            self.jobList=[]
            self.token_start="<article id="
            self.token_end="</article>"
            self.token_newJob="<h1><span class=\"arrow\"></span>"
            self.token_closeNewJob="</h1>"
            self.token_h2="<h2>"
            self.token_closeH2="</h2>"
            self.token_newSection="<section class=\"content\">"
            self.token_li="<li>"
            self.token_closeLi="</li>"
            self.num_lines=0;
            self.url=url
    def getNumLines(self):
        return self.num_lines

    def getNumJobs(self):
        return len(self.jobHashTable)
    
    # A method that checks to see if anything has been changed on the Career page.
    def hasPageChanged(self):
        socket=urllib.urlopen(self.url)
        htmlSource=socket.readlines()
        if(len(htmlSource) > self.num_lines):
            self.num_lines=len(htmlSource)
            return True
        else:
            return False
    
    # A Parser method that represents a basic DFA which creates Gaiki job objects.
    def parse(self):
        print "Gaiki Parser"
        state="start"
        socket=urllib.urlopen(self.url)
        htmlSource=socket.readlines()
        currentJob=None
        self.num_lines=len(htmlSource)
        
        for l in htmlSource:
            
            if state=="start":
                if l.find(self.token_start) != -1:
                    state="newJob"
        
            elif state=="newJob":
                if l.find(self.token_newJob) != -1:
                    l= l.replace(self.token_newJob,"")
                    l=l.replace(self.token_closeNewJob,"")
                    currentJob=GaikiJob()
                    currentJob.setTitle(l.lstrip().strip())
                    self.jobHashTable[currentJob.getTitle().lstrip().strip()]=currentJob
                    self.jobList.append(currentJob)
                
                elif l.find(self.token_newSection) !=-1:
                    state="responsibilities"
                elif l.find(self.token_end) !=-1:
                    state="start"
                        
            elif state == "responsibilities":
                if l.find(self.token_li)!= -1:
                    l= l.replace(self.token_li,"")
                    l= l.replace(self.token_closeLi,"")
                    currentJob.addResponsibility(l.lstrip().strip())
                elif l.find(self.token_newSection) !=-1:
                    state="requirements"
                elif l.find(self.token_end) !=-1:
                    state="start"

            elif state == "requirements":
                if l.find(self.token_li)!= -1:
                    l=l.replace(self.token_li,"")
                    l=l.replace(self.token_closeLi,"")
                    currentJob.addRequirments(l.lstrip().strip())
                elif l.find(self.token_newSection) !=-1:
                    state="skills"
                elif l.find(self.token_end) !=-1:
                    state="start"

            elif state == "skills":
                if l.find(self.token_li)!= -1:
                    l= l.replace(self.token_li,"")
                    l= l.replace(self.token_closeLi,"")
                    currentJob.addSkill(l.lstrip().strip())
                elif l.find(self.token_newSection) !=-1:
                    state="additionalAttributes"
                elif l.find(self.token_end) !=-1:
                    state="start"

            elif state=="additionalAttributes":
                if l.find(self.token_li)!= -1:
                    l= l.replace(self.token_li,"")
                    l= l.replace(self.token_closeLi,"")
                    currentJob.addAdditionalAttributes(l.lstrip().strip())
                elif l.find(self.token_end) !=-1:
                    state="start"
                        
        socket.close()
    # If the exact job was not entered, this function will perform a regex fuzzy search
    # only if the regex has a length greater than 1.
    def searchForBestMatch(self,title):
        json_instances=[]
        gaikijob_temp=GaikiJob()
        gaikijob_temp.setTitle(title)
        if len(title) <2:
            return None
        for j in self.jobList:
            if j.titleSubString(gaikijob_temp):
                json_instances.append(self.makeJsonInstance(j))
        
        if json_instances == []:
            return None
        else:
            return json_instances

                
    def getLineCount(self):
        htmlSource=socket.readlines()
        return len(htmlSource)
    # A Function that sets up a DICT object that makes returning a JSON object Easier
    def makeJsonInstance(self,object):
        json_instance={ 'title':object.getTitle(),'responsibilites':object.getResponsibilities(),  'requirements': object.getRequirements(), 'skills':object.getSkills(), 'additionalAttributes': object.getAdditionalAttributes() }
        return json_instance
    # A function that processes a GET request and returns the desired job or jobs based on what the user inputs.
    def getRequest(self,path):
        # If anything was added to the careers page then parse it and look for new jobs. Otherwise do not parse the page again.
        if self.hasPageChanged():
            self.parse()

# Add a check here to make sure the url is correct when not running locally.
#       if URL is malformed, return an error
#
        if "/jobs/" in path:
            json_instance =self.getInstance(path.replace("/jobs/","").replace("%20"," "))
            return json_instance
        elif "/jobs" in path:
            json_instances= self.getAllInstances()
            return json_instances
        else:
            return "Invalid URL"
    # A helper function that returns the specified job as a json object.
    # If the exact name of the job was not entered as it appears on the site, then the
    # method will try and find the best matches out of all the jobs and return a list of
    # them. I wam assuming a small dataset, otherwise indexing would have been implemented
    # to help speed up search time.
    def getInstance(self,title):
        print "Gaiki Instance finder"
        
        json_instance=""
        try:
            json_instance=self.makeJsonInstance(self.jobHashTable[title.lstrip().strip()])
        except:
            json_instance=self.searchForBestMatch(title)
            if json_instance == None:
                return "Specified job not found."
        
        return json.dumps(json_instance,sort_keys=True,indent=4, separators=(',', ': '))
    # A helper method that returns all the available jobs as an array of json objects
    def getAllInstances(self):
        print "Gaiki Instances finder"
        response=[]
       
        if(len(self.jobHashTable) == 0):
            return "No open positions currently available."
        
        for key, value in self.jobHashTable.items():
            response.append(self.makeJsonInstance(value))
        return json.dumps(response,sort_keys=True,indent=4, separators=(',', ': '))


    # The method not used in the REST api, but necessary for part one of the challenge.
    # This method is the same as the getAllInstaces method above except that it adds in
    # parsing of the webpage.
    def getJsonArray(self):
        self.parse()
        response=[]
        
        if(len(self.jobHashTable) == 0):
            return "No open positions currently available."
        
        for key, value in self.jobHashTable.items():
            response.append(self.makeJsonInstance(value))
        return json.dumps(response,sort_keys=True,indent=4, separators=(',', ': '))








