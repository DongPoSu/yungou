import urllib
import urllib.request as http_request


# 蜂巢关联供应商的商品信息
def add_supplier_product(dict):
    url = "http://120.25.134.249:8080/yunweb/product/addSupplierProduct"
    request = http_request.Request(url=url, data=dict,method="post")
    result = http_request.urlopen(request)
    print(result)

# 蜂巢关联供应商的商品信息
def add_supplier_company(dict):
    url = "http://120.25.134.249:8080/yunweb/product/addSupplierCompany"
    method = "post"
    response = http_request.urlopen(url=url, data=dict)
    print(response)
