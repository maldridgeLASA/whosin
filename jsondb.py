'''
Simple JSON database to store key, name, and authorization values.
Author: Michael Aldridge
'''
import json
import logging


class db:
    '''Class containing all database code'''
    def __init__(self, datastore):
	'''Open the datastore file and read in the existing database from disk'''
        self.t3file = datastore
        logging.debug("Loading 't3'->'t1'")
        t3data=open(self.t3file)
        self.db=json.load(t3data)
        t3data.close()

    def add(self, key, name, auth, upsert=False):
	'''Add a key to the database, if upsert is set, update an existing key'''
        logging.info("Adding new key to system")
        if key in self.db: #check if key exists
            if upsert:
                self.db[key]={"name":name, "auth":auth}
                return True
            else:
                logging.error("name '%s' already exists with key %s; (is upsert set?)",name,key) 
                return False
        else:
            self.db[key]={"name":name, "auth": auth}
            logging.info("Added name %s with key %s to database", name, key)
            self._save()
            return False

    def remove(self, key):
	'''Remove an existing key from the network'''
        logging.info("Removing key from system")
        if key in self.db: #check if key exists
            del self.db[key]
            logging.info("Key id %s removed", key)
            self._save()
            return True
        else:
            logging.warning("Key does not exist")
            return True
        
    def lookup(self, key):
	'''Checks if the given key value exists in the database, and returns data if found'''
        logging.info("Looking up key %s")
        if key in self.db: #check if key exists
            logging.info("Key found")
            logging.debug("Returned data %s", self.db[key])
            return self.db[key]["name"], self.db[key]["auth"]
        else:
            logging.warning("Key not found")
            logging.debug("Key hash was %s", key)
            return None

    def namelist(self):
	'''Gets a list of names from the database'''
        names=[]
        logging.info("Retrieving list of names")
        for key in self.db.keys():
            names.append(self.db[key]["name"])
        logging.debug("%s", names)
        return names

    def _save(self):
	'''Writes the database to disk any time an operation is made that changes it'''
        logging.info("Syncing 't1'->'t3'")
        t3data=open(self.t3file, 'w')
        #sync t1data to t3data
        json.dump(self.db, t3data, indent=2)
        t3data.close()
