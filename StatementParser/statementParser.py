import Enum

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

class StatementParser(object):
	""" Attributes	
	statement_regex
	"""

	""" Behaviours
	"""
	def __init__(self, r):
		self.statement_regex = r

class BankInformation(object):
	""" Attributes
	bank_name
	bank_id
	transactions
	parser
	"""
	def __init__(self, b_name, b_id, b_parser):
		self.bank_name = b_name
		self.bank_id   = b_id
		self.parser    = b_parser

