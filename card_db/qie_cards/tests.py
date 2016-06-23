from django.test import TestCase
from django.core.exceptions import ValidationError
from models import QieCard, Test, Tester, Attempt, Location
from django.utils import timezone


def setup():
    card1 = QieCard.objects.create(
                barcode="9900001",
                uid="01:23:45:67:89:aF",
                plane_loc = "J26",
                comments="This is a QieCard"
                )
    card2 = QieCard.objects.create(
                barcode="9900002",
                uid="00:00:00:ea:fa:01",
                plane_loc = "J25",
                comments="This is another QieCard"
                )
    card3 = QieCard.objects.create(
                barcode="9900003",
                uid="00:00:00:ea:fa:03",
                plane_loc = "J24",
                comments="This is yet another QieCard"
                )
    
    test1 = Test.objects.create(
                name="Test test 1",
                abbreviation="test1",
                description = "This is a test test",
                required=False
                )
    test2 = Test.objects.create(
                name="Test test 2",
                abbreviation="test2",
                description = "This is a test test",
                required=False
                )
    
    tester1 = Tester.objects.create(
                username="Testy McTestface",
                email="Tester@gmail.com"
                )
    tester2 = Tester.objects.create(
                username="Testina Tester",
                email="TTester@baylor.edu"
                )
    
    attempt11 = Attempt.objects.create(
                card = card1,
                test_type = test1,
                attempt_number = 1,
                tester = tester1,
                date_tested = timezone.now(),
                num_passed = 100,
                num_failed = 0,
                revoked = False,
                temperature = 10,
                humidity = 10,
                comments = "This is an attempt",
                image = "non-default.jpg",
                log_file = "log.txt"
                )
    attempt12 = Attempt.objects.create(
                card = card1,
                test_type = test1,
                attempt_number = 2,
                tester = tester1,
                date_tested = timezone.now(),
                num_passed = 100,
                num_failed = 3,
                revoked = False,
                temperature = 10,
                humidity = 10,
                comments = "This is an attempt",
                image = "non-default.jpg",
                log_file = "log.txt",
                log_comments = "This is a log"
                )
    attempt13 = Attempt.objects.create(
                card = card1,
                test_type = test2,
                attempt_number = 1,
                tester = tester1,
                date_tested = timezone.now(),
                num_passed = 100,
                num_failed = 0,
                revoked = True,
                temperature = 10,
                humidity = 10,
                comments = "This is an attempt",
                image = "non-default.jpg",
                log_file = "log.txt",
                log_comments = "This is a log"
                )
    attempt14 = Attempt.objects.create(
                card = card1,
                test_type = test2,
                attempt_number = 2,
                tester = tester1,
                date_tested = timezone.now(),
                num_passed = 100,
                num_failed = 0,
                revoked = False,
                temperature = 10,
                humidity = 10,
                comments = "This is an attempt",
                image = "non-default.jpg",
                log_file = "log.txt",
                log_comments = "This is a log"
                )
    attempt21 = Attempt.objects.create(
                card = card2,
                test_type = test1,
                attempt_number = 1,
                tester = tester1,
                date_tested = timezone.now(),
                num_passed = 100,
                num_failed = 3,
                revoked = True,
                temperature = 10,
                humidity = 10,
                comments = "This is an attempt",
                image = "non-default.jpg",
                log_file = "log.txt",
                log_comments = "This is a log"
                )
    attempt22 = Attempt.objects.create(
                card = card2,
                test_type = test1,
                attempt_number = 2,
                tester = tester1,
                date_tested = timezone.now(),
                num_passed = 100,
                num_failed = 0,
                revoked = False,
                temperature = 10,
                humidity = 10,
                )
    attempt23 = Attempt.objects.create(
                card = card2,
                test_type = test2,
                attempt_number = 1,
                tester = tester1,
                date_tested = timezone.now(),
                num_passed = 100,
                num_failed = 3,
                revoked = True,
                temperature = 10,
                humidity = 10,
                comments = "This is an attempt",
                image = "non-default.jpg",
                log_file = "log.txt",
                log_comments = "This is a log"
                )
    attempt24 = Attempt.objects.create(
                card = card2,
                test_type = test2,
                attempt_number = 2,
                tester = tester1,
                date_tested = timezone.now(),
                num_passed = 100,
                num_failed = 0,
                revoked = True,
                temperature = 10,
                humidity = 10,
                comments = "This is an attempt",
                image = "non-default.jpg",
                log_file = "log.txt",
                log_comments = "This is a log"
                )
    attempt31 = Attempt.objects.create(
                card = card3,
                test_type = test1,
                attempt_number = 1,
                tester = tester1,
                date_tested = timezone.now(),
                num_passed = 100,
                num_failed = 0,
                revoked = False,
                temperature = 10,
                humidity = 10,
                comments = "This is an attempt",
                image = "non-default.jpg",
                log_file = "log.txt"
                )
    attempt32 = Attempt.objects.create(
                card = card3,
                test_type = test2,
                attempt_number = 1,
                tester = tester1,
                date_tested = timezone.now(),
                num_passed = 100,
                num_failed = 0,
                revoked = False,
                temperature = 10,
                humidity = 10,
                comments = "This is an attempt",
                image = "non-default.jpg",
                log_file = "log.txt"
                )

    location1 = Location.objects.create(
                card = card1,
                date_received = timezone.now(),
                geo_loc = "14th floor, Wilson Hall, Batavia, IL, United States"
                )
    location2 = Location.objects.create(
                card = card1,
                date_received = timezone.now(),
                geo_loc = "LHC: CMS"
                )
    location3 = Location.objects.create(
                card = card2,
                date_received = timezone.now(),
                geo_loc = "14th floor, Wilson Hall, Batavia, IL, United States"
                )
    location4 = Location.objects.create(
                card = card2,
                date_received = timezone.now(),
                geo_loc = "LHC: CMS"
                )
    
