from exception import CommandException
from util import Output, YAMLObject

from subprocess import call


class Prerequisites(YAMLObject):
    ''' The class responsible for ensuring that a host meets the minimum
        requirements for building wander. It holds a list of requirement
        objects and checks each one.'''


    def __init__(self, commands):
        ''' The constructor. This creates the new system for checking that a
            host meets the necessary requirements for building wander.'''
        # Create the parent object
        YAMLObject.__init__(self, commands);

        # Store the command system
        self.commands = commands

        # Load the prerequisites list
        self.load('../prerequisites.yaml')


    def verify(self):
        ''' A simple method which checks that each of the requirements has been
            met.'''
        # Tell the user what's happening
        Output.header('Checking host prerequisites...')

        # Iterate through each of the prerequisites, and verify them
        for element in self.elements:
            Prerequisite(self.elements[element], self).verify()



class Prerequisite:
    ''' The prerequisite class, which stores information about a single
        prerequisite.'''


    def __init__(self, element, parent):
        ''' The init method, used to create a new prerequisite object which can
            be tested on the host system.'''
        # Store information about the prerequisite
        self.version     = str(element.get('version'))
        self.description = element.get('description') + " " + self.version
        self.link        = element.get('link')
        self.commands    = element.get('commands')

        # Extract the version information
        self.major, self.minor, self.revision = self.extrapolate(self.version)

        # Store the system for running commands
        self.parent = parent

        # Note that we've started the check
        Output.log(Output.PENDING, self.description)


    def verify(self):
        ''' The verify method, which checks that a requirement is valid, and
            prints that to the console.'''
        # Perform the tests
        Output.clear()
        Output.log(Output.TESTING, self.description)

        # Execute the test code
        version = self.parent.run(self.commands)[0]

        # Extrapolate the version information
        major, minor, revision = self.extrapolate(version)

        if major > self.major:
            # If the major is greater, we obviously have a newer version
            Output.clear()
            Output.log(Output.PASSED, self.description)

            # And return our result
            return True

        elif minor > self.minor:
            # If the minor is greater, we still have a newer version
            Output.clear()
            Output.log(Output.PASSED, self.description)

            # And return our result
            return True

        elif revision >= self.revision:
            # If the revision is greater or equal, we must have a newer version
            Output.clear()
            Output.log(Output.PASSED, self.description)

            # And return our result
            return True  

        # At this point, we obviously don't have the correct version
        Output.clear()
        Output.log(Output.FAILED, self.description)

        # And return our bad result
        return False


    def extrapolate(self, version):
        ''' A method which extracts the major, minor, and revision versions
            from a version string.'''
        # Try to extract the major version
        try:
            major = version.rsplit('.', 3)[0]
       
        except IndexError:
            major = 0

        # Try to extract the minor version
        try:
            minor = version.rsplit('.', 3)[1]

        except IndexError:
            minor = 0

        # Try to extract the revision
        try:
            revision = version.rsplit('.', 3)[2]

        except IndexError:
            revision = 0

        # And return our versions
        return major, minor, revision
