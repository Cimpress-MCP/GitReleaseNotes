import unittest
from JustReleaseNotes.writers import HtmlWriter
from string import Template
from mock import MagicMock
from mock import Mock


class HtmlWriter_Test(unittest.TestCase):
    def test_returnsHtmlExtension(self):
        writer = HtmlWriter.HtmlWriter(None,None)
        self.assertEqual(".html", writer.getExtension())

    def ticket_side_effect(*args, **kwargs):
        if args[1] == "ABCD-1":
            return {"title": "ABCD1 ticket", "ticket": "ABCD-1", "html_url": "http://some.url"}
        elif args[1] == "ABCD-2":
            return {"title": "ABCD2 ticket", "ticket": "ABCD-2", "html_url": "http://some.url"}
        return None

    def ticket_side_effect_with_embedded_link(*args, **kwargs):
        if args[1] == "ABCD-1":
            return dict(title="ABCD1 ticket that references ABCD-2", ticket="ABCD-1", html_url="http://some.url",
                        embedded_link={"ABCD-2": "http://some.url/ABCD-2"})
        elif args[1] == "ABCD-2":
            return dict(title="ABCD2 ticket that references ABCD-1", ticket="ABCD-2", html_url="http://some.url",
                        embedded_link={"ABCD-1": "http://some.url/ABCD-1"})
        return None

    def test_givenFairlyCompleteTicketHtmlBlockIsGenerated(self):
        self.maxDiff = None
        mockedTicketProvider = Mock()
        mockedTicketProvider.getTicketInfo.side_effect = self.ticket_side_effect

        writer = HtmlWriter.HtmlWriter(mockedTicketProvider, None)
        deps = {"ANY": "SomeComponent1: 2.3.*; SomeComponent2: 1.0.0"}
        version = "1.0.2.0"
        date = "01-02-2015"
        tickets = ["ABCD-1", "ABCD-2"]
        output = writer.printVersionBlock(deps, version, date, tickets)
        self.assertEqual('<div style="width:100%; border: 0px">\n'
                         '<a name="1.0.2.0"></a>\n'
                         '<h2>1.0.2.0\n<sup><small style="font-size:10px"><i> 01-02-2015</i></small></sup>\n'
                         '</h2>\n'
                         '<div style="background: #eee; "><i>Components: \n'
                         'SomeComponent1: 2.3.*; SomeComponent2: 1.0.0\n'
                         '</i></div>\n'
                         '<ul>\n'
                         '<li style="font-size:14px"><a href="http://some.url">ABCD-2</a> ABCD2 ticket</li>\n'
                         '<li style="font-size:14px"><a href="http://some.url">ABCD-1</a> ABCD1 ticket</li>\n</ul>\n</div>\n',
                         output)

    def test_embeddedLinkProvided_ReplacesContentWithLink(self):
        mockedTicketProvider = Mock()
        mockedTicketProvider.getTicketInfo = self.ticket_side_effect_with_embedded_link

        writer = HtmlWriter.HtmlWriter(mockedTicketProvider, None)
        deps = {"ANY": "SomeComponent1: 2.3.*; SomeComponent2: 1.0.0"}
        version = "1.0.2.0"
        date = "01-02-2015"
        tickets = ["ABCD-1", "ABCD-2"]
        output = writer.printVersionBlock(deps, version, date, tickets)
        self.assertEqual('<div style="width:100%; border: 0px">\n'
                         '<a name="1.0.2.0"></a>\n'
                         '<h2>1.0.2.0\n<sup><small style="font-size:10px"><i> 01-02-2015</i></small></sup>\n'
                         '</h2>\n'
                         '<div style="background: #eee; "><i>Components: \n'
                         'SomeComponent1: 2.3.*; SomeComponent2: 1.0.0\n'
                         '</i></div>\n'
                         '<ul>\n'
                         '<li style="font-size:14px"><a href="http://some.url">ABCD-2</a> ABCD2 ticket that references <a href="http://some.url/ABCD-1">ABCD-1</a></li>\n'
                         '<li style="font-size:14px"><a href="http://some.url">ABCD-1</a> ABCD1 ticket that references <a href="http://some.url/ABCD-2">ABCD-2</a></li>\n</ul>\n</div>\n',
                         output)

    def test_decorateContent_withDefaultTemplate_ReturnsContentOnly(self):
        mockedTicketProvider = Mock()
        mockedTicketProvider.getTicketInfo = self.ticket_side_effect_with_embedded_link

        writer = HtmlWriter.HtmlWriter(mockedTicketProvider, None)
        output = writer.decorateContent("abc")

        self.assertEqual("abc", output)

    def test_decorateContent_withProvidedTemplate_ReplacesContentCorrectly(self):
        mockedTicketProvider = Mock()
        mockedTicketProvider.getTicketInfo = self.ticket_side_effect_with_embedded_link

        writer = HtmlWriter.HtmlWriter(mockedTicketProvider, "begin ${content} end")
        output = writer.decorateContent("abc")

        self.assertEqual("begin abc end", output)



if __name__ == '__main__':
    unittest.main()