# -*- coding: utf-8 -*-



import base64
import logging



from suds.client import Client
from suds.transport.https import HttpAuthenticated
from suds import WebFault



IFOLDERWS_LOGGER_NAME = '{0}.pyFolder.iFolderWS'



class iFolderWS:



    def __init__ (self, cm):
        self.cm = cm
        self.__setup_suds_client ()
        self.__setup_logger ()



    def __setup_logger (self):
        self.logger = logging.getLogger (
            IFOLDERWS_LOGGER_NAME.format (self.cm.get_username ()))



    def __setup_suds_client (self):

        # Emulate the new client behavior, for reference see 
        # src/core/Domain/DomainAgent.cs:617 in the Simias source code.

        usernameBase64 = base64.b64encode (self.cm.get_username ())
        passwordBase64 = base64.b64encode (self.cm.get_password ())

        transport = HttpAuthenticated (username=usernameBase64,
                                       password=passwordBase64)

        self.client = Client (self.cm.get_ifolderws (), transport=transport)



    def create_ifolder (self, Name, Description='', SSL=False,
                        EncryptionAlgorithm='', PassPhrase=''):

        try:
            return self.client.service.CreateiFolder (
                Name, Description, SSL, EncryptionAlgorithm, PassPhrase)

        except WebFault, wf:
            self.logger.error (wf)
            raise



    def delete_ifolder (self, iFolderID):

        try:
            self.client.service.DeleteiFolder (iFolderID)

        except WebFault, wf:
            self.logger.error (wf)
            raise



    def get_all_ifolders (self):

        try:
            iFolderSet = self.client.service.GetiFolders (0, 0)

            if iFolderSet.Total > 0:
                return iFolderSet.Items.iFolder

            return None

        except WebFault, wf:
            self.logger.error (wf)
            raise



    def get_ifolder_as_entry (self, iFolderID):

        try:
            iFolderEntrySet = self.client.service.GetEntries (
                iFolderID, iFolderID, 0, 1)

            if iFolderEntrySet.Total > 0:
                for iFolderEntry in iFolderEntrySet.Items.iFolderEntry:
                    return iFolderEntry

            return None

        except WebFault, wf:
            self.logger.error (wf)
            raise



    def get_latest_change (self, iFolderID, EntryID):

        try:
            ChangeEntrySet = self.client.service.GetChanges (
                iFolderID, EntryID, 0, 1)

            if ChangeEntrySet.Total > 0:
                for Change in ChangeEntrySet.Items.ChangeEntry:
                    return Change

            return None

        except WebFault, wf:
            self.logger.error (wf)
            raise



    def get_entry_by_path (self, iFolderID, Path):

        try:
            return self.client.service.GetEntryByPath (iFolderID, Path)

        except WebFault, wf:
            self.logger.error (wf)
            raise



    def get_entries_by_name (self, iFolderID, ParentID, Operation, Pattern,
                             Index, Max):

        try:
            iFolderEntrySet = self.client.service.GetEntriesByName (
                iFolderID,
                ParentID,
                Operation,
                Pattern,
                Index,
                Max)

            if iFolderEntrySet.Total > 0:
                return iFolderEntrySet.Items.iFolderEntry

            return None

        except WebFault, wf:
            self.logger.error (wf)
            raise



    def get_children_by_ifolder (self, iFolderID):

        try:
            Operation = self.get_search_operation ()
            iFolderEntrySet = self.client.service.GetEntriesByName (
                iFolderID, iFolderID, Operation.Contains, '.', 0, 0)

            if iFolderEntrySet.Total > 0:
                return iFolderEntrySet.Items.iFolderEntry

            return None

        except WebFault, wf:
            self.logger.error (wf)
            raise



    def get_ifolder (self, iFolderID):

        try:
            return self.client.service.GetiFolder (iFolderID)

        except WebFault, wf:
            self.logger.error (wf)
            raise



    def get_entry (self, iFolderID, EntryID):

        try:
            return self.client.service.GetEntry (iFolderID, EntryID)

        except WebFault, wf:
            self.logger.error (wf)
            raise



    def open_file_read (self, iFolderID, EntryID):

        try:
            return self.client.service.OpenFileRead (iFolderID, EntryID)

        except WebFault, wf:
            self.logger.error (wf)
            raise



    def read_file (self, Handle):

        try:
            return self.client.service.ReadFile (
                Handle, self.cm.get_soapbuflen ())

        except WebFault, wf:
            self.logger.error (wf)
            raise



    def open_file_write (self, iFolderID, EntryID, Size):

        try :
            return self.client.service.OpenFileWrite (
                iFolderID, EntryID, Size)

        except WebFault, wf:
            self.logger.debug (wf)
            raise



    def write_file (self, Handle, Data):

        try:
            self.client.service.WriteFile (Handle, Data)

        except WebFault, wf:
            self.logger.error (wf)
            raise



    def close_file (self, Handle):

        try:
            self.client.service.CloseFile (Handle)

        except WebFault, wf:
            self.logger.error (wf)
            raise



    def create_entry (self, iFolderID, ParentID, Name, Type):

        try:
            return self.client.service.CreateEntry (
                iFolderID, ParentID, Type, Name)

        except WebFault, wf:
            self.logger.error (wf)
            raise



    def delete_entry (self, iFolderID, EntryID):

        try:
            self.client.service.DeleteEntry (iFolderID, EntryID)

        except WebFault, wf:
            self.logger.error (wf)
            raise



    def add_member (self, iFolderID, UserID, Rights):

        try:
            self.client.service.AddMember (iFolderID, UserID, Rights)

        except WebFault, wf:
            self.logger.error (wf)
            raise



    def get_users_by_search (self, Property, Operation, Pattern,
                             Index, Max):

        try:
            iFolderUserSet = self.client.service.GetUsersBySearch (
                Property, Operation, Pattern, Index, Max)

            if iFolderUserSet.Total > 0:
                return iFolderUserSet.Items.iFolderUser

            return None

        except WebFault, wf:
            self.logger.error (wf)
            raise



    def set_member_rights (self, iFolderID, UserID, Rights):

        try:
            self.client.service.SetMemberRights (iFolderID, UserID, Rights)

        except WebFault, wf:
            self.logger.error (wf)
            raise



    def get_authenticated_user (self):

        try:
            return self.client.service.GetAuthenticatedUser ()

        except WebFault, wf:
            self.logger.error (wf)
            raise



    def get_ifolder_entry_type (self):
        return self.client.factory.create ('iFolderEntryType')



    def get_change_entry_action (self):
        return self.client.factory.create ('ChangeEntryAction')



    def get_rights (self):
        return self.client.factory.create ('Rights')



    def get_search_property (self):
        return self.client.factory.create ('SearchProperty')



    def get_search_operation (self):
        return self.client.factory.create ('SearchOperation')
