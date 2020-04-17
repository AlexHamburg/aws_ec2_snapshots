from setuptools import setup

setup(
    name="aws_ec2_scripts",
    version="0.1",
    author="Oleksandr Trunov",
    author_email="oleksandr.trunov@gmail.com",
    description="Scripts to manage for AWS EC2",
    license="GPLv3+",
    pakages=["ec2"],
    url="https://github.com/AlexHamburg/aws_ec2_snapshots",
    install_requires=[
        "click",
        "boto3"
    ],
    entry_points='''
        [console_scripts]
        ec2=ec2.ec2:cli
    '''
)