from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import os
from django.db import models
from django.utils import timezone

# This file describes the models off of which the database tables
# will be based


LOCATION_LENGTH = 100            # Constant for maximum location size
MAX_COMMENT_LENGTH = 1000        # Constant for max comment length



def validate_card_id(value):
    """ This determines whether an input card ID is valid """
    
    # ID must be a string of digits
    if not value.isdigit():
        raise ValidationError('ID must only contain numbers')

    # ID must be 7 digits long
    if len(value) != 7:
        raise ValidationError('ID must be 7 digits long')

    curId = value[(len(value) - 3):]
    sameId = QieCard.objects.filter(barcode__iendswith=curId).exclude(barcode__exact=value)
    
    # Last 3 digits of ID must be unique
    if sameId:
        raise ValidationError(
            ('Card "%(value)s" is already recorded'),
            params={'value':curId},
        )
        

def validate_uid(uid):
    """ This determines whether a card UID is valid """
    
    parsed = uid.split(":")
    
    #UID must have 6 sections
    if not len(parsed) == 6:
        raise ValidationError("UID must have six ':'-separated sections")
        
    for part in parsed:
    
        # All UID sections must have 2 characters
        if not len(part) == 2:
            raise ValidationError("Each section must contain two characters")
        for letter in part:
            
            # All characters in the UID must be valid hexadecimal digits
            if not letter.isdigit() and not (letter.lower() >= 'a' and letter.lower() <= 'f'):
                raise ValidationError("UID may only contain hexadecimal digits")


class Test(models.Model):
    """ This model stores information about each type of test """
    
    name = models.CharField(max_length=100, default="")
    abbreviation = models.CharField(max_length=100, default="", unique=True)
    description = models.TextField(max_length=1500, default="")
    required = models.BooleanField(default=True)

    def cards_failed(self):
        """ Returns a list of cards which failed on this test """
        relatedAttempts = Attempt.objects.filter(test_type=self.pk, revoked=False)
        allCards = QieCard.objects.all()
        failed = []

        for card in allCards:
            if relatedAttempts.filter(card=card.pk, num_failed__gt=0):
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
        return round(percentage, 1)

    def cards_passed_all(self):
        """ Returns a list of which cards passed all tests """
        cards = QieCard.objects.all()
        passed = []

        for card in cards:
            if not card.get_failed() and not card.get_remaining():
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
        return round(percentage, 1)   

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
    
    barcode = models.CharField(max_length=7, validators=[validate_card_id], unique=True, default="")
    uid = models.CharField(max_length=17, validators=[validate_uid], unique=True, default="")
    plane_loc = models.CharField(max_length=LOCATION_LENGTH, default="")
    major_ver = models.CharField(max_length=4, default="")
    min_ver = models.CharField(max_length=4, default="")
    comments = models.TextField(max_length=MAX_COMMENT_LENGTH, blank=True, default="")

    def get_bar_uid(self):
        """ Returns the unique 3-digit code of this card's ID """
        return self.barcode[(len(self.barcode) - 3):]

    def get_passed(self):
        """ Returns the tests which this card passed """
        executedTests = Attempt.objects.filter(card=self.pk, revoked=False)
        allTests = Test.objects.all()
        passed = []

        for test in allTests:
            if not executedTests.filter(test_type=test.pk, num_failed__gt=0) and executedTests.filter(test_type=test.pk):
                passed.append(test)
        
        return passed

    def get_failed(self):
        """ Returns the tests which this card failed """
        executedTests = Attempt.objects.filter(card=self.pk, revoked=False)
        allTests = Test.objects.all()
        testStates = []

        for test in allTests:
            if executedTests.filter(test_type=test.pk, num_failed__gt=0):
                testStates.append(test)
        
        return testStates

    def get_remaining(self):
        """ Returns the tests on which this card has no conclusive results """
        executedTests = Attempt.objects.filter(card=self.pk, revoked=False)
        allTests = Test.objects.all()
        testStates = []

        for test in allTests:
            if not executedTests.filter(test_type=test.pk):
                testStates.append(test)
        
        return testStates

    def __str__(self):
       return str(self.barcode)


        
def images_location(upload, original_filename):
    cardName = str(QieCard.objects.get(pk=upload.barcode).barcode) + "/"
    testAbbrev = str(Test.objects.get(pk=upload.test_type_id).abbreviation) + "/"
    attemptNum = str(upload.attempt_number) + "/"
    
    return os.path.join("images/", cardName, testAbbrev, attemptNum, original_filename)
    
def logs_location(upload, original_filename):
    cardName = str(QieCard.objects.get(pk=upload.barcode).barcode) + "/"
    testAbbrev = str(Test.objects.get(pk=upload.test_type_id).abbreviation) + "/"
    attemptNum = str(upload.attempt_number) + "/"
    
    return os.path.join("uploads/", "user_uploaded_logs/", cardName, testAbbrev, attemptNum, original_filename)
        
class Attempt(models.Model):
    """ This model stores information about each testing attempt """

    card = models.ForeignKey(QieCard, on_delete=models.CASCADE)     # The card this attempt was on
    test_type = models.ForeignKey(Test, on_delete=models.PROTECT)   # The test this attempt was of
    attempt_number = models.IntegerField(default=1)
    tester = models.ForeignKey(Tester, on_delete=models.PROTECT)    # the person who enterd this attempt
    date_tested = models.DateTimeField('date tested')
    num_passed = models.IntegerField(default=-1)
    num_failed = models.IntegerField(default=-1)
    revoked = models.BooleanField(default=False)
    temperature = models.FloatField(default=-999.9)
    humidity = models.FloatField(default=-999.9)
    comments = models.TextField(max_length=MAX_COMMENT_LENGTH, blank=True, default="")
    image = models.ImageField(upload_to=images_location, default="default.png")
    log_file = models.FileField(upload_to=logs_location, default='default.png')
    log_comments = models.TextField(max_length=MAX_COMMENT_LENGTH, blank=True, default="")
    
    def passed_all(self):
        return (self.num_failed == 0)

    def has_image(self):
        """ This returns whether the attempt has a specified image """
        return (not self.image == "default.png")

    def get_css_class(self):
        """ This returns the color which the Attempt template should take """
        if self.revoked:
            return "warning"
        elif self.num_failed == 0:
            return "success"
        else:
            return "danger"
            

    def __str__(self):
        return str(self.test_type)
        

class Location(models.Model):
    """ This model stores information about a particular location where a card has been """
    
    card = models.ForeignKey(QieCard, on_delete=models.CASCADE)
    date_received = models.DateTimeField('date received', default=timezone.now)
    geo_loc = models.CharField('Location',max_length=200, default="")

# An appendage to the save function
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

@receiver(pre_save)
def pre_save_handler(sender, instance, *args, **kwargs):
    instance.full_clean()

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
