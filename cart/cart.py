from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request

    #get the current session key if it exists
        cart = self.session.get('session_key')

    #if the user is new, no session key! create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
    #Make sure cart is available on all pages of site
        self.cart = cart



    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)
            self.session.modified = True
            if self.request.user.is_authenticated:
                current_user = Profile.objects.filter(user__id=self.request.user.id)
                carty = str(self.cart)
                carty = carty.replace("\'", "\"")
                current_user.update(old_cart=str(carty))



    def add(self, product, quantity):
        product_id = str(product.id)
        product_quant = str(quantity)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_quant)

        self.session.modified = True

        #logged user
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)

            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
			# Save carty to the Profile Model
            current_user.update(old_cart=str(carty))





    def cart_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        total=0

        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    total = total + (product.price * value)
        return total



    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        #get the ids from cart
        product_ids = self.cart.keys()
        #use ids to lookup products in database model
        products = Product.objects.filter(id__in=product_ids)

        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_quant = int(quantity)

        #get cart
        ourcart = self.cart
        ourcart[product_id] = product_quant

        self.session.modified = True
        
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))

        thing = self.cart    
        return thing
    
    def delete(self, product):
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]
        
        self.session.modified=True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))