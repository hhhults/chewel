import numpy as np
import matplotlib.pyplot as plt

# -------------------------- Harper's Financial Model --------------------------
# this model assumes we waste 1-efficiency of materials
# it is also really messy.
# that being said, I've tested it a fair amount and I believe it's correct
# whether it's an accurate representation of my costs remains to be seen :+)


v = 2.6 # ml
pricePerUnit = 15 # $
length = 2 # length of cord/necklace in ft
efficiency = 0.95 # hopefully we can do better than this
currentCordPrice = 12.15 # $
wholesaleCordPrice =9 # https://www.amazon.com/Craftdady-Macrame-Bracelet-Necklace-Jewelry/dp/B07S1NFS4G/ref=sr_1_19?crid=CMSFZPM7Z6VZ&keywords=synthetic+leather+cord+1.5mm&qid=1646165264&sprefix=synthetic+leather+cor+1.5mm%2Caps%2C97&sr=8-19
currentCordLength = 75 # ft
wholesaleCordLength = 300

# calculates annual costs on a montly basis
def annualCostsPerMonth():
   annualCosts = 200 # business license
   return annualCosts/12

# calculates how much the bank account will cost if selling n units @ $price
def wellsFargoCostPerMonth(n, price):
   rate = np.where(n*price<40000, 0.032, 0.031)
   rate[np.where(n*price<15000)]=0.034
   return 25 + (rate*price + 0.15)*n

# calculates how much cord costs per unit
def calcCordRatePerNecklace(wholesale=False):
   if wholesale:
      cordPrice = wholesaleCordPrice
      cordFeet = wholesaleCordLength
   else:
      cordPrice = currentCordPrice
      cordFeet= currentCordLength
   return length* cordPrice/cordFeet

# calculates the cost of shipping n units
def calcShippingCost(n, rate=7.15):
   return n*rate

# calculates how much material costs per uni
def calcMaterialPriceDensity(n,tpe=False, smoothSilDensity=1.25, tpeDensity=1.15):
   output = np.ones(n.shape)
   if not tpe:
      for i in range(n.shape[0]):
         if n[i]<efficiency*(757/v):
            output[i]=37.16/(efficiency*(757/v))
         elif n[i]<efficiency*(3785/v):
            output[i]=138.96/(efficiency*(3785/v))
         else:
            output[i] = 575.4/(5*efficiency*3785/v) # 5 gal
      # if n<efficiency*(757/v):
      #    return 37.16/n # magic numbers from reynolds website
      # elif n<efficiency*(3785/v):
      #    return 138.94/n
      # else: return 575.4/n
   else:
                          # grams/order of tpe
      necklacesPerOrder = efficiency*(1000)/tpeDensity/v
      output*= 5.5/necklacesPerOrder
   return output

# calculates the cost to produce n units
def calcProductionCost(n):
   return n*(calcCordRatePerNecklace(wholesale=True)+calcMaterialPriceDensity(n, tpe=True))

# calculates revenue from selling n units at $p
def calcRevenue(n,p):
   return p*n

# calculates monthly costs of making n items and selling them for $p
def calcMonthlyCosts(n,p, local=False):
   if local:
      return annualCostsPerMonth()+wellsFargoCostPerMonth(n,p)+calcProductionCost(n)
   else:
      return annualCostsPerMonth()+wellsFargoCostPerMonth(n,p)+calcProductionCost(n)+calcShippingCost(n)

# calculates monthly profit if selling n units @ p dollars
def profit(n,p):
   return calcRevenue(n,p)-calcMonthlyCosts(n,p)

# makes a cost-volume-profit graph at 0-50 units/month
def createCVP():
   ns = np.arange(0,50,10)
   plt.plot(ns, costs:=calcMonthlyCosts(ns, pricePerUnit), label="Variable Costs",color='r')
   plt.plot(ns, calcRevenue(ns, pricePerUnit), label="Revenue",color="g")
   plt.plot(ns, costs[0]*np.ones(ns.shape[0]), label="Fixed Costs",color="grey")
   plt.xlabel("Units sold")
   plt.ylabel("Dollars")
   plt.title("Monthly Cost-Volume-Profit")
   plt.legend()
   plt.show()

# calculates margin selling n units/month without shipping
def calcLocalMargin(n):
   return (calcRevenue(n,pricePerUnit)-calcMonthlyCosts(n,pricePerUnit,local=True))/calcRevenue(n,pricePerUnit)


def main():

   # createCVP()

   # number sold per month
   n = np.array([100])

   # prints material costs per necklace in dollars
   print("Cord cost: {}".format(calcCordRatePerNecklace(wholesale=True)))
   print("TPE cost: {}".format(calcMaterialPriceDensity(n)))

   # prints margin with domestic shipping cost
   print("domestic margin: ")
   print((calcRevenue(n,pricePerUnit)-calcMonthlyCosts(n,pricePerUnit))/calcRevenue(n,pricePerUnit))
   
   # prints margin if selling without shipping cost
   print("local margin: ")
   print(calcLocalMargin(n))

   # fig,ax=plt.subplots(1,2)
   # ax[0].plot(ns, profit(ns,pricePerUnit))
   # ax[1].plot(ns[2:],(calcRevenue(ns,pricePerUnit)[2:]-calcMonthlyCosts(ns,pricePerUnit)[2:])/calcRevenue(ns,pricePerUnit)[2:])

   # print(calcMaterialPriceDensity(np.array([20])))

main()