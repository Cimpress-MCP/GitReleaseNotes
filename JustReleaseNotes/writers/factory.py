import JustReleaseNotes
from JustReleaseNotes import factory

def create(name, ticketProvider, templateString=None):
    return JustReleaseNotes.factory.createWithConfigAndParam("JustReleaseNotes.writers", name, ticketProvider, templateString)
