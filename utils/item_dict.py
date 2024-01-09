from itemadapter import ItemAdapter

def item_to_dict(item, d = {}):
    adap = ItemAdapter(item)

    print("valor de D", d)

    for name in adap.field_names():
        if  adap.get(name, None) is not None:
            d[name] = adap.get(name)

    return d