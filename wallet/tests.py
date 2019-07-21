from django.test import TransactionTestCase
from django.contrib.auth import get_user_model

from wallet.models import Wallet


class WalletTests(TransactionTestCase):

    BALANCE_INITIAL = 10000
    BALANCE_DEPOSIT = 1500
    BALANCE_WITHDRAWAL = 750

    def setUp(self):
        """ Setups the test environment. Creates user and wallet.
        """

        print("Setting up the test environment.")
        self.user = get_user_model()()
        self.user.save()
        print("Created user.")
        self.wallet = Wallet(
            user=self.user, name="default", balance=self.BALANCE_INITIAL)
        self.wallet.save()
        print("Created wallet.")

    def test_balance(self):
        """ Tests the wallet for initial balance.
        """

        self.assertEqual(self.wallet.balance, self.BALANCE_INITIAL)

    def test_deposit(self):
        """ Test deposit functionality on user's wallet.
        """

        self.wallet.deposit(self.BALANCE_DEPOSIT)

        # Verify the balance of wallet after deposit.
        self.assertEqual(
            self.wallet.balance, self.BALANCE_INITIAL + self.BALANCE_DEPOSIT)

        # Verify the transaction details after deposit.
        transaction_deposit = self.wallet.transaction_set.all().last()
        self.assertEqual(transaction_deposit.amount, self.BALANCE_DEPOSIT)
        self.assertEqual(
            transaction_deposit.running_balance, self.wallet.balance)

    def test_withdrawal(self):
        """ Test withdrawal functionality on user's wallet.
        """

        self.wallet.withdraw(self.BALANCE_WITHDRAWAL)

        # Verify the balance of wallet after withdrawal.
        self.assertEqual(
            self.wallet.balance,
            self.BALANCE_INITIAL - self.BALANCE_WITHDRAWAL)

        # Verify the transaction details after withdrawal.
        transaction_withdrawal = self.wallet.transaction_set.all().last()
        self.assertEqual(
            transaction_withdrawal.amount, -self.BALANCE_WITHDRAWAL)
        self.assertEqual(
            transaction_withdrawal.running_balance, self.wallet.balance)
