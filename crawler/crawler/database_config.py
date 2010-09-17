from ConfigParser import SafeConfigParser

class DatabaseConfig(object):
    """
    Allows to fetch Database properties
    """
    
    def __init__(self, dbtype='mysql', cfg='database.cfg'):
        """
        while allocating the class, dbtype can be passed as parameter, like;
        db = Database(dbtype='sqlite')
        """
        self.dbtype = dbtype
        if self.dbtype != 'mysql':
            print "Unsupported database type : '" + self.dbtype + "'"

        self.configfile = cfg
        self.config = SafeConfigParser({'username':'root', 'password':'', 'host':'localhost', 'database':'bookcrawler'})
        self.config.read(self.configfile)
        self.username = self.config.get(self.dbtype, 'username')
        self.password = self.config.get(self.dbtype, 'password')
        self.host = self.config.get(self.dbtype, 'host')
        self.database = self.config.get(self.dbtype, 'database')

    def get_dialect(self):
        return "%s://%s:%s@%s/%s"%(self.dbtype, self.username, self.password, self.host, self.database)
