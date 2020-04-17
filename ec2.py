import boto3
import botocore
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

def list_ec2_volumes(project):
    the_volumes = []

    if project:
        filters = [{'Name': 'tag:Project', 'Values': [project]}]
        the_volumes = ec2.volumes.filter(Filters = filters)
    else:
        the_volumes = ec2.volumes.all()
    
    return the_volumes

@click.group()
def cli():
    "AWS CLI scripts"

@cli.group("instances")
def instances():
    "Commands for instances"

@instances.command("list")
@click.option("--project", default=None, help="Only instances for project (tag Project:<name>)")
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
@click.option("--project", default=None, help="Only instances for project (tag Project:<name>)")
def stop_ec2_instances(project):
    "Stop EC2 instances"
    the_instances = list_ec2_instaces(project)

    for i in the_instances:
        print("Stopping {0}...".format(i.id))
        i.stop()

@instances.command("start")
@click.option("--project", default=None, help="Only instances for project (tag Project:<name>)")
def stop_ec2_instances(project):
    "Start EC2 instances"
    the_instances = list_ec2_instaces(project)

    for i in the_instances:
        print("Starting {0}...".format(i.id))
        i.start()

@cli.group("volumes")
def instances():
    "Commands for volumes"

@instances.command("all_list")
@click.option("--project", default=None, help="Only instances for project (tag Project:<name>)")
def get_all_ec2_volumes(project):
    "Get all volumes"
    the_volumes = list_ec2_volumes(project)

    for v in the_volumes:
        print(v)

@instances.command("instances_volumes")
@click.option("--project", default=None, help="Only instances for project (tag Project:<name>)")
def stop_ec2_volumes(project):
    "Get volumes of EC2 instances"
    the_instances = list_ec2_instaces(project)
    the_volumes = []

    for i in the_instances:
        for v in i.volumes.all():
            the_volumes.append(v)

    for v in the_volumes:
        print(", ".join((
            v.id,
            v.state,
            str(v.size) + "GiB",
            v.encrypted and "Encrypted" or "Not Encrypted"
        )))

@instances.command("snapshot")
@click.option("--project", default=None, help="Only instances for project (tag Project:<name>)")
def snapshot_ec2_instances(project):
    "Create snapshots of volumes of EC2 instances"
    the_instances = list_ec2_instaces(project)

    for i in the_instances:
        try:
            print("Stopping {0}...".format(i.id))
            i.stop()
        except botocore.exceptions.ClientError as e:
            print("Could not stop instance {0}.".format(i.id) + str(e))
        i.wait_until_stopped()
        for v in i.volumes.all():
            print("Snapshot for volume {0}, instance {1}...".format(v.id, i.id))
            v.create_snapshot()
        print("Start {0}...".format(i.id))
        i.start()
        try:
            print("Start {0}...".format(i.id))
            i.start()
        except botocore.exceptions.ClientError as e:
            print("Could not start instance {0}.".format(i.id) + str(e))

if __name__ == "__main__":
    cli()