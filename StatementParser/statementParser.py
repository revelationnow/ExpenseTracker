from enum import Enum
import getpass
import csv

class TransactionType(Enum):
	TRANSACTION_TYPE_INCOME  = 1
	TRANSACTION_TYPE_EXPENSE = 2
	TRANSACTION_TYPE_UNKNOWN = 3

class ExpenseType(Enum):
	EXPENSE_TYPE_MORTGAGE             = 1
	EXPENSE_TYPE_RENT                 = 2
	EXPENSE_TYPE_HOME_INSURANCE       = 3
	EXPENSE_TYPE_HOA_FEES             = 4
	EXPENSE_TYPE_CAR_PAYMENT          = 5
	EXPENSE_TYPE_CAR_INSURANCE        = 6
	EXPENSE_TYPE_GROCERY              = 7
	EXPENSE_TYPE_MERCHANDISE          = 8
	EXPENSE_TYPE_TRAVEL               = 9
	EXPENSE_TYPE_FUEL                 = 10
	EXPENSE_TYPE_CHARITY              = 11
	EXPENSE_TYPE_LIFE_INSURANCE       = 12
	EXPENSE_TYPE_ENTERTAINMENT        = 13
	EXPENSE_TYPE_SUBSCRIPTIONS        = 14
	EXPENSE_TYPE_INTERNET             = 15
	EXPENSE_TYPE_PHONE                = 16
	EXPENSE_TYPE_CABLE                = 17
	EXPENSE_TYPE_WATER                = 18
	EXPENSE_TYPE_ELECTRICITY          = 19
	EXPENSE_TYPE_STOCK_PURCHASE       = 20
	EXPENSE_TYPE_RETIREMENT_PLAN      = 21
	EXPENSE_TYPE_HSA_PLAN             = 22
	EXPENSE_TYPE_DINING_OUT           = 23
	EXPENSE_TYPE_EDUCATION            = 24
	EXPENSE_TYPE_INTERNATIONAL_TRAVEL = 25
	EXPENSE_TYPE_CAR_REGISTRATION     = 26
	EXPENSE_TYPE_MISCELLENOUS         = 27

class TransactionFieldType(Enum):
  TRANSACTION_FIELD_TYPE_MISC          = 1
  TRANSACTION_FIELD_TYPE_TRANS_DATE    = 2
  TRANSACTION_FIELD_TYPE_POST_DATE     = 3
  TRANSACTION_FIELD_TYPE_CARD_NO       = 4
  TRANSACTION_FIELD_TYPE_DESCRIPTION   = 5
  TRANSACTION_FIELD_TYPE_CATEGORY      = 6
  TRANSACTION_FIELD_TYPE_DEBIT_AMOUNT  = 7
  TRANSACTION_FIELD_TYPE_CREDIT_AMOUNT = 8
  TRANSACTION_FIELD_TYPE_MAX           = 9


class Transactions(object):
  """ Attributes
  transaction_id
  bank_id
  transaction_type
  expense_name
  expense_type_reported
  expense_type_determined
  transaction_amount
  transaction_date
  transaction_card
  """
  def __init__(self, t_id, t_type, e_name, e_type_rep, e_type_det, amount, b_id):
    self.transaction_id          = t_id
    self.transaction_type        = t_type
    self.expense_name            = e_name
    self.expense_type_reported   = e_type_rep
    self.expense_type_determined = e_type_det
    self.transaction_amount      = amount
    self.bank_id                 = b_id    
  
  def printTransaction(self):
    print("\t\tTrans_id\tTrans_type\tExpense_name\tExpense_Type\tAmount")
    print("\t\t" + str(self.transaction_id)+"\t"+ str(self.transaction_type) + "\t" + self.expense_name + "\t" + self.expense_type_reported + "\t" + self.transaction_amount)
    

