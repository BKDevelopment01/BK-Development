import cbpro

public_client = cbpro.PublicClient()

result = public_client.get_product_order_book('BTC-USD')
print(result)

