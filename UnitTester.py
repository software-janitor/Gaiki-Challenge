# Matthew Garcia
#  A test suite that has a few tests that verify the functionality requested in the coding challenge.
#
#
import urllib
import json
from json import JSONEncoder
import collections
import unittest
from GaikiParser import GaikiParser,GaikiJob









class TestRestApi(unittest.TestCase):
    baseUrl= "http://127.0.0.1:8000/"
    g_parser = GaikiParser("http://www.gaikai.com/careers")
    currentJob=None
    jobs={'Security Manager':1 , 'Senior Software Engineer':1, 'Release Engineer':1, 'Senior Python Engineer':1,'Senior Business Intelligence Analyst':1,'IT Manager':1,'Technical Operations Project Manager x2':1,'Service Reliability Engineering Manager (1x US, 1x EU)':1,'Vendor Management / Sourcing Manager':1,'Datacenter Site Operations / Provisioning Engineer':1,'Datacenter Logistics Manager':1,'Service Reliability Engineer / Systems Administrator (3x US, 5x EU)':1,'Network Automation Software Engineer':1,'Senior Network Engineer with ISP focus':1,'Content Delivery Network Engineer':1,'Network Deployment / Provisioning Engineer':1,'Enterprise Network Engineer':1,'Senior Network Engineer with Datacenter focus':1,'Technical Project Manager with Network experience':1,'Business Planning Analyst':1,'Senior Java Engineer':1,'Front-End Engineer':1,'Client Software Engineer (C++ / WebKit)':1,'Graphic Designer':1,'Jr. User Experience Designer':1,'Data Visualization Architect':1,'Senior Solution Architect':1}
    socket=None
    
    # A helper function used to build Gaiki job objects that can be tested against whatever the REST api returns.
    def buildGaikiObject(self,title,responsibilities,requirments,skills,additionalAttributes):
        self.currentJob.setTitle(title)
        for i in responsibilities:
            self.currentJob.addResponsibility(i)
        for i in requirments:
            self.currentJob.addRequirments(i)
        for i in skills:
            self.currentJob.addSkill(i)
        for i in additionalAttributes:
            self.currentJob.addAdditionalAttributes(i)
    
    def setUp(self):
        # populate the the list of jobs on the server side
        self.socket=urllib.urlopen(self.baseUrl+"jobs")
        # self.g_parser.getRequest(self.baseUrl+"jobs")
        self.currentJob=GaikiJob()
        self.socket.close()
    
    def test_JobCount(self):
         # Check to see if we get the right amount of jobs.
        socket=urllib.urlopen(self.baseUrl+"jobs")
        json_instances=json.loads(socket.read())
        
        self.assertEqual(len(json_instances), 27)
        socket.close()
    
    
    def test_GetAllInstances(self):
        print "Runnning Test for GET /jobs"
        # Check to see if we get all the correct job titles.
        self.socket=urllib.urlopen(self.baseUrl+"jobs")
        json_instances=json.loads(self.socket.read())

        for j in json_instances:
            try:
                self.assertEqual(self.jobs[j['title']],1)
            except:
                self.fail("One of the jobs is missing")
        self.socket.close()

    def test_JsonArrayMethod(self):
        json_array=json.loads(self.g_parser.getJsonArray())
        for j in json_array:
            try:
                self.assertEqual(self.jobs[j['title']],1)
            except:
                self.fail("One of the jobs is missing")
    
    def test_GetSingleInstances(self):
        # Check to see if we can find the Jr. User Experience Designer Job
        print "Running Test for GET /jobs/Jr.%20User%20Experience%20Designer"
        self.socket=urllib.urlopen(self.baseUrl+"jobs/Jr.%20User%20Experience%20Designer")
        currentJob=GaikiJob()
        title="Jr. User Experience Designer"
        responsibilities=[ "Work closely with the UIX Director, Art Director, and UIX Engineers to ensure design concepts are executed as proposed, with the ability to update or revamp changes or solutions where necessary.","Help the product development team visualize, architect, and document the concept design based on product requirements. This includes creating wireframes, mock-ups, process flows, and specifications.","Create static and interactive design presentations to key members and executive management for review and approval."]
        requirements=["1+ years of industry experience","Strong design portfolio","Expert knowledge of Adobe Creative Suite","Expert knowledge of Axure RP Pro","Understanding of how experience design works in harmony with visual design.","Good insight into current web design trends and related creative spaces.","Immaculate attention to detail; must be pixel-perfect","Excellent communication skills, both written and oral","Ability to achieve quality results on a tight deadline","Motion prototyping is a plus"]
        skills=[]
        additionalAttributes=[]
        
        self.buildGaikiObject(title,responsibilities,requirements,skills,additionalAttributes)
        json_testInstance=json.dumps(self.g_parser.makeJsonInstance(self.currentJob),sort_keys=True,indent=4, separators=(',', ': '))
        
        json_testInstanceRequested=self.socket.read()

        self.assertEqual(json_testInstance,json_testInstanceRequested)

        self.socket.close()

    def test_GetSingleInstanceBestMatch(self):
        print "Running Test for GET /jobs/jr"
        self.socket=urllib.urlopen(self.baseUrl+"jobs/jr")
        currentJob=GaikiJob()
        title="Jr. User Experience Designer"
        responsibilities=[ "Work closely with the UIX Director, Art Director, and UIX Engineers to ensure design concepts are executed as proposed, with the ability to update or revamp changes or solutions where necessary.","Help the product development team visualize, architect, and document the concept design based on product requirements. This includes creating wireframes, mock-ups, process flows, and specifications.","Create static and interactive design presentations to key members and executive management for review and approval."]
        requirements=["1+ years of industry experience","Strong design portfolio","Expert knowledge of Adobe Creative Suite","Expert knowledge of Axure RP Pro","Understanding of how experience design works in harmony with visual design.","Good insight into current web design trends and related creative spaces.","Immaculate attention to detail; must be pixel-perfect","Excellent communication skills, both written and oral","Ability to achieve quality results on a tight deadline","Motion prototyping is a plus"]
        skills=[]
        additionalAttributes=[]
            
        self.buildGaikiObject(title,responsibilities,requirements,skills,additionalAttributes)
        json_testInstance=json.dumps(self.g_parser.makeJsonInstance(self.currentJob),sort_keys=True,indent=4, separators=(',', ': '))
            
        json_testInstanceRequested=json.dumps(json.loads(self.socket.read())[0],sort_keys=True,indent=4, separators=(',', ': '))
        
        self.assertEqual(json_testInstance,json_testInstanceRequested)
            
        self.socket.close()

# def test_JobCount(self):


#def test_


if __name__ == '__main__':
    unittest.main()