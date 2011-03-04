# -*- coding: utf-8 -*-

from suds import WebFault
import logging

class Policy:
    def __init__ (self, pyFolder):
        self.pyFolder = pyFolder
        self.logger = logging.getLogger ('pyFolder.Policy')
    
    def add_directory (self, ifolder_id, entry_id, path):
        raise NotImplementedError

    def add_file (self, ifolder_id, entry_id, path):
        raise NotImplementedError

    def modify_directory (self, ifolder_id, entry_id, path):
        raise NotImplementedError

    def modify_file (self, ifolder_id, entry_id, path):
        raise NotImplementedError
    
    def delete_directory (self, ifolder_id, entry_id, path):
        raise NotImplementedError

    def delete_file (self, ifolder_id, entry_id, path):
        raise NotImplementedError

    def add_remote_directory (self, ifolder_id, parent_id, path):
        raise NotImplementedError
    
    def add_remote_file (self, ifolder_id, parent_id, path):
        raise NotImplementedError

    def modify_remote_directory (self, ifolder_id, entry_id, path):
        raise NotImplementedError
    
    def modify_remote_file (self, ifolder_id, entry_id, path):
        raise NotImplementedError

    def delete_remote_directory (self, ifolder_id, entry_id, path):
        raise NotImplementedError

    def delete_remote_file (self, ifolder_id, entry_id, path):
        raise NotImplementedError

class DEFAULT (Policy):
    """
    The DEFAULT Policy has the following features:

    [ UPDATE behavior ]
    - If an entry has any kind of remote change, the changes are also applied
      locally.
    - If a new entry is added remotely, it is also added to the local
      repository.

    [ COMMIT behavior ]
    - If an entry has local changes (modify, deletion), changes are committed.
    - New locally added entries are committed. If, at the time of the commit,
      a remote entry having the same path and name of the one that is being
      committed has been added, then the entries are renamed, adding a suffix
      with the `OwnerUserName' and both the copies are saved on the server, so
      that they will be available for all the users at the next update.
    """
    def add_directory (self, ifolder_id, entry_id, path):
        try:
            self.pyFolder.mkdir (path)
        except OSError:
            pass
        return True

    def add_file (self, ifolder_id, entry_id, path):
        self.pyFolder.fetch (ifolder_id, entry_id, path)
        return True

    def modify_directory (self, ifolder_id, entry_id, path):
        return True

    def modify_file (self, ifolder_id, entry_id, path):
        self.pyFolder.fetch (ifolder_id, entry_id, path)
        return True
    
    def delete_directory (self, ifolder_id, entry_id, path):
        try:
            self.pyFolder.rmdir (path)
        except OSError:
            pass
        return True

    def delete_file (self, ifolder_id, entry_id, path):
        try:
            self.pyFolder.delete (path)
        except OSError:
            pass
        return True

    def add_remote_directory (self, iFolderID, ParentID, Path):
        try:
            iFolderEntry = \
                self.pyFolder.remote_mkdir (iFolderID, ParentID, Path)
            return iFolderEntry
        except WebFault, wf:
            NewPath = '{0}-{1}'.format (Path, self.pyFolder.cm.get_username ())
            self.pyFolder.rename (Path, NewPath)
            self.pyFolder.add_hierarchy_locally (iFolderID, ParentID, Path)
            return self.add_remote_directory (iFolderID, ParentID, NewPath)
    
    def add_remote_file (self, iFolderID, ParentID, Path):
        try:
            iFolderEntry = \
                self.pyFolder.remote_create_file (iFolderID, ParentID, Path)
            return iFolderEntry
        except WebFault, wf:
            OriginalException = wf.fault.detail.detail.OriginalException._type

            if OriginalException == \
                    'iFolder.WebService.EntryAlreadyExistException':
                NewPath = '{0}-{1}'.format (Path, self.pyFolder.cm.get_username ())
                self.pyFolder.rename (Path, NewPath)
                self.pyFolder.add_entry_locally (iFolderID, ParentID, Path)
                return self.add_remote_file (iFolderID, ParentID, NewPath)

            elif OriginalException == 'System.NullReferenceException':
                # AncestoriFolderEntry = \
                #     self.pyFolder.find_closest_ancestor_remotely_alive (\
                #     iFolderID, Path)
                # ex. Suppose we have the hierarchy `/foo/bar/bla' and
                #     `bar' gets remotely removed.
                #
                #     We have to find the closest ancestor to `bla' which
                #     is still remotely `alive'. In this case, it is `/foo'.
                #     Then, we rename locally the part of the hierarchy 
                #     which is direct descendant of `foo' adding the 
                #     `conflicted' prefix.
                #     So, locally, we would have:
                #
                #               /foo/bar-conflicted/bla
                #
                #     Finally, we add the hierarchy remotely. We may take
                #     advantage of the `pyFolder.__commit_added_entries'
                #     method.
                #     We should also OPTIONALLY remove from the local database
                #     the old hierarchy. The latter part, could also be done
                #     at the next update, since pyFolder will detect the 
                #     deletions and apply the changes locally.

                return None

    def modify_remote_directory (self, ifolder_id, entry_id, path):
        return True
    
    def modify_remote_file (self, iFolderID, EntryID, Path):
        try:
            self.pyFolder.remote_file_write (iFolderID, EntryID, Path)
            return True
        except WebFault, wf:
            return False
    
    def delete_remote_directory (self, iFolderID, iFolderEntryID, Path):
        try:
            self.pyFolder.remote_rmdir (iFolderID, iFolderEntryID, Path)
        except WebFault, wf:
            pass
        return True

    def delete_remote_file (self, iFolderID, iFolderEntryID, Path):
        try:
            self.pyFolder.remote_delete (iFolderID, iFolderEntryID, Path)
        except WebFault, wf:
            pass
        return True

class PolicyFactory:
    @staticmethod
    def create (policy, pyFolder):
        if policy == 'DEFAULT':
            return DEFAULT (pyFolder)
    
    @staticmethod
    def get_factories ():
        return ['DEFAULT', ]
