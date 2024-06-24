from hashlib import sha256
import json
from datetime import datetime
import time
import random
import hashlib
import pyqrcode
import png
MANUFACTURER=None
DISTRIBUTORS={}
CLIENTS={}
BLOCKCHAIN=None

class Transaction:
    def __init__(self ,orderId,product_id ,status, manufacturer=None , distributor=None , client=None,timestamp=time.ctime(),verification=0):
        self.product_id = product_id
        self.timestamp = timestamp
        self.manufacturer = manufacturer
        self.distributor = distributor
        self.client = client
        self.status= status #transit To distributor,Transit To Client,Delivered to Client,order Placed
        self.orderId=orderId
        self.hash = self.calc_hash()
        self.verification=verification
        self.signature= hashlib.sha256(json.dumps({"orderId":self.orderId,"product_id":self.product_id}).encode('utf-8')).hexdigest()

    def calc_hash(self):
       return hashlib.sha256(json.dumps({"orderId":self.orderId,"time":self.timestamp}).encode('utf-8')).hexdigest()
        
    def __str__(self):
        return  str(self.__dict__)

class Blockchain:
    def __init__(self , difficulty):
        self.chain = []
        self.difficulty = difficulty
        self.pending_transactions = []
            
    # def create_genesis_block(self):
    #         return Block(0 , time.time() , [] , "0" , 0 , self.difficulty)
    def __str__(self):
        return str(self.__dict__)
    def getQR(self,orderID):
        for i in range(len(self.pending_transactions)-1,-1,-1):
            if self.pending_transactions[i].orderId == orderID:
                s = {
                    "OrderID":orderID,
                    "Timestamp":self.pending_transactions[i].timestamp,
                    "ProductId":self.pending_transactions[i].product_id,
                    "Client":self.pending_transactions[i].client.name,
                    "Status":self.pending_transactions[i].status,
                    "Mined into Blockchain":"Not yet"
                }
                s["Verification"]="Done" if self.pending_transactions[i].verification==1 else "Not Done"
                s["distributor"]="Not Assigned" if  self.pending_transactions[i].distributor==None else  self.pending_transactions[i].distributor.name
                s= str(s)
                qr = pyqrcode.create(s)
                qr.png('myqr.png', scale = 6)
                return

        for i in range(len(self.chain)-1,-1,-1):
            for j in range(len(self.chain[i].transactions)-1,-1,-1):
                if self.chain[i].transactions[j].orderId == orderID:
                    s = {
                    "OrderID":orderID,
                    "Timestamp":self.chain[i].transactions[j].timestamp,
                    "ProductId":self.chain[i].transactions[j].product_id,
                    "Client":self.chain[i].transactions[j].client.name,
                    "Status":self.chain[i].transactions[j].status,
                    "Mined into Blockchain":"Done"
                    }
                    s["Verification"]="Done" if self.chain[i].transactions[j].verification==1 else "Not Done"
                    s["distributor"]="Not Assigned" if  self.chain[i].transactions[j].distributor==None else  self.chain[i].transactions[j].distributor.name
                    s= str(s)
                    qr = pyqrcode.create(s)
                    qr.png('myqr.png', scale = 6)
                    return
        print("NOT FOUND")
        return

    def get_latest_block(self):
        return self.chain[-1]
    
    def add_transaction(self , transaction):
        self.pending_transactions.append(transaction)
        # if len(self.pending_transactions)==4:
        #     self.mine_pending_transactions()

    def mine_pending_transactions(self):
        if len(self.chain) == 0:
            hash ="0"
        else:
            # print("hello")
            hash=self.get_latest_block().hash 
        block = Block(len(self.chain) , time.time() , self.pending_transactions , hash , 0 , self.difficulty)
        block.mine_block_POW()
        self.chain.append(block)
        self.pending_transactions = []
    
    def is_chain_valid(self):
        for i in range(1 , len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i-1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.prev_hash != prev_block.hash:  
                return False
        return True
    
    def blockchain_printer(self):
        print("difficulty: ",self.difficulty)
        for i in self.chain:
            print("Block ",i,"\n")
        print("PENDING Transactions: ")
        for j in self.pending_transactions:
            print(j)


class Client:
    def __init__(self , security_deposit):
        self.name = input("Enter name: ")
        self.security_deposit = security_deposit
        CLIENTS[self.name] = self
        self.orders = {}

    def addseqDeposit(self):
        try:
            self.security_deposit+= int(input("Enter Amount to be added: "))
        except:
            pass
    def confDelivery(self):
        x=list(enumerate(self.orders))
        print(*x,sep="\n")
        try:
            id = int(input("Enter order id: "))
        except:
            print("INVALID INPUT")
            return
        if self.orders[x[id][1]][1] != 'UNASSIGNED distributor':
            BLOCKCHAIN.add_transaction(Transaction(x[id][1],self.orders[x[id][1]][0],"DELIVERED",None,self.orders[x[id][1]][1],self,verification=1))
            del(self.orders[x[id][1]])
        else:
            print("NOT Possible")


    def loop(self):
        ch=1
        while ch!=5:
            print("1. Place orders","2. Confirm Delivery","3. Add security Deposit","4. Show orders","5. LogOut",sep="\n")
            try:
                ch = int(input("Enter Choice: "))
            except:
                print("INVALID INPUT")
                self.loop()
            if ch==1:
                x = MANUFACTURER.addOrder(self)
                if x:
                    self.orders[x[0]]=x[1:]
            elif ch==2 and len(self.orders):
                self.confDelivery()
            elif ch==3:
                self.addseqDeposit()
            elif ch==4:
                print(self.orders,sep="\n")
                # print(*list(enumerate(self.orders)),sep="\n")

    def __str__(self):
        return f'Client [name: {self.name}, security_deposit: {self.security_deposit}]'
        
        
class Distributor:
    def __init__(self , security_deposit):
        self.name = input("Enter name: ")
        self.security_deposit = security_deposit  
        self.isfree = True  
        self.cur_order=None
        DISTRIBUTORS[self.name] = self

    def addseqDeposit(self):
        try:
            self.security_deposit += int(input("Enter Amount to be added: "))
        except:
            print("INVALID INPUT")

    def sendOrder(self):
        print(self.cur_order)
        BLOCKCHAIN.add_transaction(Transaction(self.cur_order[0],self.cur_order[1],"To Client",None,self,self.cur_order[2]))
        print(self.cur_order[2])
        (self.cur_order[2]).orders[self.cur_order[0]][1]=self
        self.cur_order=None
        self.isfree=True

    def loop(self):
        ch=1
        while ch!=3:
            print("1. Get Orders from Placed orders","2. Send Order","3.LogOut",sep="\n")
            try:
                ch = int(input("Enter Choice: "))
            except:
                print("INVALID CHOICE")
                self.loop()
            if ch==1 and self.isfree:
                self.isfree,self.cur_order=MANUFACTURER.giveOrders(self)
            elif ch==2 and not self.isfree:
                self.sendOrder()
            elif ch==1:
                print("Not Free")
            elif ch==2:
                print("NO order undertaken")
            

    def __str__(self):
        return f'Distributor [name: {self.name}, security_deposit: {self.security_deposit}]'
        
        
class Manufacturer:
    def __init__(self):
        # self.name = input("Enter name: ")
        self.name="BCPROJECT"
        self.products = {'ORE1341':["oreo",10],'CHI1872':["chips",10]}
        # self.addproducts()
        self.orders=[]
    
    def addproducts(self):
        addmore= "Y"
        while addmore.upper()=='Y':        
            if addmore.upper() == 'Y':
                pname=input("Enter Product name: ")
                pcost = int(input("Enter Product cost: ")) 
                pid = pname[:3].upper()+str(random.randint(1000,2000))
                # while pid not in self.products:
                    # pid = self.name[:3]+pname[:3]+str(random.randint(100,200))  
                self.products[pid] = [pname,pcost]
            else:
                break
            addmore = (input("Enter more products(y/n): "))
        
    def giveOrders(self,distri):
        for i,x in enumerate(self.orders):
            print(i,x)
        try:
            ch = int(input("Enter choice: "))
            x = list(enumerate(self.orders))[ch][1]
        except:
            print("Invalid Choice")
            return True,None
        if x[1][1]<=distri.security_deposit:
            BLOCKCHAIN.add_transaction(Transaction(x[0],x[3],"To distributor",1,distri,x[2],verification=1))
            self.orders.pop(self.orders.index(x))
            return False,(x[0],x[3],x[2])
        else:
            print("Not Enough money")
            return True,None
        
    def loop(self):
        print("1. add products\n2. Show Products\n3. Exit")
        try:
            ch=int(input("Enter Choice: "))
        except:
            print("INVALID CHOICE")
            self.loop()
        while ch!=3:
            if ch==1:
                self.addproducts()
            elif ch==2:
                print(*[str(x)+":"+"--".join(map(str,self.products[x])) for x in self.products],sep="\n")
            elif ch==3:
                return
            print("1. add products\n2. Show Products\n3. Exit")
            try:
                ch=int(input("Enter Choice: "))
            except:
                print("INVALID CHOICE")
                break
            

    def addOrder(self,client):
        x = list(enumerate(self.products))
        print(*x,sep="\n")
        try:
            pid = int(input("Enter PID: "))
        except:
            print("INVALID INPUT")
            return
        pid= x[pid][1]
        if client.security_deposit >= self.products[pid][1]:
            x = hashlib.sha256()
            x.update((str(self.products[pid])+str(client)+str(time.ctime())).encode('utf-8'))
            x = x.hexdigest()
            BLOCKCHAIN.add_transaction(Transaction(x,pid,"Ordered",1,None,client,verification=1))
            self.orders.append([x,self.products[pid],client,pid])
            return list([x,pid,"UNASSIGNED distributor"])
        else:
            print("NOt enough money")
            return None

    def __str__(self):
        return f'Manufacturer [name: {self.name}, security_deposit: {self.security_deposit}]'

def setup():
    b = Blockchain(3)
    m = Manufacturer()
    return b,m

def printlogin():
    print("1. Create User")
    print("2. Log-In ")
    print("3. Mine Block")
    print("4. Print BlockChain")
    print("5. Verify Blockchain")
    print("6. Make QR Code using Product Order ID")
    print("7. Exit")
    try:
        ch = int(input("Enter Choice: "))
    except:
        ch=7
    return ch

def usercreate():
    print("Select User Type: ","1.Distributor","2.Client",sep ="\n")
    try:
        ch = int(input("Enter Choice: "))
    except:
        print("invalid choice")
        return
    if ch==1:
        d = Distributor(2000)
        DISTRIBUTORS[d.name]=d
    elif ch ==2:
        c = Client(2000)
        CLIENTS[c.name]=c
        

def loginexist(blockchain):
    print("Select User Type: ","1.Manufacturer","2.Distributor","3.Client","4.Exit",sep ="\n")
    try:
        ch=int(input("Enter Your Choice: "))
    except:
        ch=4
    if ch==1:
        MANUFACTURER.loop()
    elif ch==2:
        x=input("Enter distributor Name: ")
        if x in DISTRIBUTORS:
            DISTRIBUTORS[x].loop()
        else:
            print("NO distributor of this name.")
    elif ch==3:
        x= input("Enter Client Name: ")
        if x in CLIENTS:
            CLIENTS[x].loop()
        else:
            print("NO client of this name.")
    elif ch==4:
        return
    loginexist(blockchain)
        
def mainloop(blockchain):
    ch=None
    while ch!=7:
        ch = printlogin()
        if ch == 1:
            usercreate()
        elif ch == 2:
            loginexist(blockchain)
        elif ch==3:
            print(BLOCKCHAIN.pending_transactions)
            blockchain.mine_pending_transactions()
        elif ch==4:
            blockchain.blockchain_printer()
        elif ch==5:
            if blockchain.is_chain_valid():
                print("verification Complete\nSUCCESS")
            else:
                print("Verification Error\nFAILED")
        elif ch==6:
            BLOCKCHAIN.getQR(input("orderID: "))
            
class Block(Transaction , Client , Manufacturer , Distributor):
    def __init__(self, index , timestamp , transactions , prev_hash , nonce , difficulty):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.nonce = nonce
        self.difficulty = difficulty
        self.hash = self.calculate_hash()
        self.merkle_root = self.build_merkle_tree()
            
    def calculate_hash(self):
        sha = hashlib.sha256("".join([str(i.hash)  for i in self.transactions]).encode('utf-8'))
        sha.update(str(self.index).encode('utf-8') + 
                   str(self.timestamp).encode('utf-8') +
                    str(self.prev_hash).encode('utf-8') +
                    str(self.nonce).encode('utf-8') +
                    str(self.difficulty).encode('utf-8'))
        return sha.hexdigest()
    
    def approve_transactions(self):
        for i , tx in enumerate(self.transactions):
            if tx.verification == 1: # If verified , then do nothing
                continue
            elif tx.transaction == 0: # If not verified , then make sure there is no issue
                for j in range (i , len(self.transactions)): # Check if there is any other transaction with same order id , in the array after this transaction
                    if tx.orderId == self.transactions[j].orderId: # This means that the customer has received the order
                        if tx.signature == self.transactions[j].signature:
                            tx.verification = 1 # If client sign matches the manufacturer's sign , then verification = 1
                
                for j in range (0 , i):
                    if tx.orderId == self.transactions[j].orderId: # This means that the distributor had received the product from the manufacturer
                        if tx.signature != self.transactions[j].signature: #Distributor is lying
                            Distributor().security_deposit -=  400
                            print("Distributor was caught lying and security deposit deducted")
                        else:
                            Client().security_deposit -= 400
                            print("Distributor was caught lying and security deposit deducted")
            else: # If not verified , then make sure there is no issue
                tx.verification = 1
                
    def mine_block_POW(self):
        # Stores the root hash of the Merkle Tree for the block's transactions
        # self.approve_transactions()
        while self.hash[:self.difficulty] != '0' * self.difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f'Block mined: {self.hash}')
        
    def build_merkle_tree(self):
        transaction_hashes = [tx.hash for tx in self.transactions]
        if len(transaction_hashes) % 2 != 0: # If odd number of transactions, duplicate last transaction to make it even
            transaction_hashes.append(transaction_hashes[-1]) # merkle tree requires even number of leaf nodes
        while len(transaction_hashes) > 1:
            new_hashes = [] # pair up adjacent hashes to make a new hash , until only one reamins
            for i in range(0, len(transaction_hashes), 2):
                new_hashes.append(hashlib.sha256((transaction_hashes[i] + transaction_hashes[i+1]).encode('utf-8')).hexdigest())
            transaction_hashes = new_hashes
            if len(transaction_hashes) % 2 != 0 and len(transaction_hashes) != 1 :
                transaction_hashes.append(transaction_hashes[-1])
            # print(transaction_hashes,"<-")
        # print("Hello")
        return transaction_hashes[0]

    def __str__(self):
        # return f'Block {self.index} [timestamp: {self.timestamp},Previous hash: {self.prev_hash},\ntransactions: {self.transactions},\nhash: {self.hash},\nMerkle Root: {self.merkle_root}\n,]'
        x= self.__dict__
        x["transactions"] = [str(i) for i in self.transactions]
        return str(x)

        
if __name__=='__main__':
    BLOCKCHAIN,MANUFACTURER = setup()
    mainloop(BLOCKCHAIN)