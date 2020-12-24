import pyEX

iexCloud = pyEX.Client(
    api_token='Tpk_1e8fef17ee254009a45873d2c1b76828',
    version='sandbox')

results = iexCloud.symbols()

print(results)
