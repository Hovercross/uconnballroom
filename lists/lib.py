from django.db import transaction
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save

import lists.models
import registration.models

import logging
logger = logging.getLogger(__name__)

class ListParseException(Exception):
    def __init__(self, s):
        self.s = s
        
    def __str__(self):
        return "List parse exception: %s" % self.s


def updateListsFor(r):
    addLists = set()
    removeLists = set()
    
    paidList = autoList('%s Paid' % r.registration_session.card_code, 'paid_list')
    unpaidList = autoList('%s Unpaid' % r.registration_session.card_code, 'paid_list')
    teamList = autoList('%s Team' % r.registration_session.card_code, 'registration_type_list')
    clubList = autoList('%s Club' % r.registration_session.card_code, 'registration_type_list')
    
    if r.paid:
        addLists.add(paidList)
        removeLists.add(unpaidList)
    else:
        addLists.add(unpaidList)
        removeLists.add(paidList)
        
    if r.team:
        addLists.add(teamList)
        removeLists.add(clubList)
    else:
        addLists.add(clubList)
        removeLists.add(teamList)
    
    #Get the appropriate lists for the person type of the user
    for apt in registration.models.PersonTypeAutoList.objects.filter(person_type=r.person_type):
        listName = "%s %s" % (r.registration_session.card_code, apt.list_name)
        addLists.add(autoList(listName, 'person_type_list'))
    
    #Get all the other lists for all the other person types for that registration session, subtracting the lists that the user will now be getting
    #The case of the person's new list will be handled by the fact that they're already in addLists
    for l in (set(lists.models.List.objects.filter(list_type='person_type_list').filter(name__startswith=r.registration_session.card_code)) - addLists):
        removeLists.add(l)
            
    for l in removeLists:
        if r.person in l.people.all():
            logger.info("Removing person %d from list %s" % (r.person.id, l))
            l.people.remove(r.person)
            l.save()
            
    for l in addLists:
        if r.person not in l.people.all():
            logger.info("Adding person %d from list %s" % (r.person.id, l))
            l.people.add(r.person)
            l.save()

def parseQueryList(s, sep):
    items = [item.strip() for item in s.split(sep)]
    
    opers = {
        'x': set.intersection,
        'X': set.intersection,
        '&': set.intersection,
        '+': set.union,
        '|': set.union,
        '-': set.difference,
        '^': set.symmetric_difference,}
    
    stack = []
    
    for lineNum, item in enumerate(items):
        if not item:
            continue
            
        if item in opers:
            try:
                op2 = stack.pop()
                op1 = stack.pop()
            except IndexError:
                raise ListParseException("Operand on an empty stack, too many operators")
            result = opers[item](op1, op2)
            stack.append(result)
        else:
            try:
                listObj = lists.models.List.objects.get(slug=item)
            except lists.models.List.DoesNotExist:
                raise ListParseException("List matching %s not found" % item)
            stack.append(set(listObj.people.all()))
            
    if len(stack) > 1:
        raise ListParseException("There were leftover lists on the stack")
    
    if len(stack) == 0:
        raise ListParseException("There were no results left on the stack")
        
    return stack[0]
    
def autoList(name, type_code):
    slug = slugify(name)

    try:
        return lists.models.List.objects.get(slug=slug)
    except lists.models.List.DoesNotExist:
        l = lists.models.List(name=name, slug=slug, list_type=type_code)
        l.save()

        return l

def updateListsEvent(sender, instance, **kwargs):
    updateListsFor(instance)

#Automatically update a registration's lists on it's save
post_save.connect(updateListsEvent, sender=registration.models.Registration)