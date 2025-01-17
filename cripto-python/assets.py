from typing import Any, Dict
from algosdk import transaction, encoding
import transfer as transModule
# Account 1 creates an asset called `rug` with a total supply
# of 1000 units and sets itself to the freeze/clawback/manager/reserve roles

def create_NFT(algod_client, acct):
    sp = algod_client.suggested_params()
    txn = transaction.AssetConfigTxn(
        sender=acct.address,
        sp=sp,
        default_frozen=False,
        unit_name="rug",
        asset_name="Really Useful Gift",
        manager=acct.address,  #Permisos sobre el NFT
        reserve=acct.address,
        freeze=acct.address,
        clawback=acct.address,
        url="https://path/to/my/asset/details.json",  #URL de la metadata del NFT en formato JSON 
        total=1,  #Numero de copias del NTF
        decimals=0, #Numero de particiones
    )

    # Sign with secret key of creator
    stxn = txn.sign(acct.private_key)
    # Send the transaction to the network and retrieve the txid.
    txid = algod_client.send_transaction(stxn)
    print(f"Sent asset create transaction with txid: {txid}")
    # Wait for the transaction to be confirmed
    results = transaction.wait_for_confirmation(algod_client, txid, 4)
    print(f"Result confirmed in round: {results['confirmed-round']}")

    # grab the asset id for the asset we just created
    created_asset = results["asset-index"]
    print(f"Asset ID created: {created_asset}")

    return created_asset


# Función para crear un NFT en el contrato
def create_nft_wContract(algod_client,contract_address, private_key, metadata):
    params = algod_client.suggested_params()
    txn = transaction.ApplicationCallTxn(
        sender=encoding.decode_address(contract_address),
        sp=params,
        index=0,  # Índice de la función de creación en el contrato
        app_args=[bytes(metadata, "utf-8")],
        on_complete=transaction.OnComplete.NoOpOC
    )
    signed_txn = txn.sign(private_key)
    txid = algod_client.send_transaction(signed_txn)
    return txid


def modify_asset(algod_client, acct):
    sp = algod_client.suggested_params()
    # Create a config transaction that wipes the
    # reserve address for the asset
    txn = transaction.AssetConfigTxn(
        sender=acct.address,
        sp=sp,
        manager=acct.address,
        reserve=None,
        freeze=acct.address,
        clawback=acct.address,
        strict_empty_address_check=False,
    )
    # Sign with secret key of manager
    stxn = txn.sign(acct.private_key)
    # Send the transaction to the network and retrieve the txid.
    txid = algod_client.send_transaction(stxn)
    print(f"Sent asset config transaction with txid: {txid}")
    # Wait for the transaction to be confirmed
    results = transaction.wait_for_confirmation(algod_client, txid, 4)
    print(f"Result confirmed in round: {results['confirmed-round']}")

def delete_nft(algod_client, acct, created_asset):
    sp = algod_client.suggested_params()
    # Create asset destroy transaction to destroy the asset
    destroy_txn = transaction.AssetDestroyTxn(
        sender=acct.address,
        sp=sp,
        index=created_asset,
    )
    signed_destroy_txn = destroy_txn.sign(acct.private_key)
    txid = algod_client.send_transaction(signed_destroy_txn)
    print(f"Sent destroy transaction with txid: {txid}")

    results = transaction.wait_for_confirmation(algod_client, txid, 4)
    print(f"Result confirmed in round: {results['confirmed-round']}")

def delete_nft_wContract(algod_client, contract_address, private_key):
    params = algod_client.suggested_params()
    txn = transaction.ApplicationCallTxn(
        sender=encoding.decode_address(contract_address),
        sp=params,
        index=3,  # Índice de la función de eliminación en el contrato
        app_args=[],
        on_complete=transaction.OnComplete.NoOpOC
    )
    signed_txn = txn.sign(private_key)
    txid = algod_client.send_transaction(signed_txn)
    return txid

def retrieve_asset_info(algod_client,created_asset):
    # Retrieve the asset info of the newly created asset
    asset_info = algod_client.asset_info(created_asset)
    asset_params: Dict[str, Any] = asset_info["params"]
    print(f"Asset Name: {asset_params['name']}")
    print(f"Asset params: {list(asset_params.keys())}")