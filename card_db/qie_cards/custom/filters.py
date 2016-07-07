from ..models import QieCard, Tester, Test, Attempt, Location


def getPassedDates(cards, tests, attempts):
    cardStates = getCardTestStatesDates(cards, tests, attempts)
    
    passedCards = []
    
    for card in cardStates:
        if len(card["failed"]) == 0 and len(card["remaining"]) == 0:
            passedCards.append(card["passed"][0][1])
        else:
            print "Failed:"
            print card["failed"]
            print "Remaining:"
            print card["remaining"]
    
    return passedCards

def getFailedDates(cards, tests, attempts):
    cardsToInd = {}
    
    for i in xrange(len(cards)):
        cardsToInd[cards[i].pk] = i
    
    cardFailed = [(False, 0)] * len(cards)
    for attempt in attempts:
        if not attempt.revoked:
            cardInd = cardsToInd[attempt.card_id]
            if not attempt.num_failed == 0:
                if cardFailed[cardInd][1] == 0:
                    cardFailed[cardInd] = (True, attempt.date_tested)
                elif cardFailed[cardInd][1] < attempt.date_tested:
                    cardFailed[cardInd] = (True, attempt.date_tested)
                
                
    failedCards = []
    for i in xrange(len(cards)):
        if cardFailed[i][0]:
            failedCards.append(cardFailed[i][1])
    
    return failedCards

def getPassedCards(cards, tests, attempts):
    cardStates = getCardTestStates(cards, tests, attempts)
    
    passedCards = []
    
    for card in cardStates:
        if card["failed"] == 0 and card["remaining"] == 0:
            passedCards.append(card.barcode)
            
    return passedCards


def getFailedCards(cards, tests, attempts):
    cardsToInd = {}
    
    for i in xrange(len(cards)):
        cardsToInd[cards[i].pk] = i
    
    cardFailed = [False] * len(cards)
    for attempt in attempts:
        if not attempt.revoked:
            if not attempt.num_failed == 0:
                cardFailed[cardsToInd[attempt.card_id]] = True
        
    failedCards = []
    for i in xrange(len(cards)):
        if cardFailed[i]:
            failedCards.append(cards[i].barcode)
    
    return failedCards

def getCardTestStatesDates(cards, tests, attempts):
    """ This function returns an array of cards and tests based on passes or fails """
    numTests = len(tests)
    testsToInd = {}

    for i in xrange(numTests):
        testsToInd[tests[i].pk] = i

    state = {}

    for card in cards:
        state[card.pk] = [(0, 0)] * numTests
    
    for attempt in attempts:
        if not attempt.revoked:
            testInd = testsToInd[attempt.test_type_id];
            if not attempt.num_failed == 0:
                if state[attempt.card_id][testInd][1] == 0:
                    state[attempt.card_id][testInd] = (2, attempt.date_tested)
                elif state[attempt.card_id][testInd][1] < attempt.date_tested:
                    state[attempt.card_id][testInd] = (2, attempt.date_tested)
            elif not attempt.num_passed == 0 and state[attempt.card_id][testInd][0] == 0:
                if state[attempt.card_id][testInd][1] == 0:
                    state[attempt.card_id][testInd] = (1, attempt.date_tested)
                elif state[attempt.card_id][testInd][1] < attempt.date_tested:
                    state[attempt.card_id][testInd] = (1, attempt.date_tested)

    cardStat = []

    for i in xrange(len(cards)):
        card = cards[i]
        curFail = []
        curPass = []
        curRem = []
        tempDict = {}
        curState = state[card.pk]

        for i in xrange(numTests):
            if curState[i][0] == 0:
                curRem.append((tests[i].name, curState[i][1]))
            elif curState[i][0] == 1:
                curPass.append((tests[i].name, curState[i][1]))
            elif curState[i][0] == 2:
                curFail.append((tests[i].name, curState[i][1]))
        
        tempDict['barcode'] = card.barcode
        tempDict['failed'] = curFail
        tempDict['passed'] = curPass
        tempDict['remaining'] = curRem
        cardStat.append(tempDict)
    return cardStat

def getCardTestStates(cards, tests, attempts):
    """ This function returns an array of cards and tests based on passes or fails """
    numTests = len(tests)
    testsToInd = {}

    for i in xrange(numTests):
        testsToInd[tests[i].pk] = i

    state = {}

    for card in cards:
        state[card.pk] = [0] * numTests
    
    for attempt in attempts:
        if not attempt.revoked:
            testInd = testsToInd[attempt.test_type_id];
            if not attempt.num_failed == 0:
                state[attempt.card_id][testInd] = 2
            elif not attempt.num_passed == 0 and state[attempt.card_id][testInd] == 0:
                state[attempt.card_id][testInd] = 1

    cardStat = []

    for i in xrange(len(cards)):
        card = cards[i]
        curFail = []
        curPass = []
        curRem = []
        tempDict = {}
        curState = state[card.pk]

        for i in xrange(numTests):
            if curState[i] == 0:
                curRem.append(tests[i].name)
            elif curState[i] == 1:
                curPass.append(tests[i].name)
            elif curState[i] == 2:
                curFail.append(tests[i].name)
        
        tempDict['barcode'] = card.barcode
        tempDict['failed'] = curFail
        tempDict['passed'] = curPass
        tempDict['remaining'] = curRem
        cardStat.append(tempDict)
    return cardStat

def getFailedCardStats(cards, tests, attempts):
    """ Returns a list of failed cards for each test """
    numCards = len(cards)
    cardsToInd = {}

    for i in xrange(numCards):
        cardsToInd[cards[i].pk] = i

    failed = {}

    for test in tests:
        failed[test.pk] = [False] * numCards
    
    for attempt in attempts:
        if not attempt.revoked:
            cardInd = cardsToInd[attempt.card_id]
            if not attempt.num_failed == 0:
                failed[attempt.test_type_id][cardInd] = True

    testStat = []

    for i in xrange(len(tests)):
        tempStat = {"name": tests[i].name}
        failCards = []
        for j in xrange(len(cards)):
            if failed[tests[i].pk][j]:
                failCards.append(cards[j].barcode)
        tempStat["cards"] = failCards
        tempStat["number"] = len(failCards)
        tempStat["percentage"] = round( float(len(failCards))/len(cards) * 100, 1)
        testStat.append(tempStat)
    
    return sorted(testStat, key=lambda k: k['percentage'], reverse=True)
    
def getPassedCardStats(cards, tests, attempts):
    """ Returns a list of cards which passed all tests """
    
    cardStates = getCardTestStates(cards, tests, attempts)
    
    cardStats = {}
    
    cardStats["cards"] = getPassedCards(cards, tests, attempts)
    cardStats["number"] = len(cardStats["cards"])
    cardStats["percentage"] = round( float(len(cardStats["cards"]))/len(cards) * 100, 1)
            
    return cardStats
