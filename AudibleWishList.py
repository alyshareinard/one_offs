from bs4 import BeautifulSoup
import urllib2
import cookielib
import urllib
import re
from collections import namedtuple
from urlparse import urljoin

target_price=9.90
audible_member=True


#print(soup.prettify())

book_links=[]

#find all the links
#my audible/amazon wish list
url = 'http://www.amazon.com/gp/registry/wishlist/..."
count=0
while url !="":
    count=count+1
#    print "url:", url
    print "page: ", count
    page = urllib2.urlopen(url)
    soup=BeautifulSoup(page)
#    print soup
    for link in soup.find_all("a", class_="a-link-normal a-declarative", href=re.compile("/dp/")):
        url='http://www.amazon.com'+link.get('href')
        book_links.append(url)
    url=""
    for link in soup.find_all("li", class_="a-last"):
        try:
            url='http://www.amazon.com'+link.next_element.get('href')
        except AttributeError:
            url=""

Book=namedtuple("Book", ['title', 'kindle_price', 'reduced_audible', 'total_price', 'Full_Audible_price'])
Books=[]
#now we go through each of the book pages
title_old=""
title=""
link_old=""
k_unlimited=[]
for link in book_links:
    if link!=link_old:
#        print "link_old", link_old
        link_old=link
#        print "link", link
        skip=0
        try:
            page = urllib2.urlopen(link)
        except:
            print "cannot open this file", link, "skipping..."
            skip=1
        if skip!=1:
            book_soup=BeautifulSoup(page)
#            print book_soup
    #looking for book title
            title_string=book_soup.find_all(id="btAsinTitle")
            for string in title_string:
                title=string.find(text=True)
            if title!=title_old:
                print "Title:", title
                title_old=title   
#    looking for kindle price
                kprice=-99
                kindle_price=book_soup.find_all(class_="price")
#                print kindle_price
                for item in kindle_price:
#                    print "item", item
#                    print "item.prev", item.previous_element.previous_element
                    if "Kindle Edition" in item.previous_element.previous_element:
                        kprice=item.find(text=True)
                        kprice=float(kprice.replace("$", ""))
#                        print "good enough"

#    looking for reduced audible price with kindle purchase
                audible_reduced_price=-99
                price=book_soup.find_all(class_="price")
                prices=[]

                for item in price:
#                    print "item", item
#                    print "item.prev", item.previous_element
#                    print "item.prev.prev", item.previous_element.previous_element
#                    print "item.prev.prev.prev", item.previous_element.previous_element.previous_element
                    if "Add narration" in item.previous_element.previous_element:
                        audible_reduced_price=item.find(text=True)
                        audible_reduced_price=float(audible_reduced_price.replace("$", ""))

        #looking for full audible price
                Full_Audible_price=-99
#                for item in price:
#                    if "Audible Audio Edition" in item.previous_element.previous_element.previous_element:
#                        print "item", item.previous_element
#                        val=item.findAll(text=True)
#                        print "vals", val
#                        Full_Audible_price=val[1]
                #turn it into a number
#                        Full_Audible_price=float(Full_Audible_price.replace("$", ""))
#                        if audible_member==True:
#                            Full_Audible_price=round(Full_Audible_price*0.7,2) #current audible discount for members is 30%, round to nearest cent

                #check to see if it's in kindleUnlimited
                KU_string=book_soup.find_all(alt="Kindle Unlimited")
 #               print "what's up here?", KU_string
                if KU_string !=[]:
                    print "Available on Kindle Unlimited"
                    k_unlimited.append(title)

                print "Kindle price: $", kprice
                #print "breakit here", KU_string/5
                total_price=99
                if audible_reduced_price !=-99:
                    print "Audible price (with Kindle purchase): $", audible_reduced_price
                    total_price=kprice+audible_reduced_price
                    print "Total price: $", total_price
                    if total_price<target_price: print "This is cheaper than your target price!!!"
                else: 
                    print "Audible discount not available"

                if Full_Audible_price !=-99:
                    print "Full Audible price $", Full_Audible_price
                    if Full_Audible_price>total_price:
                        print "Price for both is cheaper than the full audible price"
 #               else:
 #                   print "Audible book not available"
                Books.append(Book(title, kprice, audible_reduced_price, total_price, Full_Audible_price))

                print("   ")
    

print "Summary:"
print " "
print "The following books are cheaper than your target price if you buy just the audible version:"
for item in Books:
    if item.Full_Audible_price<target_price and item.Full_Audible_price>-1:
        print item.title, item.Full_Audible_price

print " "
print "The following books are cheaper than your target price if you buy kindle+audible:"
for item in Books:
    if item.total_price<target_price:
        print item.title, item.total_price

print " "
print "The following books are cheaper than the full audible price:"
for item in Books:
    if item.total_price<item.Full_Audible_price and item.total_price<target_price:
        print item.title, "$", item.total_price
 
print " "
print "The following books are available on Kindle Unlimited", len(k_unlimited)
for item in k_unlimited:
    print item
