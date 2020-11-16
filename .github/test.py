"""
A simple selenium test example written by python
"""

import unittest
import sys
import argparse
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
link_1=""
link_2=""

class TestTemplate(unittest.TestCase):
    """Include test cases on a given url"""

    def setUp(self):
        """Start web driver"""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.driver.get(url)

    def tearDown(self):
        """Stop web driver"""
        self.driver.quit()

    
    def test_case_1(self):
        print("TESTCASE 1 : TEST IF 'about' HEADER ELEMENT EXISTS")
        try:
            about=[]        
            elem_about_h1 = self.driver.find_elements_by_css_selector('h1')
            for heading in elem_about_h1:
                about.append(heading.text.lower())
            flg=0
            for elem in about:
                if 'about' in elem:
                    flg=1 
            if flg==0:
                self.fail("No heading found with 'about' text in h1 element")
        except NoSuchElementException as ex:
            self.fail(ex.msg)
            sys.exit("No heading found with 'about' text in h1 element")

    def test_case_2(self):
        print ("TESTCASE 2 : FIND IF MULTIPLE PARAGRAPHS EXISTS WITH 100 WORDS AT LEAST")
        try:
            elem_paras = self.driver.find_elements_by_css_selector('p')
            word_count = 0
            para_list = []
            for paragraph in elem_paras:
                para_list = para_list + paragraph.text.split(" ")
            word_count = len(para_list)
            if word_count < 100:
               self.fail("Minimum 100 words expected in the form of one or multiple paragraphs on the main page") 
        except NoSuchElementException as ex:
            self.fail(ex.msg)
            sys.exit("Minimum 100 words expected in the form of one or multiple paragraphs on the main page")


    def test_case_3(self):
        print("TESTCASE 3 : TEST IF 'img' ELEMENT EXISTS")
        try:
            elem_img = self.driver.find_element_by_tag_name('img')
        except NoSuchElementException as ex:
            self.fail(ex.msg)
            sys.exit("Could not find an image")
    

    
    def test_case_4(self):
        print ("TESTCASE 4: FIND LINK TO BLOG POSTS 'CS-EJ4104' AND VERIFY THE BLOG HEADER")
        try:
            global link_1
            elems = self.driver.find_elements_by_css_selector('a')
            blogs= [elem.text for elem in elems]
            links= [elem.get_attribute('href') for elem in elems]
            flg = 0 
            for i,blog in enumerate(blogs):
                if "CS-EJ4104" in blog.lower():
                    flg=1
                    link_1= elems[i].get_attribute('href')
                    #print(link_1)
                    self.driver.get(link_1)
                    hdrs=[]
                    header = self.driver.find_elements_by_css_selector('h1')
                    for heading in header:
                        hdrs.append(heading.text.lower())
                    flag=0
                    for hdr in hdrs:
                        if "CS-EJ4104" in hdr:
                            flag=1 
                    if flag==0:
                            self.fail("No header element has 'CS-EJ4104' text")
            if flg==0:
                self.fail("Blog 1 link not found")
        except NoSuchElementException as ex:
            self.fail(ex.msg)
            sys.exit("Blog 1 link not found or no header element in blog 1 has 'EJ4104' text")
  
    def test_case_5(self):
        print ("TESTCASE 5: FIND LINK TO BLOG POST 'learned or learning DevOps' AND VERIFY THE BLOG HEADER")
        try:
            global link_2
            elems = self.driver.find_elements_by_css_selector('a')
            blogs= [elem.text for elem in elems]
            links= [elem.get_attribute('href') for elem in elems]
            flg = 0 
            for i,blog in enumerate(blogs):
                if "DevOps" in blog.lower():
                    flg=1
                    link_2= elems[i].get_attribute('href')
                    #print(link_2)
                    self.driver.get(link_2)
                    hdrs=[]
                    header = self.driver.find_elements_by_css_selector('h1')
                    for heading in header:
                        hdrs.append(heading.text.lower())
                    flag=0
                    for hdr in hdrs:
                        if "DevOps" in hdr:
                            flag=1 
                    if flag==0:
                            self.fail("No header element has 'DevOps' text")
            if flg==0:
                self.fail("Blog 2 link not found")
        except NoSuchElementException as ex:
            self.fail(ex.msg)
            sys.exit("Blog 2 link not found or no header element in blog 1 has 'DevOps' text")
    def test_case_6(self):
        print("TESTCASE 6: BLOG ONE CONTAINS PARAGRAPHS OR UNORDERED LIST , WORD LIMIT : 250-500")
        try:
            global link_1
            self.driver.get(link_1)
            word_count = 0
            elem_paras = self.driver.find_elements_by_css_selector('p')
            para_list=[]
            for paragraph in elem_paras:
                para_list = para_list + paragraph.text.split(" ")
            word_count = len(para_list)
            word_count_list= 0
            elem_list= self.driver.find_elements_by_tag_name("li")
            unordered_list=[]
            for li in elem_list:
                unordered_list = unordered_list + li.text.split(" ")
            word_count_list = len(unordered_list)
           
            total_words = word_count + word_count_list
            
            if total_words < 250 or total_words > 500:
                    self.fail("Total words : "+str(total_words)+", blog 1 should have 250 to 500 words in paragraph or unordered list format.")
        except NoSuchElementException as ex:
            self.fail(ex.msg)
            sys.exit("Total words : "+str(total_words)+", blog 1 should have 250 to 500 words in paragraph or unordered list format.")
        

    def test_case_7(self):
        print("TESTCASE 7: BLOG TWO CONTAINS PARAGRAPHS OR UNORDERED LIST , WORD LIMIT : 250-500")
        try:
            global link_2
            self.driver.get(link_2)
            word_count = 0
            elem_paras = self.driver.find_elements_by_css_selector('p')
            para_list=[]
            for paragraph in elem_paras:
                para_list = para_list + paragraph.text.split(" ")
            word_count = len(para_list)
            word_count_list= 0
            elem_list= self.driver.find_elements_by_tag_name("li")
            unordered_list=[]
            for li in elem_list:
                unordered_list = unordered_list + li.text.split(" ")
            word_count_list = len(unordered_list)
           
            total_words = word_count + word_count_list
            
            if total_words < 250 or total_words > 500:
                    self.fail("Total words : "+str(total_words)+", blog 2 should have 250 to 500 words in paragraph or unordered list format.")
        except NoSuchElementException as ex:
            self.fail(ex.msg)
            sys.exit("Total words : "+str(total_words)+", blog 2 should have 250 to 500 words in paragraph or unordered list format.")
        


if __name__ == '__main__':
    link_1, link_2 = "", ""
    repo=str(sys.argv[1])
    url="https://cs-ej4104-fall-2020.github.io/"+repo.split("/")[1]
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTemplate)
    test_result = unittest.TextTestRunner(verbosity=1).run(suite)
    ret = not test_result.wasSuccessful()
    sys.exit(ret)
