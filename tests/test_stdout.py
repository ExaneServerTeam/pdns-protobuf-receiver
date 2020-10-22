
import time
import unittest
import subprocess
import dns.resolver

my_resolver = dns.resolver.Resolver(configure=False)
my_resolver.nameservers = ['127.0.0.1']

class TestStdout(unittest.TestCase):
    def test1_listening(self):
        """test listening tcp socket"""
        cmd = ["python3", "-c", 
               "import pdns_protobuf_receiver; pdns_protobuf_receiver.start_receiver()", "-v"]
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
            time.sleep(2)
            proc.kill()
            
            o = proc.stdout.read()
            print(o)
        self.assertRegex(o, b"listening")
        
    def test2_protobuf(self):
        """test to receive protobuf message"""
        cmd = ["python3", "-c", 
               "import pdns_protobuf_receiver; pdns_protobuf_receiver.start_receiver()", "-v"]

        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
            for i in range(10):
                r = my_resolver.resolve('www.github.com', 'a')
                time.sleep(1)

            proc.kill()
            
            o = proc.stdout.read()
            print(o)
        self.assertRegex(o, b"CLIENT_QUERY")
        