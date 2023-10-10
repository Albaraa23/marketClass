import pandas as pd
from random import randint, choice
import string
from datetime import datetime


# ==================================================

class Market:
    ListOfMarkets = []

    def __init__(self, marketName=''):
        super().__init__()
        self._marketName = marketName
        try:
            dataBase = {
                "productID": [],
                "Name": [],
                "Price": [],
                "Quantity": [],
                "Category": [],
                "Brand": [],
                "ExpireDate": [],
                "ProductPoints": []
            }
            invoicesDataBase = {
                "InvoiceID": [],
                "Date": [],
                "customerPh": [],
                "ProductID": [],
                "Quantity": [],
                "Sales": [],
                "Discount": [],
                "TotalPrice": []
            }
            invInOut = {
                "ID": [],
                "Date": [],
                "Total": [],
                "Paid": [],
                "Coupon": [],
                "Received": [],
                "Profit": []
            }
            users = {
                "Phone": [],
                "Points": [],
                "Visits": []
            }
            Managers = {
                "Username": [],
                "Password": [],
                "Name": [],
                "Phone": [],
                "Market": []
            }
            self._ProductsData = pd.DataFrame(dataBase)
            self._ProductsData.set_index("productID", inplace=True)
            self._InvoiceData = pd.DataFrame(invoicesDataBase)
            self._invoiceInOut = pd.DataFrame(invInOut)
            self._UsersData = pd.DataFrame(users)
            self._UsersData.set_index("Phone", inplace=True)
            self._ManagersData = pd.DataFrame(Managers)
            self._ManagersData.set_index("Username", inplace=True)
            self.ListOfMarkets.append(self)
        except Exception as e:
            # Handle the exception
            print("An error occurred during market initialization:", str(e))

    @staticmethod
    def new_ID(n=13):
        start = 10 ** (n - 1)
        end = (10 ** n) - 1
        return randint(start, end)

    @staticmethod
    def new_invoice_ID(n=13):
        characters = string.ascii_letters + string.digits
        random_string = ''.join(choice(characters) for _ in range(n))
        return random_string

    @staticmethod
    def get_date():
        current_date = datetime.now().strftime("%d/%m/%Y")
        return current_date

    def get_productName(self, ID):
        try:
            return self._ProductsData.at[ID, "Name"]
        except KeyError:
            print(f"Invalid Product ID: {ID}")
        return None

    def set_name(self, ID, newName):
        try:
            self._ProductsData.at[ID, "Name"] = newName
        except KeyError:
            print(f"Invalid Product ID: {ID}")
        return None

    def get_price(self, ID):
        try:
            return self._ProductsData.at[ID, "Price"]
        except KeyError:
            print(f"Invalid Product ID: {ID}")
        return None

    def set_price(self, ID, p):
        try:
            self._ProductsData.at[ID, "Price"] = p
        except KeyError:
            print(f"Invalid Product ID: {ID}")
        return None

    def get_quantity(self, ID):
        try:
            return self._ProductsData.at[ID, "Quantity"]
        except:
            print(f"Invalid Product ID: {ID}")
        return None

    def set_quantity(self, ID, q):
        try:
            self._ProductsData.at[ID, "Quantity"] = q
        except:
            print(f"Invalid Product ID: {ID}")
        return None

    def add_quantity(self, ID, q):
        try:
            self._ProductsData.at[ID, "Quantity"] += q
        except:
            print(f"Invalid Product ID: {ID}")
        return None

    def get_category(self, ID):
        try:
            return self._ProductsData.at[ID, "Category"]
        except:
            print(f"Invalid Product ID: {ID}")
        return None

    def set_category(self, ID, c):
        try:
            self._ProductsData.at[ID, "Category"] = c
        except:
            print(f"Invalid Product ID: {ID}")
        return None

    def get_brand(self, ID):
        try:
            return self._ProductsData.at[ID, "Brand"]
        except:
            print(f"Invalid Product ID: {ID}")
        return None

    def set_brand(self, ID, brand):
        try:
            self._ProductsData.at[ID, "Brand"] = brand
        except:
            print(f"Invalid Product ID: {ID}")
        return None

    def get_expire(self, ID):
        try:
            return self._ProductsData.at[ID, "ExpireDate"]
        except:
            print(f"Invalid Product ID: {ID}")
        return None

    def set_expire(self, ID, exp):
        try:
            self._ProductsData.at[ID, "ExpireDate"] = exp
        except:
            print(f"Invalid Product ID: {ID}")
        return None

    def add_product(self, ID=new_ID(), name='', price=0, quantity=0, category='', brand='', expire=''):
        try:
            self._ProductsData.at[ID] = [name, price, quantity, category, brand, expire]
        except:
            print(f"Invalid Product ID: {ID}")
        return None

    def remove_product(self, ID):
        try:
            self._ProductsData.drop(ID)
        except:
            print(f"Invalid Product ID: {ID}")
        return None

        # invoice data methods:

    def reset_invoice(self, invID):
        filtID = self._InvoiceData["InvoiceID"] == invID
        listOfProducts = list(self._InvoiceData.at[filtID, "ProductID"])
        listOfQuantities = list(self._InvoiceData.at[filtID, "Quantity"])
        for i in range(len(listOfProducts)):
            self.return_item(invID, listOfProducts[i], listOfQuantities[i])

    def make_invoice(self, ordersIdList=[], quantities=[], discounts=[], cusPh=0, paid=0.0, coupon=0):
        invoiceID = self.new_invoice_ID()
        while invoiceID in self._InvoiceData.index:
            invoiceID = self.new_invoice_ID()
        dateOfTheDay = self.get_date()
        newDict = {
            "InvoiceID": [],
            "Date": [],
            "customerPh": [],
            "ProductID": [],
            "Quantity": [],
            "Sales": [],
            "Discount": [],
            "TotalPrice": []
        }
        newInOut = {
            "ID": [],
            "Date": [],
            "Total": [],
            "Paid": [],
            "Coupon": [],
            "Received": [],
            "Profit": []
        }
        total = 0
        for i in range(len(ordersIdList)):
            if self._ProductsData.at[ordersIdList[i], "Quantity"] < quantities[i]:
                continue
            newDict["InvoiceID"].append(invoiceID)
            newDict["Date"].append(dateOfTheDay)
            newDict["customerPh"].append(cusPh)
            newDict["ProductID"].append(ordersIdList[i])
            newDict["Quantity"].append(quantities[i])
            price = self._ProductsData.at[ordersIdList[i], "Price"]
            total += price
            self._ProductsData.at[ordersIdList[i], "Quantity"] -= quantities[i]
            newDict["Sales"].append(price * quantities[i])
            newDict["Discount"].append(discounts[i])
            newDict["TotalPrice"].append(price - (price * discounts[i]))
            self._UsersData.at[cusPh, "Points"] += self._ProductsData.at[ordersIdList[i], "ProductPoints"]
            self._UsersData.at[cusPh, "Visits"] += 1
        newInOut['ID'].append(invoiceID)
        newInOut['Date'].append(dateOfTheDay)
        newInOut["Total"].append(total)
        newInOut["Paid"].append(paid)
        newInOut["Coupon"].append(coupon)
        newInOut["Received"].append(total - (paid + coupon))
        newInOut["Profit"].append(total - coupon)
        newInv = pd.DataFrame(newDict)
        newInvInOut = pd.DataFrame(newInOut)
        self._InvoiceData = pd.concat([self._InvoiceData, newInv], ignore_index=True)
        self._invoiceInOut = pd.concat([self._invoiceInOut, newInvInOut], ignore_index=True)

    def return_item(self, invID, productID, Quantity):
        if invID not in self._InvoiceData.index:
            print("InvoiceID is not found!")
            return False
        # Create a filter by invID and productID:
        filt = (self._InvoiceData["InvoiceID"] == invID) & (self._InvoiceData["ProductID"] == productID)
        index = self._InvoiceData[filt].index
        # remove points from user:
        self._UsersData[self._InvoiceData.at[index, "customerPh"]] -= (
                self._ProductsData.at[productID, "ProductPoints"] * Quantity)
        # Return the quantity to the market:
        self._InvoiceData.at[index, "Quantity"] -= Quantity
        if self._InvoiceData.at[index, "Quantity"] == 0:
            self._InvoiceData.drop(index, inplace=True)
        self._ProductsData.at[index, "Quantity"] += Quantity
        # at the in out invoices data frame:
        onePrice = self._ProductsData[productID, "Price"]
        onePrice = onePrice - (onePrice * self._InvoiceData.at[index, 'Discount'])
        totalPrice = onePrice * Quantity
        self._invoiceInOut.at[invID, "Total"] -= totalPrice
        self._invoiceInOut.at[invID, "Paid"] -= totalPrice

    # users data
    def new_user(self, ph, points, visits):
        if ph in self._UsersData.index:
            print("User Exist!")
            return False
        newUser = {
            "Phone": ph,
            "Points": points,
            "Visits": visits
        }
        user = pd.DataFrame(newUser)
        self._UsersData = pd.concat([self._UsersData, user], ignore_index=True)

    def remove_user(self, ph):
        try:
            self._UsersData.drop(ph, inplace=True)
            return True
        except:
            print("User Not Found!")
            return False

    def get_visits(self, ph):
        try:
            return self._UsersData.at[ph, "Visits"]
        except:
            print("User Not Found!")
        return False

    def set_visits(self, ph, newVisits):
        try:
            self._UsersData.at[ph, "Visits"] = newVisits
            return True
        except:
            print("User Not Found!")
        return False

    def inc_visits(self, ph):
        try:
            self._UsersData.at[ph, "Visits"] += 1
            return True
        except:
            print(f"Invalid user ph: {ph}")
        return False

    def dec_visits(self, ph):
        try:
            self._UsersData.at[ph, "Visits"] -= 1
            return True
        except:
            print(f"Invalid user ph: {ph}")
        return False

    def inc_points(self, ph, p=1):
        try:
            self._UsersData.at[ph, "Points"] += p
            return True
        except:
            print("User Not Found!")
        return False

    def dec_points(self, ph, p=1):
        try:
            self._UsersData.at[ph, "Points"] -= p
            return True
        except:
            print("User Not Found!")
        return False

    def set_points(self, ph, newPoints):
        try:
            self._UsersData.at[ph, "Points"] = newPoints
            return True
        except:
            print(f"Invalid user ph: {ph}")
        return False

    def get_points(self, ph):
        try:
            return self._UsersData.at[ph, "Points"]
        except:
            print("User Not Found!")
        return False


# =====================================================


# ================================================

class User:
    def __init__(self, phone='', points=0, visits=0, market=Market):
        self._phone = phone
        self._points = points
        self._visits = visits
        self.market = market
        self.market.new_user(phone, points, visits)


class Manager:
    def __init__(self, username='admin', password='admin', name='admin', phone='', market=Market()):
        self._username = username
        self._password = password
        self._name = name
        self._phone = phone
        self._market = [].append(market)