class StatementParser(object):
  """ Attributes	
  statement_format
  has_header
  dictionary
  """

  """ Behaviours
  """
  def __init__(self, r, has_header):
    self.statement_format = r
    self.has_header = has_header
    self.generateDictionary()

  def generateDictionary(self):
    fields = self.statement_format.split(',')
    self.dictionary = dict()
    count = 0
    for field in fields:
      self.dictionary[TransactionFieldType(int(field))] = count
      count = count + 1

    for i in range(TransactionFieldType.TRANSACTION_FIELD_TYPE_TRANS_DATE.value,TransactionFieldType.TRANSACTION_FIELD_TYPE_MAX.value):
      if TransactionFieldType(i) not in self.dictionary:
        print("Format must have field '" + str(i) + "'")
        exit()



    

  def getTransType(self, t_row):
    return TransactionType.TRANSACTION_TYPE_EXPENSE 

  def getExpenseName(self, t_row):
    return t_row[self.dictionary[TransactionFieldType.TRANSACTION_FIELD_TYPE_DESCRIPTION]]
  def getExpenseRep(self, t_row):
    return t_row[self.dictionary[TransactionFieldType.TRANSACTION_FIELD_TYPE_CATEGORY]]

  def getExpenseDet(self, t_row):
    return t_row[self.dictionary[TransactionFieldType.TRANSACTION_FIELD_TYPE_CATEGORY]]

  def getAmount(self, t_row):
    return t_row[self.dictionary[TransactionFieldType.TRANSACTION_FIELD_TYPE_DEBIT_AMOUNT]]
    

  def parse(self, tf_path):
    t_file = open(tf_path)
    csv_reader = csv.reader(t_file)
    flag = False
    transactions = []
    for row in csv_reader:
      if(flag == False and self.has_header == True):
        flag = True
        continue
      t_type     = self.getTransType(row)
      e_name     = self.getExpenseName(row)
      e_type_rep = self.getExpenseRep(row)
      e_type_det = self.getExpenseDet(row)
      amount     = self.getAmount(row)
      transaction = Transactions(0, t_type, e_name, e_type_rep, e_type_det, amount, 0)
      transactions.append(transaction)

    return transactions




class BankInformation(object):
  """ Attributes
  bank_name
  bank_id
  transactions
  transaction_ids
  parser
  """
  transaction_ids = 0
  def __init__(self, b_name, b_id, b_format, has_header):
    self.bank_name = b_name
    self.bank_id   = b_id
    self.parser    = StatementParser(b_format, has_header)
    self.transactions = []

  def processTransaction(self, transaction_file_path):
    new_transactions = self.parser.parse(transaction_file_path)

    for transaction in new_transactions:
      transaction.transaction_id = BankInformation.transaction_ids + 1
      transaction.bank_id = self.bank_id
      BankInformation.transaction_ids = BankInformation.transaction_ids + 1

    self.transactions.extend(new_transactions)

  def printTransactions(self):
    print("\tBANK_NAME : " + self.bank_name)
    print("\tTransaction List : ")
    for trans in self.transactions:
      trans.printTransaction()

    

class User(object):
  """ Attributes
  user_name
  user_id
  password
  u_bank_list
  address
  """

  def __init__(self, uname, passwd, uid):
    self.user_name = uname
    self.password = passwd
    self.user_id = uid
    self.u_bank_list = []

  def addBank(self, bank):
    self.u_bank_list.append(bank)

  def processTransaction(self, transaction_file_path):
    print("List of supported banks for user '" + self.user_name +"'")
    for bank in self.u_bank_list:
      print(str(bank.bank_id) + " " + bank.bank_name)

    b_check_status = True
    b_check_list = []
    while(b_check_status):
      bank_id = input("Enter id of bank from which this transaction file is : ")
      b_check_list = list(filter(lambda x:x.bank_id == int(bank_id), self.u_bank_list))
      if len(b_check_list) == 0:
        print("Bank id '" + bank_id +"' doesn't exist, try again")
      else:
        b_check_status = False
    bank = b_check_list[0]
    bank.processTransaction(transaction_file_path)

  def printSummary(self):
    print("**********************************")
    print("USERNAME : " + self.user_name)
    print("BANKS AND TRANSACTIONS : ")
    for bank in self.u_bank_list:
      bank.printTransactions()


