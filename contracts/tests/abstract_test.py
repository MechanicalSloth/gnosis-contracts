# contracts package
from contracts import ROOT_DIR
# ethereum pacakge
from ethereum import tester as t
from ethereum.tester import keys, accounts, TransactionFailed, ABIContract, GAS_PRICE
from ethereum import _solidity
from ethereum.abi import ContractTranslator
# standard libraries
from codecs import encode, decode
from unittest import TestCase
from os import walk
import string

class GasCounter(object):

    def __init__(self, account, state):
        self.account = account
        self.state = state
        self.balance_on_enter = 0
        self.balance_on_exit = 0

    def __enter__(self):
        self.balance_on_enter = self.state.get_balance(self.account)
        return self

    def __exit__(self, *args):
        self.balance_on_exit = self.state.get_balance(self.account)

    def gas_cost(self):
        return (self.balance_on_enter - self.balance_on_exit)/GAS_PRICE

class AbstractTestContracts(TestCase):

    HOMESTEAD_BLOCK = 1150000
    CONTRACT_DIR = 'solidity'

    def __init__(self, *args, **kwargs):
        super(AbstractTestContracts, self).__init__(*args, **kwargs)
        self.s = t.state()
        self.s.state.block_number = self.HOMESTEAD_BLOCK
        t.gas_limit = 10000000  # To allow estimation of gas costs larger than 4.7M

    def gas_counter(self):
        return GasCounter(accounts[0], self.s.state)

    @staticmethod
    def is_hex(s):
        return all(c in string.hexdigits for c in s)

    def get_dirs(self, path):
        abs_contract_path = '{}/{}'.format(ROOT_DIR, self.CONTRACT_DIR)
        sub_dirs = [x[0] for x in walk(abs_contract_path)]
        extra_args = ' '.join(['{}={}'.format(d.split('/')[-1], d) for d in sub_dirs])
        path = '{}/{}'.format(abs_contract_path, path)
        return path, extra_args

    def contract_at(self, address, abi):
        return ABIContract(self.s, abi, address)

    def create_abi(self, path):
        path, extra_args = self.get_dirs(path)
        abi = _solidity.compile_last_contract(path, combined='abi', extra_args=extra_args)['abi']
        return ContractTranslator(abi)

    def create_contract(self, path, params=None, libraries=None, sender=None):
        path, extra_args = self.get_dirs(path)
        if params:
            params = [x.address if isinstance(x, t.ABIContract) else x for x in params]
        if libraries:
            for name, address in libraries.items():
                if type(address) == str:
                    if self.is_hex(address):
                        libraries[name] = address
                    else:
                        libraries[name] = encode(address, 'hex')
                elif isinstance(address, t.ABIContract):
                    libraries[name] = encode(address.address, 'hex')
                else:
                    raise ValueError
        return self.s.abi_contract(None,
                                   path=path,
                                   constructor_parameters=params,
                                   libraries=libraries,
                                   language='solidity',
                                   extra_args=extra_args,
                                   sender=keys[sender if sender else 0])

