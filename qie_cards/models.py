from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from django.db import models
from django.utils import timezone

# This file describes the models off of which the database tables
# will be based


LOCATION_LENGTH = 100            # Constant for maximum location size
MAX_COMMENT_LENGTH = 1000        # Constant for max comment length



def validate_id(value):
    """ This determines whether an input card ID is valid """
    
    # ID must be a string of digits
    if not value.isdigit():
        raise ValidationError('ID must only contain numbers')

    # ID must be 7 digits long
    if len(value) != 7:
        raise ValidationError('ID must be 7 digits long')

    curId = value[(len(value) - 3):]
    sameId = QieCard.objects.filter(card_id__iendswith=curId).exclude(card_id__exact=value)
    
    # Last 3 digits of ID must be unique
    if sameId:
        raise ValidationError(
            _('Card "%(value)s" is already recorded'),
            params={'value':curId},
        )


class Test(models.Model):
    """ This model stores information about each type of test """
    
    name = models.CharField(max_length=100, default="")
    abbreviation = models.CharField(max_length=100, default="")
    description = models.TextField(max_length=1500, default="")
    required = models.BooleanField(default=False)    

    def cards_failed(self):
        """ Returns a list of cards which failed on this test """
        relatedAttempts = Attempt.objects.filter(test_type=self.pk, revoked=False)
        allCards = QieCard.objects.all()
        failed = []

        for card in allCards:
            if not relatedAttempts.filter(card=card.pk, passed=True) and relatedAttempts.filter(card=card.pk, passed=False):
                failed.append(card)
        
        return failed

    def num_failed(self):
        """ Returns how many cards failed this test """
        return len(Test.cards_failed(self))

    def perc_failed(self):
        """ Returns what percent of total cards failed this test """
        total = QieCard.objects.all().count()
        if total > 0:
            percentage = (100.0 * Test.num_failed(self)) / total
        else:
            percentage = -1
        return percentage

    def cards_passed_all(self):
        """ Returns a list of which cards passed all tests """
        cards = QieCard.objects.all()
        passed = []

        for card in cards:
            if not card.get_failed():
                passed.append(card)

        return passed
 
    def num_passed(self):
        """ Returns how many cards passed all tests """
        return len(Test.cards_passed_all(self))

    def perc_passed(self):
        """ Returns what percent of total cards passed this test """
        total = QieCard.objects.all().count()
        if total > 0:
            percentage = (100.0 * Test.num_passed(self)) / total
        else:
            percentage = -1
        return percentage   

    def __str__(self):
       return self.name


class Tester(models.Model):
    """ This model stores information about the testers of the cards """

    username = models.CharField(max_length=100, default="", unique=True)
    email = models.EmailField(max_length=255)    

    def __str__(self):
       return self.username


class QieCard(models.Model):
    """ This model stores information about the different QIE cards """
    
    card_id = models.CharField(max_length=7, validators=[validate_id], default="NULL", blank=True)
    uid = models.CharField(max_length=17, unique=True, default="")
    geo_loc = models.CharField(max_length=30, default="")
    plane_loc = models.CharField(max_length=LOCATION_LENGTH, default="")
    comments = models.TextField(max_length=MAX_COMMENT_LENGTH, blank=True, default="")
    temperature = models.FloatField(default=-999.9)
    humidity = models.FloatField(default=-999.9)

    def get_bar_uid(self):
        """ Returns the unique 3-digit code of this card's ID """
        return card_id[(len(card_id) - 3):]

    def get_passed(self):
        """ Returns the tests which this card passed """
        executedTests = Attempt.objects.filter(card=self.pk, revoked=False)
        allTests = Test.objects.all()
        passed = []

        for test in allTests:
            if executedTests.filter(test_type=test.pk, passed=True):
                passed.append(test)
        
        return passed

    def get_failed(self):
        """ Returns the tests which this card failed """
        executedTests = Attempt.objects.filter(card=self.pk, revoked=False)
        allTests = Test.objects.all()
        testStates = []

        for test in allTests:
            if not executedTests.filter(test_type=test.pk, passed=True) and executedTests.filter(test_type=test.pk):
                testStates.append(test)
        
        return testStates

    def get_remaining(self):
        """ Returns the tests on which this card has no conclusive results """
        executedTests = Attempt.objects.filter(card=self.pk, revoked=False)
        allTests = Test.objects.all()
        testStates = []

        for test in allTests:
            if not executedTests.filter(test_type=test.pk, passed=True) and not executedTests.filter(test_type=test.pk):
                testStates.append(test)
        
        return testStates

    def set_temperature(self, t):
        """ Sets temperature to passed value """
        temperature = t

    def set_humidity(self, h):
        """ Sets humidity to passed value """
        humidty = h

    def __str__(self):
       return str(self.card_id)


class Attempt(models.Model):
    """ This model stores information about each testing attempt """

    card = models.ForeignKey(QieCard, on_delete=models.CASCADE)     # The card this attempt was on
    test_type = models.ForeignKey(Test, on_delete=models.PROTECT)   # The test this attempt was of
    attempt_number = models.IntegerField(default=1)
    tester = models.ForeignKey(Tester, on_delete=models.PROTECT)    # the person who enterd this attempt
    date_tested = models.DateTimeField('date tested')
    passed = models.BooleanField(default=False)
    revoked = models.BooleanField(default=False)
    comments = models.TextField(max_length=MAX_COMMENT_LENGTH, blank=True, default="")
    image = models.ImageField(upload_to="images", default="default.png")
    log_file = models.FileField(upload_to='uploads/%Y-%m-%d/', default='default.png')
    log_comments = models.TextField(max_length=MAX_COMMENT_LENGTH, blank=True, default="")
    
    def has_image(self):
        """ This returns whether the attempt has a specified image """
        return (not self.image == "default.png")

    def get_css_class(self):
        """ This returns the color which the Attempt template should take """
        if self.revoked:
            return "warning"
        elif self.passed:
            return "success"
        else:
            return "danger"

    def __str__(self):
        return str(self.test_type)


# An appendage to the delete function
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

@receiver(pre_delete, sender=Attempt)
def mymodel_delete(sender, instance, **kwargs):
    """ Deletes the stored image """
    if instance.image != "default.png":
        instance.image.delete(False)
    if instance.log_file != "default.png":
        instance.log_file.delete(False)
