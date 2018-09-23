class Notes:
    AUTO_INCREMENT = (
        'categories.category_id',
        'products.product_id'

    )

    FOREIGN_KEY ={
        'users' : ('user_type.type_id',
                   'ratings.rating_value'),

        'products' : ('categories.category_id',
                      'ratings.rating',
                      'users.email_id'),





    }
    @classmethod
    def printlist(cls, list=()):
        for item in list:
            print(item)

    @classmethod
    def printDict(cls, dict={}):
        for item in dict:
            print(item)
            cls.printlist()

if __name__ == '__main__':
    Notes.printlist(Notes.AUTO_INCREMENT)
    Notes.printDict(Notes.FOREIGN_KEY)
