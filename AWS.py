import boto3
rds = boto3.client('rds')

def list_aws_databases():
    try:
        dbs = rds.describe_db_instances()
        for db in dbs['DBInstances']:
            print("%s@s:%s %s)" % (db['MasterUsername'], db['Endpoint']['Address'], db['DBInstanceStatus']))
    except Exception as e:
        raise e
list_aws_databases()


def create_database():
    print("\n\r Create Database Instance")
    response = rds.create_db_instance(
        DBInstanceIdentifier='newdb',
        MasterUsername="testuser",
        MasterUserPassword="t1ck2099",
        DBInstanceClass="db.t2.micro",
        Engine="mysql",
        AllocatedStorage=5
    )

def delete_database():
    print("\n\r Create Database Instance")
    response = rds.delete_db_instance(
        DBInstanceIdentifier='newdb',
        SkipFinalSnapshot=True,
    )
    print(response)

