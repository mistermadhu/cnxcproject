
from faker import Faker
class FakerUtility:
    def __init__(self):
        self.fake = Faker()
        self.faker_functions={}
        self.faker_functions["name"]=self.fake.name
        self.faker_functions["address"]=self.fake.address
        self.faker_functions["first_name"]=self.fake.first_name
        self.faker_functions["last_name"]=self.fake.last_name
        self.faker_functions["prefix"]=self.fake.prefix
        self.faker_functions["suffix"]=self.fake.suffix
        self.faker_functions["email"]=self.fake.email
        self.faker_functions["phone_number"]=self.fake.phone_number
        self.faker_functions["date_of_birth"]=self.fake.date_of_birth
        self.faker_functions["ssn"]=self.fake.ssn
        self.faker_functions["city"]=self.fake.city
        self.faker_functions["state"]=self.fake.state
        self.faker_functions["country"]=self.fake.country
        self.faker_functions["postcode"]=self.fake.postcode
        self.faker_functions["street_address"]=self.fake.street_address
        self.faker_functions["random_digit"]=self.fake.random_digit
        self.faker_functions["future_date"]=self.fake.future_date
        self.faker_functions["past_date"]=self.fake.past_date
        self.faker_functions["company"]=self.fake.company
        self.faker_functions["credit_card_number"]=self.fake.credit_card_number

    def getFakeData(self,tdtype):
        return self.faker_functions[tdtype]()
    
