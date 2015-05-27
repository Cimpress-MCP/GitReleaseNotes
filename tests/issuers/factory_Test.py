import unittest
import requests_mock
import JustReleaseNotes.issuers
from JustReleaseNotes.issuers import factory

class factory_Test(unittest.TestCase):

    def test_factoryRetrievesGithubIssues(self):
        with requests_mock.mock() as m:
            m.get('https://some.url', text="{}")
            self.assertIsNotNone(JustReleaseNotes.issuers.factory.create(
                {
                "Provider" : "GitHubIssues",
                "HtmlUrl" : "https://jiratrain101.vistaprint.net/jira/browse",
                "Authorization" : "Basic dmNzbTpzdGFzaDN4dDNuZA==",
                "Url" : "https://some.url"
                }))

    def test_factoryRetrievesJiraIssues(self):
        self.assertIsNotNone(JustReleaseNotes.issuers.factory.create(
            {
             "Provider" : "JiraIssues",
             "HtmlUrl" : "https://jiratrain101.vistaprint.net/jira/browse",
             "Authorization" : "Basic dmNzbTpzdGFzaDN4dDNuZA==",
             "Url" : "https://some.url",
            }))

    def test_failsIfIssuerUnknown(self):
        with self.assertRaises(Exception):
            JustReleaseNotes.issuers.factory.create({ "Provider": "abrakadabra" })