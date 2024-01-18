
import os
import reframe as rfm
import reframe.utility.sanity as sn

class BaseSpackTest(rfm.RegressionTest):
    build_system = 'Spack'

    @run_after('performance')
    def upload_results(self):
        from pymongo import MongoClient
        # Get user:password string
        userpass = os.environ['MONGODB_USER_PASSWORD']
        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        CONNECTION_STRING = f"mongodb+srv://{userpass}@cluster0.x8ncpxi.mongodb.net/PerformanceMonitoring"
        # Create a connection using MongoClient.
        client = MongoClient(CONNECTION_STRING)
        # Create the new entry dictionary
        entry = {
            "Spack specs": self.build_system.specs,
            "Environment vars": self.env_vars,
        }
        entry.update(self.perfvalues._MappingView__mapping)
        # Create the database for our example (we will use the same database throughout the tutorial
        collection = client['PerformanceMonitoring'][self.mongodb_collection]
        collection.insert_one(entry)