class TestTest(TestCase):
    
    def test_cards_failed(self): 
        setup()
        test1 = Test.objects.get(abbreviation="test1")
        test2 = Test.objects.get(abbreviation="test2")
        self.assertEqual(len(test1.cards_failed()), 1)
        self.assertEqual(len(test2.cards_failed()), 0)
   
    def test_num_failed(self):
        setup()
        test1 = Test.objects.get(abbreviation="test1")
        test2 = Test.objects.get(abbreviation="test2")
        self.assertEqual(test1.num_failed(), 1)
        self.assertEqual(test2.num_failed(), 0)

    def test_perc_failed(self):
        setup()
        test1 = Test.objects.get(abbreviation="test1")
        test2 = Test.objects.get(abbreviation="test2")
        self.assertEqual(test1.perc_failed(), 33.3)
        self.assertEqual(test2.perc_failed(), 0)

    def test_cards_passed_all(self):
        setup()
        test1 = Test.objects.get(abbreviation="test1")
        test2 = Test.objects.get(abbreviation="test2")  
        self.assertEqual(len(test1.cards_passed_all()), 1)
        self.assertEqual(len(test2.cards_passed_all()), 1)

    def test_num_passed(self):
        setup()
        test1 = Test.objects.get(abbreviation="test1")
        test2 = Test.objects.get(abbreviation="test2")
        self.assertEqual(test2.num_passed(), 1)
        self.assertEqual(test2.num_passed(), 1)

    def test_perc_passed(self):
        setup()
        test1 = Test.objects.get(abbreviation="test1")
        test2 = Test.objects.get(abbreviation="test2")
        self.assertEqual(test1.perc_passed(), 33.3)
        self.assertEqual(test2.perc_passed(), 33.3)

    def returnTrue():
        return True
    

