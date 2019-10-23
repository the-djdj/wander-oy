from exception import CommandException

import os
from subprocess import Popen, PIPE, STDOUT
from yaml import safe_load as load, YAMLError


class Output:
    ''' The output class. This creates a new object for managing the output,
        and provides an array of useful methods for console output.'''


    def __init__(self):
        ''' The constructor. This assigns the default values used in the
            object.'''
        pass



class Commands:
    ''' The commands class. This allows for commands to be run as a subprocess
        and for the results of that command to be stored.'''


    def call(self, command, environment):
        ''' The call command. This executes a command on a subprocess and
            returns the output that that command generates.'''
        # Store the raw output of the command
        raw = Popen(command, shell=True, env=environment,
                        stdout=PIPE,
                        stderr=STDOUT)

        # Get the stdout and stderr from the command
        stdout, stderr = raw.communicate(command)

        # Return the results of the command
        return stdout, stderr



class YAMLObject:
    ''' The YAMLObject class. This is the object which is loaded from a YAML
        file.'''


    def __init__(self, commands):
        ''' The init method. This creates a new YAML object.'''
        # Create all of the lists for the application
        self.preamble = dict()
        self.elements = dict()

        # Create the command system
        self.commands = commands


    def load(self, filename):
        ''' The system that loads the object yaml file.'''
        # Load the YAML file
        with open(filename, 'r') as stream:

            # Read from the stream
            try:

                # Store the file contents
                elements = load(stream)

                # Sort out the preamble
                preamble = elements['preamble']

                # Sort out the elements
                self.elements = elements['elements']

            # If the syntac is improper, indicate as such
            except YAMLError as error:
                print(error)

        # Process the preamble into a usable environment
        self.environment = os.environ.copy()

        # Iterate through each preamble element
        for element in preamble:

            # Add the key-value pair to the environment
            if self.environment.get(element) is None:
                self.environment[element] = preamble[element]

            else:
                self.environment[element] += ':' + preamble[element]


    def run(self, elements):
        ''' The run method, which runs a list of commands, and returns the
            results.'''
        # Create a list for the result of the commands
        result = list()

        # Iterate through each of the commands in the preamble.
        for element in elements:
            # Get the response of the command
            command = self.commands.call(element, self.environment)

            # Check if there were any errors
            if command[1] is not None:
                raise CommandException(command[1])

            # And append the output
            result.append(command[0])

        # And return the output
        return result
