import hashlib
import binascii

def hashIt(firstTxHash, secondTxHash):
    # Reverse inputs before and after hashing
    # due to big-endian
    unhex_reverse_first = binascii.unhexlify(firstTxHash)[::-1]
    unhex_reverse_second = binascii.unhexlify(secondTxHash)[::-1]

    concat_inputs = unhex_reverse_first+unhex_reverse_second
    first_hash_inputs = hashlib.sha256(concat_inputs).digest()
    final_hash_inputs = hashlib.sha256(first_hash_inputs).digest()
    # reverse final hash and hex result
    return binascii.hexlify(final_hash_inputs[::-1])
 
 # Hash pairs of items recursively until a single value is obtained
def merkleCalculator(hashList):
    if len(hashList) == 1:
        return hashList[0]
    newHashList = []
    # Process pairs. For odd length, the last is skipped
    for i in range(0, len(hashList)-1, 2):
        newHashList.append(hashIt(hashList[i], hashList[i+1]))
    if len(hashList) % 2 == 1: # odd, hash last item twice
        newHashList.append(hashIt(hashList[-1], hashList[-1]))
    return merkleCalculator(newHashList)

# Demo :
# https://chainz.cryptoid.info/grs/block.dws?3641180.htm
print('Expected MerkleRoot :   8efa9b8d755ea7dfa4a964bc58ee3b176eb382363ff99da9e7144922a73d82b8')

# Transaction Hashes of block #3641180
txHashes = [
    '48df5c1c348813adc57e41498e7879153ec4b0d1651c14e8e2f64f056a60cf4d',
    'fbe27eedf04b69ab8191410451093f463ec67a23d231b504269adffbe0d23ee83',
    'f7942734fc960da59c7a7375ca3464664565adbc0fbe86a72708d8cb1031c525',
    '70fab1507f663e1c736a67e6085bfb6ca457f39a8b268e45511b28acc2a2bafa'
]   

CalculatedMerkleRoot = str(merkleCalculator(txHashes), 'utf-8')
print('Calculated MerkleRoot : ' + CalculatedMerkleRoot)

