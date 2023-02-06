from rave_python import Rave
from decouple import config

class FlutterwavePaymentCollector:
    def __init__(self, country="NG"):
        self.rave = Rave(secretKey=config('FLW_SEC_KEY'), publicKey=config('FLW_PLC_KEY'), usingEnv=False)
        self.country = country

    def create_virtual_account(self, account_alias, email, tx_ref):
        response = self.rave.VirtualAccount.create(
            {"is_permanent":False, "firstname": account_alias, "tx_ref":tx_ref, "email":email, "account_alias":account_alias, "narration": account_alias}
        )
        if response["error"]:
            return {"error": response["message"]}
        else:
            return response["data"]

    def retrieve_transactions(self, account_number):
        response = self.rave.VirtualAccount.transactions(account_number)

        if response["status"] == "success":
            return response["data"]
        else:
            return {"error": response["message"]}
            
    def verify_bank_account(self, bank_code, account_number):
        response = self.rave.Account.verify(bank_code, account_number)

        if response["status"] == "success":
            return response["data"]
        else:
            return {"error": response["message"]}
            
    def confirm_payment(self, account_number, transaction_ref):
        response = self.rave.VirtualAccount.confirm_payment(account_number, transaction_ref)

        if response["status"] == "success":
            return response["data"]
        else:
            return {"error": response["message"]}
            
    def withdraw_funds(self, account_number, amount, currency="NGN"):
        response = self.rave.VirtualAccount.withdraw_funds(
            account_number=account_number,
            amount=amount,
            currency=currency
        )

        if response["status"] == "success":
            return response["data"]
        else:
            return {"error": response["message"]}

