# Designed and Developed by Matthew Garcia


# This is an interface class that will allow my to keep my code consistent when
# reusing this code in the future. Other developers can take Parser objects as
# input on their server and then implement many different parsing mechanisms
# that will be intergrated while keeping the server code universal in nature.
class Parser():
    
   
    
    def __init__(self,url):
        self.url=url
        print "Parent Constructor"
    def parse(self):
        print "Parent Tokenizer"
    def getInstance(self):
        print "Parent Instance finder"
    def getAllInstances(self):
        print "Parent Instances finder"