class QieCardTest(TestCase):
    def test_barcode_validation(self):
        setup()
        with self.assertRaisesMessage(ValidationError,
                "ID must only contain numbers"):
            QieCard.objects.create(
                    barcode="9a00000",
                    uid="01:23:45:67:89:ab",
                    plane_loc = "J26",
                    comments="This is a QieCard"
                    )
        with self.assertRaisesMessage(ValidationError,
                "ID must be 7 digits long"):
            QieCard.objects.create(
                    barcode="90000000",
                    uid="01:23:45:67:89:ab",
                    plane_loc = "J26",
                    comments="This is a QieCard"
                    )
        with self.assertRaisesMessage(ValidationError,
                'Card "001" is already recorded'):
            QieCard.objects.create(
                    barcode="9000001",
                    uid="01:23:45:67:89:ab",
                    plane_loc = "J26",
                    comments="This is a QieCard"
                    )
        with self.assertRaisesMessage(ValidationError, 'exists'):
            QieCard.objects.create(
                    barcode="9900001",
                    uid="01:23:45:67:89:ab",
                    plane_loc = "J26",
                    comments="This is a QieCard"
                    )

    def test_uid_validation(self):
        setup()
        with self.assertRaisesMessage(ValidationError,
                "UID must have six ':'-separated sections"):
            QieCard.objects.create(
                    barcode="9900000",
                    uid="01:23:45:67:89ab", 
                    plane_loc = "J26",
                    comments="This is a QieCard"
                    )
        with self.assertRaisesMessage(ValidationError,
                "Each section must contain two characters"):
            QieCard.objects.create(
                    barcode="9900000",
                    uid="01:23:45:7:89:ab",
                    plane_loc = "J26",
                    comments="This is a QieCard"
                    )
        with self.assertRaisesMessage(ValidationError,
                'UID may only contain hexadecimal digits'):
            QieCard.objects.create(
                    barcode="9000001",
                    uid="01:23:45:67:89:aq", 
                    plane_loc = "J26", 
                    comments="This is a QieCard"
                    )
        with self.assertRaisesMessage(ValidationError, 'exists'):
            QieCard.objects.create(
                    barcode="9000001", 
                    uid="01:23:45:67:89:aF",
                    plane_loc = "J26",
                    comments="This is a QieCard"
                    )

    def test_get_bar_uid(self):
        setup()
        testObj = QieCard.objects.all()[0]
        self.assertEqual(testObj.get_bar_uid(), "001")

    def test_get_passed(self):
        setup()
        test1 = QieCard.objects.get(barcode="9900001")
        test2 = QieCard.objects.get(barcode="9900002")
        self.assertEqual(len(test1.get_passed()), 1)
        self.assertEqual(len(test2.get_passed()), 1)

    def test_get_failed(self):
        setup()
        test1 = QieCard.objects.get(barcode="9900001")
        test2 = QieCard.objects.get(barcode="9900002")
        self.assertEqual(len(test1.get_failed()), 1)
        self.assertEqual(len(test2.get_failed()), 0)

    def test_get_remaining(self):
        setup()
        test1 = QieCard.objects.get(barcode="9900001")
        test2 = QieCard.objects.get(barcode="9900002")
        self.assertEqual(len(test1.get_remaining()), 0)
        self.assertEqual(len(test2.get_remaining()), 1)


class AttemptTest(TestCase):

    def test_passed_all(self):
        setup()
        card1 = QieCard.objects.get(barcode="9900001")
        card2 = QieCard.objects.get(barcode="9900002")
        test1 = Test.objects.all()[0]
        test2 = Test.objects.all()[1]
        attempt1 = Attempt.objects.get(
                        card = card1,
                        test_type = test1,
                        attempt_number = 2
                        )
        attempt2 = Attempt.objects.get(
                        card = card2,
                        test_type = test2,
                        attempt_number = 2
                        )
        self.assertEqual(attempt1.passed_all(), False)
        self.assertEqual(attempt2.passed_all(), True)

    def test_has_image(self):
        setup()
        card1 = QieCard.objects.get(barcode="9900001")
        card2 = QieCard.objects.get(barcode="9900002")
        test1 = Test.objects.all()[0]
        test2 = Test.objects.all()[1]
        attempt1 = Attempt.objects.get(
                        card = card1,
                        test_type = test1,
                        attempt_number = 1
                        )
        attempt2 = Attempt.objects.get(
                        card = card2,
                        test_type = test1,
                        attempt_number = 2
                        )
        self.assertEqual(attempt1.has_image(), True)
        self.assertEqual(attempt2.has_image(), False)

    def test_get_css_class(self):
        setup()
        card1 = QieCard.objects.get(barcode="9900001")
        card2 = QieCard.objects.get(barcode="9900002")
        test1 = Test.objects.all()[0]
        test2 = Test.objects.all()[1]
        attempt1 = Attempt.objects.get(
                        card = card1,
                        test_type = test1,
                        attempt_number = 1
                        )
        attempt2 = Attempt.objects.get(
                        card = card1,
                        test_type = test1,
                        attempt_number = 2
                        )
        attempt3 = Attempt.objects.get(
                        card = card2,
                        test_type = test2,
                        attempt_number = 1
                        )
        attempt4 = Attempt.objects.get(
                        card = card2,
                        test_type = test2,
                        attempt_number = 2
                        )
        self.assertEqual(attempt1.get_css_class(), "success")
        self.assertEqual(attempt2.get_css_class(), "danger")
        self.assertEqual(attempt3.get_css_class(), "warning")
        self.assertEqual(attempt4.get_css_class(), "warning")
