from eStore import db, bcrypt
from eStore.models import Users, User_type, Categories, Products
from random import randint

def add_users_table():
    for i in range(5,10):
        email_id = 'user' + str(i) + '@gmail.com'
        name = 'user' + str(i)
        user_name = 'user_name' + str(i)
        password = 'password' + str(i)
        user_type = 3
        address_line1 = 'addrOne' + str(i)
        address_line2 = 'addrTwo' + str(i)
        area = 'area' + str(i)
        city = 'city' + str(i)
        state = 'state' + str(i)
        country = 'country' + str(i)
        pincode = 123456
        phone = '999999999' + str(i)
        rating = 0

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user1 = Users(email_id=email_id,
                     name=name,
                     user_name=user_name,
                     password=hashed_password,
                     user_type=user_type,
                     address_line1=address_line1,
                     address_line2=address_line2,
                     area=area,
                     city=city,
                     state=state,
                     country=country,
                     pincode=pincode,
                     phone=phone,
                     rating=rating)

        # db.session.add(user1)

    # db.session.commit()

def add_categories_table():
    for i in range(1, 11):
        category_name = 'cat' + str(i)
        cat = Categories(category_name=category_name)
        # db.session.add(cat)

    # db.session.commit()



def add_products_table():
    sel_id = []
    for i in range(1, 21):
        product_name = 'prod' + str(i)
        category_id = randint(1,10)
        qty = randint(0,100)
        price = randint(300,5000)
        rating = 0
        seller_name = 'user' + str(randint(5,9))
        seller_id = Users.query.filter_by(name=seller_name).first().email_id
        sel_id.append(seller_id)
        description = 'desc' + str(i)

        prod = Products(product_name=product_name,category_id=category_id,qty=qty,price=price,rating=rating,seller_id=seller_id,description=description)
        # db.session.add(prod)

    # db.session.commit()
    print(sel_id)



if __name__ == '__main__':
    add_users_table()