"""Five-validator GLSim flow for label compilation and one care cycle."""

import json
from pathlib import Path

from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address


def _ok(receipt):
    assert tx_execution_succeeded(receipt), json.dumps(receipt, default=str)


def _context():
    profile = {"wash": "MACHINE_COLD", "bleach": "SKIP", "dry": "LINE", "iron": "LOW"}
    validators = get_validator_factory().batch_create_mock_validators(
        5,
        mock_llm_response={"nondet_exec_prompt": {"Compile a frozen textile care label": json.dumps(profile)}},
    )
    return {"validators": [validator.to_dict() for validator in validators]}


def test_five_validator_compile_and_reusable_care_cycle():
    publisher_account, item_owner_account = create_accounts(2)
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "care_label_guide.py")
    deployed = factory.deploy_contract_tx(args=[], account=publisher_account, wait_transaction_status=TransactionStatus.FINALIZED)
    _ok(deployed)
    address = extract_contract_address(deployed)
    publisher = factory.build_contract(address, account=publisher_account)
    item_owner = factory.build_contract(address, account=item_owner_account)
    label_id = f"{str(publisher_account.address).lower()}:SHIRT-A"
    item_id = f"{str(item_owner_account.address).lower()}:ITEM-1"
    label = "Machine wash cold on a gentle cycle. Do not bleach. Line dry away from direct sunlight. Iron at low temperature if needed."
    _ok(publisher.register_label(args=["SHIRT-A", label, "fixture://garment-label"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(publisher.compile_label(args=[label_id]).transact(transaction_context=_context(), wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(item_owner.register_item(args=["ITEM-1", label_id, "Blue cotton community-uniform shirt with a sewn care label."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(item_owner.start_cycle(args=[item_id]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    operations = [("WASH", "MACHINE_COLD", "Washed cold on the stated gentle setting."), ("BLEACH", "SKIP", "Bleach was not used for this care cycle."), ("DRY", "LINE", "Line dried away from direct sunlight."), ("IRON", "LOW", "Low-temperature ironing completed where needed.")]
    for stage, operation, note in operations:
        _ok(item_owner.record_stage(args=[item_id, stage, operation, note]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    assert item_owner.get_item(args=[item_id]).call()["status"] == "COMPLETE"
