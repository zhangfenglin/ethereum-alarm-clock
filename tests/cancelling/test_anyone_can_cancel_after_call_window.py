import pytest

from ethereum.tester import (
    TransactionFailed,
    accounts,
    encode_hex,
)


deploy_contracts = [
    "CallLib",
    "TestCallExecution",
]


def test_anyone_can_cancel_after_call_window(deploy_client, deployed_contracts,
                                             deploy_future_block_call, deploy_coinbase,
                                             CallLib):
    client_contract = deployed_contracts.TestCallExecution

    target_block = deploy_client.get_block_number() + 300

    call = deploy_future_block_call(
        client_contract.setBool,
        target_block=target_block,
    )

    deploy_client.wait_for_block(call.target_block() + call.grace_period() + 1)

    assert call.is_cancelled() is False

    txn_h = call.cancel(_from=encode_hex(accounts[1]))
    txn_r = deploy_client.wait_for_transaction(txn_h)
    txn = deploy_client.get_transaction_by_hash(txn_h)

    assert txn['from'] != deploy_coinbase
    assert call.is_cancelled() is True