
import eosfactory.core.setup as setup
setup.node_api = "eosjs"

import unittest
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE, Verbosity.DEBUG])

CONTRACT_WORKSPACE = "_wslqwjvacdyugodewiyd"

class Test(unittest.TestCase):

    def run(self, result=None):
        super().run(result)
        print('''
=============================================================================
==============================================================================
''')

    @classmethod
    def setUpClass(cls):
        SCENARIO('''
        Create a contract from template, then build and deploy it.
        ''')
        reset()

        # setup.is_print_command_line = True        
        create_master_account("master")

        COMMENT('''
        Create test accounts:
        ''')
        create_account("alice", master)
        create_account("carol", master)
        create_account("bob", master)

    def test_01(self):
        COMMENT('''
        Create, build and deploy the contract:
        ''')

        create_account("host", master)

        contract = Contract(host, project_from_template(
            CONTRACT_WORKSPACE, template="01_hello_world", 
            remove_existing=True))
        contract.build()
        contract.deploy()
        contract.code()
        return
        COMMENT('''
        Test an action for Alice, including the debug buffer:
        ''')
        host.push_action(
            "hi", {"user":alice}, permission=(alice, Permission.ACTIVE))
        self.assertTrue("alice" in DEBUG())

        COMMENT('''
        Test an action for Carol, including the debug buffer:
        ''')
        host.push_action(
            "hi", {"user":carol}, permission=(carol, Permission.ACTIVE))
        self.assertTrue("carol" in DEBUG())

        COMMENT('''
        WARNING: This action should fail due to being duplicate!
        ''')
        with self.assertRaises(DuplicateTransactionError):
            host.push_action(
                "hi", {"user":carol}, permission=(carol, Permission.ACTIVE))

        COMMENT('''
        WARNING: This action should fail due to authority mismatch!
        ''')
        with self.assertRaises(MissingRequiredAuthorityError):
            host.push_action(
                "hi", {"user":carol}, permission=(bob, Permission.ACTIVE))
 
        contract.delete()


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        # get_wallet().private_keys()
        get_wallet().stop()
        # stop()


if __name__ == "__main__":
    unittest.main()
