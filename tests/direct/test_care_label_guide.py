"""Direct tests for label compilation and the care-stage automaton."""

import json


LABEL = "Machine wash cold on a gentle cycle. Do not bleach. Line dry away from direct sunlight. Iron at low temperature if needed."
PROFILE = {"wash": "MACHINE_COLD", "bleach": "SKIP", "dry": "LINE", "iron": "LOW"}


def _label(contract, direct_vm, publisher):
    direct_vm.sender = publisher
    label_id = contract.register_label("SHIRT-A", LABEL, "fixture://garment-label")
    direct_vm.mock_llm(r".*Compile a frozen textile care label.*", json.dumps(PROFILE))
    contract.compile_label(label_id)
    return label_id


def _item(contract, direct_vm, owner, label_id, key="ITEM-1"):
    direct_vm.sender = owner
    return contract.register_item(key, label_id, "Blue cotton community-uniform shirt with a sewn care label.")


def test_compiled_profile_is_content_bound(contract, direct_vm, direct_alice):
    label_id = _label(contract, direct_vm, direct_alice)
    label = contract.get_label(label_id)
    assert label["status"] == "COMPILED"
    assert label["profile_sha256"].startswith("sha256:")


def test_only_publisher_can_compile_label(contract, direct_vm, direct_alice, direct_bob):
    direct_vm.sender = direct_alice
    label_id = contract.register_label("SHIRT-A", LABEL, "fixture://garment-label")
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("only_label_publisher"):
        contract.compile_label(label_id)


def test_automaton_enforces_stage_order(contract, direct_vm, direct_alice, direct_bob):
    label_id = _label(contract, direct_vm, direct_alice)
    item_id = _item(contract, direct_vm, direct_bob, label_id)
    contract.start_cycle(item_id)
    with direct_vm.expect_revert("stage_out_of_order"):
        contract.record_stage(item_id, "DRY", "LINE", "Trying to skip directly to drying.")


def test_automaton_rejects_operation_not_in_profile(contract, direct_vm, direct_alice, direct_bob):
    label_id = _label(contract, direct_vm, direct_alice)
    item_id = _item(contract, direct_vm, direct_bob, label_id)
    contract.start_cycle(item_id)
    with direct_vm.expect_revert("operation_not_allowed"):
        contract.record_stage(item_id, "WASH", "MACHINE_HOT", "Hot washing conflicts with the compiled label.")


def test_full_cycle_completes_and_can_repeat(contract, direct_vm, direct_alice, direct_bob):
    label_id = _label(contract, direct_vm, direct_alice)
    item_id = _item(contract, direct_vm, direct_bob, label_id)
    contract.start_cycle(item_id)
    contract.record_stage(item_id, "WASH", "MACHINE_COLD", "Washed cold on the stated gentle setting.")
    contract.record_stage(item_id, "BLEACH", "SKIP", "Bleach was not used for this care cycle.")
    contract.record_stage(item_id, "DRY", "LINE", "Line dried away from direct sunlight.")
    contract.record_stage(item_id, "IRON", "LOW", "Low-temperature ironing completed where needed.")
    assert contract.get_item(item_id)["status"] == "COMPLETE"
    contract.start_cycle(item_id)
    assert contract.get_item(item_id)["cycle_number"] == 2


def test_only_item_owner_records_stage(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    label_id = _label(contract, direct_vm, direct_alice)
    item_id = _item(contract, direct_vm, direct_bob, label_id)
    contract.start_cycle(item_id)
    direct_vm.sender = direct_charlie
    with direct_vm.expect_revert("only_item_owner"):
        contract.record_stage(item_id, "WASH", "MACHINE_COLD", "Unauthorized care-stage record attempt.")


def test_invalid_compilation_value_fails_closed(contract, direct_vm, direct_alice):
    direct_vm.sender = direct_alice
    label_id = contract.register_label("BAD", LABEL, "fixture://garment-label")
    direct_vm.mock_llm(
        r".*Compile a frozen textile care label.*",
        json.dumps({**PROFILE, "wash": "BOIL"}),
    )
    with direct_vm.expect_revert("unknown_profile_value"):
        contract.compile_label(label_id)
    assert contract.get_label(label_id)["status"] == "REGISTERED"
