from subprocess import check_output
from tests import BaseTestCase, TESTDATA, PROJECT_DIR, TESTS_DIR
from mock import patch

MYTH = str(PROJECT_DIR / "map")


def output_of(command):
    """
    :param command:
    :return:
    """
    return check_output(command, shell=True).decode("UTF-8")


class CommandLineToolTestCase(BaseTestCase):
    # def test_disassemble_code_correctly(self):
    #     command = "python3 {} disassemble --bin-runtime -c 0x5050".format(MYTH)
    #     self.assertIn("0 POP\n1 POP\n", output_of(command))


    def test_failure_json(self):
        command = "python3 {} analyze doesnt_exist.sol -o json".format(MYTH)
        print(output_of(command))
        self.assertIn(""""success": false""", output_of(command))

    def test_failure_text(self):
        command = "python3 {} analyze doesnt_exist.sol".format(MYTH)
        assert output_of(command) == ""

    def test_failure_jsonv2(self):
        command = "python3 {} analyze doesnt_exist.sol -o jsonv2".format(MYTH)
        self.assertIn(""""level": "error""" "", output_of(command))

    def test_analyze(self):
        solidity_file = str(TESTDATA / "input_contracts" / "origin.sol")
        contract_name='Origin'
        command = "python3 {} analyze {}:{} --solv 0.5.0".format(MYTH, solidity_file,contract_name)
        output=output_of(command)
        self.assertIn("115", output)






