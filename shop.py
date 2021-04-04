from collections import namedtuple
Customer = namedtuple('Customer','name loyality')
goods = {
    'cabbage': 10, 'carrot': 15, 'tea': 40, 'nutella': 200
         }
class LineItem:
    def __init__(self,product,quantity,price):
        self.product = product
        self.quantity = quantity
        self.price = price
    def cost(self):
        return int(self.quantity * self.price)
class Order:
    def __init__(self,customer,foodcart,promotion = None):
        self.customer = customer
        self.foodcart = foodcart
        self.promotion = promotion
    def total(self):
        return sum(item.cost() for item in self.foodcart)
    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion
        return self.total() - discount
def different_discount(order:Order) -> float:
    return order.total() * 0.05 if len([item.product for item in order.foodcart]) else 0
def loyality_discount(order) -> float:
    return order.total() * 0.1 if order.customer.loyality >= 1000 else 0
def large_discount(order:Order) -> float:
    discount = 0
    for item in order.foodcart:
        if item.quantity >= 20:
            discount += item.cost() * 0.07
    return discount
def shop_products() -> None:
    print('| {:^10} | {:^8} |'.format('product', 'price'))
    global goods
    for product in goods:
        print('| {:^10} | {:^8} |'.format(product, goods[product]))
    return None
def idintifity() -> Customer:
  name = input('enter your name:').strip()
  loyality = input('enter your loyality:').strip()
  try:
      loyal = int(loyality)
      customer = Customer(name, loyal)
  except:
      customer = Customer('default_customer', 0)
  return customer
def creating_cart() -> Order:
    order = Order(idintifity(),[])
    print('please, choose products, print "stop" to stop:')
    while True:

        inp1 = input().strip().lower()
        if inp1 != 'stop':
            try:
                inp2 = inp1.split()
                try:
                  q = int(inp2[1])
                except:
                    continue
                if inp2[0] in goods and len(inp2) == 2:
                    order.foodcart.append(LineItem(inp2[0], q, goods[inp2[0]]))
            except IndexError:
                LookupError('please,enter product quantity')
        else:
            break
    return order
def same_things(order:Order) -> Order:
    d = dict()
    for product in order.foodcart:
        if product.product not in d:
            d[product.product] = product.quantity
        else:
            d[product.product] += product.quantity
    order.foodcart = [LineItem(product, d[product], goods[product]) for product in d]
    return order

def print_check() -> None:
    order = same_things(creating_cart())
    print('| {:^10} | {:^10} | {:^10} | {:^10} |'.format('product','quantity','price','cost'))
    for product in order.foodcart:
        print('| {:^10} | {:^10} | {:^10} | {:^10} |'.format(
            product.product,product.quantity,product.price,product.cost()
        ))
    order.promotion = int(max(different_discount(order), large_discount(order), loyality_discount(order)))
    print(f'{order.total()} - {order.promotion} = {order.due()}')
    return None
shop_products()
print_check()
