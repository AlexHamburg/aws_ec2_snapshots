import boto3
import click

session = boto3.Session(profile_name="developer")
ec2 = session.resource("ec2")

def list_ec2_instaces(project):
    the_instances = []

    if project:
        filters = [{'Name': 'tag:Project', 'Values': [project]}]
        the_instances = ec2.instances.filter(Filters = filters)
    else:
        the_instances = ec2.instances.all()
    
    return the_instances

@click.group()
def instances():
    "Commands for instances"

@instances.command("list")
@click.option("--project", default=None, help="Omly instances for project (tag Project:<name>)")
def get_ec2_instances(project):
    "Get all EC2 instances"
    the_instances = list_ec2_instaces(project)

    for i in the_instances:
        tags = {t["Key"]: t["Value"] for t in i.tags or []}
        print(",".join((
            i.id, 
            i.instance_type, 
            i.placement["AvailabilityZone"], 
            i.state["Name"], 
            i.public_dns_name, 
            tags.get('Project', '<no project>'))))

@instances.command("stop")
@click.option("--project", default=None, help="Omly instances for project (tag Project:<name>)")
def stop_ec2_instances(project):
    "Stop EC2 instances"
    the_instances = list_ec2_instaces(project)

    for i in the_instances:
        print("Stopping {0}...".format(i.id))
        i.stop()

@instances.command("start")
@click.option("--project", default=None, help="Omly instances for project (tag Project:<name>)")
def stop_ec2_instances(project):
    "Start EC2 instances"
    the_instances = list_ec2_instaces(project)

    for i in the_instances:
        print("Starting {0}...".format(i.id))
        i.start()

if __name__ == "__main__":
    instances()