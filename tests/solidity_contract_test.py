from pathlib import Path


from batin.solidity.soliditycontract import SolidityContract
from tests import BaseTestCase
import batin.util as helper
TEST_FILES = Path(__file__).parent / "testdata/input_contracts"
solc_binary = helper._init_solc_binary("v0.5.0")


class SolidityContractTest(BaseTestCase):
    def test_get_source_info_without_name_gets_latest_contract_info(self):
        input_file = TEST_FILES / "multi_contracts.sol"
        contract = SolidityContract(str(input_file), solc_binary=solc_binary)

        code_info = contract.get_source_info(116)
        self.assertEqual(code_info.filename, str(input_file))
        self.assertEqual(code_info.lineno, 14)
        self.assertEqual(code_info.code, "msg.sender.transfer(2 ether)")

    def test_get_source_info_with_contract_name_specified(self):
        input_file = TEST_FILES / "multi_contracts.sol"
        contract = SolidityContract(
            str(input_file), name="Transfer1", solc_binary=solc_binary
        )

        code_info = contract.get_source_info(116)

        self.assertEqual(code_info.filename, str(input_file))
        self.assertEqual(code_info.lineno, 6)
        self.assertEqual(code_info.code, "msg.sender.transfer(1 ether)")

    def test_get_source_info_with_contract_name_specified_constructor(self):
        input_file = TEST_FILES / "constructor_assert.sol"
        contract = SolidityContract(
            str(input_file), name="AssertFail", solc_binary=solc_binary
        )

        code_info = contract.get_source_info(75, constructor=True)

        self.assertEqual(code_info.filename, str(input_file))
        self.assertEqual(code_info.lineno, 6)
        self.assertEqual(code_info.code, "assert(var1 > 0)")
