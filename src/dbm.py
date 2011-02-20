from datetime import *
import sqlite3
import os

class DBM:
    Q_CREATE_TABLE_ENTRIES = \
        """
        CREATE TABLE entry (
           ifolder        TEXT REFERENCES ifolder (id),
           id             TEXT,
           mtime          timestamp,
           digest         TEXT,
           PRIMARY KEY (ifolder, id)
        )
        """

    Q_CREATE_TABLE_IFOLDERS = \
        """
        CREATE TABLE ifolder (
           id             TEXT PRIMARY KEY,
           mtime          timestamp
        )
        """

    Q_ADD_ENTRY = \
        """
        INSERT INTO entry VALUES (?, ?, ?, ?)
        """
    
    Q_UPDATE_ENTRY = \
        """
        UPDATE entry SET mtime=(?), digest=(?)
        WHERE ifolder=(?) AND id=(?)
        """
    
    Q_GET_ENTRY = \
        """
        SELECT * FROM entry AS e 
        WHERE e.ifolder=? AND e.id=?
        """

    Q_GET_MTIME_BY_ENTRY = \
        """
        SELECT e.mtime FROM entry AS e
        WHERE i.ifolder=? AND i.id=?
        """

    Q_GET_DIGEST_BY_ENTRY = \
        """
        SELECT e.digest FROM entry AS e
        WHERE e.ifolder=? AND e.id=?
        """
    Q_GET_ENTRIES_BY_IFOLDER = \
        """
        SELECT * FROM entry AS e WHERE e.ifolder=?
        """

    Q_ADD_IFOLDER = \
        """
        INSERT INTO ifolder VALUES (?, ?)
        """

    Q_UPDATE_IFOLDER = \
        """
        UPDATE ifolder SET mtime=(?)
        WHERE id=(?)
        """

    Q_GET_MTIME_BY_IFOLDER = \
        """
        SELECT i.mtime FROM ifolder AS i
        WHERE i.id=?
        """
    Q_GET_IFOLDERS = \
        """
        SELECT i.id, i.mtime FROM ifolder AS i
        """

    def __init__ (self, pathtodb):
        self.pathtodb = pathtodb
        self.cx = sqlite3.connect (pathtodb, detect_types=\
                                       sqlite3.PARSE_DECLTYPES| \
                                       sqlite3.PARSE_COLNAMES)

    def __create_tables (self):
        cu = self.cx.cursor ()
        cu.execute (DBM.Q_CREATE_TABLE_IFOLDERS)
        cu.execute (DBM.Q_CREATE_TABLE_ENTRIES)        

    def create_schema (self):
        try:
            self.__create_tables ()
        except sqlite3.OperationalError, oe:
            self.cx.close ()
            if os.path.isfile (self.pathtodb):
                os.remove (self.pathtodb)
            self.cx = sqlite3.connect (self.pathtodb)
            self.__create_tables ()
        finally:
            self.cx.commit ()

    def add_ifolder (self, ifolder):
        cu = self.cx.cursor ()
        cu.execute (DBM.Q_ADD_IFOLDER, (ifolder.ID, ifolder.LastModified))
        self.cx.commit ()

    def get_ifolders (self):
        cu = self.cx.cursor ()
        cu.execute (DBM.Q_GET_IFOLDERS)
        return cu.fetchall ()

    def update_ifolder (self, ifolder_id, mtime):
        cu = self.cx.cursor ()
        cu.execute (DBM.Q_UPDATE_IFOLDER, (mtime, ifolder_id))
        self.cx.commit ()

    def add_entry (self, ifolder_id, change, digest):
        cu = self.cx.cursor ()
        cu.execute (DBM.Q_ADD_ENTRY, (ifolder_id, change.ID, change.Time, digest))
        self.cx.commit ()

    def update_entry (self, ifolder_id, change, digest):
        cu = self.cx.cursor ()
        cu.execute (DBM.Q_UPDATE_ENTRY, \
                        (change.Time, digest, ifolder_id, change.ID))
        self.cx.commit ()
    
    def get_mtime_by_entry (self, ifolder, change):
        cu = self.cx.cursor ()
        cu.execute (DBM.Q_GET_ENTRY_MTIME, (ifolder.ID, change.ID))
        return cu.fetchone ()

    def get_digest_by_entry (self, ifolder, change):
        cu = self.cx.cursor ()
        cu.execute (DBM.Q_GET_ENTRY_DIGEST, (ifolder.ID, change.ID))
        return cu.fetchone ()

    def get_entry (self, ifolder_id, entry_id):
        cu = self.cx.cursor ()
        cu.execute (DBM.Q_GET_ENTRY, (ifolder_id, entry_id))
        return cu.fetchone ()

    def get_entries_by_ifolder (self, ifolder_id):
        cu = self.cx.cursor ()
        cu.execute (DBM.Q_GET_ENTRIES_BY_IFOLDER, (ifolder_id,))
        return cu.fetchall ()

    def __del__ (self):
        self.cx.commit ()
        self.cx.close ()