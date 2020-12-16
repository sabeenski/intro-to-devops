# Script for testing workflow

import unittest
import sys
import argparse
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

__unittest = True

HEADER  = '\033[95m'
OKBLUE  = '\033[94m'
OKCYAN  = '\033[96m'
OKGREEN = '\u001b[32;1m' #'\033[92m'
WARNING = '\033[93m'
FAILRED = '\033[91m'
ENDC    = '\033[0m'
BOLD    = '\033[1m'

failures         = 0
motivation_link  = None
learning_link    = None

motivation_links = set()
learning_links   = set()

PROJECT_DESCRIPTION_URL = "https://mycourses.aalto.fi/mod/page/view.php?id=655682"

def _pi( message ):
    print( "[i] ", message, sep='' )
def _ph( message ):
    print( BOLD, "[>] ", message, ENDC, sep='' )
def _ps( message ):
    print( OKGREEN, "    ", message, ENDC, sep='' )
def _pf( message ):
    print( FAILRED, "    ", message, ENDC, sep='' )
def _pp( message ):
    print( "\n", BOLD, "[*] ", message, ENDC, sep='' )

class TestProject(unittest.TestCase):
    # Tests compliance with projects against requirements

    def setUp(self):
        # Tests compliance with projects against requirements
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(2)
        BASE_URL = None

    def tearDown(self):
        # Stop web driver
        self.driver.quit()

    def test_case_01(self):
        _ph("Homepage has intended content")
        global failures
        # There is a big enough image
        try:
            at_least_one_big_enough_image = False
            page = self.driver.get(TestProject.BASE_URL)
            images = self.driver.find_elements_by_tag_name('img')
            for image in images:
                max_dimension = max( image.size['width'], image.size['height'], 
                    int( image.get_attribute( 'naturalWidth' ) ),  int( image.get_attribute( 'naturalHeight' ) ) )
                if ( max_dimension >= 250 ):
                    _ps("There is an image with width or hight of at least 250px")
                    at_least_one_big_enough_image = True
                    break
            if at_least_one_big_enough_image == False:
                _pf("None of the {} image(s) found in the homepage has both width and height of at least 250px".format(len(images)))
                failures += 1
        except NoSuchElementException as ex:
            # No images found
            _pf("No images found in homepage")
            failures += 1
        except Exception as exception:
            _pf("Unexpected error: {}".format(exception.args[0]))
            failures += 1
        # Heading found with intended text
        try:
            found_headings = 0
            headings = self.driver.find_elements_by_xpath(u'//*[substring-after(name(), "h") > 0]')
            for heading in headings:
                if "about" in heading.get_attribute('innerHTML').lower():
                    _ps("Case-insensitive text 'About' correctly found in heading")
                    #
                    found_headings += 1
                    #
                    words = 0
                    paragraphs_or_items = 0
                    try:
                        paragraphs = heading.find_elements_by_xpath(u'../..//descendant::p')
                        if len(paragraphs) > 0: paragraphs_or_items += 1
                        for paragraph in paragraphs:
                            words += len( paragraph.get_attribute('innerText').split() )
                    except NoSuchElementException:
                        # There might be also list items
                        pass
                    try:
                        list_items = heading.find_elements_by_xpath(u'../..//descendant::li')
                        if len(list_items) > 0: paragraphs_or_items += 1
                        for item in list_items:
                            paragraphs_within_item = item.find_elements_by_xpath('./p')
                            if not paragraphs_within_item:
                                # Words in paragraphs not already counted
                                words += len( item.get_attribute('innerText').split() )
                    except NoSuchElementException:
                        # There might have been paragraphs
                        pass
                    if paragraphs_or_items == 0:
                        _pf("Could not find any paragraphs nor list items in homepage, there should be either")
                    elif ( words < 100 ):
                        _pf("The text does not contain enough words in paragraphs or list items: {} instead of at least 100".format(words))
                    else:
                        _ps("The text contains {} words according to the project description".format(words))
                        return
            failures += 1
            if found_headings == 0:
                _pf("Heading with case-insensitive text 'About' not found")
        except NoSuchElementException as ex:
            _pf("Case-insensitive text 'About' not found in heading")
            failures += 1
        except Exception as exception:
            _pf("Unexpected error: {}".format(exception.args[0]))
            failures += 1


    def test_case_05(self):
        _ph("Homepage contains links to relevant blog posts")
        global failures, motivation_links, learning_links
        # Blog post on motivation
        try:
            page = self.driver.get(self.BASE_URL)
            links = self.driver.find_elements_by_xpath(u'//a[contains(translate(text(),"CSEJ","csej"),"cs-ej4104")]')
            if len(links) == 0: raise NoSuchElementException
            for link in links:
                motivation_links.add( link.get_attribute('href') )
                _ps("Link with case-insensitive text 'CS-EJ4104' correctly found")
        except NoSuchElementException:
            _pf("Link with case-insensitive text 'CS-EJ4104' not found")
            failures += 1
        except Exception as exception:
            _pf("Unexpected error: {}".format(exception.args[0]))
            failures += 1
        # Blog post on learning
        try:
            link_found = False
            links = self.driver.find_elements_by_xpath(u'//a[contains(translate(text(),"DO","do"),"devops")]')
            for link in links:
                if "learning devops" in link.get_attribute('innerText').lower() or \
                    "learned devops" in link.get_attribute('innerText').lower():
                    learning_links.add( link.get_attribute('href') )
                    link_found=True
                    _ps("Link with case-insensitive text 'learning (learned) DevOps' correctly found")
        except NoSuchElementException as ex:
            _pf("Link with case-insensitive text 'learning (learned) DevOps' not found")
            failures += 1
        except Exception as exception:
            _pf("Unexpected error: {}".format(exception.args[0]))
            failures += 1
        if not link_found:
            _pf("Link with case-insensitive text 'learning (learned) DevOps' not found")
            failures += 1

    def test_case_10(self):
        _ph("Blog post on this course has intended content")
        global failures, motivation_links
        if not motivation_links:
            _pf("Blog post not found")
            failures +=1
            return
        # Heading has intended text
        if len(motivation_links)>1:
            _pi("Multiple links found ({}), checking them one by one".format( len(motivation_links) ))
        link_failures = 0
        for number, link in enumerate( motivation_links ):
            _pi("Link #{}: {}".format( number+1, link ) )
            try:
                found_headings = 0
                page = self.driver.get(link)
                headings = self.driver.find_elements_by_xpath(u'//*[substring-after(name(), "h") > 0]')
                for heading in headings:
                    if "cs-ej4104" in heading.get_attribute('innerText').lower():
                        _ps("Case-insensitive text 'CS-EJ4104' correctly found in heading")
                        #
                        found_headings += 1
                        #
                        words = 0
                        paragraphs_or_items = 0
                        try:
                            paragraphs = heading.find_elements_by_xpath(u'../../..//descendant::p')
                            if len(paragraphs) > 0: paragraphs_or_items += 1
                            for paragraph in paragraphs:
                                words += len( paragraph.get_attribute('innerText').split() )
                        except NoSuchElementException:
                            # There might be also list items
                            pass
                        try:
                            list_items = heading.find_elements_by_xpath(u'../../..//descendant::li')
                            if len(list_items) > 0: paragraphs_or_items += 1
                            for item in list_items:
                                paragraphs_within_item = item.find_elements_by_xpath('./p')
                                if not paragraphs_within_item:
                                    # Words in paragraphs not already counted
                                    words += len( item.get_attribute('innerText').split() )
                        except NoSuchElementException:
                            # There might have been paragraphs
                            pass
                        if paragraphs_or_items == 0:
                            _pf("Could not find any paragraphs nor list items in blog post, there should be either")
                        elif ( words < 250 ):
                            _pf("The text does not contain enough words in paragraphs or list items: {} instead of at least 250".format(words))
                        elif ( words > 500 ):
                            _pf("The text does has too many words in paragraphs or list items: {} instead of at most 500".format(words))
                        else:
                            _ps("The text contains {} words according to the project description".format(words))
                            return
                if found_headings == 0:
                    _pf("Link with case-insensitive text 'CS-EJ4104' not found")
                link_failures += 1
            except NoSuchElementException as ex:
                _pf("No headings found")
                link_failures += 1
            except Exception as exception:
                _pf("Unexpected error: {}".format(exception.args[0]))
                failures += 1
                return
            failures += (link_failures == len(motivation_links) )

    def test_case_20(self):
        _ph("Blog post on learning has intended content")
        global failures, learning_links
        if not learning_links:
            _pf("Blog post not found")
            failures +=1
            return
        # Heading has intended text
        if len(learning_links)>1:
            _pi("Multiple links found ({}), checking them one by one".format( len(learning_links) ))
        link_failures = 0
        for number, link in enumerate( learning_links ):
            _pi("Link #{}: {}".format( number+1, link ) )
            try:
                found_headings = 0
                page = self.driver.get(link)
                headings = self.driver.find_elements_by_xpath(u'//*[substring-after(name(), "h") > 0]')
                for heading in headings:
                    if "learning devops" in heading.get_attribute('innerText').lower() or \
                        "learned devops" in heading.get_attribute('innerText').lower():
                        _ps("Case-insensitive text 'learning (learned) DevOps' correctly found in heading")
                        #
                        found_headings += 1
                        #
                        words = 0
                        paragraphs_or_items = 0
                        try:
                            paragraphs = heading.find_elements_by_xpath(u'../../..//descendant::p')
                            if len(paragraphs) > 0: paragraphs_or_items += 1
                            for paragraph in paragraphs:
                                words += len( paragraph.get_attribute('innerText').split() )
                        except NoSuchElementException:
                            # There might be also list items
                            pass
                        try:
                            list_items = heading.find_elements_by_xpath(u'../../..//descendant::li')
                            if len(list_items) > 0: paragraphs_or_items += 1
                            for item in list_items:
                                paragraphs_within_item = item.find_elements_by_xpath('./p')
                                if not paragraphs_within_item:
                                    # Words in paragraphs not already counted
                                    words += len( item.get_attribute('innerText').split() )
                        except NoSuchElementException:
                            # There might have been paragraphs
                            pass
                        if paragraphs_or_items == 0:
                            _pf("Could not find any paragraphs nor list items in blog post, there should be either")
                        elif ( words < 250 ):
                            _pf("The text does not contain enough words in paragraphs or list items: {} instead of at least 250".format(words))
                        elif ( words > 500 ):
                            _pf("The text does has too many words in paragraphs or list items: {} instead of at most 500".format(words))
                        else:
                            _ps("The text contains {} words according to the project description".format(words))
                            return
                if found_headings == 0:
                    _pf("Link with case-insensitive text 'learning DevOps' not found")
                link_failures += 1
            except NoSuchElementException:
                _pf("No headings found")
                link_failures += 1
            except Exception as exception:
                _pf("Unexpected error: {}".format(exception.args[0]))
                failures += 1
                return
            failures += (link_failures == len(learning_links) )


if __name__ == '__main__':
    if str(sys.argv[1]) == "-r":
        (group, project) = ( str(sys.argv[2]).split('/')[0], str(sys.argv[2]).split('/')[1])
        repository_url = "http://{}.github.io/{}/".format(group, project)
    else:
        repository_url = str(sys.argv[1])
    _pi("Test URL: {}".format(repository_url))
    TestProject.BASE_URL =  repository_url
    suite = unittest.TestLoader().loadTestsFromTestCase(TestProject)
    test_result = unittest.TextTestRunner(verbosity=0).run(suite)
    #ret = not test_result.wasSuccessful()
    _pp("SUMMARY")
    if ( failures>0 ):
        _pf( "Tests completed with {} failure(s), check the feedback above and the project requirements at {}".format( failures, PROJECT_DESCRIPTION_URL ) )
    else:
        _ps( "All tests completed successfully" )
    #print(dir(TestProject))
    sys.exit(failures)
