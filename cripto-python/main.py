#from algosdk import AlgodClient
from algosdk.v2client import algod
import accounts, assets, transfer, contract
from pyteal import Mode, compileTeal

def create_client():
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    algod_server = "http://localhost"
    algod_port = 4001
    algod_client = algod.AlgodClient(algod_token, algod_server, algod_port)
    #algod_client = AlgodClient(algod_token, algod_server, algod_port)

    return algod_client

#Creamos un cliente para conectarnos con la red de prueba (Tesnet) de Algorand
#y asi poder realizar operaciones
algod_client = create_client()

#Creacion de cuentas
accts = []
num_accounts = 3
accts = accounts.generate_keypair(num_accounts,accts)

#Compilar smart contract
teal_code = compileTeal(contract.nft_contract(), mode=Mode.Application)
print(teal_code)

#Transaccion de la creacion de contrato
contract_id = transfer.create_contract_trans(algod_client,teal_code)

#Creacion de NFT sin contrato
nft_id = assets.create_NFT(accts[0], contract_id)

# Llamada a la función para crear un NFT con contrato
metadata = "Metadata del NFT"  # Personalizar los metadatos del NFT aquí
txid = assets.create_nft_wContract(algod_client,contract_id, accts[0].private_key, metadata)
print("Transacción enviada. ID de la transacción de creacion de NFT con contrato:", txid)

#Detalles de la transacción para transferencia de nft sin contrato
sender_acct = accts[0]
receiver_acct = accts[1]
txid = transfer.transfer_nft(algod_client,sender_acct,receiver_acct,nft_id)
print("Transacción enviada. ID de la transacción de transferencia de NFT sin contrato:", txid)

#Detalles de la transacción para transferencia de nft con contrato
sender_acct = accts[0]
receiver_acct = accts[1]
txid = transfer.transfer_nft_wContract(algod_client, contract_id, accts[0].private_key, sender_acct, receiver_acct)
print("Transacción enviada. ID de la transacción de transferencia de NFT con contrato:", txid)

#Eliminacion del NFT sin contrato
acct_delete = accts[0]
txid = assets.delete_nft(algod_client, acct_delete, nft_id)
print("Transacción enviada. ID de la transacción de eliminacion de NFT sin contrato:", txid)

#€liminacion del NFT con contrato
txid = assets.delete_nft_wContract(algod_client, contract_id, accts[0].private_key)
print("Transacción enviada. ID de la transacción de eliminaciòn de NFT con contrato:", txid)

# now, trying to fetch the asset info should result in an error
try:
    info = algod_client.asset_info(nft_id)
except Exception as e:
    print("Expected Error:", e)



#address: 5X7HTSTGUJTMBG3IV4SRG2NPBNLU3YKMKOI4OMGYG3UYXG4JQE3GV7H57A
#private key: wQdCJj8SpdUS+lFhKT3IYERqZ09HKh5MOAA+8lLupiXt/nnKZqJmwJtoryUTaa8LV03hTFORxzDYNumLm4mBNg== 
#mnemonic: wealth amount nasty catalog enforce rely spatial faint club visa goat ecology stand supply denial clean long thrive abandon catalog planet romance coffee ability noise