class App(object):
  """ Attributes
  user_list
  bank_list
  bank_ids
  user_ids
  """
  bank_ids = 0
  user_ids = 0

  def __init__(self):
    self.user_list = []
    self.bank_list = []
    App.bank_ids = 0
    App.user_ids = 0

  def addUser(self, uname, passwd):
    user = User(uname, passwd, App.user_ids)
    App.user_ids = App.user_ids + 1
    self.user_list.append(user)

  def addBank(self, b_name, b_format, b_has_header):
    bank = BankInformation(b_name, App.bank_ids, b_format, b_has_header)
    App.bank_ids = App.bank_ids + 1
    self.bank_list.append(bank)

  def addUserMenu(self):
    check_status = True
    while check_status:
      uname = input("Enter user name : ")
      check_list = list(filter(lambda x:x.user_name == uname, self.user_list))
      if len(check_list) == 0:
        check_status = False
      else:
        print("Username '" + uname + "' already exists choose a new one")
    passwd = getpass.getpass("Enter your password : ")
    self.addUser(uname, passwd)
    print("User '" + uname + "' added")

  def addBankMenu(self):
    check_status = True
    while check_status:
      b_name = input("Enter bank name : ")
      check_list = list(filter(lambda x:x.bank_name == b_name, self.bank_list))
      if len(check_list) == 0:
        check_status = False
      else:
        print("Bank '" + b_name + "' already exists, please enter again")

    print("Available bank fields are : ")

    b_format = input("Enter bank format as 'Field1,Field2,Field3,...' : ")
    b_has_header_ip = input("Enter 1 if bank CSV file has headers, 0 otherwise : ")
    b_has_header = True
    if(b_has_header_ip != '1'):
      b_has_header = False

    self.addBank(b_name, b_format, b_has_header)
    print("Bank '" + b_name + "' with format '" + b_format + "' added")



  def selectUserAddBankMenu(self, user):
    print("Available banks are :\n")
    for bank in self.bank_list:
      print(str(bank.bank_id) + " " +  bank.bank_name)

    b_check_status = True
    b_check_list = []
    while(b_check_status):
      b_choice = input("Enter bank id : ")
      b_check_list = list(filter(lambda x:x.bank_id == int(b_choice), self.bank_list))
      if(len(b_check_list) == 0):
        print("Bank id '" + b_choice + "' doesn't exist, try again")
      else:
        b_check_status = False
    bank = b_check_list[0]
    user.addBank(bank)
    print("Added bank '" + bank.bank_name + "' to User '" + user.user_name +"'")


  def selectUserMenu(self):
    uname = input("Enter user name of user to select : ")
    passwd = getpass.getpass("Enter password of user : ")
    check_list = list(filter(lambda x:x.user_name == uname, self.user_list))
    check_status = True;
    if(len(check_list) == 0):
      check_status = False
    elif(check_list[0].password != passwd):
      check_status = False

    if(check_status == False):
      print("User not found or password didn't match, please try again")
    else:
      user = check_list[0]
      while(1):
        print("What would you like to do : ")
        u_choice = input("Your options are :\n1. Add a Bank to User\n2. Parse transactions\n3. Get user summaries\n4. Log out\nEnter your choice : ")
  
        if(u_choice == '1'):
          self.selectUserAddBankMenu(user)
  
        elif(u_choice == '2'):
          transaction_file = input("Enter path to transaction file : ")
          user.processTransaction(transaction_file)
          print("Transaction file added!")
        elif(u_choice == '3'):
          self.printUserSummary(user)
        elif(u_choice == '4'):
          print("Logging out")
          break

  def printUserSummary(self, user):
    user.printSummary()

  def appMain(self):
    while(1):
      print("What do you want to do : ")
      print("Your options are :\n1. Add User\n2. Select User\n3. Add Bank\n4. Exit")
      choice = input("Enter your choice : ")
      if(choice == '1'):
        self.addUserMenu()
        
      elif(choice == '4'):
        print("\nExiting!\n")
        break

      elif(choice == '3'):
        self.addBankMenu()

      elif(choice == '2'):
        self.selectUserMenu()      



if __name__ == '__main__' :
  app = App()
  app.appMain()

