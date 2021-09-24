
from slither.slither import Slither

import sha3
class Function_info():
    def __init__(self,solidity_file:str, contract_name:str):
        self.solidity_file=solidity_file
        self.contract_name=contract_name.lstrip().rstrip()

    def functions_dict_slither(self):
        '''
        get function info
        :param contract_file:
        :param contract_name:
        :return: list of (function: r_sv_list: w_sv_list)
        '''
        # Init slither
        slither = Slither(self.solidity_file)

        # Get the contract
        contract = slither.get_contract_from_name(self.contract_name)

        if not contract:
            return {}

        function_dict = {}

        i = 2 # 0 is reserved for constructor and 1 for fallback
        for f in contract.functions:
            if f.name.__eq__('slitherConstructorVariables'): continue
            if f.name.__eq__('slitherConstructorConstantVariables'): continue

            if f.is_constructor: continue


            # only consider public, external functions
            summary=f.get_summary()
            if len(summary)>=3:
                if summary[2] not in ['public','external']:
                    continue

            if f.name.__eq__('fallback'):
                func_hash = 'None'
            else:
                func_hash = self.get_function_id(f.full_name)

            r_list = []
            f_r = f.all_conditional_state_variables_read()


            if len(f_r) > 0:
                # consider state variables read in all conditions
                r_list = [sv.name for sv in f_r]
                # # only consider state variables read in require and assert statements
                # r_list = [sv.name for sv in f_r if f.is_reading_in_require_or_assert(sv.name)]

            w_list = []
            f_w = f.all_state_variables_written()
            if len(f_w) > 0:
                w_list = [sv.name for sv in f_w]

            # if len(r_list) != 0 or len(w_list) != 0:
            #     if f.name.__eq__('fallback'):
            #         function_dict['f1'] = [f.name, r_list, w_list, func_hash, 1]
            #     else:
            #         function_dict['f' + str(i)] = [f.full_name, r_list, w_list, func_hash,i]
            #         i = i + 1

            if f.name.__eq__('fallback'):
                function_dict['f1'] = [f.name, r_list, w_list, func_hash, 1]
            else:
                function_dict['f' + str(i)] = [f.full_name, r_list, w_list, func_hash,i]
                i = i + 1

        if 'f1' not in function_dict.keys():
            function_dict['f1'] = ["fallback", [], [], "None", 1]

        function_dict['f0'] = ["constructor", [], [], "", 0]

        return function_dict

    def get_function_id(self,sig: str) ->str:
        """'
            Return the function id of the given signature
        Args:
            sig (str)
        Return:
            (int)
        """
        s = sha3.keccak_256()
        s.update(sig.encode("utf-8"))
        return s.hexdigest()[:8]




if __name__=='__main__':
    # ftn_info = Function_info('/home/wei/PycharmProjects/Contracts/_wei/wei_test.sol', 'wei_test')
    #ftn_info=Function_info('/home/wei/PycharmProjects/Contracts/_wei/HoloToken.sol', 'HoloToken')
    # ftn_info = Function_info('/home/wei/PycharmProjects/Contracts/_wei/wei_test.sol', 'wei_test')
    # ftn_info = Function_info('/home/wei/PycharmProjects/Contracts/_wei/play_me_quiz.sol', 'play_me_quiz')
    # ftn_info = Function_info('/home/wei/PycharmProjects/Contracts/example_contracts/ZetTokenMint.sol', 'ZetTokenMint')
    # ftn_info = Function_info('/home/wei/PycharmProjects/Contracts/example_contracts/AaronTestCoin.sol', 'AaronTestCoin')
    ftn_info = Function_info('/home/wei/PycharmProjects/Contracts/example_contracts/DxLockEth4Rep.sol', 'Avatar')

    ftn_dict= ftn_info.functions_dict_slither()
    print("===== ftn_dict ====")
    for key, value in ftn_dict.items():
        print("\t{}:  {}".format(key, value))
    pass



    # a=[24, 29, 189, 34, 118, 194, 265, 39]
    # pairs=get_valid_pc_interval(a,1000)
    # if pc_is_valid(90,pairs):
    #     print(f'90 is in {pairs}')



