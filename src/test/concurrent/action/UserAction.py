# -*- coding: utf-8 -*-



from Action import *



class UserAction (Action):



    def __init__ (self, User, pyFolder):
        Action.__init__ (self, User, pyFolder)
        self.Target = None
        self.Scenario = self.build_scenario ()



    def find_response (self, ClientActionList):

        # `Scenario' is a list of the possible actions done by pyFolder, 
        # in response to the execution of the current user action. Each
        # class that inherits from UserAction, should build its own scenario,
        # by redefining the build_scenario abstract method.

        for PossibleAction in self.Scenario:

            if PossibleAction in ClientActionList:
                return ClientActionList.remove (PossibleAction)

        return None



    def build_scenario (self):
        raise NotImplementedError
