import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from random import randint, choice
import string
from datetime import datetime


# ==================================================

class Market:
    def __init__(self, marketName=''):
        self.marketName = marketName
        try:
            dataBase = {
                "productID": [],
                "Name": [],
                "Cost": [],
                "Price": [],
                "Quantity": [],
                "Category": [],
                "Brand": [],
                "ExpireDate": [],
                "ProductPoints": [],
                "Sold": []
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
        current_date = datetime.now().date()
        return current_date

    def get_productCost(self, ID):
        try:
            return self._ProductsData.loc[ID, 'Cost']
        except KeyError:
            print(f"Invalid Product ID: {ID}")
        return None

    def set_productCost(self, ID, newCost):
        try:
            self._ProductsData.loc[ID, 'Cost'] = newCost
            return True
        except KeyError:
            print(f"Invalid Product ID: {ID}")
            return False

    def inc_sold(self, ID, s):
        try:
            self._ProductsData.loc[ID, 'Sold'] += s
            return True
        except KeyError:
            print(f"Invalid Product ID: {ID}")
            return False

    def dec_sold(self, ID, s):
        try:
            self._ProductsData.loc[ID, 'Sold'] -= s
            return True
        except KeyError:
            print(f"Invalid Product ID: {ID}")
            return False

    def get_productName(self, ID):
        try:
            return self._ProductsData.loc[ID, "Name"]
        except KeyError:
            print(f"Invalid Product ID: {ID}")
        return None

    def set_ProductName(self, ID, newName):
        try:
            self._ProductsData.loc[ID, "Name"] = newName
        except KeyError:
            print(f"Invalid Product ID: {ID}")
        return None

    def get_ProductPrice(self, ID):
        try:
            return self._ProductsData.loc[ID, "Price"]
        except KeyError:
            print(f"Invalid Product ID: {ID}")
        return None

    def set_ProductPrice(self, ID, p):
        try:
            self._ProductsData.at[ID, "Price"] = p
        except KeyError:
            print(f"Invalid Product ID: {ID}")
        return None

    def get_quantity(self, ID):
        try:
            return self._ProductsData.loc[ID, "Quantity"]
        except KeyError:
            print(f"Invalid Product ID: {ID}")
        return None

    def set_quantity(self, ID, q):
        try:
            self._ProductsData.loc[ID, "Quantity"] = q
        except KeyError:
            print(f"Invalid Product ID: {ID}")
        return None

    def add_quantity(self, ID, q):
        try:
            self._ProductsData.loc[ID, "Quantity"] += q
        except KeyError:
            print(f"Invalid Product ID: {ID}")
        return None

    def get_category(self, ID):
        try:
            return self._ProductsData.loc[ID, "Category"]
        except KeyError:
            print(f"Invalid Product ID: {ID}")
        return None

    def set_category(self, ID, c):
        try:
            self._ProductsData.loc[ID, "Category"] = c
        except KeyError:
            print(f"Invalid Product ID: {ID}")
        return None

    def get_brand(self, ID):
        try:
            return self._ProductsData.loc[ID, "Brand"]
        except KeyError:
            print(f"Invalid Product ID: {ID}")
        return None

    def set_brand(self, ID, brand):
        try:
            self._ProductsData.loc[ID, "Brand"] = brand
        except KeyError:
            print(f"Invalid Product ID: {ID}")
        return None

    def get_expire(self, ID):
        try:
            return self._ProductsData.loc[ID, "ExpireDate"]
        except KeyError:
            print(f"Invalid Product ID: {ID}")
        return None

    def set_expire(self, ID, exp):
        try:
            self._ProductsData.loc[ID, "ExpireDate"] = exp
        except KeyError:
            print(f"Invalid Product ID: {ID}")
        return None

    def add_product(self, ID=new_ID(), name='', price=0, quantity=0, category='', brand='', expire=''):
        try:
            self._ProductsData.loc[ID] = [name, price, quantity, category, brand, expire]
        except KeyError:
            print(f"Invalid Product ID: {ID}")
        return None

    def remove_product(self, ID):
        try:
            self._ProductsData.drop(ID)
        except KeyError:
            print(f"Invalid Product ID: {ID}")
        return None

        # invoice data methods:

    def reset_invoice(self, invID):
        filtID = self._InvoiceData["InvoiceID"] == invID
        listOfProducts = list(self._InvoiceData.loc[filtID, "ProductID"])
        listOfQuantities = list(self._InvoiceData.loc[filtID, "Quantity"])
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
            if self._ProductsData.loc[ordersIdList[i], "Quantity"] < quantities[i]:
                continue
            newDict["InvoiceID"].append(invoiceID)
            newDict["Date"].append(dateOfTheDay)
            newDict["customerPh"].append(cusPh)
            newDict["ProductID"].append(ordersIdList[i])
            newDict["Quantity"].append(quantities[i])
            price = self._ProductsData.loc[ordersIdList[i], "Price"]
            total += price
            self._ProductsData.loc[ordersIdList[i], "Quantity"] -= quantities[i]
            newDict["Sales"].append(price * quantities[i])
            newDict["Discount"].append(discounts[i])
            newDict["TotalPrice"].append(price - (price * discounts[i]))
            self._UsersData.loc[cusPh, "Points"] += self._ProductsData.loc[ordersIdList[i], "ProductPoints"]
            self.inc_sold(ordersIdList[i], quantities[i])
        self.inc_visits(cusPh)
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
        self._UsersData[self._InvoiceData.loc[index, "customerPh"]] -= (
                self._ProductsData.loc[productID, "ProductPoints"] * Quantity)
        # Return the quantity to the market:
        self._InvoiceData.loc[index, "Quantity"] -= Quantity
        if self._InvoiceData.loc[index, "Quantity"] == 0:
            self._InvoiceData.drop(index, inplace=True)
        self.add_quantity(index, Quantity)
        self.dec_sold(productID, Quantity)
        # at the in out invoices data frame:
        onePrice = self._ProductsData[productID, "Price"]
        onePrice = onePrice - (onePrice * self._InvoiceData.loc[index, 'Discount'])
        totalPrice = onePrice * Quantity
        self._invoiceInOut.loc[invID, "Total"] -= totalPrice
        self._invoiceInOut.loc[invID, "Paid"] -= totalPrice

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
        return True

    def remove_user(self, ph):
        try:
            self._UsersData.drop(ph, inplace=True)
            return True
        except KeyError:
            print("User Not Found!")
            return False

    def get_visits(self, ph):
        try:
            return self._UsersData.loc[ph, "Visits"]
        except KeyError:
            print("User Not Found!")
        return False

    def set_visits(self, ph, newVisits):
        try:
            self._UsersData.loc[ph, "Visits"] = newVisits
            return True
        except KeyError:
            print("User Not Found!")
        return False

    def inc_visits(self, ph):
        try:
            self._UsersData.loc[ph, "Visits"] += 1
            return True
        except KeyError:
            print(f"Invalid user ph: {ph}")
        return False

    def dec_visits(self, ph):
        try:
            self._UsersData.loc[ph, "Visits"] -= 1
            return True
        except KeyError:
            print(f"Invalid user ph: {ph}")
        return False

    def inc_points(self, ph, p=1):
        try:
            self._UsersData.loc[ph, "Points"] += p
            return True
        except KeyError:
            print("User Not Found!")
        return False

    def dec_points(self, ph, p=1):
        try:
            self._UsersData.loc[ph, "Points"] -= p
            return True
        except KeyError:
            print("User Not Found!")
        return False

    def set_points(self, ph, newPoints):
        try:
            self._UsersData.loc[ph, "Points"] = newPoints
            return True
        except KeyError:
            print(f"Invalid user ph: {ph}")
        return False

    def get_points(self, ph):
        try:
            return self._UsersData.loc[ph, "Points"]
        except KeyError:
            print("User Not Found!")
        return False

    def new_manager(self, username='admin', password='admin', name='admin', ph=''):
        if username in self._ManagersData.index:
            print("This username is used")
            return False
        self._ManagersData.loc[username] = [password, name, ph]

    def remove_manager(self, user):
        try:
            self._ManagersData.drop(user)
            return True
        except KeyError:
            return False

    # All new methods

    def top_selling(self, n=5):
        topsDF = self._ProductsData.nlargest(n, columns=['Sold'])
        return topsDF

    def less_selling(self, n=5):
        lessDF = self._ProductsData.nsmallest(n, columns=['Sold'])
        return lessDF

    def sales_rate(self, product='all'):
        if product == 'all':
            salesRateDF = self._ProductsData.loc[:, ['Quantity', 'Sold']]
        else:
            salesRateDF = self._ProductsData.loc[product, ['Quantity', 'Sold']]
        salesRateDF['Sales_Rate'] = salesRateDF['Sold'].div(salesRateDF['Quantity'])
        salesRateDF['Sales_Rate'] = salesRateDF['Sales_Rate'] * 100
        return salesRateDF

    def prediction_emptiness(self, ID):
        if ID not in self._ProductsData.index:
            print('Invalid Product ID')
            return None
        quantity = self._ProductsData.loc[ID, "Quantity"]
        sold = self._ProductsData.loc[ID, 'Sold']

        if quantity <= 0 or sold == 0:
            print("no quantity or sold values")
            return None
        dates_sold = self._InvoiceData[self._InvoiceData['ProductID'] == ID]['Date'].unique()
        quantities_sold = self._InvoiceData[self._InvoiceData['ProductID'] == ID]['Quantity']
        model = DecisionTreeRegressor()
        model.fit(dates_sold.reshape(-1, 1), quantities_sold)
        zero_date = model.predict([[0]])
        zero_date = datetime.fromordinal(int(zero_date))
        return zero_date

    def profit_margin(self, ID):
        if ID not in self._ProductsData.index:
            print("invalid ID")
            return False
        cost = self._ProductsData.loc[ID, "Cost"]
        price = self._ProductsData.loc[ID, "Price"]
        profit = ((price - cost) / price) * 100
        return profit

    def total_profit(self, start_date=datetime, end_date=datetime):
        min_date = self._invoiceInOut['Date'].min()
        max_date = self._invoiceInOut['Date'].max()
        if start_date > min_date or end_date < max_date:
            print("invalid dates")
            return False
        filterDate = (self._invoiceInOut['Date'] >= start_date) & (self._invoiceInOut['Date'] <= end_date)
        value = self._invoiceInOut.loc[filterDate, 'Profit'].sum()
        return value

    def customer_loyalty(self, ph):
        try:
            report = f"User <{ph}> points: <" + str(self._UsersData.loc[ph, 'Points']) + "> ,visits: <" + str(
                self._UsersData.loc[ph, 'Visits']) + "> "
            return report
        except Exception as e:
            print(f"error name: {e}")
            return False

    def best_category(self, n=1):
        try:
            bestCategory = self._ProductsData.copy()
            bestCategory["TotalRevenue"] = bestCategory["Sold"] * bestCategory["Price"]
            bestCategory = bestCategory.groupby("Category").agg({'TotalRevenue': 'sum',
                                                                 'Price': 'median',
                                                                 'Sold': 'count'})
            bestCategory = bestCategory[["TotalRevenue", "MedianPrice", "TotalSold"]]
            bestCategory = bestCategory.sort_values("TotalRevenue", ascending=False)
            return bestCategory.head(n)
        except Exception as e:
            print(f"error: <{e}>")
            return None

    def best_brand(self, n=1):
        try:
            bestBrand = self._ProductsData.copy()
            bestBrand["TotalRevenue"] = bestBrand['Sold'] * bestBrand['price']
            bestBrand = bestBrand.groupby('Brand').agg({"TotalRevenue": "sum",
                                                        "Price": "median",
                                                        "Sold": "count"})
            bestBrand = bestBrand[["TotalRevenue", "MedianPrice", "TotalSold"]]
            bestBrand = bestBrand.sort_values("TotalRevenue", ascending=False)
            return bestBrand.head(n)
        except Exception as e:
            print(f"error: <{e}>")
            return None

    def will_expire_products(self, n=5):
        dayDate = self.get_date()
        sortedByExpire = self._ProductsData.copy()
        sortedByExpire['Reminding'] = sortedByExpire['ExpireDate'].apply(lambda x: (x.date() -
                                                                                    dayDate).days)
        sortedByExpire = sortedByExpire[['Name', 'Quantity', 'Category', 'Brand', 'ExpireDate', 'Reminding']]
        sortedByExpire = sortedByExpire.nsmallest(n, columns=['Reminding'])
        return sortedByExpire

    def recommend_product(self, n=3, ph=None):
        filteredInv = self._InvoiceData.loc[self._InvoiceData['Phone'] == ph]
        grouped = filteredInv.groupby('ProductID').agg({'Quantity': 'sum', 'TotalPrice': 'sum '})
        grouped['Volume'] = grouped.Quantity * grouped.TotalPrice
        grouped = grouped.nlargest(n, columns=['Volume'])
        return grouped

    def generate_report(self, date=datetime):
        try:
            reportDF = self._InvoiceData
            reportDF['Date'] = pd.to_datetime(reportDF['Date'])
            reportDF = reportDF.loc[reportDF['Date'] == date]
            reportDF = reportDF.groupby('ProductID').agg({'Quantity': 'sum', 'Discount': 'sum', 'TotalPrice': 'sum'})
            reportDF['Volume'] = reportDF['Quantity'] * reportDF['TotalPrice']
            return reportDF
        except Exception as e:
            print(f"Error occurred <{e}>")

    def plot_sales_category(self, category):
        try:
            plotingDF = self._ProductsData.copy()
            plotingDF = plotingDF.loc[plotingDF['Category'] == category]
            plotingDF = plotingDF[['Sold', 'Name']]
            plotingDF.sort_values('Sold', ascending=False, inplace=True)
            plotingDF.plot.bar(x='Name', y='Sold')
        except Exception as e:
            print(f"Error: <{e}>")

    def plot_sales_brand(self, brand):
        try:
            plotingDF = self._ProductsData.copy()
            plotingDF = plotingDF.loc[plotingDF['Category'] == brand]
            plotingDF = plotingDF[['Sold', 'Name']]
            plotingDF.sort_values('Sold', ascending=False, inplace=True)
            plotingDF.plot.bar(x='Name', y='Sold')
        except Exception as e:
            print(f"Error: <{e}>")

    def plot_sales_date(self, date=datetime):
        try:
            plotingDF = self._InvoiceData.copy().loc[self._InvoiceData['Date'] == date]
            plotingDF.groupby('ProductID').agg({'Quantity': 'sum', 'TotalPrice': 'sum'})
            plotingDF['Volume'] = plotingDF['Quantity'] * plotingDF['TotalPrice']
            nList = list()
            for i in plotingDF.index:
                nList.append(self._ProductsData.loc[i, 'Name'])
            plotingDF['Name'] = nList
            plotingDF.sort_values(by='Volume', ascending=False, inplace=True)
            plotingDF.plot.bar(x='Name', y='Volume')
        except Exception as e:
            print(f'error: <{e}>')

    def barcode_reader(self):
        pass


# ================================================


class Cashier:
    pass


class Manager:
    def __init__(self, username='admin', password='admin', name='admin', phone='', market=Market()):
        self._username = username
        self._password = password
        self._name = name
        self._phone = phone
        self._market = market
