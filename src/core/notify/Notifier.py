# -*- coding: utf-8 -*-



class Notifier:
    


    ## Notifies the user about the given information message.
    #
    #  @param title The title of the message.
    #  @param text The text of the message.
    
    def info (self, title, text):
        raise NotImplementedError



    ## Notifies the user about the given warning message.
    #
    #  @param title The title of the message.
    #  @param text The text of the message.

    def warning (self, title, text):
        raise NotImplementedError

    

    ## Notifies the user about the given error message.
    #
    #  @param title The title of the message.
    #  @param text The text of the message.

    def error (self, title, text):
        raise NotImplementedError
